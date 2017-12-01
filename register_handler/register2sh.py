# -*- coding:utf-8 -*-
import requests
# from register_config import *
import yaml
from ToolHandler import *


class Register2sh(ToolHandler):
    def __init__(self, filepath):
        """
        Initializes _login_session = None
        """
        self._login_session = None

        self.filepath = filepath

        f = open('settings.yaml')
        self.settings = yaml.load(f)

    def register_vehicle_info(self):
        self._login_session = requests.session()

        # register_url http://106.14.51.20:8080/EvdataAPI/veh/add
        register_url = self.settings['register_2_shanghai']['registerurl']

        # config register header:
        appkey = self.settings['register_header']['appKey']
        secret = self.settings['register_header']['secret']
        secretKey = self.settings['register_header']['secretKey']
        signt = self.invoke_time()
        sign = self.header_sign(appkey, secret, secretKey, signt)

        register_headers = {'appKey': appkey, 'secret': secret,
                            'signt': signt, 'sign': sign}

        # config register_body
        user_data = self.read_sh_re_info(self.filepath)
        # print user_data

        vehicle_common_info = self.settings['register_vehicle_common_info']

        vehicle_body_info = self.body_config(user_data, vehicle_common_info)

        # Encrypt body info
        encrypt_body = self.get_encrypt_data(self.settings['register_2_shanghai']['publickey'], vehicle_body_info)

        # print encrypt_body

        r = self._login_session.post(register_url, headers=register_headers,
                            data=encrypt_body)

        # print r.url
        # print r.json()

        # Login success or not determined by code
        if r.status_code == 200:
            print "Connection to shanghai Data Center Success!"
            response = r.json()

            if response['status'] == "SUCCESS":
                print 'Register Success'
            # print "shanghai response: " + str(r.json())
            else:
                print response
        else:
            print "Error Code: " + str(r.status_code)
            print "shanghai response: " + str(r.json())
            print r.raise_for_status()

if __name__ == '__main__':

    i = Register2sh('C:\\Users\\Gary\\Desktop\\temp_vehicle_v3.0.xlsx')
    i.register_vehicle_info()
