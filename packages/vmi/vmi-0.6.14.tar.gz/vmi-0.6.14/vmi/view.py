from typing import List, Optional, Union

import numpy as np
import vtk
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtWidgets import *

import vmi

vtk.vtkObject().SetGlobalWarningDisplay(0)


class Mouse:
    """响应鼠标事件的对象"""

    def __init__(self, menu=None):
        i = 0

        def e():
            nonlocal i
            name = '_MouseEvent{}'.format(i)
            if not hasattr(self, name):
                setattr(self, '_MouseEvent{}'.format(i), self.mousePass)
                i += 1
            return getattr(self, name)

        self.mouse = {
            'NoButton': {'Enter': e(), 'Leave': e(), 'Wheel': e(), 'Move': e()},
            'LeftButton': {'Press': e(), 'PressMove': e(), 'PressMoveRelease': e(), 'PressRelease': e()},
            'MidButton': {'Press': e(), 'PressMove': e(), 'PressMoveRelease': e(), 'PressRelease': e()},
            'RightButton': {'Press': e(), 'PressMove': e(), 'PressMoveRelease': e(), 'PressRelease': e()}}

        for b in self.mouse:
            for e in self.mouse[b]:
                self.mouse[b][e] = []

        if menu is not None:
            self.mouse['RightButton']['PressRelease'] = [menu.menuexec]

    @staticmethod
    def mousePass(**kwargs):
        pass

    @staticmethod
    def mouseBlock(**kwargs):
        return True


class Menu:
    """响应菜单事件的对象"""

    def __init__(self):
        self.menu = QMenu()
        self.menu.setTitle('选项')

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu']}
        return state

    def menuexec(self, **kwargs):
        """在当前鼠标位置弹出菜单"""
        self.menu.exec_(QCursor.pos())
        return True


