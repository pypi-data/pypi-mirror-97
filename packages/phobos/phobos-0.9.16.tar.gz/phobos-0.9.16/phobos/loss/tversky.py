import torch
import torch.nn as nn


class TverskyLoss(nn.Module):
    r"""Creates a criterion that measures the Tversky Error
    between each element in the input :math:`X` and target :math:`Y`.

    Tversky Coefficient is computed as:

    .. math:: TC(X,Y) = \frac{ TP + \epsilon }{ TP + \alpha \cdot FP + \beta \cdot FN + \epsilon }

    where,

    :math:`TP \equiv` Number of True Positives :math:`= \left| X \cap Y \right|`

    :math:`FP \equiv` Number of False Positives :math:`= \left| X \; \cap \sim Y \right|`

    :math:`FN \equiv` Number of False Negatives :math:`= \left| \sim X \cap Y \right|`

    and :math:`\epsilon` is a constant added for numerical stability.

    Tversky Loss is computed as:

    .. math:: Loss_{TC}(X,Y) = 1 - TC(X,Y)

    If :math:`\alpha = \beta = 0.5 , TC(X,Y) \equiv` Dice Coefficient

    If :math:`\alpha = \beta = 1.0 , TC(X,Y) \equiv` Tanimoto Coefficient

    If :math:`\alpha + \beta = 1.0 , TC(X,Y) \equiv` F Beta Coefficient

    Parameters
    ----------
    args : type
        Description of parameter `args`.

    References
    ----------
    https://arxiv.org/abs/1706.05721

    """

    def __init__(self, args):
        """Initialise loss module.

        Parameters
        ----------
        args : list
            arguments list.

        """
        super(TverskyLoss, self).__init__()
        self.alpha = args.alpha
        self.beta = args.beta
        self.gpu = args.gpu

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

        if hasattr(args, 'size_average'):
            self.size_average = args.size_average
        else:
            self.size_average = True

    def forward(self, predicted, target):
        """Compute loss between :attr:`predicted` and :attr:`target`.

        :attr:`predicted` and :attr:`target` are tensors of shape :math:`[B,1,H,W]`

        Parameters
        ----------
        predicted : torch.Tensor
            Predicted output tensor from a model.
        target : torch.Tensor
            Ground truth tensor.

        Returns
        -------
        torch.Tensor
            Tversky loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.float()
        target = target.unsqueeze(1)

        neg_predicted = 1 - predicted
        neg_target = 1 - target

        dims = tuple(range(2, len(predicted.shape)))

        tps = torch.sum(predicted * target, dims)
        fps = self.alpha * torch.sum(predicted * neg_target, dims)
        fns = self.beta * torch.sum(neg_predicted * target, dims)

        numerator = tps + self.eps
        denominator = tps + fps + fns + self.eps

        tversky_loss = 1 - (numerator / denominator)

        return tversky_loss.mean()
