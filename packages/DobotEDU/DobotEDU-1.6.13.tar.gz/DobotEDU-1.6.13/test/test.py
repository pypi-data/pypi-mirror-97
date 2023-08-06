from DobotEDU import DobotEDU
import requests
import json
import base64
import time


def test_shili():
    do = DobotEDU()
    assert do.__init__


def test_shili2():
    do = DobotEDU('222', '333')
    assert do.__init__


def test_shili3():
    dobotEdu = DobotEDU('yuejiang', 'YJ123456')
    assert dobotEdu.__init__


def test_tx():
    dobotEdu = DobotEDU('yuejiang', 'YJ123456')
    r = dobotEdu.nlp.topic('警方通报女游客无故推倒景区设施：由于个人生活发生重大变故导致情绪行为')
    # print(r)
    assert type(r) is str


def test_settoken():
    dobotEdu = DobotEDU()
    url = "https://dobotlab.dobot.cc/api/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = {"account": "yuejiang", "password": "YJ123456"}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    token = json.loads(r.content.decode())["data"]["token"]
    dobotEdu.token = token
    print(token)
    r = dobotEdu.nlp.topic('警方通报女游客无故推倒景区设施：由于个人生活发生重大变故导致情绪行为')
    # print(r)
    assert type(r) is str


def test_sy():
    dobotEdu = DobotEDU('yuejiang', 'YJ123456')
    r = dobotEdu.speech.synthesis('你好', 1)
    # print(r)
    assert type(r) is bytes


def ToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        return base64_data


def test_voice():
    do = DobotEDU('yuejiang', 'YJ123456')
    res = ToBase64('D:/gitttt/dobotedu/test/222.mp3')
    # print(res)
    res1 = do.speech.asr(res)
    # print(res1)
    assert type(res1) is str


def test_image():
    do = DobotEDU('yuejiang', 'YJ123456')
    res = ToBase64('D:/gitttt/dobotedu/test/4.jpg')
    # print(res)
    res2 = do.face.create_person(group_id="123",
                                 person_name="shua",
                                 person_id="333",
                                 image=res)
    assert res2 is not True
    # print(res2)


def test_magicbox():
    do = DobotEDU('yuejiang', 'YJ123456')
    res = do.magicbox.search_dobot()
    port = res[0]["portName"]
    do.magicbox.connect_dobot(port)
    do.m_lite.set_homecmd(port)
    do.magicbox.set_ptpwith_lcmd(port, 0)


def test_magicianlite():
    do = DobotEDU('yuyuyu', 'yuyu78YU')
    res = do.m_lite.search_dobot()
    print(res)
    port = res[0]["portName"]
    do.m_lite.connect_dobot(port)
    do.m_lite.set_homecmd(port)
    do.m_lite.set_jogjoint_params(velocity=10, acceleration=20)


def test_magicianhhh():
    do = DobotEDU('yuyuyu', 'yuyu78YU')
    res = do.magician.search_dobot()
    print(res)
    port = res[0]["portName"]
    do.magician.connect_dobot(port)
    do.magician.set_ptpcmd(port, 0, 200, 100, 0, 0)


def test_setporthhh():
    do = DobotEDU('yuyuyu', 'yuyu78YU')
    res = do.magician.search_dobot()
    print(res)
    port = "COM12"
    do.portname = port
    do.magician.connect_dobot()
    do.magician.set_homecmd()


def test_mbox():
    do = DobotEDU('yuyuyu', 'yuyu78YU')
    res = do.magicbox.search_dobot()
    print(res)
    port = res[0]["portName"]
    do.magicbox.connect_dobot(port)
    do.magicbox.set_ptpcmd(port, 0, 200, 100, 0, 0)


def test_portbox():
    do = DobotEDU('yuyuyu', 'yuyu78YU')
    res = do.magicbox.search_dobot()
    print(res)
    port = "COM12"
    do.portname = port
    do.magicbox.connect_dobot()
    do.magicbox.set_homecmd()


def test_setport():
    do = DobotEDU('yuyuyu', 'yuyu78YU')
    res = do.m_lite.search_dobot()
    print(res)
    port = "COM12"
    do.portname = port
    do.m_lite.connect_dobot()
    do.m_lite.set_homecmd()


def test_urlone():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    url = "https://dobotlab.dobot.cc"
    dobotEdu.url = url
    r = dobotEdu.speech.synthesis('你好', 1)
    print(r)


def test_urltwo():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    r = dobotEdu.speech.synthesis('你好', 1)
    print(r)


def test_urlthree():
    dobotEdu = DobotEDU("huang", "huangHUANG123")
    url = "https://dev.dobotlab.dobot.cc"
    dobotEdu.url = url
    r = dobotEdu.speech.synthesis('你好', 1)
    print(r)


# 测试重构后的wrapper函数get_portname
def test_getport():
    do = DobotEDU("yuyuyu", "yuyu78YU")
    res = do.m_lite.search_dobot()
    print(res)
    port = res[0]["portName"]
    do.m_lite.connect_dobot(port)
    do.m_lite.set_homecmd(port_name=port)
    do.m_lite.set_ptpcmd(port, ptp_mode=0, x=200, y=50, z=150, r=0)
    do.m_lite.set_ptpcmd(port, 0, 150, -20, 50, 0)
    do.m_lite.set_ptpcmd(port, 0, 200, 50, 150, r=0)
    do.m_lite.disconnect_dobot(port)
    print('another method')
    do.set_portname(port)  # 重新实例化，需要重连
    print(999)
    do.m_lite.connect_dobot()
    do.m_lite.set_ptpcmd(0, 149, -20, 50, 0)
    do.m_lite.set_ptpcmd(0, 200, 50, 150, r=0)


def test_boxm5():
    do = DobotEDU("yuyuyu", "yuyu78YU")
    res = do.magicbox.search_dobot()
    print(res)
    portname = res[0]["portName"]
    do.magicbox.connect_dobot(portname)
    # do.magicbox.set_led_rgb(portname, 1, 2, 1, 200, 200)
    # do.magicbox.set_led_color(portname, 1, 2, "white", 10)
    # do.magicbox.set_led_state(portname, 1, 1, False)
    # do.magicbox.set_tts_volume(portname, 2, 2)
    # do.magicbox.set_tts_play(portname, 2, "加油")

    # do.magicbox.set_tts_tone(portname, 2, 5)
    # time.sleep(5)
    # do.magicbox.set_tts_cmd(portname, 2, 0)

    # do.magicbox.set_oled_text(portname, 4, "hehehe")
    # do.magicbox.set_oled_clear(portname, 4)
    # do.magicbox.set_oled_pos_text(portname, 4, 2, 1, "ttt")
    value = do.magicbox.get_color_result(portname, 3)
    print(value)


def test_cccccc():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    res = dobotEdu.robot.conversation(query="你好", session_id="")
    print(res)


def test_go():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    dobotEdu.set_portname("com2")
    dobotEdu.magiciango.set_rgb_light("LED_1", 0, 23, 23, 23, 23, 9)

def test_betago():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    dobotEdu.set_portname("com2")
    dobotEdu.beta_go.is_nearby([1,2])