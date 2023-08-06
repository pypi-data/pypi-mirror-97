from typing import List, Union

from nvidia.dali.pipeline import Pipeline
import nvidia.dali.ops as ops

from torch import no_grad
from numpy import array

from .audiovisual_dataset import AVDataset

__all__ = ['BasePipeline', 'AudioVisualPipeline']


class BasePipeline(Pipeline):
    """
    THIS CLASS DEFINES HOW THE DATA FLOWS THROUGH READERS, BUT IT DOESNT DEFINE WHERE THE DATA COMES FROM
    """

    def __init__(self,
                 # General kwargs
                 batch_size: int, num_threads: int, device_id: int, seed: int,
                 prefetch_queue_depth: int, exec_pipelined: bool,
                 # Flags
                 read_video: bool, read_sk: bool, read_accompaniment: bool, compute_spectrogram: bool,
                 # Video reader kwargs
                 video_reader: dict, mean: List[float], std: List[float],
                 video_file_list: str,
                 # Spectrogram-related kwargs
                 n_fft, hop_length, stft_window):
        super(BasePipeline, self).__init__(batch_size, num_threads, device_id, seed=seed,
                                           prefetch_queue_depth=prefetch_queue_depth,
                                           exec_pipelined=exec_pipelined)
        # VARIABLES
        self.ops = video_reader['ops']
        self.video_enabled = read_video
        self.sk_enabled = read_sk
        self.acmt_enabled = read_accompaniment
        self.video_backend = video_reader['backend']
        self.compute_spectrogram=compute_spectrogram

        # AUDIO STUFF

        # Defining spectrogram computation
        if stft_window.__name__ == 'hann_window':
            window_fn = []
            # window_fn = STFT_WINDOW(N_FFT).tolist()
        else:
            window_fn = stft_window(n_fft).tolist()
        self.spectrogram = ops.Spectrogram(device="gpu",
                                           nfft=n_fft,
                                           window_length=n_fft,
                                           window_step=hop_length,
                                           window_fn=window_fn,
                                           power=1)  # Power 1 matches torch/librosa

        # Audio reader as an external source to seek for specific parts
        self.audio_main_data = ops.ExternalSource()
        self.audio_acmt_data = ops.ExternalSource()

        # Skeleton data
        # It will be detached from the graph if not used
        self.skeleton_data = ops.ExternalSource()
        self.index_data = ops.ExternalSource()

        if self.video_enabled:
            pass
        else:
            return None

        # Defining video reader
        # Compatible GPU codecs are h264 for yuv420
        self._vreader_opts = ['VideoReader', 'VideoReaderResize', 'Numpy']
        self.set_video_reader(video_reader, video_file_list)

        # Axes are the dims over you don't want to normalize. Batch dim doesnt count in the indexing
        # This means that (mean,std)=(0,1) in the missing dimension, 3
        self.normalize = ops.Normalize(device='gpu', batch=False, axes=[0, 1, 2])
        self.start_x = ops.Uniform(range=(0, 1))
        self.start_y = ops.Uniform(range=(0, 1))

        kw = dict()
        if 'crop' not in self.ops:
            kw['crop_pos_x'] = 0.5
            kw['crop_pos_y'] = 0.5

        self.crop = ops.CropMirrorNormalize(crop=(video_reader["VID_CROP_X"], video_reader["VID_CROP_Y"]),
                                            device='gpu',
                                            output_layout="FCHW",
                                            mean=mean,
                                            std=std,
                                            **kw)

        self.flip = ops.Flip(device='gpu')
        self.coinflip = ops.CoinFlip()

    def set_video_reader(self, video_reader, video_file_list):
        assert video_reader['backend'] in self._vreader_opts
        if video_reader['backend'] == 'VideoReaderResize':
            self.vreader = ops.VideoReaderResize(device="gpu", file_list=video_file_list,
                                                 sequence_length=video_reader["N_VIDEO_FRAMES"],
                                                 shard_id=0, num_shards=1, file_list_frame_num=True,
                                                 random_shuffle=False, skip_vfr_check=True,
                                                 resize_x=video_reader["VID_RESIZE_X"],
                                                 resize_y=video_reader["VID_RESIZE_Y"])
        elif video_reader['backend'] == 'VideoReader':
            self.vreader = ops.VideoReader(device="gpu", file_list=video_file_list,
                                           sequence_length=video_reader["N_VIDEO_FRAMES"],
                                           shard_id=0, num_shards=1, file_list_frame_num=True,
                                           random_shuffle=False, skip_vfr_check=True)
        elif video_reader['backend'] == 'Numpy':
            self.vreader = ops.ExternalSource()

    def gen_resources(self):
        resources = ['index', 'audio']
        if self.compute_spectrogram:
            resources.append('spectrogram')
        if self.acmt_enabled:
            resources.append('audio_acmt')
            if self.compute_spectrogram:
                resources.append('spectrogram_acmt')
                resources.append('spectrogram_mix')
        if self.sk_enabled:
            resources.append('skeleton')
        if self.video_enabled:
            if 'crop' in self.ops:
                resources.append('crop_pos_x')
                resources.append('crop_pos_y')
            if 'flip' in self.ops:
                resources.append('coin')
            resources.append('video')
        return resources

    def define_graph(self):
        self.audio_main = self.audio_main_data(name='audio_main').gpu()
        self.index = self.index_data()
        resources = [ self.index, self.audio_main]
        if self.compute_spectrogram:
            sp_main = self.spectrogram(self.audio_main)
            resources.append(sp_main)

        if self.acmt_enabled:
            self.audio_acmt = self.audio_acmt_data(name='audio_accompaniment').gpu()
            resources.append(self.audio_acmt)
            if self.compute_spectrogram:
                sp_acmt = self.spectrogram(self.audio_acmt)
                sp_mix = self.spectrogram(self.audio_main + self.audio_acmt)
                resources.append(sp_acmt)
                resources.append(sp_mix)

        if self.sk_enabled:
            self.skeleton = self.skeleton_data(name='skeleton').gpu()
            resources.append(self.skeleton)

        if self.video_enabled:
            if isinstance(self.vreader, ops.ExternalSource):

                self.video = self.vreader(name='video').gpu()
            else:
                self.video = self.vreader(name='video')[0] / 255

            kw = dict()
            if 'crop' in self.ops:
                crop_pos_x = self.start_x()
                crop_pos_y = self.start_y()
                kw['crop_pos_x'] = crop_pos_x.gpu()
                kw['crop_pos_y'] = crop_pos_y.gpu()
                resources.append(crop_pos_x)
                resources.append(crop_pos_y)
            if 'flip' in self.ops:
                coin = self.coinflip()
                kw['mirror'] = coin.gpu()
                resources.append(coin)

            video = self.crop(self.video, **kw)
            resources.append(video)

        return resources


