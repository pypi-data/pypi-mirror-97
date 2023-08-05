import torch
import unittest

class TestCuda(unittest.TestCase):

    def test_cuda_available(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.assertEqual(device.type, 'cuda')


if __name__ == '__main__':
    unittest.main()