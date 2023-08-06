# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains functionality for managing the configuration of experiment runs
in Azure Machine Learning.

The key class in this module is :class:`azureml.contrib.core.k8srunconfig.K8sComputeConfiguration`,
which encapsulates information necessary to submit a training run on k8s compute target."""
import collections

from azureml._base_sdk_common.field_info import _FieldInfo
from azureml._base_sdk_common.abstract_run_config_element import _AbstractRunConfigElement


class AISuperComputerConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for experiments that target AISuperComputer.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param instance_type: The class of compute to be used. Supported values: Any
        `AI Super Computer size <https://aiscaasdocs.azurewebsites.net/docs/instanceseries.md>`_.
    :type instance_type: str
    :param image_version: The image version to use.
    :type image_version: str
    :param location: The location where the run will execute. Will default to workspace region if not specified.
    :type location: str
    :param interactive: Whether or not the job should be run in interactive mode. Default: False.
    :type interactive: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("instance_type", _FieldInfo(str, "The class of compute to be used."
                                          "The list of instance types is available in '"
                                          "https://aiscaasdocs.azurewebsites.net/docs/instanceseries.md")
         ),
        ("image_version", _FieldInfo(str, "The image version to use.")),
        ("location", _FieldInfo(str, "The location where the run will execute.")),
        ("interactive", _FieldInfo(bool, "Whether or not the job should run in interactive mode. Default: False."))
    ])

    def __init__(self):
        """Class AISuperComputerConfiguration constructor."""
        self.instance_type = None
        self.image_version = None
        self.location = None
        self.interactive = False
