from typing import Tuple

from torch import matmul, nn, reshape, stack, zeros


class Reshape(nn.Module):
    """
    Reshape Module

    Just a helper since PyTorch uses different functions for different type of inputs at the moment.
    """

    def __init__(self, *args):
        super(Reshape, self).__init__()
        self.shape = args

    def forward(self, x):
        if isinstance(self.shape, tuple):
            return x.unflatten(1, self.shape)
        else:
            return x.view(self.shape)


class GANAttention2d(nn.Module):
    """
    Custom Attention Module inspired by https://github.com/AdalbertoCq/Pathology-GAN/blob/master/models/generative/ops.py (attention_block)

    GAN related Attention Paper: https://arxiv.org/pdf/1805.08318.pdf
    """

    def __init__(self, z: Tuple[int, int, int], channel_divisor: int, gain: int = 1e-4):
        """
        Init for GANGAttention2d

        :param z: input
        :type tuple(int, int, int): input with format of tuple(channels, width, height)
        :param channel_divisor: divisor to calculate f_g_channel (f_g_channel=channels//channel_divisor)
        :type channel_divisor: int
        :param gain: weight parameter for orthogonal initialization 
        :type gain: float
        """

        super(GANAttention2d, self).__init__()
        self.gain = gain

        def block_conv_spectral(in_channels, out_channels, kernel_size, stride, padding):
            # Conv + spectral norm
            return [nn.utils.spectral_norm(nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,
                                                     stride=stride, bias=True, padding=padding), n_power_iterations=1, eps=1e-12)]

        self.channels, self.height, self.width = z

        self.gamma = zeros(1)

        self.f_g_channels = self.channels//channel_divisor

        self.f = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.f_g_channels, kernel_size=(1, 1), stride=(1, 1), padding=0)
                               )

        self.g = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.f_g_channels, kernel_size=(1, 1), stride=(1, 1), padding=0)
                               )

        self.h = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.channels, kernel_size=(1, 1), stride=(1, 1), padding=0)
                               )

        # Initiliaze weights
        self.init_weights()

    def forward(self, x):
        f_flat = reshape(self.f(x), stack(
            [x.size(0), self.f_g_channels, self.height*self.width]))
        g_flat = reshape(self.g(x), stack(
            [x.size(0), self.f_g_channels, self.height*self.width]))
        h_flat = reshape(self.h(x), stack(
            [x.size(0), self.channels, self.height*self.width]))

        s = matmul(g_flat, f_flat, transpose_b=True)

        beta = nn.functional.softmax(s)

        o = matmul(beta, h_flat)
        o = reshape(o, shape=stack(
            [x.size(0), self.channels, self.height, self.width]))
        y = self.gamma*o + x

        return y

    def init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.orthogonal_(module.weight, gain=self.gain)
                nn.init.constant_(module.bias, 0)
