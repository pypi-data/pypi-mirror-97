import torch.nn as nn

from .dice import DiceLoss
from .dice_spline import DiceSplineLoss
from .focal import FocalLoss
from .jaccard import JaccardLoss
from .binary_jaccard import BCEJaccardLoss
from .spline import SplineLoss
from .tversky import TverskyLoss

__all__ = ['DiceLoss', 'DiceSplineLoss', 'FocalLoss',
           'JaccardLoss', 'SplineLoss', 'TverskyLoss',
           'BCEJaccardLoss']

loss_map_args = {
    'dice': DiceLoss,
    'focal': FocalLoss,
    'jaccard': JaccardLoss,
    'tversky': TverskyLoss,
    'spline': SplineLoss,
    'dice_spline': DiceSplineLoss,
    'binary_jaccard': BCEJaccardLoss
}

loss_map_noargs = {
    'ce': nn.CrossEntropyLoss,
    'mlsml': nn.MultiLabelSoftMarginLoss,
    'mlbce': nn.BCEWithLogitsLoss
}


def get_loss(args):
    """Get loss function based on passed args.

    Parameters
    ----------
    args : args
        Parsed arguments.

    Returns
    -------
    phobos.loss
        Selected loss class object.

    """

    if args.loss in loss_map_args:
        loss = loss_map_args[args.loss]
        return loss(args)

    if args.loss in loss_map_noargs:
        loss = loss_map_noargs[args.loss]
        return loss()
