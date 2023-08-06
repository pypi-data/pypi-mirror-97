import os
from inspect import getmodule
from argparse import ArgumentParser

import json


class Grain(ArgumentParser):
    """A class derived from class ArgumentParser which can
    be used for creating python objects from arguments.

    These arguments can be obtained from:

    1. Command Line Inputs
    2. Metadata JSON Files

    Grain can also be used to load arguments for models
    and log model inputs

    Parameters
    ----------
    polyaxon_exp : polyaxon.tracking.Run
        polyaxon experiment
    *args : list
        a non keyworded arguments' list.
    **kwargs : list
        a keyworded arguments' list.

    Attributes
    ----------
    add_argument : function
        adds arguments to Grain object.
    _band_ids_sep : function
        splits band ids.
    _input_shape_sep : function
        splits input shape.
    polyaxon_exp

    """

    def __init__(self, polyaxon_exp=None, *args, **kwargs):
        """Initialise Grain object using CLI arguments

        Parameters
        ----------
        polyaxon_exp : a polyaxon experiment to instantiate
                Grain object
        *args        : a non keyworded arguments' list
        **kwargs     : a keyworded arguments' list

        *args and **kwargs can be of any length
        """
        super(Grain, self).__init__(*args, **kwargs)
        self.polyaxon_exp = polyaxon_exp

        self.add_argument('--sensor',
                          type=str,
                          required=True,
                          help='Sensor in use (sentinel-2, landsat, planet)')

        self.add_argument('--band_ids',
                          type=self._band_ids_sep,
                          required=True,
                          help='Sensor band ids used in experiment')

        self.add_argument('--input_shape',
                          type=self._input_shape_sep,
                          required=True,
                          help='patch size for training process')

        self.add_argument('--resolution',
                          type=int,
                          required=True,
                          help='resolution of training process tensor')

    def parse_args(self, args=None, namespace=None):
        """Parse arguments passed as CLI Inputs

        Parameters
        ----------
        args      : list of arguments to be parsed.
                (default : None)
        namespace : namespace to validate arguments from
                (default : None)

        Returns
        -------
        type
            list of parsed arguments
        """
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = ('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))

        if self.polyaxon_exp:
            self.polyaxon_exp.log_inputs(**vars(args))

        return args

    def parse_args_from_json(self, json_file):
        """Parse arguments passed in json_file

        Parameters
        ----------
        json_file  : metadata JSON file

        Returns
        -------
        type
            list of parsed arguments
        """
        with open(json_file, 'r') as fin:
            metadata = json.load(fin)
            self.set_defaults(**metadata)

            args = self.parse_args([
                '--sensor', metadata['sensor'], '--band_ids',
                metadata['band_ids'], '--input_shape', metadata['input_shape'],
                '--resolution',
                str(metadata['resolution'])
            ])
            return args

    def load_model(self, model_cls, **kwargs):
        """Log and instantiate a model with keyword arguments

        Parameters
        ----------
        model_cls : torch.nn.modules.module.Module
            A pytorch model class to instantiate.
        **kwargs :
            all model positional arguments

        Returns
        -------
        type
            pytorch model object created from keyword arguments.

        """
        if self.polyaxon_exp:
            self._log_model(model_cls, **kwargs)
        return model_cls(**kwargs)

    def _log_model(self, model_cls, **kwargs):
        """Log model inputs

        Parameters
        ----------
        model_cls : torch.nn.modules.module.Module
            A pytorch model class.
        **kwargs :
            all model positional arguments

        """
        print("Logging model inputs")
        model_module = getmodule(model_cls).__name__
        model_path = os.path.relpath(getmodule(model_cls).__file__)
        model_name = model_cls.__name__

        self.polyaxon_exp.log_inputs(model_path=model_path,
                                     model_name=model_name,
                                     model_module=model_module,
                                     model_args=kwargs)

    @staticmethod
    def _band_ids_sep(band_ids):
        """splits band ids.

        Parameters
        ----------
        band_ids : list or string
            band ids to select.

        Returns
        -------
        list
            list of band ids.

        """
        if isinstance(band_ids, list):
            return band_ids
        return band_ids.split(',')

    @staticmethod
    def _input_shape_sep(input_shape):
        """splits input shape.

        Parameters
        ----------
        input_shape : list or string
            shape of input patch.

        Returns
        -------
        list
            list of input patch dimensions.

        """
        if isinstance(input_shape, list):
            return input_shape
        return list(map(int, input_shape.split(',')))
