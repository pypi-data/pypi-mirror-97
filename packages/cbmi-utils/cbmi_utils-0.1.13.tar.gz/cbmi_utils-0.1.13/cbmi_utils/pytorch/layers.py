from typing import Tuple

from torch import Tensor, matmul, nn, reshape, transpose

from .padding import get_padding_same_conv2d


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

    def __init__(self, z: Tuple[int, int, int], channel_divisor: int, gamma: Tensor, gain: int = 1e-4):
        """
        Init for GANGAttention2d

        :param z: input
        :type tuple(int, int, int): input with format of tuple(channels, width, height)
        :param channel_divisor: divisor to calculate f_g_channel (f_g_channel=channels//channel_divisor)
        :type channel_divisor: int
        :param gamma: hyperparameter, scalar and should be initialized as 0
        :type gamma: Tensor
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

        # Global value for all pixels, measures how important is the context for each of them.
        self.gamma = gamma

        self.f_g_channels = self.channels//channel_divisor

        padding_same_channels = get_padding_same_conv2d(
            self.channels, kernel_size=1, stride=1, dilation=1)

        self.f = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.f_g_channels, kernel_size=1, stride=1, padding=padding_same_channels)
                               )

        self.g = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.f_g_channels, kernel_size=1, stride=1, padding=padding_same_channels)
                               )

        self.h = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.channels, kernel_size=1, stride=1, padding=padding_same_channels)
                               )

        # Initiliaze weights
        self.init_weights()

    def forward(self, x):
        # Flatten f, g, and h per channel.
        f_flat = reshape(
            self.f(x), shape=[x.size(0), self.f_g_channels, self.height*self.width])
        g_flat = reshape(
            self.g(x), shape=[x.size(0), self.f_g_channels, self.height*self.width])
        h_flat = reshape(
            self.h(x), shape=[x.size(0), self.channels, self.height*self.width])

        # TODO changed due to different handling between tf and pytorch logic
        s = matmul(transpose(g_flat, dim0=1, dim1=2), f_flat)

        beta = nn.functional.softmax(s, dim=1)

        # TODO changed due to different handling between tf and pytorch logic
        o = matmul(h_flat, beta)

        o = reshape(o, shape=[x.size(0), self.channels,
                              self.height, self.width])
        y = self.gamma*o + x

        return y

    def init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.orthogonal_(module.weight, gain=self.gain)
                nn.init.constant_(module.bias, 0)

