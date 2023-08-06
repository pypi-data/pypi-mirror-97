import os
import pathlib
import pickle
import pprint
import shutil
import sys
import threading
import time
from typing import Optional, List

import PySide2
import lz4
import scipy
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWinExtras import *
from lz4.frame import compress, decompress, COMPRESSIONLEVEL_MINHC

import vmi

app = QApplication()
app.setOrganizationName('vmi')
app.setApplicationName('vmi')
app.setStyle(QStyleFactory.create('Fusion'))

desktopPath: str = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
appDataPath: str = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
os.makedirs(appDataPath, exist_ok=True)

appViews = []

_AppWindow = None
_TaskbarButton = QWinTaskbarButton()
_Progress = _TaskbarButton.progress()


def appexit() -> None:
    """退出主程序"""
    shutil.rmtree(appDataPath, ignore_errors=True)
    sys.exit()


def appwindow(w: QWidget) -> None:
    """设置主程序窗口"""
    global _AppWindow
    _AppWindow = w
    _TaskbarButton.setParent(w)
    _TaskbarButton.setWindow(w.windowHandle())
    _Progress.setVisible(True)
    _Progress.setRange(0, 100)
    _Progress.setValue(0)


def appupdate():
    app.processEvents(QEventLoop.ExcludeUserInputEvents)


def appexec(w: QWidget, width: int = 1600, height: int = 900) -> int:
    """
    设置主程序窗口，居中显示，启动主程序

    :param w: 主程序窗口
    :param width: 窗口宽度
    :param height: 窗口高度
    :return: int - 主程序结束状态
    """
    appwindow(w)
    rect = QGuiApplication.screens()[0].geometry()
    rect = QRect(rect.center() - QPoint(int(width / 2), int(height / 2)), QSize(width, height))
    w.setGeometry(rect)
    w.showMaximized()
    return app.exec_()


def appwait(thread: threading.Thread, progress: Optional[List[int]] = None) -> None:
    """
    执行后台线程并等待，默认在windows系统任务栏循环更新进度，设置progress=[value]可以显示真实进度

    :param thread: 后台线程
    :param progress: 进度
    :return: None
    """
    while thread.is_alive():
        if progress is None:
            value = (_Progress.value() + 5) % 100
        else:
            value = progress[0]
        _Progress.setValue(value)
        time.sleep(0.1)
    _Progress.setValue(0)


def app_about(self):
    text = ''
    text += '软件名称：{}'.format(app.applicationName())
    text += '\n软件版本：{}'.format(app.applicationVersion())
    text += '\n软件环境：'
    text += '\nPython\t{}.{}.{} {} {}'.format(
        sys.version_info.major, sys.version_info.minor, sys.version_info.micro,
        sys.version_info.releaselevel, sys.version_info.serial)
    text += '\nvmi\t{}'.format(vmi.__version__)
    text += '\nPySide2\t{}'.format(PySide2.__version__)
    text += '\nSimpleITK\t{}'.format(vmi.sitk.Version.VersionString())
    text += '\npydicom\t{}'.format(vmi.pydicom.__version__)
    text += '\nvtk\t{}'.format(vmi.vtk.VTK_VERSION)
    text += '\nnumba\t{}'.format(vmi.numba.__version__)
    text += '\nnumpy\t{}'.format(vmi.np.__version__)
    text += '\nscipy\t{}'.format(scipy.__version__)
    text += '\nlz4\t{}'.format(lz4.__version__)
    vmi.askInfo(text, '关于')