class View(QGLWidget, Menu, Mouse):
    """场景视图，在QWidget内显示vtkRenderWindow内容"""

    def __init__(self, parent=None):
        vmi.appViews.append(self)
        QGLWidget.__init__(self, parent)
        Menu.__init__(self)

        self.actions = {'CameraFit': QAction(self.tr('最适 (Fit)')),
                        'CameraReverse': QAction(self.tr('反向 (Reverse)')),
                        'CameraAxial': QAction(self.tr('横断位 (Axial)')),
                        'CameraSagittal': QAction(self.tr('矢状位 (Sagittal)')),
                        'CameraCoronal': QAction(self.tr('冠状位 (Coronal)')),
                        'Snapshot': QAction(self.tr('快照 (Snapshot)')), }

        self.actions['CameraFit'].triggered.connect(self.setCamera_FitAll)
        self.actions['CameraReverse'].triggered.connect(self.setCamera_Reverse)
        self.actions['CameraAxial'].triggered.connect(self.setCamera_Axial)
        self.actions['CameraSagittal'].triggered.connect(self.setCamera_Sagittal)
        self.actions['CameraCoronal'].triggered.connect(self.setCamera_Coronal)
        self.actions['Snapshot'].triggered.connect(self.actionSnapshot)

        self.menu.addAction(self.actions['CameraFit'])
        self.menu.addAction(self.actions['CameraReverse'])
        self.menu.addAction(self.actions['CameraAxial'])
        self.menu.addAction(self.actions['CameraSagittal'])
        self.menu.addAction(self.actions['CameraCoronal'])
        self.menu.addAction(self.actions['Snapshot'])

        Mouse.__init__(self, menu=self)
        self.mouse['LeftButton']['PressMove'] = [self.mouseRotateFocal]
        self.mouse['MidButton']['PressMove'] = [self.mousePan]
        self.mouse['RightButton']['PressMove'] = [self.mouseZoom]
        self.mouse['NoButton']['Wheel'] = [self.mouseRotateLook]

        rect = QGuiApplication.screens()[0].geometry()
        rect = QRect(rect.center() - QPoint(800, 450), QSize(1600, 900))
        self.setGeometry(rect)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setMouseTracking(True)

        # 渲染器
        self._Renderer = vtk.vtkRenderer()
        self._Renderer.SetUseHiddenLineRemoval(1)  # 隐线消除
        self._Renderer.SetUseFXAA(False)  # 快速近似抗锯齿
        self._Renderer.SetBackground(1, 1, 1)

        # 渲染窗口
        self._RenderWindow = vtk.vtkRenderWindow()
        self._RenderWindow.SetWindowInfo(str(int(self.winId())))
        self._RenderWindow.AddRenderer(self._Renderer)

        # 交互器
        self._Interactor = vtk.vtkGenericRenderWindowInteractor()
        self._Interactor.SetRenderWindow(self._RenderWindow)
        self._Interactor.Initialize()

        # 方位标
        self._OrientationMarker = _init_orientation_marker(self._Interactor)

        # 照相机
        self._Camera = self.renderer().GetActiveCamera()
        self._BindCamera = [self]
        self.camera().SetParallelProjection(True)  # 平行投影

        # 拾取器
        self._Picker = vtk.vtkPicker()
        self._PickerProp = vtk.vtkPropPicker()
        self._PickerPoint = vtk.vtkPointPicker()
        self._PickerCell = vtk.vtkCellPicker()
        self._Picker.SetTolerance(0.005)
        self._PickerPoint.SetTolerance(0.005)
        self._PickerCell.SetTolerance(0.005)

        # 刷新计时器
        self._Timer = QTimer(self)
        self._Timer.timeout.connect(self._timeout)
        self._Timer.start(10)

        self._Time = QTime()
        self._Time.start()
        self._FPS = self._UpdateSum = 0

        # 创建一个隐藏控件，当销毁时调用清理vtk元素
        self._Hidden = QWidget(self)
        self._Hidden.hide()
        self._Hidden.destroyed.connect(self.delete)

        # 更新请求
        self._UpdateAtOnce: bool = False

        # 鼠标位置
        self._DblClick = False
        self._MousePosLast: QPoint = QPoint(0, 0)
        self._MousePos: QPoint = QPoint(0, 0)

        # 鼠标正在交互的对象
        self._PProp: Optional[vtk.vtkProp] = None
        self._PView: Optional[View] = None

        # 鼠标按键状态
        self._ButtonPress = self._ButtonPressMove = 'NoButton'

        self.setCamera_Axial()

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            if kw not in ['_Visible']:
                getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        QTimer.singleShot(10, self.show if state['set']['_Visible'] else self.hide)

        del state['vtk']
        del state['set']
        self.__dict__.update(state)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in
                 ['menu', 'menuCamera', 'actions', '_OrientationMarker', '_Timer', '_Hidden', 'aboutToClose',
                  '__METAOBJECT__']}

        state_set = {'_Enabled': self.isEnabled(), '_Visible': self.isVisible(), '_WindowTitle': self.windowTitle()}
        state = {kw: state[kw] for kw in state if kw not in state_set}

        state_vtk = {}
        for kw in state:
            if isinstance(state[kw], vtk.vtkObject):
                if not hasattr(vmi, 'pickle_' + state[kw].__class__.__name__):
                    state_vtk[kw] = vmi.vtkInstance_gets(state[kw])
        state = {kw: state[kw] for kw in state if kw not in state_vtk}

        state['set'] = state_set
        state['vtk'] = state_vtk
        return state

    def closeEvent(self, ev):
        self.delete()

    def delete(self):
        """停止场景刷新"""
        self._Timer.stop()
        self._RenderWindow.Finalize()

    def mouseExec(self, cats, button, event, picked=None, **kwargs) -> None:
        """
        顺序响应鼠标事件

        :param cats: 响应者列表
        :param button: 鼠标按键
        :param event: 事件内容
        :param picked: 鼠标正在交互的对象
        :param kwargs: 其它参数
        :return: None
        """
        if picked is None:
            if self._PView:
                picked = self._PView
            if self._PProp:
                picked = self._PProp

        for cat in [cat for cat in cats if isinstance(cat, Mouse)]:
            for mbe in cat.mouse[button][event]:
                if mbe(picked=picked, **kwargs):
                    return

    def entered(self):
        """返回鼠标正在交互的对象"""
        return self._PProp if self._PProp else (self._PView if self._PView else self)

    def enterEvent(self, ev):
        self._PView = self
        self._PProp = self.pickerExec(pos=ev.pos(), picker=self._PickerProp)[0]
        self.mouseExec([self._PView, self._PProp], 'NoButton', 'Enter')

    def leaveEvent(self, ev):
        self.mouseExec([self._PProp, self._PView], 'NoButton', 'Leave')
        self._PView = self._PProp = None
        self._ButtonPress = self._ButtonPressMove = 'NoButton'

    def mouseMoveEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == 'NoButton':
            prop = self.pickerExec(pos=ev.pos(), picker=self._PickerProp)[0]
            last_prop, self._PProp = self._PProp, prop

            if not last_prop and not prop:
                self.mouseExec([self._PView], 'NoButton', 'Move')
            elif not last_prop and prop:
                self.mouseExec([prop], 'NoButton', 'Enter', prop)
            elif last_prop and not prop:
                self.mouseExec([last_prop], 'NoButton', 'Leave', last_prop)
            elif last_prop and prop and last_prop is prop:
                self.mouseExec([self._PProp, self._PView], 'NoButton', 'Move')
            elif last_prop and prop and last_prop is not prop:
                self.mouseExec([last_prop], 'NoButton', 'Leave', last_prop)
                self.mouseExec([prop], 'NoButton', 'Enter', prop)
        elif self._MousePosLast != self._MousePos:
            self._ButtonPressMove = self._ButtonPress
            self.mouseExec([self._PProp, self._PView], self._ButtonPressMove, 'PressMove')
        ev.accept()

    def mousePressEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == 'NoButton':
            b = ev.button().name.decode()
            if b in ['LeftButton', 'MidButton', 'RightButton']:
                self._ButtonPress = b
                self._DblClick = ev.type() == QEvent.Type.MouseButtonDblClick
                self.mouseExec([self._PProp, self._PView], self._ButtonPress, 'Press', double=self._DblClick)
        ev.accept()

    def mouseReleaseEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPressMove == ev.button().name.decode():
            last_button = self._ButtonPress
            self._ButtonPress = self._ButtonPressMove = 'NoButton'
            self.mouseExec([self._PProp, self._PView], last_button, 'PressMoveRelease')
        elif self._ButtonPress == ev.button().name.decode():
            last_button, last_double = self._ButtonPress, self._DblClick
            self._ButtonPress = self._ButtonPressMove = 'NoButton'
            self._DblClick = False
            self.mouseExec([self._PProp, self._PView], last_button, 'PressRelease', double=last_double)

    def mouseRotateFocal(self, **kwargs):
        """响应鼠标移动，观察者绕焦点旋转"""
        dx, dy = self.pickVt_Display()
        rx, ry = -200 * dx / self.height(), 200 * dy / self.width()
        self.camera().Azimuth(rx)
        self.camera().Elevation(ry)
        self.camera().OrthogonalizeViewUp()
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()
        return True

    def mouseRotateLook(self, **kwargs):
        """响应鼠标移动，观察者绕视线旋转"""
        self.camera().Roll(0.5 if kwargs['delta'] > 0 else -0.5)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()
            if i._Interactor.GetLightFollowCamera():
                i._Renderer.UpdateLightsGeometryToFollowCamera()
        return True

    def mousePan(self, **kwargs):
        """响应鼠标移动，观察者平移"""
        self.updateInTime()
        over = self.pickVt_FocalPlane()
        fp, cp = self.cameraPt_Focal(), self.cameraPt_Lens()
        fp -= over
        cp -= over
        self.camera().SetFocalPoint(fp)
        self.camera().SetPosition(cp)

        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()
            if i._Interactor.GetLightFollowCamera():
                i._Renderer.UpdateLightsGeometryToFollowCamera()
        return True

    def mouseZoom(self, **kwargs):
        """响应鼠标移动，观察者放缩"""
        self.updateInTime()
        c = self._Renderer.GetCenter()
        _, dy = self.pickVt_Display()
        factor = 1.1 ** (10 * -dy / c[1])

        if self.camera().GetParallelProjection():
            self.camera().SetParallelScale(self.camera().GetParallelScale() / factor)
        else:
            self.camera().Dolly(factor)

        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()
            if self._Interactor.GetLightFollowCamera():
                self._Renderer.UpdateLightsGeometryToFollowCamera()
        return True

    def pickPt_Display(self) -> np.ndarray:
        """
        拾取鼠标指针所在的屏幕坐标

        :return: [x, y]
        """
        return np.array([self._MousePos.x(), self._MousePos.y()])

    def pickPt_FocalPlane(self, pos: Union[QPoint, List[float]] = None) -> np.ndarray:
        """
        拾取鼠标指针在焦平面上的点

        :param pos: 指针位置，默认事件发生位置
        :return: [x, y, z]
        """
        if pos is None:
            pos = self._MousePos
        if not isinstance(pos, QPoint):
            pos = QPoint(pos[0], pos[1])

        t = [0, 0, 0, 0]
        vtk.vtkInteractorObserver.ComputeDisplayToWorld(self._Renderer, pos.x(), self.height() - pos.y(), 0, t)
        pt = np.array([_ / t[3] for _ in t[:3]])

        fp, look = self.cameraPt_Focal(), self.cameraVt_Look()
        pt = vmi.ptOnPlane(pt, fp, look)
        return pt

    def pickPt_Prop(self, pos: Optional[QPoint] = None) -> vtk.vtkProp:
        """
        拾取鼠标指针所在的物体

        :param pos: 指针位置，默认事件发生位置
        :return: prop
        """
        if pos is None:
            pos = self._MousePos
        return self.pickerExec(pos=pos, picker=self._PickerProp)[0]

    def pickPt_Cell(self, pos: Optional[QPoint] = None) -> np.ndarray:
        if pos is None:
            pos = self._MousePos
        return self.pickerExec(pos=pos, picker=self._PickerCell)[1]

    def pickVt_Display(self) -> np.ndarray:
        """
        拾取鼠标指针最近一次移动的屏幕位移

        :return: [dx, dy]
        """
        return np.array([self._MousePos.x() - self._MousePosLast.x(), self._MousePos.y() - self._MousePosLast.y()])

    def pickVt_FocalPlane(self) -> np.ndarray:
        """
        拾取鼠标指针最近一次移动的焦平面位移

        :return: [dx, dy, dz]
        """
        pt = np.array(self.pickPt_FocalPlane(self._MousePos))
        ptLast = np.array(self.pickPt_FocalPlane(self._MousePosLast))
        vt = pt - ptLast
        return vt

    def pickPt_DisplayInv(self, pt):
        """
        拾取世界坐标点pt对应的屏幕坐标

        :param pt: 世界坐标点
        :return: [x, y]
        """
        t = [0, 0, 0]
        vtk.vtkInteractorObserver.ComputeWorldToDisplay(self._Renderer, pt[0], pt[1], pt[2], t)
        return np.array([t[0], self.height() - t[1]])

    def paintEngine(self):
        return None

    def paintEvent(self, ev):
        self._Interactor.Render()

    # 可能会导致app.processEvents崩溃

    def pickerExec(self, picker: vtk.vtkPicker, pos: Optional[QPoint] = None) -> [vtk.vtkProp, np.ndarray,
                                                                                  vtk.vtkPicker]:
        pos = self._MousePos if pos is None else pos

        picker.Pick(pos.x(), self.height() - pos.y(), 0, self._Renderer)
        prop = picker.GetViewProp()
        prop = prop._Prop if prop else None
        return prop, np.array(picker.GetPickPosition()), picker

    def resizeEvent(self, ev):
        w = self.width()
        h = self.height()
        vtk.vtkRenderWindow.SetSize(self._RenderWindow, w, h)
        self._Interactor.SetSize(w, h)
        self._Interactor.ConfigureEvent()
        self.update()

        props: vtk.vtkPropCollection = self._Renderer.GetViewProps()
        props.InitTraversal()
        prop = props.GetNextProp()

        while prop:
            if hasattr(prop, '_Prop') and hasattr(prop._Prop, 'resize'):
                prop._Prop.resize()
            prop = props.GetNextProp()

        self.updateInTime()

    def renderer(self) -> vtk.vtkRenderer:
        """返回渲染器vtkRenderer"""
        return self._Renderer

    def camera(self) -> vtk.vtkCamera:
        """返回观察者vtkCamera"""
        return self._Camera

    def bindCamera(self, others):
        """关联相机，使视图采用other视图的视角，other = self 关联自身，other = None 重新关联当前对象"""
        binds = others.copy()
        if self not in binds:
            binds.append(self)
        for i in binds:
            i._BindCamera = binds.copy()
        for i in self._BindCamera:
            i.camera().DeepCopy(self._BindCamera[0].camera())
            i.updateInTime()

    def cameraPt_Focal(self) -> np.ndarray:
        """返回观察焦点坐标"""
        return np.array(self.camera().GetFocalPoint())

    def cameraPt_Lens(self) -> np.ndarray:
        """返回观察者位置坐标"""
        return np.array(self.camera().GetPosition())

    def cameraVt_Up(self) -> np.ndarray:
        """返回观察者上向向量"""
        up = np.array(self.camera().GetViewUp())
        up /= np.linalg.norm(up)
        return up

    def cameraVt_Look(self) -> np.ndarray:
        """返回观察者视向向量"""
        look = self.cameraPt_Focal() - self.cameraPt_Lens()
        look /= np.linalg.norm(look)
        return look

    def cameraVt_Right(self) -> np.ndarray:
        """返回观察者右向向量"""
        right = np.cross(self.cameraVt_Look(), self.cameraVt_Up())
        right /= np.linalg.norm(right)
        return right

    def cameraCS_FPlane(self) -> vmi.CS4x4:
        """返回观察坐标系

        原点是视图左上角[0, 0]在焦平面上的拾取点

        坐标轴分别是[right, -up, look]向量"""
        cs = vmi.CS4x4()
        cs.setOrigin(self.pickPt_FocalPlane(QPoint(0, 0)))
        cs.setAxis(0, self.cameraVt_Right())
        cs.setAxis(1, -self.cameraVt_Up())
        cs.setAxis(2, self.cameraVt_Look())
        return cs

    def cameraCS_Height(self) -> float:
        return 2 * self.camera().GetParallelScale()

    def setCamera_FPlane(self, cs: vmi.CS4x4, height: float) -> None:
        """
        设置视图的观察坐标系

        :param cs: 观察坐标系
        :param height: 视图高度对应场景中的世界尺寸
        :return: None
        """
        width = height * self.width() / self.height()
        fp = cs.mpt([0.5 * width, 0.5 * height, 0])
        b6 = self._Renderer.ComputeVisiblePropBounds()
        d = ((b6[1] - b6[0]) ** 2 + (b6[3] - b6[2]) ** 2 + (b6[5] - b6[4]) ** 2) ** 0.5
        cp = cs.mpt([0.5 * width, 0.5 * height, -d])

        self.camera().SetPosition(cp)
        self.camera().SetFocalPoint(fp)
        self.camera().SetViewUp(list(-cs.axis(1)))
        self.camera().SetParallelScale(0.5 * height)

        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCamera_Focal(self, focal=Union[np.ndarray, List[float]]) -> None:
        """设置观察焦点，镜头位置随之平移"""
        vl = self.cameraVt_Look()
        b = np.array(self._Renderer.ComputeVisiblePropBounds())
        dxyz = np.array([b[1] - b[0], b[3] - b[2], b[5] - b[4]])
        diagonal = np.linalg.norm(dxyz)
        cp = focal - diagonal * vl

        self.camera().SetPosition(cp)
        self.camera().SetFocalPoint(focal)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCamera_FitAll(self) -> None:
        """设置观察范围适应全部场景可见物体"""
        b = np.array(self._Renderer.ComputeVisiblePropBounds())
        dxyz = np.array([b[1] - b[0], b[3] - b[2], b[5] - b[4]])
        self._Renderer.ResetCamera(b)

        vr, vu, vl = self.cameraVt_Right(), self.cameraVt_Up(), self.cameraVt_Look()
        dr = np.abs(vr / np.linalg.norm(vr))
        dr = np.dot(dr, dxyz)
        dr = dr if dr != 0 else 1
        du = np.abs(vu / np.linalg.norm(vu))
        du = np.dot(du, dxyz)
        du = du if du != 0 else 1
        scale = 0.5 * du
        if du / dr < self.height() / self.width():
            scale = 0.5 * dr * self.height() / self.width()

        focal = b[::2] + 0.5 * dxyz
        diagonal = np.linalg.norm(dxyz)
        cp = focal - diagonal * vl
        self.camera().SetPosition(cp)
        self.camera().SetFocalPoint(focal)
        self.camera().SetParallelScale(scale)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCamera_Reverse(self) -> None:
        """设置观察者反向，镜头位置切换到焦点的对侧"""
        fp, cp = self.cameraPt_Focal(), self.cameraPt_Lens()
        for i in range(3):
            cp[i] = 2 * fp[i] - cp[i]
        self.camera().SetPosition(cp)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCamera_Axial(self) -> None:
        """设置观察者正视横断面"""
        vu = [np.array([0, 0, 1]), np.array([0, 0, 1]), np.array([0, -1, 0])][2]
        vr = [np.array([0, -1, 0]), np.array([1, 0, 0]), np.array([1, 0, 0])][2]
        vl = np.cross(vu, vr)

        fp = self.cameraPt_Focal()
        d = self.camera().GetDistance()
        cp = fp - d * vl

        self.camera().SetPosition(cp)
        self.camera().SetFocalPoint(fp)
        self.camera().SetViewUp(vu)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCamera_Sagittal(self) -> None:
        """设置观察者正视矢状面"""
        vu = [np.array([0, 0, 1]), np.array([0, 0, 1]), np.array([0, -1, 0])][0]
        vr = [np.array([0, -1, 0]), np.array([1, 0, 0]), np.array([1, 0, 0])][0]
        vl = np.cross(vu, vr)

        fp = self.cameraPt_Focal()
        d = self.camera().GetDistance()
        cp = fp - d * vl

        self.camera().SetPosition(cp)
        self.camera().SetFocalPoint(fp)
        self.camera().SetViewUp(vu)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCamera_Coronal(self) -> None:
        """设置观察者正视冠状面"""
        vu = [np.array([0, 0, 1]), np.array([0, 0, 1]), np.array([0, -1, 0])][1]
        vr = [np.array([0, -1, 0]), np.array([1, 0, 0]), np.array([1, 0, 0])][1]
        vl = np.cross(vu, vr)

        fp = self.cameraPt_Focal()
        d = self.camera().GetDistance()
        cp = fp - d * vl

        self.camera().SetPosition(cp)
        self.camera().SetFocalPoint(fp)
        self.camera().SetViewUp(vu)
        for i in self._BindCamera:
            i.camera().DeepCopy(self.camera())
            i.updateInTime()

    def setCornerVisible_LeftBottom(self, visible: bool):
        """显示或隐藏左下角方位标"""
        self._OrientationMarker.GetOrientationMarker().SetVisibility(visible)
        self.updateInTime()

    def sizeHint(self):
        return QSize(1600, 900)

    def snapshot(self) -> QImage:
        """快照，保存视图画面为QImage"""
        self.updateAtOnce()
        vmi.appupdate()
        return self.windowHandle().screen().grabWindow(self.winId()).toImage()

    def actionSnapshot(self):
        self.snapshot_PNG()

    def snapshot_PNG(self, file=None) -> None:
        """
        快照，保存视图画面为png图像文件

        :param file: png文件路径
        :return: None
        """
        if file is None:
            file = vmi.askSaveFile(self.tr('快照 (Snapshot)'), '*.png')
        if file is not None:
            if not file.endswith('.png'):
                file += '.png'
            self.snapshot().save(file)

    def _timeout(self):
        if self._UpdateAtOnce:
            self.updateAtOnce()
        self._UpdateSum += 1

        if self._Time.elapsed() > 0.5e3:
            self._FPS = 1000 * self._UpdateSum / self._Time.elapsed()
            self.setWindowTitle(QApplication.applicationName() + ' FPS: {:.0f}'.format(self._FPS))
            self._Time.restart()
            self._UpdateSum = 0

    def updateInTime(self) -> None:
        """及时刷新视图"""
        self._UpdateAtOnce = True

    def updateAtOnce(self) -> None:
        """立即刷新视图"""
        if self._Timer.isActive():
            self._UpdateAtOnce = False
            self._Renderer.ResetCameraClippingRange()
            self._RenderWindow.Render()

    def wheelEvent(self, ev):
        d = int(ev.delta() / 120)
        self.mouseExec([self.entered()], 'NoButton', 'Wheel', delta=d)
        ev.accept()


