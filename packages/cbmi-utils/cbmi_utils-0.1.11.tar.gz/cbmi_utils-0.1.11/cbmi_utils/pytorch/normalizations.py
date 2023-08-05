from typing import Tuple

from torch import nn, ones, std_mean, zeros
from torch.nn.functional import batch_norm


class GANAdaptiveInstanceNorm(nn.Module):
    """
    TODO NOT WORKING AS EXPECTED, PROBABLY NEEDS A REWRITE + INHERETING CLASSES

    Base class, should not be called directly.

    Custom Adaptive Instance Normalization from https://github.com/AdalbertoCq/Pathology-GAN/blob/master/models/generative/normalization.py (conditional_batch_norm)

    GAN related AdaIN Paper: https://arxiv.org/pdf/1812.04948.pdf
    """

    def __init__(self, inputs, c, spectral: bool = False, n_power_iterations: int = 1, eps: float = 1e-12, gain: float = 1e-4):
        """        
        :param inputs: number of inputs
        :type inputs: int
        :param c: TODO
        :type c: int
        :param spectral: defines if spectral normalization is used
        :type spectral: boolean
        :param n_power_iterations: number of power iterations for spectral normalization
        :type n_power_iterations: int
        :param eps: hyperparameter for spectral normalization
        :type eps: float
        :param gain: weight parameter for orthogonal initialization 
        :type gain: float
        """
        super(GANAdaptiveInstanceNorm, self).__init__()
        self.gain = gain

        def block_dense(in_feat, out_feat, activation=True, spectral=True, n_power_iterations=1, eps=1e-12):
            # Linear + Spectral Norm (optional) + Relu (optional)
            if spectral:
                layers = [nn.utils.spectral_norm(
                    nn.Linear(in_feat, out_feat), n_power_iterations=n_power_iterations, eps=eps)]
            else:
                layers = [nn.Linear(in_feat, out_feat)]

            if activation:
                layers.append(nn.ReLU(inplace=True))

            return layers

        self.momentum = 0.9  # was decay in tf
        self.epsilon = 1e-5

        self.test_mean = zeros([inputs], requires_grad=False)
        self.test_variance = ones([inputs], requires_grad=False)

        # MLP for gamma, and beta
        inter_dim = int((inputs+c)/2)

        # in_feat=c in tf code
        self.net = nn.Sequential(
            *block_dense(in_feat=inputs, out_feat=inter_dim, activation=True, spectral=spectral, n_power_iterations=n_power_iterations, eps=eps))

        self.gamma = nn.Sequential(
            *block_dense(in_feat=inter_dim, out_feat=inputs, activation=True, spectral=spectral, n_power_iterations=n_power_iterations, eps=eps))

        self.beta = nn.Sequential(
            *block_dense(in_feat=inter_dim, out_feat=inputs, activation=False, spectral=spectral, n_power_iterations=n_power_iterations, eps=eps))

        self.init_weights()

    def forward(self, x):
        if len(x) == 4:
            batch_variance, batch_mean = std_mean(x, dim=[2, 3], keepdim=True)
        else:
            batch_variance, batch_mean = std_mean(x, dim=[1], keepdim=True)

        x_net = self.net(x)

        x_net_gamma = self.gamma(x_net)
        x_net_beta = self.beta(x_net)

        # according to https://discuss.pytorch.org/t/example-on-how-to-use-batch-norm/216/22, gamma and beta should correspond to .weight and .bias, respectively.
        # batch_norm_output = batch_norm(
        #     x, batch_mean, batch_variance, weight=x_net_gamma, bias=x_net_beta, momentum=self.momentum, eps=self.epsilon)

        # workaround for the moment
        batch_norm_output = (x_net_gamma*(x-batch_mean) /
                             batch_variance)+x_net_beta

        return batch_norm_output

    def init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.orthogonal_(module.weight, gain=self.gain)
                nn.init.constant_(module.bias, 0)


class GANAdaptiveInstanceNorm1d(GANAdaptiveInstanceNorm):
    """
    Custom Adaptive Instance Normalization 1d Wrapper
    """

    def __init__(self, num_feat: int, spectral: bool = False, n_power_iterations: int = 1, eps: float = 1e-12, gain: float = 1e-4):
        """
        Init for Normalization1d

        :param num_feat: number of input features
        :type num_feat: int
        :param spectral: defines if spectral normalization is used
        :type spectral: boolean
        :param n_power_iterations: number of power iterations for spectral normalization
        :type n_power_iterations: int
        :param eps: hyperparameter for spectral normalization
        :type eps: float
        :param gain: weight parameter for orthogonal initialization 
        :type gain: float
        """
        # c is always 1 for 1d
        super(GANAdaptiveInstanceNorm1d, self).__init__(
            inputs=num_feat, c=1, spectral=spectral, n_power_iterations=n_power_iterations, eps=eps, gain=gain)


class GANAdaptiveInstanceNorm2d(GANAdaptiveInstanceNorm):
    """
    Custom Adaptive Instance Normalization 2d Wrapper
    """

    def __init__(self, channels: int, c: int, spectral: bool = False, n_power_iterations: int = 1, eps: float = 1e-12, gain: float = 1e-4):
        """
        Init for Normalization1d

        :param channels: number of channels
        :type channels: int
        :param c: TODO
        :type c: int
        :param spectral: defines if spectral normalization is used
        :type spectral: boolean
        :param n_power_iterations: number of power iterations for spectral normalization
        :type n_power_iterations: int
        :param eps: hyperparameter for spectral normalization
        :type eps: float
        :param gain: weight parameter for orthogonal initialization 
        :type gain: float
        """
        super(GANAdaptiveInstanceNorm2d, self).__init__(
            inputs=channels, c=c, spectral=spectral, n_power_iterations=n_power_iterations, eps=eps, gain=gain)

