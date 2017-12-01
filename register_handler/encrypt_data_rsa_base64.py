import json

def get_encrypt_data(params):
    """Block Encryption"""
    params = json.dumps(params)
    params = params.encode("utf-8")
    length = len(params)
    default_length = 117
    if length < default_length:
        return encrypt_data(params)
    offset = 0
    params_lst = []
    while length - offset > 0:
        if length - offset > default_length:
            params_lst.append(encrypt_data(params[offset:offset+default_length]))
        else:
            params_lst.append(encrypt_data(params[offset:]))
        offset += default_length
    res = "".join(params_lst)
    return res, base64.b64encode(res)
