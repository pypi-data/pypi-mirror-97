from typing import Tuple
from random import randint

import torch

from .audiovisual_dataset import BaseHelper, AVDataset
from ..framework.allocator import Allocator

__all__ = ['BSSHelper', 'InpaintinHelper']


class InpaintinHelper(BaseHelper):
    def __init__(self,
                 # Mask kwargs
                 silent_mask_mode: str, silent_mask_max: float, silent_mask_min: float,
                 # Video kwargs
                 video_frames_in: int, video_frames_out: int,
                 # Flags
                 read_video: bool, read_sk: bool,
                 # Acapella kwargs
                 root, preprocessing, audio_exclude, audio_key, video_key, sk_key,
                 # Dataset_args
                 debug: bool, yield_mode: str, traces, **kwargs):
        use_accompaniment = False
        silent_accompaniment = 0
        accompaniment_dataset = None
        accompaniment_audio_key = None
        n_sources = None
        super(InpaintinHelper, self).__init__(read_video, read_sk, use_accompaniment, silent_accompaniment, root,
                                              preprocessing,
                                              audio_exclude, audio_key, video_key, sk_key, accompaniment_dataset,
                                              accompaniment_audio_key, n_sources, debug, yield_mode, traces, **kwargs)

        self.cuda1 = Allocator(1, dataparallel=False)  # Allocator (toolkit)
        self.cpu = Allocator('cpu', dataparallel=False)  # Allocator (toolkit)
        # Slice to take those frames
        rate = video_frames_in / video_frames_out
        self.indexing = [round(rate * i) + 3 for i in range(video_frames_out)]

        self.silent_mask_mode = silent_mask_mode.lower()
        self.silent_mask_max = silent_mask_max
        self.silent_mask_min = silent_mask_min
        assert 0 <= silent_mask_max <= 1, f'silent_mask_max arg has to be a float between 0 and 1'
        assert 0 <= silent_mask_min <= 1, f'silent_mask_min arg has to be a float between 0 and 1'
        assert silent_mask_mode.lower() in ['dynamic', 'static'], f'silent_mask_mode must be either dynamic or static'

    def get_silent_mask(self, shape: Tuple[int, int], n_bins: int, device: torch.device = 'cpu'):
        assert n_bins <= shape[1], f'Number of silent bins has to be smaller or equal than the total number of bins'
        tensor = torch.ones(*shape, dtype=torch.float, device=device)
        start_idx = torch.randint(0, shape[1] - n_bins, (1,))
        tensor[start_idx:start_idx + n_bins].zero_()
        return tensor

    def _cal_nbins_static(self, shape):
        total_bins = shape[1]
        return int(total_bins * self.silent_mask_max)

    def _cal_nbins_dynamic(self, shape):
        total_bins = shape[1]
        min_bins = int(self.silent_mask_min * total_bins)
        max_bins = int(self.silent_mask_max * total_bins)
        return randint(min_bins, max_bins)

    def calc_nbins(self, shape):
        if self.silent_mask_mode == 'dynamic':
            return self._cal_nbins_dynamic(shape)
        elif self.silent_mask_mode == 'static':
            return self._cal_nbins_static(shape)
        else:
            raise ValueError(f'silent_mask_mode should be either dynamic or static but {self.silent_mask_mode} found')

    def batched_silent_mask(self, tensor_like, ):
        batch_size = tensor_like.shape[0]
        shape = tensor_like.shape[-2:]
        device = tensor_like.device
        nbins = self.calc_nbins(shape)
        return torch.stack([self.get_silent_mask(shape, nbins, device) for _ in range(batch_size)])


class BSSHelper(BaseHelper):
    def __init__(self,
                 # BSS Args
                 weighted_loss: bool, video_frames_in: int, video_frames_out: int,
                 # Flags
                 read_video: bool, read_sk: bool, use_accompaniment: bool, silent_accompaniment: float,
                 # Acapella kwargs
                 root, preprocessing, audio_exclude, audio_key, video_key, sk_key,
                 # Accompaniment_ds
                 accompaniment_dataset: AVDataset, accompaniment_audio_key, n_sources,
                 # Dataset_args
                 debug: bool, yield_mode: str, traces, **kwargs):
        super(BSSHelper, self).__init__(read_video, read_sk, use_accompaniment, silent_accompaniment, root,
                                        preprocessing,
                                        audio_exclude, audio_key, video_key, sk_key, accompaniment_dataset,
                                        accompaniment_audio_key, n_sources, debug, yield_mode, traces, **kwargs)

        self.weighted_loss = weighted_loss

        self.cuda1 = Allocator(1, dataparallel=False)  # Allocator (toolkit)
        self.cpu = Allocator('cpu', dataparallel=False)  # Allocator (toolkit)
        # Slice to take those frames
        rate = video_frames_in / video_frames_out
        self.indexing = [round(rate * i) + 3 for i in range(video_frames_out)]

    @staticmethod
    def binary_mask_dali(sp, spm, debug):
        if debug['isnan']:
            for i in sp:
                if torch.isnan(i).any() or torch.isinf(i).any():
                    raise Exception('NaN or Inf found in raw spectrograms.')
            if torch.isnan(spm).any() or torch.isinf(spm).any():
                raise Exception('NaN or Inf found in spm after getting mag and phase.')
        indices = sp.max(dim=0)[1]
        gt = torch.zeros_like(sp)
        for idx, sp_i in enumerate(gt):
            sp_i.masked_fill_(indices == idx, 1.)
        return spm, gt[0]

    def batched_binary_mask(self, data):
        sp = torch.stack([data['spectrogram'], data['spectrogram_acmt']], dim=1)
        gt = []
        spm = []
        for sp_i, spm_i in zip(sp, data['spectrogram_mix']):
            spm_o, gt_o = self.binary_mask_dali(sp_i, spm_i, self.debug)
            spm.append(spm_o)
            gt.append(gt_o)
        spm = torch.stack(spm)
        gt = torch.stack(gt)
        return spm, gt
