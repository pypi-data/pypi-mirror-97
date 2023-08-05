import re
import os
import requests

from urllib.parse import urljoin


class Pybrary:
    __base_api_url = 'https://nyu.databrary.org/api/'
    __base_url = 'https://nyu.databrary.org/'
    __supersuer = None
    __session = None
    __instance = None

    @staticmethod
    def get_instance(username=None, password=None, superuser=False):
        if Pybrary.__instance is None:
            Pybrary(username, password, superuser)
        return Pybrary.__instance

    def __init__(self, username, password, superuser=False):
        if Pybrary.__instance is not None:
            raise Exception(
                'You are already logged in as {}, call Pybrary.get_instance().'.format(username))
        else:
            self.__supersuer = superuser
            try:
                self.__session = self.__login(username, password, superuser)
            except AttributeError as e:
                raise
            Pybrary.__instance = self

    def __login(self, username, password, superuser):
        """
        Login to Databrary
        :param username: a valid user name (email)
        :param password: Databrary password
        :return: a session
        """
        session = requests.Session()
        url = urljoin(self.__base_api_url, 'user/login')
        credentials = {
            "email": username,
            "password": password,
            "superuser": superuser
        }

        response = session.post(url=url, json=credentials)
        if response.status_code == 200:
            response_json = response.json()
            if 'csverf' in response_json:
                session.headers.update({
                    "x-csverf": response_json['csverf']
                })
        else:
            raise AttributeError('Login failed, please check your username and password')

        return session

    def logout(self):
        """
        Disconnect from Databrary
        :return:
        """
        url = urljoin(self.__base_api_url, 'user/logout')
        response = self.__session.post(url=url)
        if response.status_code == 200:
            Pybrary.__instance = None
            __username = None
            __supersuer = None
            del self.__session
        else:
            raise AttributeError('Login failed, please check your username and password')

    def get_party(self, party_id):
        """
        Get user info
        :param party_id: user id
        :return: user info in json format
        """
        url = urljoin(self.__base_api_url, 'party/' + str(party_id))
        response = self.__session.get(url=url)
        if response.status_code == 200:
            return response.json()
        else:
            raise AttributeError('Cannot fetch party data')

    def get_csv(self, volume_id, target_dir):
        """
        Download a CSV file from a Databrary volume, read access to the volume is required.
        :param volume_id: Databrary volume id
        :param target_dir: CSV file directory target
        :return: Path to the CSV file
        """

        def get_filename_from_cd(cd):
            """
            Get filename from content-disposition
            """
            if not cd:
                return None
            fname = re.findall('filename="(.+)"', cd)
            if len(fname) == 0:
                return None
            return fname[0]

        url = urljoin(self.__base_url, 'volume/' + str(volume_id) + '/csv')

        response = self.__session.get(url, allow_redirects=True)
        if response.status_code == 200:
            file_name = get_filename_from_cd(response.headers.get('content-disposition'))
            file_path = os.path.join(target_dir, file_name)
            open(file_path, 'wb').write(response.content)
            return file_path
        else:
            raise AttributeError('Cannot download CSV file from volume %d', volume_id)

    def get_session_records(self, volume_id, session_id):
        """
        Get session records
        :param volume_id: volume id
        :param session_id: session id
        :return:
        """
        payload = {'records': 1}
        url = urljoin(self.__base_api_url, 'volume/' + str(volume_id) + '/slot/' + str(session_id))

        response = self.__session.get(url=url, params=payload)
        if response.status_code == 200:
            return response.json()['records']
        else:
            raise AttributeError('Cannot retrieve records list from session %d in volume %d', session_id, volume_id)

    def get_session_participants(self, volume_id, session_id):
        """
        Get session participants
        :param volume_id: Volume id
        :param session_id: Session id
        :return:
        """
        records = self.get_session_records(volume_id, session_id)
        participants_list = [record for record in records if record.get("record", {}).get("category") == 1]
        return participants_list

    def get_session_assets(self, volume_id, session_id):
        """
        Get volume's asset list
        :param volume_id: Databrary volume id
        :param session_id: Databrary session id
        :return: a list of session ids in JSON format
        """
        payload = {'assets': 1}
        url = urljoin(self.__base_api_url, 'volume/' + str(volume_id) + '/slot/' + str(session_id))

        response = self.__session.get(url=url, params=payload)
        if response.status_code == 200:
            return response.json()['assets']
        else:
            raise AttributeError('Cannot retrieve asset list from session %d in volume %d', session_id, volume_id)

    def get_sessions(self, volume_id):
        """
        Get a list of containers(session) from a Databrary volume
        :param volume_id: Databrary volume id
        :return: a list of session ids in JSON format
        """
        payload = {'containers': 1}
        url = urljoin(self.__base_api_url, 'volume/' + str(volume_id))

        response = self.__session.get(url=url, params=payload)
        if response.status_code == 200:
            return response.json()['containers']
        else:
            raise AttributeError(
                'Cannot retrieve sessions list from volume %d', volume_id)

    def get_volume_assets(self, volume_id):
        """
        Get volume assets, the function will fetch assets found in the volume sessions
        :param volume_id: Volume id
        :return: a list of assets in json format
        """
        sessions = []
        for session in self.get_sessions(volume_id):
            session.update({"assets": self.get_session_assets(volume_id, session['id'])})
            sessions.append(session)
        return sessions

    def get_volume_info(self, volume_id):
        """
        Get volume's info
        :param volume_id:  Volume id
        :return: volume's info in json format
        """
        payload = {
            'access': "",
            'citation': "",
            'links': "",
            'funding': "",
            'top': "",
            'tags': "",
            'excerpts': "",
            'comments': "",
            'records': "",
            'containers': "all",
            'metrics': "",
            'state': "",
        }

        url = urljoin(self.__base_api_url, 'volume/' + str(volume_id))

        response = self.__session.get(url=url, params=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise AttributeError('Cannot retrieve volume %d info', volume_id)

    def get_asset_info(self, asset_id):
        """
        Get asset Id
        :param asset_id:
        :return:
        """
        url = urljoin(self.__base_api_url, 'asset/' + str(asset_id))

        response = self.__session.get(url=url)
        if response.status_code == 200:
            return response.json()
        else:
            raise AttributeError('Cannot retrieve asset %d info', asset_id)

    def post_asset_name(self, asset_id, asset_name):
        """
        Change asset name
        :param asset_id: Asset id
        :param asset_name: New asset name
        :return:
        """
        payload = {'name': str(asset_name)}
        url = urljoin(self.__base_api_url, 'asset/' + str(asset_id))

        response = self.__session.post(url=url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise AttributeError('Cannot change asset name to %s', str(asset_name))

    def post_asset_permission(self, asset_id, permission):
        """
        Change asset permissions, permissions are:
            Private = 0
            Authorized = 1
            Learning = 2
            Public = 3
        :param asset_id: asset id
        :param permission: permission id
        :return:
        """
        payload = {
            'name': self.get_file_info(asset_id)['name'],
            'classification': permission
        }
        url = urljoin(self.__base_api_url, 'asset/' + str(asset_id))
        response = self.__session.post(url=url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise AttributeError('Cannot change asset permission to %s', str(permission))