class Main(QMainWindow):
    """通用应用程序外壳"""

    def __init__(self, return_globals):
        QMainWindow.__init__(self)
        brush = QBrush(QColor(255, 255, 255, 255))
        palette = QPalette()
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.setPalette(palette)

        self._ScrollArea = QScrollArea()
        self._ScrollArea.setWidgetResizable(True)
        self.setCentralWidget(self._ScrollArea)

        self._ScrollAreaWidget = QWidget()
        self._Layout = QGridLayout(self._ScrollAreaWidget)
        self._ScrollArea.setWidget(self._ScrollAreaWidget)

        self._AppName = str()
        self._AppVersion = str()
        self._SaveFile = str()
        self._SaveDateTime = str()
        self.updateWindowTitle()

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        menuFile = QMenu('文件', menubar)
        menubar.addAction(menuFile.menuAction())

        actionDataSheet = QAction('数据表', self)
        actionDataSheet.setShortcut(QKeySequence('Ctrl+D'))
        actionDataSheet.triggered.connect(self.actionDataSheet)
        menuFile.addAction(actionDataSheet)

        actionSave = QAction('保存', self)
        actionSave.setShortcut(QKeySequence('Ctrl+S'))
        actionSave.triggered.connect(self.actionSave)
        menuFile.addAction(actionSave)

        menuHelp = QMenu('帮助', menubar)
        menubar.addAction(menuHelp.menuAction())

        actionAbout = QAction('关于', self)
        actionAbout.triggered.connect(app_about)
        menuHelp.addAction(actionAbout)

        self.dataTree = QTreeWidget()
        self.dataTree.setWindowTitle('数据表')
        self.dataTree.setColumnCount(3)
        self.dataTree.setHeaderLabels(['名称', '类型', '内容'])
        self.dataTree.setAlternatingRowColors(True)
        self.dataTree.setSortingEnabled(True)
        self.dataTree.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.dataTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        self.globals = return_globals
        self.excludeKeys = list(self.globals().keys())

    def appName(self):
        return self._AppName

    def appVersion(self):
        return self._AppVersion

    def setAppName(self, name) -> None:
        """设置程序名称"""
        self._AppName = name
        app.setApplicationName(self._AppName)
        self.updateWindowTitle()

    def setAppVersion(self, version) -> None:
        """设置程序版本"""
        self._AppVersion = version
        app.setApplicationVersion(self._AppVersion)
        self.updateWindowTitle()

    def setSaveFile(self, save_file) -> None:
        """设置程序存档文件"""
        self._SaveFile = str(save_file)
        self.updateWindowTitle()

    def setSaveDateTime(self, save_date_time) -> None:
        """设置程序存档文件时间"""
        self._SaveDateTime = str(save_date_time)
        self.updateWindowTitle()

    def layout(self) -> QGridLayout:
        """返回布局器"""
        return self._Layout

    def scrollArea(self) -> QScrollArea:
        return self._ScrollArea

    def closeEvent(self, ev: QCloseEvent):
        if vmi.askYesNo('退出？'):
            ev.accept()
            appexit()
        else:
            ev.ignore()

    def actionDataSheet(self):
        self.dataTree.clear()
        objs = self.globals()
        objs = {kw: objs[kw] for kw in objs if kw not in self.excludeKeys}
        for kw in objs:
            content = pprint.pformat(objs[kw], width=500, compact=True)
            item = QTreeWidgetItem([kw, repr(type(objs[kw])), content])
            self.dataTree.addTopLevelItem(item)
        for i in range(self.dataTree.columnCount()):
            self.dataTree.resizeColumnToContents(i)
        self.dataTree.showMaximized()

    def actionSave(self):
        f = vmi.askSaveFile(nameFilter='*.vmi', title='存档')
        if f is not None:
            self._SaveFile = f
            self._SaveDateTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

            ba = self.dumps()
            pathlib.Path(f).write_bytes(ba)
            vmi.askInfo('保存完成 {:.2f} MB'.format(len(ba) / (2 ** 20)))
            self.updateWindowTitle()

    def dumps(self) -> bytes:
        """存档当前程序状态为字节码"""
        objs = self.globals()
        objs = {kw: objs[kw] for kw in objs if kw not in self.excludeKeys}
        for kw in ['_AppName', '_AppVersion', '_SaveFile', '_SaveDateTime']:
            if hasattr(self, kw):
                objs[kw] = getattr(self, kw)
        ba = pickle.dumps(objs)
        ba = compress(ba, compression_level=COMPRESSIONLEVEL_MINHC)
        return ba

    def loads(self, ba: bytes):
        """读取存档字节码，更新主文件全局变量"""
        ba = decompress(ba)
        objs = pickle.loads(ba)
        for kw in ['_AppName', '_AppVersion', '_SaveFile', '_SaveDateTime']:
            if hasattr(self, kw):
                getattr(self, kw.replace('_', 'set', 1))(objs[kw])
                del objs[kw]
        self.updateWindowTitle()
        self.globals().update(objs)

    def screenWidth(self) -> int:
        """返回屏幕宽度，单位是像素"""
        return QGuiApplication.screens()[0].geometry().width()

    def updateWindowTitle(self):
        """更新窗体标题文字"""
        self.setWindowTitle('{} {} {} {}'.format(self._AppName, self._AppVersion, self._SaveFile, self._SaveDateTime))


