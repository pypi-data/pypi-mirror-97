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


class DucklingEntityExtractorInstanceDetail(object):
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
        'name': 'str',
        'id': 'str',
        'long_name': 'str',
        'desc': 'str',
        'readonly': 'bool',
        'reference_time': 'str'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'long_name': 'long_name',
        'desc': 'desc',
        'readonly': 'readonly',
        'reference_time': 'reference_time'
    }

    def __init__(self, name=None, id=None, long_name=None, desc=None, readonly=None, reference_time=None):  # noqa: E501
        """DucklingEntityExtractorInstanceDetail - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._id = None
        self._long_name = None
        self._desc = None
        self._readonly = None
        self._reference_time = None
        self.discriminator = None

        self.name = name
        self.id = id
        if long_name is not None:
            self.long_name = long_name
        if desc is not None:
            self.desc = desc
        if readonly is not None:
            self.readonly = readonly
        if reference_time is not None:
            self.reference_time = reference_time

    @property
    def name(self):
        """Gets the name of this DucklingEntityExtractorInstanceDetail.  # noqa: E501

        The sluggy-url-friendly-name of the instance.  # noqa: E501

        :return: The name of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DucklingEntityExtractorInstanceDetail.

        The sluggy-url-friendly-name of the instance.  # noqa: E501

        :param name: The name of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def id(self):
        """Gets the id of this DucklingEntityExtractorInstanceDetail.  # noqa: E501

        The unique id of a specific version of the instance.  # noqa: E501

        :return: The id of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DucklingEntityExtractorInstanceDetail.

        The unique id of a specific version of the instance.  # noqa: E501

        :param id: The id of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def long_name(self):
        """Gets the long_name of this DucklingEntityExtractorInstanceDetail.  # noqa: E501

        The human-friendly-name of the instance.  # noqa: E501

        :return: The long_name of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._long_name

    @long_name.setter
    def long_name(self, long_name):
        """Sets the long_name of this DucklingEntityExtractorInstanceDetail.

        The human-friendly-name of the instance.  # noqa: E501

        :param long_name: The long_name of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """

        self._long_name = long_name

    @property
    def desc(self):
        """Gets the desc of this DucklingEntityExtractorInstanceDetail.  # noqa: E501

        The longer existential description of this instance's purpose in life.  # noqa: E501

        :return: The desc of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._desc

    @desc.setter
    def desc(self, desc):
        """Sets the desc of this DucklingEntityExtractorInstanceDetail.

        The longer existential description of this instance's purpose in life.  # noqa: E501

        :param desc: The desc of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """

        self._desc = desc

    @property
    def readonly(self):
        """Gets the readonly of this DucklingEntityExtractorInstanceDetail.  # noqa: E501

        Indicates if the model is readonly and not editable.  # noqa: E501

        :return: The readonly of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: bool
        """
        return self._readonly

    @readonly.setter
    def readonly(self, readonly):
        """Sets the readonly of this DucklingEntityExtractorInstanceDetail.

        Indicates if the model is readonly and not editable.  # noqa: E501

        :param readonly: The readonly of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :type: bool
        """

        self._readonly = readonly

    @property
    def reference_time(self):
        """Gets the reference_time of this DucklingEntityExtractorInstanceDetail.  # noqa: E501

        The reference time of the date parser. Uses international standard date notation 'YYYY-MM-DD hh:mm+hh:mm' e.g. '2017-12-01', '2017-12-01 10:00' (server local zone), '2017-12-01 10:00+02:00'  # noqa: E501

        :return: The reference_time of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._reference_time

    @reference_time.setter
    def reference_time(self, reference_time):
        """Sets the reference_time of this DucklingEntityExtractorInstanceDetail.

        The reference time of the date parser. Uses international standard date notation 'YYYY-MM-DD hh:mm+hh:mm' e.g. '2017-12-01', '2017-12-01 10:00' (server local zone), '2017-12-01 10:00+02:00'  # noqa: E501

        :param reference_time: The reference_time of this DucklingEntityExtractorInstanceDetail.  # noqa: E501
        :type: str
        """

        self._reference_time = reference_time

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
        if issubclass(DucklingEntityExtractorInstanceDetail, dict):
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
        if not isinstance(other, DucklingEntityExtractorInstanceDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
