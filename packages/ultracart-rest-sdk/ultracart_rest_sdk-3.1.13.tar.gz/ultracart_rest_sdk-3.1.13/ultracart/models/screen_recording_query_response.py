# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ScreenRecordingQueryResponse(object):
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
        'error': 'Error',
        'filter': 'ScreenRecordingFilter',
        'filter_values': 'ScreenRecordingFilterValues',
        'metadata': 'ResponseMetadata',
        'screen_recordings': 'list[ScreenRecording]',
        'success': 'bool',
        'warning': 'Warning'
    }

    attribute_map = {
        'error': 'error',
        'filter': 'filter',
        'filter_values': 'filter_values',
        'metadata': 'metadata',
        'screen_recordings': 'screen_recordings',
        'success': 'success',
        'warning': 'warning'
    }

    def __init__(self, error=None, filter=None, filter_values=None, metadata=None, screen_recordings=None, success=None, warning=None):  # noqa: E501
        """ScreenRecordingQueryResponse - a model defined in Swagger"""  # noqa: E501

        self._error = None
        self._filter = None
        self._filter_values = None
        self._metadata = None
        self._screen_recordings = None
        self._success = None
        self._warning = None
        self.discriminator = None

        if error is not None:
            self.error = error
        if filter is not None:
            self.filter = filter
        if filter_values is not None:
            self.filter_values = filter_values
        if metadata is not None:
            self.metadata = metadata
        if screen_recordings is not None:
            self.screen_recordings = screen_recordings
        if success is not None:
            self.success = success
        if warning is not None:
            self.warning = warning

    @property
    def error(self):
        """Gets the error of this ScreenRecordingQueryResponse.  # noqa: E501


        :return: The error of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: Error
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this ScreenRecordingQueryResponse.


        :param error: The error of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: Error
        """

        self._error = error

    @property
    def filter(self):
        """Gets the filter of this ScreenRecordingQueryResponse.  # noqa: E501


        :return: The filter of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: ScreenRecordingFilter
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """Sets the filter of this ScreenRecordingQueryResponse.


        :param filter: The filter of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: ScreenRecordingFilter
        """

        self._filter = filter

    @property
    def filter_values(self):
        """Gets the filter_values of this ScreenRecordingQueryResponse.  # noqa: E501


        :return: The filter_values of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: ScreenRecordingFilterValues
        """
        return self._filter_values

    @filter_values.setter
    def filter_values(self, filter_values):
        """Sets the filter_values of this ScreenRecordingQueryResponse.


        :param filter_values: The filter_values of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: ScreenRecordingFilterValues
        """

        self._filter_values = filter_values

    @property
    def metadata(self):
        """Gets the metadata of this ScreenRecordingQueryResponse.  # noqa: E501


        :return: The metadata of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: ResponseMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ScreenRecordingQueryResponse.


        :param metadata: The metadata of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: ResponseMetadata
        """

        self._metadata = metadata

    @property
    def screen_recordings(self):
        """Gets the screen_recordings of this ScreenRecordingQueryResponse.  # noqa: E501


        :return: The screen_recordings of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: list[ScreenRecording]
        """
        return self._screen_recordings

    @screen_recordings.setter
    def screen_recordings(self, screen_recordings):
        """Sets the screen_recordings of this ScreenRecordingQueryResponse.


        :param screen_recordings: The screen_recordings of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: list[ScreenRecording]
        """

        self._screen_recordings = screen_recordings

    @property
    def success(self):
        """Gets the success of this ScreenRecordingQueryResponse.  # noqa: E501

        Indicates if API call was successful  # noqa: E501

        :return: The success of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: bool
        """
        return self._success

    @success.setter
    def success(self, success):
        """Sets the success of this ScreenRecordingQueryResponse.

        Indicates if API call was successful  # noqa: E501

        :param success: The success of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: bool
        """

        self._success = success

    @property
    def warning(self):
        """Gets the warning of this ScreenRecordingQueryResponse.  # noqa: E501


        :return: The warning of this ScreenRecordingQueryResponse.  # noqa: E501
        :rtype: Warning
        """
        return self._warning

    @warning.setter
    def warning(self, warning):
        """Sets the warning of this ScreenRecordingQueryResponse.


        :param warning: The warning of this ScreenRecordingQueryResponse.  # noqa: E501
        :type: Warning
        """

        self._warning = warning

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
        if issubclass(ScreenRecordingQueryResponse, dict):
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
        if not isinstance(other, ScreenRecordingQueryResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
