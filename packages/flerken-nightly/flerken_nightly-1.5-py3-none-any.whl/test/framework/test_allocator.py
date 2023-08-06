import unittest
import torch
from flerken.framework.allocator import Allocator


def cpu_tensor():
    return torch.rand(1)


def gpu_tensor():
    return torch.rand(1, device='cuda:0')


@unittest.skipIf(not torch.cuda.is_available(), 'Cuda is not available in the system')
class TestClassItems(unittest.TestCase):
    def setUp(self) -> None:
        self.cuda = 'cuda:0'
        self.gpu_alloc = Allocator(self.cuda, dataparallel=False)
        self.cpu_alloc = Allocator('cpu', dataparallel=False)
        self.dp_alloc = Allocator('cpu', dataparallel=True)

    def test_cpu_gpu_list(self):
        cpu = [cpu_tensor() for _ in range(2)]
        gpu = [x.to(self.cuda) for x in cpu]

        alloc = self.gpu_alloc(cpu)

        for x, y in zip(gpu, alloc):
            self.assertTrue((x == y).all())

    def test_gpu_cpu_list(self):
        gpu = [gpu_tensor() for _ in range(2)]
        cpu = [x.to('cpu') for x in gpu]

        alloc = self.cpu_alloc(gpu)

        for x, y in zip(cpu, alloc):
            self.assertTrue((x == y).all())

    def test_cpu_gpu_list_list(self):
        cpu0 = [cpu_tensor() for _ in range(2)]
        cpu1 = [cpu_tensor() for _ in range(2)]
        gpu0 = [x.to(self.cuda) for x in cpu0]
        gpu1 = [x.to(self.cuda) for x in cpu1]

        cpu = [cpu0, cpu1]
        gpu = [gpu0, gpu1]

        alloc = self.gpu_alloc(cpu)
        self.assertIsInstance(alloc, list)
        self.assertIsInstance(alloc[0], list)
        self.assertIsInstance(alloc[1], list)
        self.assertTrue(alloc[0][0] == gpu[0][0])
        self.assertTrue(alloc[0][1] == gpu[0][1])
        self.assertTrue(alloc[1][1] == gpu[1][1])
        self.assertTrue(alloc[1][0] == gpu[1][0])

    def test_cpu_gpu_list_tuple(self):
        cpu0 = tuple([cpu_tensor() for _ in range(2)])
        cpu1 = tuple([cpu_tensor() for _ in range(2)])
        gpu0 = tuple([x.to(self.cuda) for x in cpu0])
        gpu1 = tuple([x.to(self.cuda) for x in cpu1])

        cpu = [cpu0, cpu1]
        gpu = [gpu0, gpu1]

        alloc = self.gpu_alloc(cpu)
        self.assertIsInstance(alloc, list)
        self.assertIsInstance(alloc[0], tuple)
        self.assertIsInstance(alloc[1], tuple)
        self.assertTrue(alloc[0][0] == gpu[0][0])
        self.assertTrue(alloc[0][1] == gpu[0][1])
        self.assertTrue(alloc[1][1] == gpu[1][1])
        self.assertTrue(alloc[1][0] == gpu[1][0])

    def test_cpu_gpu_dict(self):
        cpu = {'tensor0': cpu_tensor()}
        gpu = {'tensor0': cpu['tensor0'].to(self.cuda)}

        alloc = self.gpu_alloc(cpu)
        self.assertTrue(gpu['tensor0'] == alloc['tensor0'])

    def test_cpu_gpu_dict_list(self):
        cpu = {'tensor0': [cpu_tensor()]}
        gpu = {'tensor0': [cpu['tensor0'][0].to(self.cuda)]}

        alloc = self.gpu_alloc(cpu)
        self.assertTrue(gpu['tensor0'][0] == alloc['tensor0'][0])

    def test_cpu_gpu_list_dict_list_dict(self):
        cpu = [{'tensor0': cpu_tensor()}]
        gpu = [{'tensor0': cpu[0]['tensor0'].to(self.cuda)}]

        cpu = [{'list_dict': cpu}, {'list_dict': cpu}]
        gpu = [{'list_dict': gpu}]

        alloc = self.gpu_alloc(cpu)
        self.assertTrue(gpu[0]['list_dict'][0]['tensor0'] == alloc[0]['list_dict'][0]['tensor0'])

    def test_dataparallel(self):
        cpu = [cpu_tensor() for _ in range(2)]
        gpu = [x.to(self.cuda) for x in cpu]

        alloc = self.dp_alloc(cpu)
        with self.assertRaises(RuntimeError):
            for x, y in zip(gpu, alloc):
                self.assertTrue((x == y).all())

        self.assertTrue(alloc[0].device == torch.device('cpu'))

    def test_non_tensors(self):
        cpu = [{'tensor0': cpu_tensor()}, 5, 'jamon']
        gpu = [{'tensor0': cpu[0]['tensor0'].to(self.cuda)}]

        cpu = [{'list_dict': cpu}, {'list_dict': cpu}]
        gpu = [{'list_dict': gpu}]

        alloc = self.gpu_alloc(cpu)
        self.assertTrue(gpu[0]['list_dict'][0]['tensor0'] == alloc[0]['list_dict'][0]['tensor0'])