def reformat_trace(trace, idx):
    indices = [x['indices'][idx] for x in trace]
    kwargs = [x['kwargs'][idx] for x in trace]
    return zip(indices, kwargs)


class AudioVisualPipeline(BasePipeline):
    def __init__(self, *,
                 # General kwargs
                 batch_size: int, num_threads: int, device_id: int, seed: int, debug: dict,
                 prefetch_queue_depth: int, exec_pipelined: bool,
                 # Traces
                 main_trace, accompaniment_trace,
                 # Flags
                 read_video: bool, read_sk: bool, read_accompaniment: bool, compute_spectrogram: bool,
                 # Datasets
                 main_dataset, accompaniment_ds,
                 # Video reader kwargs
                 video_reader: dict, mean: List[float], std: List[float], video_file_list: str,
                 # Spectrogram-related kwargs
                 n_fft, hop_length, stft_window

                 ):
        super().__init__(batch_size, num_threads, device_id, seed,
                         prefetch_queue_depth, exec_pipelined, read_video, read_sk, read_accompaniment,
                         compute_spectrogram,
                         video_reader, mean, std, video_file_list, n_fft, hop_length, stft_window)

        self.debug = debug
        self.main_ds = main_dataset
        self.acmt_ds = accompaniment_ds
        self.idx = 0
        self.main_trace = [main_trace[i * batch_size:(i + 1) * batch_size] for i in
                           range(len(main_trace) // batch_size)]
        self.acmt_trace = None
        if self.acmt_enabled:
            self.acmt_trace = [accompaniment_trace[i * batch_size:(i + 1) * batch_size] for i in
                               range(len(main_trace) // batch_size)]

    def iter_setup(self):
        trace_main = reformat_trace(self.main_trace[self.idx], 0)

        audio_main = self.main_ds.load_audio(trace_main)[0]
        if self.acmt_enabled:
            trace_slave = reformat_trace(self.acmt_trace[self.idx], 0)
            audio_acmt = self.acmt_ds.load_audio(trace_slave)[0]
            self.feed_input(self.audio_acmt, audio_acmt)
        self.feed_input(self.audio_main, audio_main)
        if self.main_ds.read_sk:
            # Trace is a generator and gets exahusted
            trace_main = reformat_trace(self.main_trace[self.idx], 0)
            skeleton = self.main_ds.load_sk(trace_main)
            self.feed_input(self.skeleton, skeleton)
        if self.video_enabled and self.video_backend == 'Numpy':
            trace_main = reformat_trace(self.main_trace[self.idx], 0)
            video = self.main_ds.load_video(trace_main)
            self.feed_input(self.video, video, layout='FHWC')  # The layout is necessary, exception otherwise

        self.feed_input(self.index, [array(self.idx) for _ in range(len(audio_main))])
        self.idx += 1
        if self.idx >= len(self.main_trace):
            self.idx = 0
            raise StopIteration


class PostProcessor:
    def __init__(self, dataset: AVDataset, device):
        self.main_device = device
        self.dataset = dataset

    def __iter__(self):
        with no_grad():  # (torch)
            for (data) in self.dali_dataloader:
                data = data[0]
                index = data['index'][0].item()
                trace = self.dali_dataloader._pipes[0].main_trace[index]
                trace_slave = self.dali_dataloader._pipes[0].acmt_trace[index]

                yield self.dataset.postprocessor(data, index=index, trace=trace, trace_acmt=trace_slave)
        self.dali_dataloader.reset()

    def __call__(self, dali_dataloader):
        self.dali_dataloader = dali_dataloader
        self.batch_size = dali_dataloader.batch_size
        self.N = len(self.dali_dataloader._pipes[0].main_trace) * self.batch_size
        return self

    def __len__(self):
        return self.N // self.batch_size
