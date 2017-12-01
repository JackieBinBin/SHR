# -*- coding:utf-8 -*-
import xlrd
import datetime
import time
import json
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import hashlib
# import sys
# sys.setdefaultencoding('utf-8')

class ToolHandler(object):

    # invoke_time = lambda: int(round(time.time() * 1000))

    def invoke_time(self):
        return int(round(time.time() * 1000))

    def read_sh_re_info(self, filepath):

        user_data = []

        data = xlrd.open_workbook(filepath)
        table = data.sheets()[0]
        # get col
        # col_count = table.ncols
        # get row
        row_count = table.nrows

        for row in range(3, row_count+1):
            if table.row(row)[1].value == "":
                break
            else:
                user_data.append(table.row_values(row))
        return user_data


    def __encrypt_data(self, public_key, params):
        """Encrypt data with shanghai public key"""
        key = public_key
        rsakey = RSA.importKey(base64.b64decode(key))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.encrypt(params)
        return text

    def get_encrypt_data(self, public_key, params):
        """Block Encryption"""
        params = json.dumps(params)
        params = params.encode("utf-8")
        print params
        length = len(params)
        # print length
        default_length = 117
        if length < default_length:
            return self.__encrypt_data(public_key, params)
        offset = 0
        params_lst = []
        while length - offset > 0:
            if length - offset > default_length:
                params_lst.append(self.__encrypt_data(public_key, params[offset:offset+default_length]))
            else:
                params_lst.append(self.__encrypt_data(public_key, params[offset:]))
            offset += default_length
        res = "".join(params_lst)
        # return res, base64.b64encode(res)
        return base64.b64encode(res)

    def header_sign(self, appkey, secret, secretKey, signt):
        sign_str = "appKey=" + str(appkey) +",secret=RSA,signt=" + str(signt) +",secretKey=" + str(secretKey)
        # print sign_str
        sign = hashlib.md5(sign_str).hexdigest()
        # print sign
        return sign

    def body_config(self, userdata, vehicle_common_info, vehicle_business_info={}):

        body_info = []

        for vehicle_info_index in range(len(userdata)):

            vehicle_common_info['modelCode'] = userdata[vehicle_info_index][1]
            vehicle_common_info['vin'] = str(userdata[vehicle_info_index][2])
            vehicle_common_info['vehUse'] = int(userdata[vehicle_info_index][3])
            vehicle_common_info['vehMakeDate'] = userdata[vehicle_info_index][4]
            vehicle_common_info['saleDate'] = userdata[vehicle_info_index][5]
            vehicle_common_info['batAccuCode'] = str(userdata[vehicle_info_index][6])
            vehicle_common_info['accuMakeDate'] = userdata[vehicle_info_index][7]
            vehicle_common_info['sn'] = str(userdata[vehicle_info_index][8])
            vehicle_common_info['iccid'] = str(userdata[vehicle_info_index][9])
            vehicle_common_info['drivLicenNum'] = int(userdata[vehicle_info_index][10])
            vehicle_common_info['buyerCarCounty'] = int(userdata[vehicle_info_index][11])
            # vehicle_common_info['terminalType'] = int(userdata[vehicle_info_index][12])
            vehicle_common_info['terminalFirm'] = userdata[vehicle_info_index][13]
            vehicle_common_info['dynNo'] = str(userdata[vehicle_info_index][14])
            vehicle_common_info['engineNo'] = str(userdata[vehicle_info_index][15])
            vehicle_common_info['inDate'] = datetime.datetime.now().strftime("%Y-%m-%d")

            if userdata[vehicle_info_index][3] == 1:#Public Area
                vehicle_business_info['vehNo'] = str(userdata[vehicle_info_index][16])
                vehicle_business_info['motonCompany'] = userdata[vehicle_info_index][17]
                vehicle_business_info['addr'] = userdata[vehicle_info_index][18]
                vehicle_business_info['linkman'] = userdata[vehicle_info_index][19]
                vehicle_business_info['linkphone'] = int(userdata[vehicle_info_index][20])
                vehicle_business_info['operatUnitLegal'] = userdata[vehicle_info_index][21]
                vehicle_business_info['operatUnitLegalTel'] = int(userdata[vehicle_info_index][22])
                vehicle_business_info['operatUnitAddress'] = userdata[vehicle_info_index][23]
                vehicle_business_info['operatAddress'] = userdata[vehicle_info_index][24]
                vehicle_business_info['vehChargeAddress'] = userdata[vehicle_info_index][25]

                new_body_info = vehicle_common_info.copy()
                new_body_info.update(vehicle_business_info)
                body_info.append(new_body_info)
            elif userdata[vehicle_info_index][3] == 2:#Private Area
                body_info.append(vehicle_common_info)

            return body_info











