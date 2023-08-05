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


class EmailCampaign(object):
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
        'click_rate_formatted': 'str',
        'created_dts': 'str',
        'deleted': 'bool',
        'email_campaign_uuid': 'str',
        'email_communication_sequence_uuid': 'str',
        'end_once_customer_purchases': 'bool',
        'esp_campaign_folder_uuid': 'str',
        'esp_domain_user': 'str',
        'esp_domain_uuid': 'str',
        'esp_friendly_name': 'str',
        'library_item_oid': 'int',
        'memberships': 'list[EmailListSegmentMembership]',
        'merchant_id': 'str',
        'name': 'str',
        'open_rate_formatted': 'str',
        'prevent_sending_due_to_spam': 'bool',
        'revenue_formatted': 'str',
        'revenue_per_customer_formatted': 'str',
        'scheduled_dts': 'str',
        'screenshot_large_full_url': 'str',
        'status': 'str',
        'status_dts': 'str',
        'storefront_oid': 'int'
    }

    attribute_map = {
        'click_rate_formatted': 'click_rate_formatted',
        'created_dts': 'created_dts',
        'deleted': 'deleted',
        'email_campaign_uuid': 'email_campaign_uuid',
        'email_communication_sequence_uuid': 'email_communication_sequence_uuid',
        'end_once_customer_purchases': 'end_once_customer_purchases',
        'esp_campaign_folder_uuid': 'esp_campaign_folder_uuid',
        'esp_domain_user': 'esp_domain_user',
        'esp_domain_uuid': 'esp_domain_uuid',
        'esp_friendly_name': 'esp_friendly_name',
        'library_item_oid': 'library_item_oid',
        'memberships': 'memberships',
        'merchant_id': 'merchant_id',
        'name': 'name',
        'open_rate_formatted': 'open_rate_formatted',
        'prevent_sending_due_to_spam': 'prevent_sending_due_to_spam',
        'revenue_formatted': 'revenue_formatted',
        'revenue_per_customer_formatted': 'revenue_per_customer_formatted',
        'scheduled_dts': 'scheduled_dts',
        'screenshot_large_full_url': 'screenshot_large_full_url',
        'status': 'status',
        'status_dts': 'status_dts',
        'storefront_oid': 'storefront_oid'
    }

    def __init__(self, click_rate_formatted=None, created_dts=None, deleted=None, email_campaign_uuid=None, email_communication_sequence_uuid=None, end_once_customer_purchases=None, esp_campaign_folder_uuid=None, esp_domain_user=None, esp_domain_uuid=None, esp_friendly_name=None, library_item_oid=None, memberships=None, merchant_id=None, name=None, open_rate_formatted=None, prevent_sending_due_to_spam=None, revenue_formatted=None, revenue_per_customer_formatted=None, scheduled_dts=None, screenshot_large_full_url=None, status=None, status_dts=None, storefront_oid=None):  # noqa: E501
        """EmailCampaign - a model defined in Swagger"""  # noqa: E501

        self._click_rate_formatted = None
        self._created_dts = None
        self._deleted = None
        self._email_campaign_uuid = None
        self._email_communication_sequence_uuid = None
        self._end_once_customer_purchases = None
        self._esp_campaign_folder_uuid = None
        self._esp_domain_user = None
        self._esp_domain_uuid = None
        self._esp_friendly_name = None
        self._library_item_oid = None
        self._memberships = None
        self._merchant_id = None
        self._name = None
        self._open_rate_formatted = None
        self._prevent_sending_due_to_spam = None
        self._revenue_formatted = None
        self._revenue_per_customer_formatted = None
        self._scheduled_dts = None
        self._screenshot_large_full_url = None
        self._status = None
        self._status_dts = None
        self._storefront_oid = None
        self.discriminator = None

        if click_rate_formatted is not None:
            self.click_rate_formatted = click_rate_formatted
        if created_dts is not None:
            self.created_dts = created_dts
        if deleted is not None:
            self.deleted = deleted
        if email_campaign_uuid is not None:
            self.email_campaign_uuid = email_campaign_uuid
        if email_communication_sequence_uuid is not None:
            self.email_communication_sequence_uuid = email_communication_sequence_uuid
        if end_once_customer_purchases is not None:
            self.end_once_customer_purchases = end_once_customer_purchases
        if esp_campaign_folder_uuid is not None:
            self.esp_campaign_folder_uuid = esp_campaign_folder_uuid
        if esp_domain_user is not None:
            self.esp_domain_user = esp_domain_user
        if esp_domain_uuid is not None:
            self.esp_domain_uuid = esp_domain_uuid
        if esp_friendly_name is not None:
            self.esp_friendly_name = esp_friendly_name
        if library_item_oid is not None:
            self.library_item_oid = library_item_oid
        if memberships is not None:
            self.memberships = memberships
        if merchant_id is not None:
            self.merchant_id = merchant_id
        if name is not None:
            self.name = name
        if open_rate_formatted is not None:
            self.open_rate_formatted = open_rate_formatted
        if prevent_sending_due_to_spam is not None:
            self.prevent_sending_due_to_spam = prevent_sending_due_to_spam
        if revenue_formatted is not None:
            self.revenue_formatted = revenue_formatted
        if revenue_per_customer_formatted is not None:
            self.revenue_per_customer_formatted = revenue_per_customer_formatted
        if scheduled_dts is not None:
            self.scheduled_dts = scheduled_dts
        if screenshot_large_full_url is not None:
            self.screenshot_large_full_url = screenshot_large_full_url
        if status is not None:
            self.status = status
        if status_dts is not None:
            self.status_dts = status_dts
        if storefront_oid is not None:
            self.storefront_oid = storefront_oid

    @property
    def click_rate_formatted(self):
        """Gets the click_rate_formatted of this EmailCampaign.  # noqa: E501

        Click rate of emails  # noqa: E501

        :return: The click_rate_formatted of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._click_rate_formatted

    @click_rate_formatted.setter
    def click_rate_formatted(self, click_rate_formatted):
        """Sets the click_rate_formatted of this EmailCampaign.

        Click rate of emails  # noqa: E501

        :param click_rate_formatted: The click_rate_formatted of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._click_rate_formatted = click_rate_formatted

    @property
    def created_dts(self):
        """Gets the created_dts of this EmailCampaign.  # noqa: E501

        Created date  # noqa: E501

        :return: The created_dts of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._created_dts

    @created_dts.setter
    def created_dts(self, created_dts):
        """Sets the created_dts of this EmailCampaign.

        Created date  # noqa: E501

        :param created_dts: The created_dts of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._created_dts = created_dts

    @property
    def deleted(self):
        """Gets the deleted of this EmailCampaign.  # noqa: E501

        True if this campaign was deleted  # noqa: E501

        :return: The deleted of this EmailCampaign.  # noqa: E501
        :rtype: bool
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this EmailCampaign.

        True if this campaign was deleted  # noqa: E501

        :param deleted: The deleted of this EmailCampaign.  # noqa: E501
        :type: bool
        """

        self._deleted = deleted

    @property
    def email_campaign_uuid(self):
        """Gets the email_campaign_uuid of this EmailCampaign.  # noqa: E501

        Email campaign UUID  # noqa: E501

        :return: The email_campaign_uuid of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._email_campaign_uuid

    @email_campaign_uuid.setter
    def email_campaign_uuid(self, email_campaign_uuid):
        """Sets the email_campaign_uuid of this EmailCampaign.

        Email campaign UUID  # noqa: E501

        :param email_campaign_uuid: The email_campaign_uuid of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._email_campaign_uuid = email_campaign_uuid

    @property
    def email_communication_sequence_uuid(self):
        """Gets the email_communication_sequence_uuid of this EmailCampaign.  # noqa: E501

        Email communication sequence UUID  # noqa: E501

        :return: The email_communication_sequence_uuid of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._email_communication_sequence_uuid

    @email_communication_sequence_uuid.setter
    def email_communication_sequence_uuid(self, email_communication_sequence_uuid):
        """Sets the email_communication_sequence_uuid of this EmailCampaign.

        Email communication sequence UUID  # noqa: E501

        :param email_communication_sequence_uuid: The email_communication_sequence_uuid of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._email_communication_sequence_uuid = email_communication_sequence_uuid

    @property
    def end_once_customer_purchases(self):
        """Gets the end_once_customer_purchases of this EmailCampaign.  # noqa: E501

        True if the customer should end the flow once they purchase  # noqa: E501

        :return: The end_once_customer_purchases of this EmailCampaign.  # noqa: E501
        :rtype: bool
        """
        return self._end_once_customer_purchases

    @end_once_customer_purchases.setter
    def end_once_customer_purchases(self, end_once_customer_purchases):
        """Sets the end_once_customer_purchases of this EmailCampaign.

        True if the customer should end the flow once they purchase  # noqa: E501

        :param end_once_customer_purchases: The end_once_customer_purchases of this EmailCampaign.  # noqa: E501
        :type: bool
        """

        self._end_once_customer_purchases = end_once_customer_purchases

    @property
    def esp_campaign_folder_uuid(self):
        """Gets the esp_campaign_folder_uuid of this EmailCampaign.  # noqa: E501

        Campaign folder UUID.  Null for uncategorized  # noqa: E501

        :return: The esp_campaign_folder_uuid of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._esp_campaign_folder_uuid

    @esp_campaign_folder_uuid.setter
    def esp_campaign_folder_uuid(self, esp_campaign_folder_uuid):
        """Sets the esp_campaign_folder_uuid of this EmailCampaign.

        Campaign folder UUID.  Null for uncategorized  # noqa: E501

        :param esp_campaign_folder_uuid: The esp_campaign_folder_uuid of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._esp_campaign_folder_uuid = esp_campaign_folder_uuid

    @property
    def esp_domain_user(self):
        """Gets the esp_domain_user of this EmailCampaign.  # noqa: E501

        User of the sending address  # noqa: E501

        :return: The esp_domain_user of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._esp_domain_user

    @esp_domain_user.setter
    def esp_domain_user(self, esp_domain_user):
        """Sets the esp_domain_user of this EmailCampaign.

        User of the sending address  # noqa: E501

        :param esp_domain_user: The esp_domain_user of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._esp_domain_user = esp_domain_user

    @property
    def esp_domain_uuid(self):
        """Gets the esp_domain_uuid of this EmailCampaign.  # noqa: E501

        UUID of the sending domain  # noqa: E501

        :return: The esp_domain_uuid of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._esp_domain_uuid

    @esp_domain_uuid.setter
    def esp_domain_uuid(self, esp_domain_uuid):
        """Sets the esp_domain_uuid of this EmailCampaign.

        UUID of the sending domain  # noqa: E501

        :param esp_domain_uuid: The esp_domain_uuid of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._esp_domain_uuid = esp_domain_uuid

    @property
    def esp_friendly_name(self):
        """Gets the esp_friendly_name of this EmailCampaign.  # noqa: E501

        Friendly name of the sending email  # noqa: E501

        :return: The esp_friendly_name of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._esp_friendly_name

    @esp_friendly_name.setter
    def esp_friendly_name(self, esp_friendly_name):
        """Sets the esp_friendly_name of this EmailCampaign.

        Friendly name of the sending email  # noqa: E501

        :param esp_friendly_name: The esp_friendly_name of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._esp_friendly_name = esp_friendly_name

    @property
    def library_item_oid(self):
        """Gets the library_item_oid of this EmailCampaign.  # noqa: E501

        If this item was ever added to the Code Library, this is the oid for that library item, or 0 if never added before.  This value is used to determine if a library item should be inserted or updated.  # noqa: E501

        :return: The library_item_oid of this EmailCampaign.  # noqa: E501
        :rtype: int
        """
        return self._library_item_oid

    @library_item_oid.setter
    def library_item_oid(self, library_item_oid):
        """Sets the library_item_oid of this EmailCampaign.

        If this item was ever added to the Code Library, this is the oid for that library item, or 0 if never added before.  This value is used to determine if a library item should be inserted or updated.  # noqa: E501

        :param library_item_oid: The library_item_oid of this EmailCampaign.  # noqa: E501
        :type: int
        """

        self._library_item_oid = library_item_oid

    @property
    def memberships(self):
        """Gets the memberships of this EmailCampaign.  # noqa: E501

        List and segment memberships  # noqa: E501

        :return: The memberships of this EmailCampaign.  # noqa: E501
        :rtype: list[EmailListSegmentMembership]
        """
        return self._memberships

    @memberships.setter
    def memberships(self, memberships):
        """Sets the memberships of this EmailCampaign.

        List and segment memberships  # noqa: E501

        :param memberships: The memberships of this EmailCampaign.  # noqa: E501
        :type: list[EmailListSegmentMembership]
        """

        self._memberships = memberships

    @property
    def merchant_id(self):
        """Gets the merchant_id of this EmailCampaign.  # noqa: E501

        Merchant ID  # noqa: E501

        :return: The merchant_id of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._merchant_id

    @merchant_id.setter
    def merchant_id(self, merchant_id):
        """Sets the merchant_id of this EmailCampaign.

        Merchant ID  # noqa: E501

        :param merchant_id: The merchant_id of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._merchant_id = merchant_id

    @property
    def name(self):
        """Gets the name of this EmailCampaign.  # noqa: E501

        Name of email campaign  # noqa: E501

        :return: The name of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EmailCampaign.

        Name of email campaign  # noqa: E501

        :param name: The name of this EmailCampaign.  # noqa: E501
        :type: str
        """
        if name is not None and len(name) > 250:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `250`")  # noqa: E501

        self._name = name

    @property
    def open_rate_formatted(self):
        """Gets the open_rate_formatted of this EmailCampaign.  # noqa: E501

        Open rate of emails  # noqa: E501

        :return: The open_rate_formatted of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._open_rate_formatted

    @open_rate_formatted.setter
    def open_rate_formatted(self, open_rate_formatted):
        """Sets the open_rate_formatted of this EmailCampaign.

        Open rate of emails  # noqa: E501

        :param open_rate_formatted: The open_rate_formatted of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._open_rate_formatted = open_rate_formatted

    @property
    def prevent_sending_due_to_spam(self):
        """Gets the prevent_sending_due_to_spam of this EmailCampaign.  # noqa: E501

        True if this campaign is prevented from sending at this time due to spam complaints.  # noqa: E501

        :return: The prevent_sending_due_to_spam of this EmailCampaign.  # noqa: E501
        :rtype: bool
        """
        return self._prevent_sending_due_to_spam

    @prevent_sending_due_to_spam.setter
    def prevent_sending_due_to_spam(self, prevent_sending_due_to_spam):
        """Sets the prevent_sending_due_to_spam of this EmailCampaign.

        True if this campaign is prevented from sending at this time due to spam complaints.  # noqa: E501

        :param prevent_sending_due_to_spam: The prevent_sending_due_to_spam of this EmailCampaign.  # noqa: E501
        :type: bool
        """

        self._prevent_sending_due_to_spam = prevent_sending_due_to_spam

    @property
    def revenue_formatted(self):
        """Gets the revenue_formatted of this EmailCampaign.  # noqa: E501

        Revenue associated with campaign  # noqa: E501

        :return: The revenue_formatted of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._revenue_formatted

    @revenue_formatted.setter
    def revenue_formatted(self, revenue_formatted):
        """Sets the revenue_formatted of this EmailCampaign.

        Revenue associated with campaign  # noqa: E501

        :param revenue_formatted: The revenue_formatted of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._revenue_formatted = revenue_formatted

    @property
    def revenue_per_customer_formatted(self):
        """Gets the revenue_per_customer_formatted of this EmailCampaign.  # noqa: E501

        Revenue per customer associated with campaign  # noqa: E501

        :return: The revenue_per_customer_formatted of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._revenue_per_customer_formatted

    @revenue_per_customer_formatted.setter
    def revenue_per_customer_formatted(self, revenue_per_customer_formatted):
        """Sets the revenue_per_customer_formatted of this EmailCampaign.

        Revenue per customer associated with campaign  # noqa: E501

        :param revenue_per_customer_formatted: The revenue_per_customer_formatted of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._revenue_per_customer_formatted = revenue_per_customer_formatted

    @property
    def scheduled_dts(self):
        """Gets the scheduled_dts of this EmailCampaign.  # noqa: E501

        Scheduled date  # noqa: E501

        :return: The scheduled_dts of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._scheduled_dts

    @scheduled_dts.setter
    def scheduled_dts(self, scheduled_dts):
        """Sets the scheduled_dts of this EmailCampaign.

        Scheduled date  # noqa: E501

        :param scheduled_dts: The scheduled_dts of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._scheduled_dts = scheduled_dts

    @property
    def screenshot_large_full_url(self):
        """Gets the screenshot_large_full_url of this EmailCampaign.  # noqa: E501

        URL to a large full length screenshot  # noqa: E501

        :return: The screenshot_large_full_url of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._screenshot_large_full_url

    @screenshot_large_full_url.setter
    def screenshot_large_full_url(self, screenshot_large_full_url):
        """Sets the screenshot_large_full_url of this EmailCampaign.

        URL to a large full length screenshot  # noqa: E501

        :param screenshot_large_full_url: The screenshot_large_full_url of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._screenshot_large_full_url = screenshot_large_full_url

    @property
    def status(self):
        """Gets the status of this EmailCampaign.  # noqa: E501

        Status of the campaign of draft, archived, and sent  # noqa: E501

        :return: The status of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this EmailCampaign.

        Status of the campaign of draft, archived, and sent  # noqa: E501

        :param status: The status of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def status_dts(self):
        """Gets the status_dts of this EmailCampaign.  # noqa: E501

        Timestamp when the last status change happened  # noqa: E501

        :return: The status_dts of this EmailCampaign.  # noqa: E501
        :rtype: str
        """
        return self._status_dts

    @status_dts.setter
    def status_dts(self, status_dts):
        """Sets the status_dts of this EmailCampaign.

        Timestamp when the last status change happened  # noqa: E501

        :param status_dts: The status_dts of this EmailCampaign.  # noqa: E501
        :type: str
        """

        self._status_dts = status_dts

    @property
    def storefront_oid(self):
        """Gets the storefront_oid of this EmailCampaign.  # noqa: E501

        Storefront oid  # noqa: E501

        :return: The storefront_oid of this EmailCampaign.  # noqa: E501
        :rtype: int
        """
        return self._storefront_oid

    @storefront_oid.setter
    def storefront_oid(self, storefront_oid):
        """Sets the storefront_oid of this EmailCampaign.

        Storefront oid  # noqa: E501

        :param storefront_oid: The storefront_oid of this EmailCampaign.  # noqa: E501
        :type: int
        """

        self._storefront_oid = storefront_oid

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
        if issubclass(EmailCampaign, dict):
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
        if not isinstance(other, EmailCampaign):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
