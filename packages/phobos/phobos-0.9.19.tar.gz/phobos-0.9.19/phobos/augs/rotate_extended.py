import numpy as np
from scipy import ndimage as ndi

# from albumentations.augmentations import functional as F
from albumentations.core.transforms_interface import DualTransform, \
    to_tuple


class Rotate(DualTransform):
    r"""Rotate images and labels.

    Rotate RGB and Grayscale images and corresponding 2D masks, boundig boxes,
    and keypoints.

    Parameters
    ----------
    limit: float, default=90.0
        Maximum rotation angle allowed.

    border_mode: str, default='reflect'
        Type of border padding to be used.

    cval: float, default=0.0
        Value used for points outside the boundaries of the input if :attr: `border_mode='constant'`.

    always_apply: bool, default=False
        Flag to apply transform regardless of selection probability passed or not.

    p: float, default=0.5
        Value to set the selection probability which when passed allows transform to be applied.

    Examples
    ----------
    >>> import numpy as np
    >>> from phobos.augs import Rotate
    >>> rotate = Rotate()
    >>> img = np.random.randn(32, 32, 3)
    >>> random_angle = rotate.get_params()['angle']
    >>> img_r = rorate.apply(img, angle=random_angle)

    References
    ----------
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.rotate.html
    """

    def __init__(self, limit=90, border_mode='reflect', cval=0.0,
                 always_apply=False, p=0.5):
        super(Rotate, self).__init__(always_apply, p)

        self.limit = to_tuple(limit)
        self.border_mode = border_mode
        self.cval = cval

    def apply(self, im_arr, angle=0, border_mode='reflect', cval=0):
        """Apply rotation on image array im_arr using rotation parameters.

        Parameters
        ----------
        im_arr : ndarray
            image array to perform rotation on.

        angle : float, default=0.0
            rotational angle in degrees.

        border_mode : str, default='reflect'
            points outside input array border are filled according to given mode
            available options :
                (‘constant’, ‘nearest’,‘reflect’,‘wrap’).
        cval : scalar, default=0.0
            value required for input array border if border_mode = 'constant'.

        Returns
        -------
        ndarray
            The rotated image.

        Examples
        ----------
        >>> import numpy as np
        >>> from phobos.augs import Rotate
        >>> rotate = Rotate()
        >>> img = np.random.randn((32, 32, 3))
        >>> img_r = rotate.apply(img, angle=30)

        """
        return ndi.interpolation.rotate(im_arr, angle=angle,
                                        mode=self.border_mode, cval=self.cval)

    def get_params(self):
        """Retrieve and return rotation angle

           This angle is chosen at random between 0 and :attr: `limit`.

        Returns
        -------
        dict
            {key,value} pair where
              key   : 'angle'
              value : randomly generated rotation angle

        """
        return {'angle': np.random.randint(self.limit[0], self.limit[1])}

    def apply_to_bbox(self, bbox, angle=0, **params):
        """Apply rotation to bounding box bbox using rotation parameters.

        Parameters
        ----------
        bbox : tuple
            input bounding box (x_min, y_min, x_max, y_max).

        angle : float, default=0.0
            rotational angle in degrees.

        **params : list
            list of other rotation parameters.

        Returns
        -------
        type
            tuple: A rotated bounding box (x_min, y_min, x_max, y_max).

        """
        raise NotImplementedError
        # return F.bbox_rotate(bbox, angle, **params)

#    def apply_to_keypoint(self):
        """Apply rotation to keypoint

           Not implemented yet. NotImplementedError is raised for now"""
    #    raise NotImplementedError
