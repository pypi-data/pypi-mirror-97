import torch.nn as nn

from .dice import DiceLoss
from .spline import SplineLoss


class DiceSplineLoss(nn.Module):
    r"""Creates a criterion that measures the Dice Spline Error
    between each element in the input :math:`X` and target :math:`Y`.

    Dice Spline loss is computed as a weighted average between Dice Loss and Spline Loss:

    .. math:: Loss(X,Y) = (1 - \alpha) \cdot Loss_{DC}(X,Y) + \alpha \cdot Loss_{AC}(X,Y)

    where :math:`\alpha` is Dice Spline Weight

    :math:`Loss_{DC}(X,Y)` is the Dice Loss component,which is computed as:

    .. math:: Loss_{DC}(X,Y) = 1 - DC(X,Y)

    here, :math:`DC(X,Y)` is Dice Cofficient between inputs :math:`X` and :math:`Y`, which is computed as:

    .. math:: DC(X,Y) = \frac{2 \cdot | X \cap Y | + \epsilon }{|X| + |Y| + \epsilon}

    where :math:`\epsilon` is a constant added for numerical stability.

    :math:`Loss_{AC}(X,Y)` is the Active Contour loss or Spline Loss component, which is computed as:

    .. math:: Loss_{AC} = Length + \lambda \cdot Region

    in which,

    .. math:: Length = \int_C \left| \nabla X \right| ds

    .. math:: Region = \int_{\Omega} ((1-Y)^{2} - Y^{2})Xdu

    :math:`Length` and :math:`Region` can be written in pixel wise form as:

    .. math:: Length = \sum\limits_{\Omega}^{i=1,j=1} \sqrt{\left| (\nabla X_{u_{i,j}})^{2} + (\nabla X_{v_{i,j}})^{2}\right| + \epsilon }

    where :math:`u` and :math:`v` from :math:`X_{u_{i,j}}` and :math:`X_{v_{i,j}}` are horizontal and vertical directions respectively,

    and :math:`\epsilon` is a constant added for numerical stability.

    .. math:: Region = \left| \sum\limits_{\Omega}^{i=1,j=1} X_{i,j} \cdot (1-Y_{i,j})^{2}\right| + \left| \sum\limits_{\Omega}^{i=1,j=1} (1-X_{i,j}) \cdot Y_{i,j}^{2}\right|

    Parameters
    ----------
    args : list
        arguments list.

    References
    ----------
    https://www.kaggle.com/bigironsphere/loss-function-library-keras-pytorch

    https://sci-hub.do/https://ieeexplore.ieee.org/document/8953484

    """

    def __init__(self, args):
        """Initialise loss module.

        Parameters
        ----------
        args : list
            arguments list.

        """
        super(DiceSplineLoss, self).__init__()
        self.gpu = args.gpu
        self.patch_size = args.input_shape[2]

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

        self.dice = DiceLoss(args)
        self.spline = SplineLoss(args)
        self.alpha = args.dice_spline_cntrl

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
            DiceSpline loss computed between :attr:`predicted` and
            :attr:`target`.

        """
        return (1 - self.alpha) * self.dice(predicted, target) + \
            self.alpha * self.spline(predicted, target)
