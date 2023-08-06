import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    r"""Creates a criterion that measures the Focal Error
    between each element in the input :math:`X` and target :math:`Y`..

    Focal loss is computed as:

    .. math:: Loss(X,Y) = \alpha \cdot (1 - E_{BCE}(X,Y))^{\gamma} \cdot Loss_{BCE}(X,Y) , \gamma \geqslant 0

    where :math:`Loss_{BCE}(X,Y)` is the BCE Loss component, which is computed as:

    .. math::
        Loss_{BCE}(X,Y) = \sum\limits_{i=1}^N l(x_i,y_i), l(x_i,y_i) = - w_i \left[ y_i \cdot \log x_i + (1 - y_i) \cdot \log (1 - x_i) \right]

    where :math:`x_i \in X` and :math:`y_i \in Y` and :math:`E_{BCE} = exp( - Loss_{BCE}(X,Y))`

    Parameters
    ----------
    args : type
        Description of parameter `args`.

    References
    ----------
    https://arxiv.org/pdf/1708.02002.pdf

    """

    def __init__(self, args):
        """Initialise loss module.

        Parameters
        ----------
        args : type
            Description of parameter `args`.

        """
        super(FocalLoss, self).__init__()
        self.gamma = args.gamma

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
            Focal loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.long()
        target = target.unsqueeze(1)
        p = predicted
        t = target

        if p.dim() > 2:
            p = p.view(p.size(0), p.size(1), -1)
            t = t.view(t.size(0), t.size(1), -1)
        else:
            p = p.unsqueeze(2)
            t = t.unsqueeze(2)

        logpt = F.log_softmax(p, dim=1)

        if target.shape[1] == 1:
            logpt = logpt.gather(1, t.long())
            logpt = torch.squeeze(logpt, dim=1)

        pt = torch.exp(logpt)

        weight = torch.pow(-pt + 1.0, self.gamma)

        if target.shape[1] == 1:
            loss = torch.mean(-weight * logpt, dim=1)
        # else:
        #    loss = torch.mean(-weight * t * logpt, dim=-1)

        return loss.mean()
