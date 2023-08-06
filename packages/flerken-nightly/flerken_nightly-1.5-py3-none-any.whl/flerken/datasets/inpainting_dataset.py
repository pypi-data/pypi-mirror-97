import torch

from .audiovisual_dataset import BaseHelper, AVDataset
from ..framework.allocator import Allocator

class InpaintingHelper(BaseHelper):
    def __init__(self,
                 # Inpainting kwargs

                 # Flags
                 read_sk: bool,
                 # Acapella kwargs
                 root, audio_prep, audio_exclude, audio_key, sk_key,
                 # Dataset_args
                 debug: bool, yield_mode: str, traces, **kwargs):
        read_video = False
        use_accompaniment = False
        silent_accompaniment = None
        video_key = None
        accompaniment_dataset = None
        accompaniment_audio_key = None
        n_sources = None
        super(InpaintingHelper, self).__init__(read_video, read_sk, use_accompaniment, silent_accompaniment, root, audio_prep,
                                        audio_exclude, audio_key, video_key, sk_key, accompaniment_dataset,
                                        accompaniment_audio_key, n_sources, traces, debug, yield_mode, **kwargs)