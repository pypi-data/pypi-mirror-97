# coding: utf-8

"""
    FeersumNLU API

    This is the HTTP API for Feersum NLU. See https://github.com/praekelt/feersum-nlu-api-wrappers for examples of how to use the API.  # noqa: E501

    OpenAPI spec version: 2.0.54.dev2
    Contact: nlu@feersum.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ModelRevision(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'version': 'int',
        'uuid': 'str',
        'message': 'str'
    }

    attribute_map = {
        'version': 'version',
        'uuid': 'uuid',
        'message': 'message'
    }

    def __init__(self, version=None, uuid=None, message=None):  # noqa: E501
        """ModelRevision - a model defined in Swagger"""  # noqa: E501

        self._version = None
        self._uuid = None
        self._message = None
        self.discriminator = None

        self.version = version
        self.uuid = uuid
        self.message = message

    @property
    def version(self):
        """Gets the version of this ModelRevision.  # noqa: E501

        The revision ID, a non-consecutive increasing unique number.  # noqa: E501

        :return: The version of this ModelRevision.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelRevision.

        The revision ID, a non-consecutive increasing unique number.  # noqa: E501

        :param version: The version of this ModelRevision.  # noqa: E501
        :type: int
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def uuid(self):
        """Gets the uuid of this ModelRevision.  # noqa: E501

        A universally unique ID used to reference this revision.  # noqa: E501

        :return: The uuid of this ModelRevision.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this ModelRevision.

        A universally unique ID used to reference this revision.  # noqa: E501

        :param uuid: The uuid of this ModelRevision.  # noqa: E501
        :type: str
        """
        if uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def message(self):
        """Gets the message of this ModelRevision.  # noqa: E501

        A longer existential description of this revision.  # noqa: E501

        :return: The message of this ModelRevision.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ModelRevision.

        A longer existential description of this revision.  # noqa: E501

        :param message: The message of this ModelRevision.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ModelRevision, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ModelRevision):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