_scripts = pathlib.Path(sys.executable).parent / 'Scripts'
_lupdate = str(_scripts / 'pyside2-lupdate')
_uic = str(_scripts / 'pyside2-uic')
_rcc = str(_scripts / 'pyside2-rcc')

_pyside2 = pathlib.Path(sys.executable).parent / 'Lib/site-packages/PySide2'
_designer = str(_pyside2 / 'designer')
_linguist = str(_pyside2 / 'linguist')
_lrelease = str(_pyside2 / 'lrelease')


def app_uic(ui_dir: str = 'ui', py_dir: str = '.', prefix: str = 'Ui_') -> None:
    """
    将ui_dir目录下的所有.ui文件转换到py_dir目录下.py文件并附加前缀ui_

    :param ui_dir: 界面文件（.ui）目录
    :param py_dir: 转换后的源代码文件（.py）目录
    :param prefix: 转换后的文件名前缀
    :return: None
    """
    py_dir = pathlib.Path(py_dir)

    for ui in pathlib.Path(ui_dir).rglob('*.ui'):
        if ui.is_file():
            py = py_dir / (prefix + ui.with_suffix('.py').name)
            os.system(_uic + ' ' + str(ui) + ' -o ' + str(py) + ' -x')
            print('[uic.exe]', _uic, ui, '-o', py, '-x')


def app_lupdate(py_dir: str = '.', ts_file: str = 'zh_CN.ts') -> None:
    """
    将py_dir目录下的所有.py文件更新翻译到同目录下的.ts文件ts_file

    :param py_dir: 源代码文件（.py)目录
    :param ts_file: 转换后的翻译文件（.ts）路径
    :return: None
    """
    py_dir = pathlib.Path(py_dir)
    pys = str()

    for py in pathlib.Path(py_dir).rglob('*.py'):
        if py.is_file():
            pys += str(py) + ' '

    if len(pys) > 0:
        ts_file = py_dir / ts_file
        os.system(_lupdate + ' ' + str(pys) + ' -ts ' + str(ts_file))
        print('[lupdate.exe]', _lupdate, pys, '-ts', ts_file)


def app_lrelease(ts_file: str = './zh_CN.ts',
                 qm_file: str = 'qrc/tr/zh_CN.qm') -> None:
    """
    将可读翻译文件ts_file转换为二进制翻译文件qm_file

    :param ts_file: 可读翻译文件（.ts）
    :param qm_file: 转换后的二进制翻译文件（.qm）
    :return: None
    """
    os.system(_lrelease + ' ' + ts_file + ' -qm ' + qm_file)
    print('[lrelease.exe]', _lrelease, ts_file, '-qm', qm_file)
    os.system(_linguist + ' ' + './zh_CN.ts')


def app_rcc(rc_dir: str = 'qrc', qrc_file: str = 'vmi.qrc', py_file: str = 'vrc.py') -> None:
    """
    将rc_dir目录下的所有文件转换为.qrc资源文件qrc_file，再转换为.py文件py_file

    :param rc_dir: 资源文件目录
    :param qrc_file: 资源文件（.qrc）
    :param py_file: 转换后的源代码文件（.py）
    :return: None
    """
    rc_dir = pathlib.Path(rc_dir)
    indent = ' ' * 4
    rcs = str()

    for rc in pathlib.Path(rc_dir).rglob('*'):
        if rc.is_file():
            rc = str(rc).replace('\\', '/')
            rcs += indent * 2 + '<file>' + rc + '</file>' + '\n'

    if len(rcs) > 0:
        t = '<!DOCTYPE RCC>'
        t += '<RCC version="1.0">' + '\n'
        t += indent + '<qresource prefix="/">' + '\n'
        t += rcs
        t += indent + '</qresource>' + '\n'
        t += '</RCC>'

        with open(qrc_file, 'w') as f:
            f.write(t)

        os.system(_rcc + ' ' + qrc_file + ' -o ' + py_file)
        print('[rcc.exe]', _rcc, qrc_file, '-o', py_file)


if __name__ == '__main__':
    # app_uic()  # 更新界面.ui文件
    # app_lupdate()  # 更新翻译.ts文件
    # app_lrelease()  # 更新翻译.qm文件
    app_rcc()  # 更新.qrc文件

    # os.startfile(_designer)  # 打开界面.ui文件
