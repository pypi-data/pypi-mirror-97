from torch.optim.lr_scheduler import (MultiplicativeLR, StepLR,
                                      LambdaLR, MultiStepLR, ExponentialLR,
                                      ReduceLROnPlateau, CyclicLR,
                                      OneCycleLR, CosineAnnealingWarmRestarts)

scheduler_map = {
    'multiplicative': MultiplicativeLR,
    'step': StepLR,
    'lmbda': LambdaLR,
    'multistep': MultiStepLR,
    'exponential': ExponentialLR,
    'plateau': ReduceLROnPlateau,
    'cyclic': CyclicLR,
    'one_cycle': OneCycleLR,
    'cos_anneal': CosineAnnealingWarmRestarts
}


def get_scheduler(key, args, optimizer):
    """Creates and returns a scheduler based on scheduler type and arguments.

    Parameters
    ----------
    key : string
        type of scheduler instance
    args : dict
        dictionary of scheduler parameters.
    optimizer : torch.optim
        optimizer instance.

    Returns
    -------
    torch.optim.lr_scheduler
        scheduler instance.

    """

    scheduler = scheduler_map[key]
    args['optimizer'] = optimizer
    return scheduler(**args)
