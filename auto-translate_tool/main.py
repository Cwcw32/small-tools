import subprocess
import time
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from m import Ui_MainWindow
import sys
# from setting import Ui_Dialog
import os
# 测试读取剪切板数据
import pyperclip
import time
import json
from huaweicloud_nlp.NlpfClient import NlpfClient
from huaweicloud_nlp.HWNlpClientAKSK import HWNlpClientAKSK
from huaweicloud_nlp.MtClient import MtClient
from PIL import Image
import sys
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtCore import Qt, pyqtSignal
import logging
import base64
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkocr.v1 import *
cliptext = ''
ak = '8M6K1TP0QZFUPKK591RU'
sk = 'CS7GTtMcTwQG7amGn3i3O7YFQQKwyJDOogD0w4hs'
region = 'cn-north-4'
pid = '0d98f3544580f2af2fadc0008ed248d3'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class ScreenShotsWin(QMainWindow):
    # 定义一个信号
    oksignal = pyqtSignal()
    cg_clip=pyqtSignal(int,str)

    def __init__(self):
        super(ScreenShotsWin, self).__init__()
        self.initUI()
        self.start = (0, 0)  # 开始坐标点
        self.end = (0, 0)  # 结束坐标点

    def initUI(self):
        # self.showFullScreen()
        self.setWindowOpacity(0.4)
        self.btn_ok = QPushButton('保存', self)

        self.oksignal.connect(lambda: self.screenshots(self.start, self.end))

    def screenshots(self, start, end):
        '''
        截图功能
        :param start:截图开始点
        :param end:截图结束点
        :return:
        '''
        logger.debug('开始截图,%s, %s', start, end)

        x = min(start[0], end[0])
        y = min(start[1], end[1])
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])

        des = QApplication.desktop()
        screen = QApplication.primaryScreen()
        if screen:
            self.setWindowOpacity(0.0)
            pix = screen.grabWindow(des.winId(), x, y, width, height)

      #  fileName = QFileDialog.getSaveFileName(self, '保存图片', '.', ".png;;.jpg")
       # if fileName[0]:
        pix.save('jietu.jpg')
        s=''
        global  ak,sk,pid,region
     #   img = Image.open("jietu.jpg")
        with open("jietu.jpg", 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            credentials = BasicCredentials(ak, sk, pid)
            client = OcrClient.new_builder() \
                        .with_credentials(credentials) \
                        .with_region(OcrRegion.value_of(region)) \
                        .build()
        try:
            request = RecognizeGeneralTextRequest()
            request.body = GeneralTextRequestBody(
                quick_mode=False,
                detect_direction=False,
                image=s)
            print(s)
            response = client.recognize_general_text(request)
            print(response)
            result = json.loads(str(response))
            print(result)
            # 本版本仅支持单词哦所以下面是[0]
            cl=result.get('result').get('words_block_list')[0].get('words')
            print(cl)
            self.cg_clip.emit(1,cl)
        except exceptions.ClientRequestException as e:
            print(e.status_code)
            print(e.request_id)
            print(e.error_code)
            print(e.error_msg)

        self.close()

    def paintEvent(self, event):
        '''
        给出截图的辅助线
        :param event:
        :return:
        '''
        logger.debug('开始画图')
        x = self.start[0]
        y = self.start[1]
        w = self.end[0] - x
        h = self.end[1] - y

        pp = QPainter(self)
        pp.drawRect(x, y, w, h)

    def mousePressEvent(self, event):

        # 点击左键开始选取截图区域
        if event.button() == Qt.LeftButton:
            self.start = (event.pos().x(), event.pos().y())
            logger.debug('开始坐标：%s', self.start)

    def mouseReleaseEvent(self, event):

        # 鼠标左键释放开始截图操作
        if event.button() == Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            logger.debug('结束坐标：%s', self.end)

            self.oksignal.emit()
            logger.debug('信号提交')
            # 进行重新绘制
            self.update()

    def mouseMoveEvent(self, event):

        # 鼠标左键按下的同时移动鼠标绘制截图辅助线
        if event.buttons() and Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            # 进行重新绘制
            self.update()

# 线程2用来对新数据进行翻译



# 采用线程2来进行翻译工作
class Thread2(QThread):
    changeTrans = pyqtSignal(str)

    def run(self):
        global cliptext, ak, sk, region, pid
        akskClient = HWNlpClientAKSK(ak,  # 用户的ak
                                     sk,  # 用户的sk
                                     region,  # region值
                                     pid)  # projectId
        mtClient = MtClient(akskClient)
        # 根据初始化Client章节选择认证方式构造完成mtClient后调用
        response = mtClient.translate_text(cliptext, "en", "zh", "common")
        # 结果为code和json结构体
        print(response.code)
        #  print(json.dumps(response.res, ensure_ascii=False))
        tr_t = response.res.get('translated_text')
        print(tr_t)
        self.changeTrans.emit(tr_t)
        print('finish')


# 线程1用来获取剪贴板数据
class Thread1(QThread):  # 采用线程来
    changeClip = pyqtSignal(int, str)

    def clipboard_get(self):
        """获取剪贴板数据"""
        data = pyperclip.paste()  # 主要这里差别
        return data

    def run(self):
        print(1)
        """后台脚本：每隔0.2秒，读取剪切板文本，检查有无指定字符或字符串，如果有则执行替换"""
        # recent_txt 存放最近一次剪切板文本，初始化值只多执行一次paste函数读取和替换
        recent_txt = self.clipboard_get()
        i = 1
        while True:
            # txt 存放当前剪切板文本
            print(i)
            txt = self.clipboard_get().replace('\n', '').replace('\r', '')
            print(txt)
            # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
            if txt != recent_txt:
                # print(f'txt:{txt}')
                recent_txt = txt  # 没查到要替换的子串，返回None
                # 发送新数据？
                i = i + 1
                self.changeClip.emit(i, recent_txt)
            # 检测间隔（延迟0.2秒）
            time.sleep(1)


from setting import Ui_Dialog

# 设置界面（账户信息）
class mysetting(Ui_Dialog, QDialog):
    s_signal = pyqtSignal(str, str, str, str)  # Processbar

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
        # self.ok.clicked.connect(self.ok)
        # self.cancel.clicked.connect(self.cancel)
        self.O.clicked.connect(self.ok)
        self.C.clicked.connect(self.cancel)

    def ok(self):
        print("确定保存！")
        ak = self.ak.text()
        sk = self.sk.text()
        region = self.region.text()
        pid = self.pid.text()
        self.s_signal.emit(ak, sk, region, pid)
        self.hide()

    def cancel(self):
        print("取消保存！")
        self.hide()


class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.Child1 = mysetting()
        self.Child1.s_signal.connect(self.change_zhanghu)

        self.addSystemTray()

        """
        bind functions
        """
        self.cold.clicked.connect(self.btn_zhiding)  # 置顶
        self.start.clicked.connect(self.btn_start)  # 开始
        self.retrans.clicked.connect(self.btn_retrans)  # 重新翻译
        self.zhanghu.clicked.connect(self.btn_zhanghu)  # 账户信息
        self.jietu.clicked.connect(self.btn_jietu)  # 截图识别
        self.history.clicked.connect(self.btn_history)  # 历史记录
        """
            状态参数
        """
        self.autotrans = True
        self.zhiding = False
        self.is_duqufuzhi = False
        """
            变量参数
        """
        self.cliptext = ''
        self.zhanghu_ak = ''
        self.zhanghu_sk = ''
        self.pid = ''

    # srf
    "历史记录"

    def btn_history(self):
        pass

    "重新翻译"

    def btn_retrans(self):
        pass

    "截图识别"

    def btn_jietu(self):
        self.showMinimized()
        self.screenshot = ScreenShotsWin()
        self.screenshot.cg_clip.connect(self.setClipboardContent)
        self.screenshot.showFullScreen()
        pass

    "账户信息"

    def btn_zhanghu(self):
        self.Child1.show()

    "置顶"

    def change_zhanghu(self, a, s, r, p):
        global ak, sk, region, pid
        ak = a
        sk = s
        region = r
        pid = p
        print("ak:%s",a)
        print("sk:%s",s)
        print("region:",r)
        print("pid:%s",p)

    def btn_zhiding(self):
        if self.zhiding:
            print('?')
            self.setWindowFlags(Qt.WindowStaysOnBottomHint)
            self.zhiding = False
        else:
            print("!")
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.zhiding = True
        self.show()
    "开始读取复制内容"
    def btn_start(self):
        if self.is_duqufuzhi:
            pass
        else:
            th = Thread1(self)
            print('复了搁制')
            th.changeClip.connect(self.setClipboardContent)
            th.start()

    "线程1剪切板内容改变的槽函数"
    "改变第一个板子的内容"
    def setClipboardContent(self, i, newtext):
        print(newtext)
        # self.clipboard.setText(newtext)
        print(i)
        print("剪切板已更新：%s", newtext)
        self.clipboard.setText(newtext)
        print("###")
        print(self.clipboard.toPlainText())
        print("###")
        self.cliptext = newtext
        if self.autotrans:
            global cliptext
            cliptext = newtext
            print("公共text文本:%s", cliptext)
            th2 = Thread2(self)
            print('Thread2准备启动！！！')
            th2.changeTrans.connect(self.setTransboardContent)
            th2.start()

    def setTransboardContent(self, newtext):
        print('正在进行翻译版更新')
        print(newtext)
        #  newtext=newtext.relpace("\n",'')
        print("翻译板已更新：%s", newtext)
        self.transboard.setText(newtext)


    def addSystemTray(self):
        minimizeAction = QAction("Mi&nimize", self, triggered=self.hide)
        maximizeAction = QAction("Ma&ximize", self, triggered=self.showMaximized)
        restoreAction = QAction("&Restore", self, triggered=self.showNormal)
        quitAction = QAction("&Quit", self,
                             triggered=self.close)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(minimizeAction)
        self.trayIconMenu.addAction(maximizeAction)
        self.trayIconMenu.addAction(restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(quitAction)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("icon.png"))
        self.setWindowIcon(QIcon("icon.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())
