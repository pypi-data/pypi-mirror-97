import torch
import torch.nn as nn


class DiceLoss(nn.Module):
    r"""Creates a criterion that measures and maximizes Dice Error
    between each element in the input :math:`X` and target :math:`Y`.

    Dice Cofficient between inputs :math:`X` and :math:`Y` is computed as:

    .. math:: DC(X,Y) = \frac{2 \cdot | X \cap Y | + \epsilon }{|X| + |Y| + \epsilon}

    where :math:`\epsilon` is a constant added for numerical stability.

    Dice Loss is computed as:

    .. math:: Loss_{DC}(X,Y) = 1 - DC(X,Y)

    Please note that Dice Loss computed finally will be negated as our
    intention is to maximize Dice Loss. General PyTorch optimizers can be
    employed to minimize Dice Loss.

    Parameters
    ----------
    args : list
        arguments list.

    References
    ----------
    https://www.kaggle.com/bigironsphere/loss-function-library-keras-pytorch

    """

    def __init__(self, args):
        """Initialise loss module.

        Parameters
        ----------
        args : list
            arguments list.

        """
        super(DiceLoss, self).__init__()
        self.gpu = args.gpu

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

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
            Dice loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.long()
        target = target.unsqueeze(1)

        dims = tuple(range(2, len(predicted.shape)))
        intersection = torch.sum(target * predicted, dim=dims)

        target_o = torch.sum(target, dim=dims)
        predicted_o = torch.sum(predicted, dim=dims)

        denominator = target_o + predicted_o

        dice_loss = 1.0 - (2.0 * intersection + self.eps) /\
                          (denominator + self.eps)

        return dice_loss.mean()
