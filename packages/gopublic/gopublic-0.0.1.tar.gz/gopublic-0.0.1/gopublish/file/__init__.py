from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from gopublish.client import Client

from future import standard_library

import getpass

standard_library.install_aliases()


class FileClient(Client):
    """
    Manipulate files managed by Gopublish
    """

    def list(self):
        """
        List files published in Gopublish

        :rtype: list
        :return: List of files
        """

        body = {}
        return self._api_call("get", "list_files", body)['files']

    def search(self, file_name):
        """
        Launch a pull task

        :type file_name: str
        :param file_name: Either a file name, or a file UID

        :rtype: list
        :return: List of files matching the search
        """
        body = {"file": file_name}

        return self._api_call("get", "search", body, inline=True)['files']

    def publish(self, path, username, version=1, contact="", email=""):
        """
        Launch a publish task

        :type path: str
        :param path: Path to the file to be published

        :type username: str
        :param username: Username for the login

        :type version: int
        :param version: Version of the file to publish

        :type contact: str
        :param contact: Contact email for this file

        :type email: str
        :param email: Contact email for notification when publication is done

        :rtype: dict
        :return: Dictionnary containing the response
        """
        body = {"path": path, "version": version, "contact": contact, "email": email}
        auth = None
        if email:
            body['email'] = email

        if contact:
            body['contact'] = contact

        if self.gopublish_mode == "prod":
            try:
                password = getpass.getpass(prompt='Enter your GenOuest password ')
            except Exception as error:
                print('Error', error)

            auth = (username, password)
        else:
            body['username'] = username

        return self._api_call("post", "publish_file", body, auth=auth)
