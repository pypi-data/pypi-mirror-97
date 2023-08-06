from DobotRPC import loggers
from .function import Util, Face, Speech, Nlp, Ocr, Robot, Tmt
from .pyimageom import Pyimageom
from .device import LiteApi, MagicBoxApi, MagicianApi, MagicianGoApi
from .betago import BetaGoApi
import requests
import json
import sounddevice
import soundfile
import playsound
import scipy

loggers.set_use_file(False)


class DobotEDU(object):
    def __init__(self, account: str = None, password: str = None):
        if account is not None and password is not None:
            try:
                url = "https://dobotlab.dobot.cc/api/auth/login"
                headers = {"Content-Type": "application/json"}
                payload = {"account": account, "password": password}
                r = requests.post(url,
                                  headers=headers,
                                  data=json.dumps(payload))
                data = json.loads(r.content.decode())
                status = data["status"]
                if status == "error":
                    raise Exception(data["message"])
                token = data["data"]["token"]
            except Exception as e:
                token = None
                loggers.get('DobotEDU').exception(e)
                loggers.get('DobotEDU').error(
                    f"Please check that the account name and password are correct.If correct, please contact the technician:{e}"
                )
        else:
            token = None
            loggers.get('DobotEDU').info(
                "You have not entered your username and password. AI API cannot be used!"
            )

        self.__magician_api = MagicianApi()
        self.__lite_api = LiteApi()
        self.__magicbox_api = MagicBoxApi()
        self.__magiciango_api = MagicianGoApi()
        self.__util = Util()
        self.__pyimageom = Pyimageom()
        self.__betago = BetaGoApi()

        self.__token = token
        self.__robot = Robot(self.__token)
        self.__face = Face(self.__token)
        self.__ocr = Ocr(self.__token)
        self.__nlp = Nlp(self.__token)
        self.__speech = Speech(self.__token)
        self.__tmt = Tmt(self.__token)

    def set_portname(self, port_name: str):
        self.__lite_api._port_name = port_name
        self.__magiciango_api._port_name = port_name
        self.__magician_api._port_name = port_name
        self.__magicbox_api._port_name = port_name
        self.__betago._port_name = port_name

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token: str):
        self.__token = token

        self.__robot.token = token
        self.__face.token = token
        self.__ocr.token = token
        self.__nlp.token = token
        self.__speech.token = token
        self.__tmt.token = token

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url: str):

        self.__robot.url = url
        self.__face.url = url
        self.__ocr.url = url
        self.__nlp.url = url
        self.__speech.url = url
        self.__tmt.url = url

    @property
    def face(self):
        return self.__face

    @property
    def ocr(self):
        return self.__ocr

    @property
    def nlp(self):
        return self.__nlp

    @property
    def speech(self):
        return self.__speech

    @property
    def robot(self):
        return self.__robot

    @property
    def tmt(self):
        return self.__tmt

    @property
    def util(self):
        return self.__util

    @property
    def pyimageom(self):
        return self.__pyimageom

    @property
    def beta_go(self):
        return self.__betago
    # @property
    # def log(self):
    #     return loggers

    @property
    def magician(self):
        return self.__magician_api

    @property
    def m_lite(self):
        return self.__lite_api

    @property
    def magicbox(self):
        return self.__magicbox_api

    @property
    def magiciango(self):
        return self.__magiciango_api