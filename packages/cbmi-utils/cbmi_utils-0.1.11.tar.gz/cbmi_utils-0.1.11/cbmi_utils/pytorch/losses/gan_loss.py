import abc

from torch import Tensor, ones_like, relu, zeros_like
from torch.nn.functional import binary_cross_entropy_with_logits


class GANLoss(abc.ABC):
    @abc.abstractmethod
    def discriminator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        raise NotImplementedError()

    @abc.abstractmethod
    def generator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        raise NotImplementedError()


class RaSGAN(GANLoss):
    """
    Relativistic Average Standard

    Paper: https://arxiv.org/abs/1807.00734v3
    """

    def __init__(self) -> None:
        super(RaSGAN, self).__init__()

    def discriminator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        relativistic_real_validity = real_validity - fake_validity.mean()
        relativistic_fake_validity = fake_validity - real_validity.mean()

        real_label = ones_like(real_validity)
        fake_label = zeros_like(fake_validity)

        relativistic_real_probability = binary_cross_entropy_with_logits(
            relativistic_real_validity, real_label)
        relativistic_fake_probability = binary_cross_entropy_with_logits(
            relativistic_fake_validity, fake_label)

        loss = (relativistic_real_probability +
                relativistic_fake_probability) / 2

        return loss.unsqueeze(0)

    def generator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        relativistic_real_validity = real_validity - fake_validity.mean()
        relativistic_fake_validity = fake_validity - real_validity.mean()

        real_label = ones_like(real_validity)
        fake_label = zeros_like(fake_validity)

        relativistic_real_probability = binary_cross_entropy_with_logits(
            relativistic_real_validity, fake_label)
        relativistic_fake_probability = binary_cross_entropy_with_logits(
            relativistic_fake_validity, real_label)

        loss = (relativistic_real_probability +
                relativistic_fake_probability) / 2

        return loss


class RaLSGAN(GANLoss):
    """
    Relativistic Average Least Square

    Paper: https://arxiv.org/abs/1611.04076v3
    """

    def __init__(self) -> None:
        super(RaLSGAN, self).__init__()

    def discriminator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        relativistic_real_validity = real_validity - fake_validity.mean()
        relativistic_fake_validity = fake_validity - real_validity.mean()

        real_loss = (relativistic_real_validity - 1.0) ** 2
        fake_loss = (relativistic_fake_validity + 1.0) ** 2

        loss = (fake_loss.mean() + real_loss.mean()) / 2

        return loss.unsqueeze(0)

    def generator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        relativistic_real_validity = real_validity - fake_validity.mean()
        relativistic_fake_validity = fake_validity - real_validity.mean()

        real_loss = (relativistic_real_validity + 1.0) ** 2
        fake_loss = (relativistic_fake_validity - 1.0) ** 2

        loss = (fake_loss.mean() + real_loss.mean()) / 2

        return loss


class RaHinge(GANLoss):
    """
    Relativistiv Average Hinge

    Paper: https://papers.nips.cc/paper/1998/file/a14ac55a4f27472c5d894ec1c3c743d2-Paper.pdf
    """

    def __init__(self) -> None:
        super(RaHinge, self).__init__()

    def discriminator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        relativistic_real_validity = real_validity - fake_validity.mean()
        relativistic_fake_validity = fake_validity - real_validity.mean()

        real_loss = relu(1.0 - relativistic_real_validity)
        fake_loss = relu(1.0 + relativistic_fake_validity)

        loss = (real_loss.mean() + fake_loss.mean()) / 2

        return loss

    def generator_loss(self, real_validity: Tensor, fake_validity: Tensor) -> Tensor:
        relativistic_real_validity = real_validity - fake_validity.mean()
        relativistic_fake_validity = fake_validity - real_validity.mean()

        real_loss = relu(1.0 - relativistic_fake_validity)
        fake_loss = relu(1.0 + relativistic_real_validity)

        loss = (fake_loss.mean() + real_loss.mean()) / 2

        return loss
