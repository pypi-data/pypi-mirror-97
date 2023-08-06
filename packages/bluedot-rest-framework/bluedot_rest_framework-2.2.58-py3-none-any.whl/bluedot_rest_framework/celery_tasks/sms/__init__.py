from yunpian_python_sdk.ypclient import YunpianClient
from yunpian_python_sdk.model import constant as YC


class SMS:
    clnt = YunpianClient('4dfe458293048805e8693f76e10187a4')
    # clnt = YunpianClient('aa3bfb5616d08bd4cd9a5ff938010cbc')

    def __init__(self, tel, text):
        self.param = {'mobile': tel, 'text': text}

    def send(self):
        return self.clnt.sms().single_send(self.param)
