from typing import Union, List
from itertools import accumulate
from random import random
from bisect import bisect_left

from torch.utils.data.dataset import Dataset

from flerken.utils import ClassDict
from .audiovisual_dataset import AVDataset

example = {
    'name': str,
    'dataset': Dataset,
    'query_elements': List[str],
    'cluster': Union[int, None],
    'nsources': Union[None, int]
}

__all__ = ['FlerkenDataset']


class FlerkenDataset:
    def __init__(self, *datasets: List[dict], n_iterations: int, batch_size: int, balanced_sampling: bool):
        self._required_keys = ['name', 'dataset', 'cluster']
        self.traces = {}
        self.bal_sampling = balanced_sampling
        datasets = [ClassDict(dataset) for dataset in datasets]
        self.n_iterations = n_iterations
        self.batch_size = batch_size
        self._check_datasets_format(datasets)
        self._define_clusters(datasets)
        self._define_datasets(datasets)

    def custom_ops(self, data: dict, traces: dict, datasets_used: dict, idx: int):
        NotImplementedError

    def __len__(self):
        return self.n_iterations * self.batch_size

    def __getitem__(self, idx):
        data = {}
        traces = {}
        datasets_used = {}
        for cluster_name in self.clusters:
            trace, output, dataset_name = self.sample_from_cluster(cluster_name, idx)
            data[cluster_name] = output
            datasets_used[cluster_name] = dataset_name
            traces[cluster_name] = trace
        return self.custom_ops(data, traces, datasets_used, idx)

    def sample_from_cluster(self, cluster_name, sample_idx):
        trace = self.traces.get(cluster_name)
        cluster = self.clusters[cluster_name]
        if trace is None:
            acc_probs = self.sampling_probs[cluster_name]
            uniform_sample = random()
            dataset_idx = bisect_left(acc_probs, uniform_sample)

        else:
            trace = trace[sample_idx]
            dataset_name = list(trace.keys())[0]
            trace = self._reformat_trace(trace)
            dataset_idx = [x['name'] for x in cluster].index(dataset_name)

        cluster = cluster[dataset_idx]
        dataset = cluster['dataset']
        dataset_name = cluster['name']
        data, trace = dataset.getitem(idx=trace,
                                      N=cluster['nsources'],
                                      elements=cluster['query_elements'],
                                      trazability=True,
                                      )

        return trace, data, dataset_name

    def _reformat_trace(self, trace):
        indices = list(trace.values())[0]['indices']
        kwargs = list(trace.values())[0]['kwargs']
        yield from zip(indices, kwargs)

    def _check_dataset_format(self, dataset):
        assert isinstance(dataset, dict), f'dataset must be a dictionary but {type(dataset)} found'
        for key in self._required_keys:
            assert key in dataset.keys(), f'Dataset missing key {key}. Required format is {example}'
        assert isinstance(dataset.get('dataset'), AVDataset), f'Datasets must be of type {type(AVDataset)}'

    def _check_datasets_format(self, datasets):
        assert isinstance(datasets, list), 'datasets must be a list'

        used_names = []
        for dataset in datasets:
            self._check_dataset_format(dataset)
            name = dataset['name']
            assert name not in used_names, f'Name {name} has been already used'
            used_names.append(name)

    def _define_clusters(self, datasets):
        self.clusters = {}
        for dataset in datasets:
            cluster = dataset['cluster']
            if cluster not in self.clusters:
                self.clusters[cluster] = []
            self.clusters[cluster].append(dataset)

        self.sampling_probs = {}
        for cluster in self.clusters:
            if self.bal_sampling:
                n_elements = []

                for dataset_dict in self.clusters[cluster]:
                    dataset = dataset_dict['dataset']
                    n_elements.append(len(dataset))
                total = sum(n_elements)
                abs_prob = [x / total for x in n_elements]

            else:
                abs_prob = [1 / len(self.clusters[cluster]) for _ in range(len(self.clusters[cluster]))]
            self.sampling_probs[cluster] = list(accumulate(abs_prob))  # Accumulated prob

    def _define_datasets(self, datasets):
        for dataset in datasets:
            setattr(self, dataset['name'], dataset)