def _init_orientation_marker(i):
    """
    :param i: vtk.vtkRenderWindowInteractor
    :return: vtk.vtkOrientationMarkerWidget
    """

    vtk.vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()

    cube = vtk.vtkAnnotatedCubeActor()
    cube.SetFaceTextScale(0.65)
    cube.SetXPlusFaceText("L")
    cube.SetXMinusFaceText("R")
    cube.SetYPlusFaceText("P")
    cube.SetYMinusFaceText("A")
    cube.SetZPlusFaceText("S")
    cube.SetZMinusFaceText("I")

    prop = cube.GetCubeProperty()
    prop.SetColor(0.75, 0.75, 1)

    prop = cube.GetTextEdgesProperty()
    prop.SetLineWidth(1)
    prop.SetDiffuse(0)
    prop.SetAmbient(1)
    prop.SetColor(0, 0, 0)

    prop = cube.GetXPlusFaceProperty()
    prop.SetColor(1, 0, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetXMinusFaceProperty()
    prop.SetColor(1, 0, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetYPlusFaceProperty()
    prop.SetColor(0, 1, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetYMinusFaceProperty()
    prop.SetColor(0, 1, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetZPlusFaceProperty()
    prop.SetColor(0, 0, 1)
    prop.SetInterpolationToFlat()
    prop = cube.GetZMinusFaceProperty()
    prop.SetColor(0, 0, 1)
    prop.SetInterpolationToFlat()

    axes = vtk.vtkAxesActor()

    axes.SetShaftTypeToCylinder()
    axes.SetXAxisLabelText("X")
    axes.SetYAxisLabelText("Y")
    axes.SetZAxisLabelText("Z")

    axes.SetTotalLength(1.5, 1.5, 1.5)
    axes.SetCylinderRadius(0.500 * axes.GetCylinderRadius())
    axes.SetConeRadius(1.025 * axes.GetConeRadius())
    axes.SetSphereRadius(1.500 * axes.GetSphereRadius())

    prop = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(1, 0, 0)

    prop = axes.GetYAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(0, 1, 0)

    prop = axes.GetZAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(0, 0, 1)

    assembly = vtk.vtkPropAssembly()
    assembly.AddPart(axes)
    assembly.AddPart(cube)

    ort = vtk.vtkOrientationMarkerWidget()
    ort.SetOrientationMarker(assembly)
    ort.SetViewport(0.0, 0.0, 0.2, 0.2)
    ort.SetInteractor(i)
    ort.SetEnabled(1)
    ort.SetInteractive(0)
    ort.On()

    return ort
