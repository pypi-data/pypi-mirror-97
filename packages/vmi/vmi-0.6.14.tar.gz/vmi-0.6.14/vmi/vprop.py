import pathlib
import pprint
import tempfile
from typing import List, Optional, Union, Dict

import numpy as np
import vtk
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import vmi


class PolyActor(QObject, vmi.Menu, vmi.Mouse):
    """三维物体，将vtkPolyData通过vtkPolyDataMapper/vtkActor显示"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 highlightable: bool = True, repres: str = 'surface',
                 color: Union[QColor, List[float]] = QColor('lightgray'), opacity: float = 1.0, point_size: int = 1,
                 line_width: int = 1, shade: bool = True, always_on_top: bool = False):
        """

        :param view: 视图
        :param visible: 可见
        :param pickable: 可交互
        :param highlightable: 可高亮
        :param repres: 表达形式 'points' / 'wireframe' / 'surface'
        :param color: 颜色
        :param opacity: 不透明度
        :param point_size: 点粗，单位是显示像素
        :param line_width: 线粗，单位是显示像素
        :param shade: 阴影
        :param always_on_top: 置顶显示，遮挡关系
        """
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        vmi.Mouse.__init__(self)

        self._Mapper = vtk.vtkPolyDataMapper()
        self._Prop = vtk.vtkActor()
        self._Prop._Prop = self

        self._Property: vtk.vtkProperty = self._Prop.GetProperty()
        self._Prop.SetBackfaceProperty(self._Property)

        self._Data = vtk.vtkPolyData()
        self._BindData = self

        self._View = self._Visible = self._Pickable = self._Repres = None
        self._Color = self._Opacity = self._PointSize = self._LineWidth = self._Shade = self._AlwaysOnTop = None
        self._Highlightable = None
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.setHighlightable(highlightable)
        self.setRepres(repres)
        self.setColor(color)
        self.setOpacity(opacity)
        self.setPointSize(point_size)
        self.setLineWidth(line_width)
        self.setShade(shade)
        self.setAlwaysOnTop(always_on_top)

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        del state['vtk']
        del state['set']
        self.__dict__.update(state)
        self.setView(self._View)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu', 'actions', '__METAOBJECT__']}

        state_set = {kw: getattr(self, kw) for kw in
                     ['_AlwaysOnTop', '_Color', '_Data', '_LineWidth', '_Opacity', '_Pickable', '_PointSize', '_Repres',
                      '_Shade', '_Visible']}
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

    def __repr__(self):
        state = self.__getstate__()['set']
        state['_Data'] = {'GetActualMemorySize': self.data().GetActualMemorySize(),
                          'GetBounds': self.data().GetBounds(),
                          'GetCenter': self.data().GetCenter(),
                          'GetNumberOfCells': self.data().GetNumberOfCells(),
                          'GetNumberOfPoints': self.data().GetNumberOfPoints(),
                          'GetScalarRange': self.data().GetScalarRange()}
        return pprint.pformat(state, width=400, compact=True)

    def view(self) -> vmi.View:
        """返回视图"""
        return self._View

    def prop(self) -> vtk.vtkActor:
        """返回vtkActor"""
        return self._Prop

    def prop_property(self) -> vtk.vtkProperty:
        """返回渲染属性"""
        return self._Property

    def setView(self, view) -> None:
        """设置视图，同时更新数据关联"""
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)
        self.bindData()

    def updateInTime(self) -> None:
        """及时刷新视图"""
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        """返回可见状态"""
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        """设置可见状态"""
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        """切换可见状态"""
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        """返回可交互状态"""
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        """设置可交互状态"""
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def setHighlightable(self, able: bool) -> None:
        """设置可高亮"""
        self.updateInTime()
        self._Highlightable = able
        if self._Highlightable:
            for b in self.mouse:
                for e in self.mouse[b]:
                    if e == 'Enter':
                        self.mouse[b][e] = [self.mouseEnter]
                    elif e == 'Leave':
                        self.mouse[b][e] = [self.mouseLeave]
                    elif e == 'Press':
                        self.mouse[b][e] = [self.mousePress]
                    elif e == 'PressMoveRelease':
                        self.mouse[b][e] = [self.mouseRelease]
                    elif e == 'PressRelease':
                        self.mouse[b][e] = [self.mouseRelease]
        else:
            for b in self.mouse:
                for e in self.mouse[b]:
                    if e == 'Enter':
                        self.mouse[b][e] = [self.mousePass]
                    elif e == 'Leave':
                        self.mouse[b][e] = [self.mousePass]
                    elif e == 'Press':
                        self.mouse[b][e] = [self.mousePass]
                    elif e == 'PressMoveRelease':
                        self.mouse[b][e] = [self.mousePass]
                    elif e == 'PressRelease':
                        self.mouse[b][e] = [self.mousePass]

    def repres(self) -> str:
        """返回表达形式"""
        return self._Repres

    def setRepres(self, repres: str) -> None:
        """设置表达形式 'points' / 'wireframe' / 'surface'"""
        self.updateInTime()
        if repres == 'points':
            self._Repres = repres
            self._Property.SetRepresentationToPoints()
        elif repres == 'wireframe':
            self._Repres = repres
            self._Property.SetRepresentationToWireframe()
        elif repres == 'surface':
            self._Repres = repres
            self._Property.SetRepresentationToSurface()

    def color(self) -> QColor:
        """返回颜色"""
        return self._Color

    def setColor(self, color: Union[QColor, List[float]]) -> None:
        """设置颜色"""
        self.updateInTime()
        if isinstance(color, QColor):
            self._Color = color
        else:
            self._Color = QColor.fromRgbF(color[0], color[1], color[2])
        self._Property.SetColor(self._Color.redF(), self._Color.greenF(), self._Color.blueF())

    def opacity(self) -> float:
        """返回不透明度"""
        return self._Opacity

    def setOpacity(self, opacity: float) -> None:
        """设置不透明度"""
        self.updateInTime()
        opacity = min(max(opacity, 0.0), 1.0)
        self._Opacity = opacity
        self._Property.SetOpacity(self._Opacity)

    def pointSize(self) -> int:
        """返回点粗，单位是显示像素"""
        return self._PointSize

    def setPointSize(self, point_size: int) -> None:
        """设置点粗，单位是显示像素"""
        point_size = min(max(point_size, 1), 100)
        self._PointSize = point_size
        self._Property.SetPointSize(self._PointSize)

    def lineWidth(self) -> int:
        """返回线粗，单位是显示像素"""
        return self._LineWidth

    def setLineWidth(self, point_size: int) -> None:
        """设置线粗，单位是显示像素"""
        point_size = min(max(point_size, 1), 100)
        self._LineWidth = point_size
        self._Property.SetLineWidth(self._LineWidth)

    def shade(self) -> bool:
        """返回阴影状态"""
        return self._Shade

    def setShade(self, shade: bool) -> None:
        """设置阴影状态"""
        self.updateInTime()
        self._Shade = shade
        self._Property.SetAmbient(0 if self._Shade else 1)
        self._Property.SetDiffuse(1 if self._Shade else 0)

    def alwaysOnTop(self) -> bool:
        """返回置顶状态"""
        return self._AlwaysOnTop

    def setAlwaysOnTop(self, always_on_top: bool) -> None:
        """设置置顶状态"""
        self.updateInTime()
        self._AlwaysOnTop = always_on_top
        if self._AlwaysOnTop:
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
        else:
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-1)

    def data(self) -> vtk.vtkPolyData:
        """返回数据"""
        return self._Data

    def bindData(self, other=None) -> None:
        """关联数据到视图，可以关联其它对象，other = self 关联自身对象，other = None 关联当前对象"""
        self.updateInTime()
        if hasattr(other, '_Data'):
            self._BindData = other
        self._Mapper.SetInputData(self._BindData.data())
        self._Prop.SetMapper(self._Mapper)

    def setData(self, other) -> None:
        """设置数据，可以直接设置其它同类实例，或TopoDS_Shape / Polyhedron_3"""
        self.updateInTime()
        if hasattr(other, '_Data'):
            self.data().ShallowCopy(other.data())
        elif isinstance(other, self.data().__class__):
            self.data().ShallowCopy(other)
        elif isinstance(other, vmi.TopoDS_Shape):
            other = vmi.ccPd_Sh(other)
            self.setData(other)
        elif isinstance(other, vmi.Polyhedron_3):
            other = vmi.cgPd_Ph(other)
            self.setData(other)
        else:
            self.data().ShallowCopy(self.data().__class__())
        self.bindData()

    def scalar(self, image: Optional[vtk.vtkImageData] = None,
               lookup_table: Optional[vtk.vtkScalarsToColors] = None) -> None:
        if image and lookup_table:
            self._Mapper.SetColorModeToMapScalars()
            self._Mapper.SetUseLookupTableScalarRange(1)
            self._Mapper.SetScalarVisibility(1)
            self._Mapper.SetLookupTable(lookup_table)

            probe = vtk.vtkProbeFilter()
            probe.SetInputData(self._BindData.data())
            probe.SetSourceData(image)
            probe.Update()
            self.setData(probe.GetOutput())
        else:
            self._Mapper.SetScalarVisibility(0)
            self._Mapper.SetLookupTable(None)

    def delete(self) -> None:
        """清除视图关联，在del之前调用"""
        self.updateInTime()
        self.data().ReleaseData()
        self.setView(None)

    def mouseEnter(self, **kwargs) -> None:
        self.updateInTime()
        c = self._Color.lighter(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())

    def mousePress(self, **kwargs) -> None:
        self.updateInTime()
        c = self._Color.darker(120)
        self._Property.SetColor(c.redF(), c.greenF(), c.blueF())

    def mouseRelease(self, **kwargs) -> None:
        self.updateInTime()
        self._Property.SetColor(self._Color.redF(), self._Color.greenF(), self._Color.blueF())

    def mouseLeave(self, **kwargs) -> None:
        self.updateInTime()
        self._Property.SetColor(self._Color.redF(), self._Color.greenF(), self._Color.blueF())


class ImageBox(QObject, vmi.Menu, vmi.Mouse):
    """二维图标，将QImage通过vtkImageMapper/vtkActor2D显示"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 image: QImage = QImage(1, 1, QImage.Format.Format_RGB32),
                 size: List[float] = (0.5, 0.5), pos: List[float] = (0.5, 0.5), anchor: List[float] = (0.5, 0.5)):
        """
        :param view: 视图
        :param visible: 可见
        :param pickable: 可交互
        :param image: 图像
        :param size: 显示大小，单位是视图宽高比例
        :param pos: 定位位置，单位是视图宽高比例
        :param anchor: 定位锚点，单位是视图宽高比例
        """
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        vmi.Mouse.__init__(self)
        for b in self.mouse:
            for e in self.mouse[b]:
                if e == 'Enter':
                    self.mouse[b][e] = [self.mouseEnter]
                elif e == 'Leave':
                    self.mouse[b][e] = [self.mouseLeave]
                elif e == 'Press':
                    self.mouse[b][e] = [self.mousePress]
                elif e == 'PressMoveRelease':
                    self.mouse[b][e] = [self.mousePass if b == 'RightButton' else self.mouseRelease]
                elif e == 'PressRelease':
                    self.mouse[b][e] = [self.mousePass if b == 'RightButton' else self.mouseRelease]

        self._Mapper = vtk.vtkImageMapper()
        self._Mapper.SetColorLevel(128)
        self._Mapper.SetColorWindow(256)

        self._Prop = vtk.vtkActor2D()
        self._Prop._Prop = self
        self._Property: vtk.vtkProperty = self._Prop.GetProperty()
        self._Data = vtk.vtkImageData()
        self._BindData = self

        self._View = self._Visible = self._Pickable = None
        self._Image = QImage(1, 1, QImage.Format.Format_RGB32)
        self._Size = [0.5, 0.5]
        self._Pos = [0.5, 0.5]
        self._Anchor = [0.5, 0.5]
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.draw(image=image, size=size, pos=pos, anchor=anchor)

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        self.draw(image=state['draw']['_Image'], size=state['draw']['_Size'], pos=state['draw']['_Pos'],
                  anchor=state['draw']['_Anchor'])

        del state['vtk']
        del state['draw']
        del state['set']
        self.__dict__.update(state)
        self.setView(self._View)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu', 'actions', '__METAOBJECT__']}

        state_set = {kw: getattr(self, kw) for kw in ['_Pickable', '_Visible']}
        state = {kw: state[kw] for kw in state if kw not in state_set}

        state_draw = {kw: getattr(self, kw) for kw in ['_Anchor', '_Image', '_Pos', '_Size']}

        state_vtk = {}
        for kw in state:
            if isinstance(state[kw], vtk.vtkObject):
                if not hasattr(vmi, 'pickle_' + state[kw].__class__.__name__):
                    state_vtk[kw] = vmi.vtkInstance_gets(state[kw])
        state = {kw: state[kw] for kw in state if kw not in state_vtk}

        state['set'] = state_set
        state['draw'] = state_draw
        state['vtk'] = state_vtk
        return state

    def __repr__(self):
        state = self.__getstate__()
        state = {**state['set'], **state['draw']}
        return pprint.pformat(state, width=400, compact=True)

    def resize(self) -> None:
        self.draw()

    def data(self) -> vtk.vtkImageData:
        """返回数据"""
        return self._Data

    def bindData(self, other=None) -> None:
        """关联数据到视图，可以关联其它对象，other = self 关联自身对象，other = None 关联当前对象"""
        self.updateInTime()
        if hasattr(other, '_Data'):
            self._BindData = other
        self._Mapper.SetInputData(self._BindData.data())
        self._Prop.SetMapper(self._Mapper)

    def delete(self) -> None:
        """清除视图关联，在del之前调用"""
        self.updateInTime()
        self.data().ReleaseData()
        self.setView(None)

    def draw(self, image: QImage = None, size: List[float] = None, pos: List[float] = None,
             anchor: List[float] = None) -> None:
        """
        重绘，同时更新参数

        :param image: 图像
        :param size: 显示大小，单位是视图宽高比例
        :param pos: 定位位置，单位是视图宽高比例
        :param anchor: 定位锚点，单位是视图宽高比例
        :return: None
        """
        self.updateInTime()

        if image is not None:
            self._Image = image

        if size is not None:
            self._Size = [min(max(size[0], 0), 1), min(max(size[1], 0), 1)]

        if pos is not None:
            self._Pos = [min(max(pos[0], 0), 1), min(max(pos[1], 0), 1)]

        if anchor is not None:
            self._Anchor = [min(max(anchor[0], 0), 1), min(max(anchor[1], 0), 1)]

        if self.view():
            # 图像缩放
            size = [round(self._Size[0] * self.view().width()), round(self._Size[1] * self.view().height())]
            image = self._Image.scaled(size[0], size[1], Qt.AspectRatioMode.KeepAspectRatio)

            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '.png'
                image.save(str(p), 'PNG')

                r = vtk.vtkPNGReader()
                r.SetFileName(str(p))
                r.Update()
                self.data().ShallowCopy(r.GetOutput())

            # 图像定位
            pos = [round(self._Pos[0] * self.view().width()), round(self._Pos[1] * self.view().height())]
            anchor = [round(self._Anchor[0] * image.width()), round((1 - self._Anchor[1]) * image.height())]

            self._Prop.SetPosition(pos[0] - anchor[0], self.view().height() - pos[1] - anchor[1])

    def view(self) -> vmi.View:
        """返回视图"""
        return self._View

    def setView(self, view) -> None:
        """设置视图，同时更新数据关联"""
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)
        self.bindData()
        self.draw()

    def updateInTime(self) -> None:
        """及时刷新视图"""
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        """返回可见状态"""
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        """设置可见状态"""
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        """切换可见状态"""
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        """返回可交互状态"""
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        """设置可交互状态"""
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def image(self) -> QImage:
        """返回图像"""
        return self._Image

    def size(self) -> List[float]:
        """显示大小，单位是视图宽高比例"""
        return self._Size

    def pos(self) -> List[float]:
        """定位位置，单位是视图宽高比例"""
        return self._Pos

    def anchor(self) -> List[float]:
        """定位锚点，单位是视图宽高比例"""
        return self._Anchor

    def mouseEnter(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(96)
        self._Mapper.SetColorWindow(256)

    def mousePress(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(160)
        self._Mapper.SetColorWindow(256)

    def mouseRelease(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(128)
        self._Mapper.SetColorWindow(256)

    def mouseLeave(self, **kwargs) -> None:
        self.updateInTime()
        self._Mapper.SetColorLevel(128)
        self._Mapper.SetColorWindow(256)


class TextBox(ImageBox):
    """二维文字，将str通过vtkImageMapper/vtkActor2D显示"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 text: str = str(), text_font: str = '等线', text_align: str = 'AlignCenter',
                 fore_color: QColor = QColor('black'), back_color: QColor = QColor('whitesmoke'),
                 bold: bool = False, italic: bool = False, underline: bool = False,
                 size: List[float] = (0.5, 0.5), pos: List[float] = (0.5, 0.5), anchor: List[float] = (0.5, 0.5)):
        """
        :param view: 视图
        :param visible: 可见
        :param pickable: 可交互
        :param text: 文字
        :param text_font: 字体
        :param text_align: 对齐方式 'AlignCenter' / 'AlignLeft' / 'AlignRight'
        :param fore_color: 前景色
        :param back_color: 背景色
        :param bold: 粗体状态
        :param italic: 斜体状态
        :param underline: 下划线状态
        :param size: 显示大小，单位是视图宽高比例
        :param pos: 定位位置，单位是视图宽高比例
        :param anchor: 定位锚点，单位是视图宽高比例
        """
        ImageBox.__init__(self, visible=visible, size=size, pos=pos, anchor=anchor, pickable=pickable)

        self._Text = str()
        self._TextFont = '等线'
        self._TextAlign = 'AlignCenter'
        self._ForeColor = QColor('black')
        self._BackColor = QColor('whitesmoke')
        self._Bold = False
        self._Italic = False
        self._Underline = False
        self.draw_text(text=text, text_font=text_font, text_align=text_align,
                       fore_color=fore_color, back_color=back_color,
                       bold=bold, italic=italic, underline=underline,
                       size=size, pos=pos, anchor=anchor)
        self.setView(view)

    def font(self) -> str:
        """返回字体"""
        return self._TextFont

    def text(self) -> str:
        """返回文字"""
        return self._Text

    def text_align(self) -> str:
        """返回对齐方式"""
        return self._TextAlign

    def fore_color(self) -> QColor:
        """返回前景色"""
        return self._ForeColor

    def back_color(self) -> QColor:
        """返回背景色"""
        return self._BackColor

    def bold(self) -> bool:
        """返回粗体状态"""
        return self._Bold

    def italic(self) -> bool:
        """返回斜体状态"""
        return self._Italic

    def underline(self) -> bool:
        """返回下划线状态"""
        return self._Underline

    def draw_text(self, text: str = None, text_font: str = None, text_align: str = None,
                  fore_color: QColor = None, back_color: QColor = None,
                  bold: bool = None, italic: bool = None, underline: bool = None,
                  size: List[float] = None, pos: List[float] = None, anchor: List[float] = None) -> None:
        """
        重绘，同时更新参数

        :param text: 文字
        :param text_font: 字体
        :param text_align: 对齐方式 'AlignCenter' / 'AlignLeft' / 'AlignRight'
        :param fore_color: 前景色
        :param back_color: 背景色
        :param bold: 粗体状态
        :param italic: 斜体状态
        :param underline: 下划线状态
        :param size: 显示大小，单位是视图宽高比例
        :param pos: 定位位置，单位是视图宽高比例
        :param anchor: 定位锚点，单位是视图宽高比例
        :return: None
        """
        if text is not None:
            self._Text = text
        if text_font is not None:
            self._TextFont = text_font
        if text_align is not None:
            self._TextAlign = text_align
        if fore_color is not None:
            self._ForeColor = fore_color
        if back_color is not None:
            self._BackColor = back_color
        if bold is not None:
            self._Bold = bold
        if italic is not None:
            self._Italic = italic
        if underline is not None:
            self._Underline = underline

        if self.view():
            w = round(self._Size[0] * self.view().width())
            h = round(self._Size[1] * self.view().height())

            pa = QPainter()

            # 字体
            font_size = 16
            font = QFont(self._TextFont, font_size)
            font.setPointSizeF(font_size)
            font.setBold(self._Bold)
            font.setItalic(self._Italic)
            font.setUnderline(self._Underline)

            # 计算字体大小
            image = QImage(w, h, QImage.Format.Format_RGB32)

            pa.begin(image)
            pa.setPen(self._ForeColor)
            # for s in range(2,18):
            pa.setFont(font)
            rect = pa.drawText(0, 0, w, h, getattr(Qt, self._TextAlign), self._Text)
            if rect.width() > 0 and rect.height() > 0:
                if 0.5 * h / rect.height() < (w - 20) / rect.width():
                    font_size *= 0.5 * h / rect.height()
                else:
                    font_size *= (w - 20) / rect.width()
                font.setPointSizeF(font_size)
            pa.end()

            # 绘制文本
            image = QImage(w, h, QImage.Format.Format_RGB32)
            pa.begin(image)
            pa.setFont(font)
            pa.setPen(self._ForeColor)
            pa.fillRect(0, 0, w, h, self._BackColor)
            pa.drawText(0, 0, w, h, getattr(Qt, self._TextAlign), self._Text)
            pa.end()

            self.draw(image=image, size=size, pos=pos, anchor=anchor)

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        self.draw_text(text=state['draw']['_Text'], text_font=state['draw']['_TextFont'],
                       text_align=state['draw']['_TextAlign'], fore_color=state['draw']['_ForeColor'],
                       back_color=state['draw']['_BackColor'], bold=state['draw']['_Bold'],
                       italic=state['draw']['_Italic'], underline=state['draw']['_Underline'],
                       size=state['draw']['_Size'], pos=state['draw']['_Pos'], anchor=state['draw']['_Anchor'])

        del state['vtk']
        del state['draw']
        del state['set']
        self.__dict__.update(state)
        self.setView(self._View)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu', 'actions', '__METAOBJECT__']}

        state_set = {kw: getattr(self, kw) for kw in ['_Pickable', '_Visible']}
        state = {kw: state[kw] for kw in state if kw not in state_set}

        state_draw = {kw: getattr(self, kw) for kw in
                      ['_Anchor', '_BackColor', '_Bold', '_ForeColor', '_Italic', '_Pos', '_Size', '_Text',
                       '_TextAlign', '_TextFont', '_Underline']}

        state_vtk = {}
        for kw in state:
            if isinstance(state[kw], vtk.vtkObject):
                if not hasattr(vmi, 'pickle_' + state[kw].__class__.__name__):
                    state_vtk[kw] = vmi.vtkInstance_gets(state[kw])
        state = {kw: state[kw] for kw in state if kw not in state_vtk}

        state['set'] = state_set
        state['draw'] = state_draw
        state['vtk'] = state_vtk
        return state

    def __repr__(self):
        state = self.__getstate__()
        state = {**state['set'], **state['draw']}
        return pprint.pformat(state, width=400, compact=True)

    def setView(self, view) -> None:
        """设置视图，同时更新数据关联"""
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)
        self.bindData()
        self.draw_text()

    def resize(self) -> None:
        self.draw_text()


class ValueBox(TextBox):
    """数值框，具有数值调节默认交互的控件"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 value_format: str = '{}', value_min: float = 0, value: float = 0, value_max: float = 1,
                 value_decimals: int = 0, value_step: float = 1, value_update=None,
                 text_font: str = '等线', text_align: str = 'AlignCenter',
                 fore_color: QColor = QColor('black'), back_color: QColor = QColor('whitesmoke'),
                 bold: bool = False, italic: bool = False, underline: bool = False,
                 size: List[float] = (0.5, 0.5), pos: List[float] = (0.5, 0.5), anchor: List[float] = (0.5, 0.5)):
        """
        :param view: 视图
        :param visible: 可见
        :param pickable: 可交互
        :param value_format: 数值显示格式
        :param value_min: 数值最小值
        :param value: 数值初始值
        :param value_max: 数值最大值
        :param value_decimals: 数值的小数位数
        :param value_step: 数值调节最小单位
        :param text_font: 字体
        :param text_align: 对齐方式 'AlignCenter' / 'AlignLeft' / 'AlignRight'
        :param fore_color: 前景色
        :param back_color: 背景色
        :param bold: 粗体状态
        :param italic: 斜体状态
        :param underline: 下划线状态
        :param size: 显示大小，单位是视图宽高比例
        :param pos: 定位位置，单位是视图宽高比例
        :param anchor: 定位锚点，单位是视图宽高比例
        """
        TextBox.__init__(self, visible=visible, pickable=pickable,
                         text_font=text_font, text_align=text_align,
                         fore_color=fore_color, back_color=back_color,
                         bold=bold, italic=italic, underline=underline,
                         size=size, pos=pos, anchor=anchor)

        self._ValueFormat = value_format
        self._ValueMin = value_min
        self._Value = value
        self._ValueMax = value_max
        self._ValueDecimals = max(0, value_decimals)
        self._ValueStep = value_step
        self.draw_value(value_format=value_format,
                        value_min=value_min, value=value, value_max=value_max,
                        value_decimals=value_decimals, value_step=value_step,
                        text_font=text_font, text_align=text_align,
                        fore_color=fore_color, back_color=back_color,
                        bold=bold, italic=italic, underline=underline,
                        size=size, pos=pos, anchor=anchor)
        self.setView(view)

        self.mouse['LeftButton']['PressRelease'] = [self._ask_value]
        self.mouse['NoButton']['Wheel'] = [self._wheel_value]
        self.value_update = value_update

    def _ask_value(self, **kwargs):
        value = vmi.askFloat(self._ValueMin, self._Value, self._ValueMax, self._ValueDecimals, self._ValueStep)
        if value is not None:
            self.draw_value(value=value)
            if self.value_update:
                self.value_update()

    def _wheel_value(self, **kwargs):
        value = self._Value + self._ValueStep * kwargs['delta']
        value = min(max(value, self._ValueMin), self._ValueMax)
        self.draw_value(value=value)
        if self.value_update:
            self.value_update()

    def draw_value(self, value_format: str = None, value_min: float = None, value: float = None,
                   value_max: float = None, value_decimals: float = None,
                   value_step: float = None, text_font: str = None, text_align: str = None,
                   fore_color: QColor = None, back_color: QColor = None,
                   bold: bool = None, italic: bool = None, underline: bool = None,
                   size: List[float] = None, pos: List[float] = None, anchor: List[float] = None) -> None:
        """
        重绘，同时更新参数

        :param value_format: 数值显示格式
        :param value_min: 数值最小值
        :param value: 数值初始值
        :param value_max: 数值最大值
        :param value_decimals: 数值的小数位数
        :param value_step: 数值调节最小单位
        :param text_font: 字体
        :param text_align: 对齐方式 'AlignCenter' / 'AlignLeft' / 'AlignRight'
        :param fore_color: 前景色
        :param back_color: 背景色
        :param bold: 粗体状态
        :param italic: 斜体状态
        :param underline: 下划线状态
        :param size: 显示大小，单位是视图宽高比例
        :param pos: 定位位置，单位是视图宽高比例
        :param anchor: 定位锚点，单位是视图宽高比例
        :return: None
        """
        if value_format is not None:
            self._ValueFormat = value_format
        if value_min is not None:
            self._ValueMin = value_min
        if value is not None:
            self._Value = value
        if value_max is not None:
            self._ValueMax = value_max
        if value_decimals is not None:
            self._ValueDecimals = value_decimals
        if value_step is not None:
            self._ValueStep = value_step

        if self.view():
            self.draw_text(text=self._ValueFormat.format(self._Value),
                           text_font=text_font, text_align=text_align,
                           fore_color=fore_color, back_color=back_color,
                           bold=bold, italic=italic, underline=underline,
                           size=size, pos=pos, anchor=anchor)

    def value_format(self) -> str:
        """返回数值格式"""
        return self._ValueFormat

    def value_min(self) -> float:
        """返回数值最小值"""
        return self._ValueMin

    def value(self) -> float:
        """返回数值"""
        return self._Value

    def value_max(self) -> float:
        """返回数值最大值"""
        return self._ValueMax

    def value_decimals(self) -> float:
        """返回数值小数位数"""
        return self._ValueDecimals

    def value_step(self) -> float:
        """返回数值调节最小单位"""
        return self._ValueStep

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        self.draw_value(value_format=state['draw']['_ValueFormat'], value_min=state['draw']['_ValueMin'],
                        value=state['draw']['_Value'], value_max=state['draw']['_ValueMax'],
                        value_decimals=state['draw']['_ValueDecimals'],
                        value_step=state['draw']['_ValueStep'], text_font=state['draw']['_TextFont'],
                        text_align=state['draw']['_TextAlign'], fore_color=state['draw']['_ForeColor'],
                        back_color=state['draw']['_BackColor'], bold=state['draw']['_Bold'],
                        italic=state['draw']['_Italic'], underline=state['draw']['_Underline'],
                        size=state['draw']['_Size'], pos=state['draw']['_Pos'], anchor=state['draw']['_Anchor'])

        del state['vtk']
        del state['draw']
        del state['set']
        self.__dict__.update(state)
        self.setView(self._View)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu', 'actions', '__METAOBJECT__']}

        state_set = {kw: getattr(self, kw) for kw in ['_Pickable', '_Visible']}
        state = {kw: state[kw] for kw in state if kw not in state_set}

        state_draw = {kw: getattr(self, kw) for kw in
                      ['_Anchor', '_BackColor', '_Bold', '_ForeColor', '_Italic', '_Pos', '_Size',
                       '_Text', '_TextAlign', '_TextFont', '_Underline',
                       '_ValueFormat', '_ValueMin', '_Value', '_ValueMax', '_ValueDecimals', '_ValueStep']}

        state_vtk = {}
        for kw in state:
            if isinstance(state[kw], vtk.vtkObject):
                if not hasattr(vmi, 'pickle_' + state[kw].__class__.__name__):
                    state_vtk[kw] = vmi.vtkInstance_gets(state[kw])
        state = {kw: state[kw] for kw in state if kw not in state_vtk}

        state['set'] = state_set
        state['draw'] = state_draw
        state['vtk'] = state_vtk
        return state

    def __repr__(self):
        state = self.__getstate__()
        state = {**state['set'], **state['draw']}
        return pprint.pformat(state, width=400, compact=True)

    def setView(self, view) -> None:
        """设置视图，同时更新数据关联"""
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)
        self.bindData()
        self.draw_value()

    def resize(self) -> None:
        self.draw_value()


class ImageSlice(QObject, vmi.Menu, vmi.Mouse):
    """图像断层，将vtkImageData通过vtkImageResliceMapper/vtkImageSlice显示"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = True,
                 colorWindow: List[int] = (350, 50)):
        """
        :param view: 视图
        :param visible: 可见
        :param pickable: 可交互
        :param colorWindow: 窗宽窗位 [width, level]
        """
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        self.actions = {'SlicePlaneValueNormal': QAction(''),
                        'SlicePlaneAxial': QAction('横断位 (Axial)'),
                        'SlicePlaneSagittal': QAction('矢状位 (Sagittal)'),
                        'SlicePlaneCoronal': QAction('冠状位 (Coronal)'),
                        'WindowValue': QAction(''),
                        'WindowAuto': QAction('自动 (Auto)'),
                        'WindowBone': QAction('骨骼 (Bone)'),
                        'WindowSoft': QAction('组织 (Soft)')}

        self.actions['SlicePlaneAxial'].triggered.connect(self.setSlicePlaneNormal_Axial)
        self.actions['SlicePlaneSagittal'].triggered.connect(self.setSlicePlaneNormal_Sagittal)
        self.actions['SlicePlaneCoronal'].triggered.connect(self.setSlicePlaneNormal_Coronal)
        self.actions['WindowAuto'].triggered.connect(self.setColorWindow_Auto)
        self.actions['WindowBone'].triggered.connect(self.setColorWindow_Bone)
        self.actions['WindowSoft'].triggered.connect(self.setColorWindow_Soft)

        def aboutToShow():
            self.actions['SlicePlaneValueNormal'].setText(
                '法向 (Normal)' + ' = ' + repr(tuple(self._SlicePlaneNormal)))
            self.actions['WindowValue'].setText(
                '宽/位 (W/L)' + ' = ' + (repr(tuple(self._ColorWindow))))

            self.menu.clear()

            menu = QMenu('切面 (Slice plane)')
            menu.addAction(self.actions['SlicePlaneValueNormal'])
            menu.addSeparator()
            menu.addAction(self.actions['SlicePlaneAxial'])
            menu.addAction(self.actions['SlicePlaneSagittal'])
            menu.addAction(self.actions['SlicePlaneCoronal'])
            self.menu.addMenu(menu)

            menu = QMenu('窗 (Window)')
            menu.addAction(self.actions['WindowValue'])
            menu.addSeparator()
            menu.addAction(self.actions['WindowAuto'])
            menu.addAction(self.actions['WindowBone'])
            menu.addAction(self.actions['WindowSoft'])
            self.menu.addMenu(menu)

        self.menu.aboutToShow.connect(aboutToShow)

        vmi.Mouse.__init__(self, menu=self)
        self.mouse['NoButton']['Wheel'] = [self.slice]
        self.mouse['LeftButton']['PressMove'] = [self.windowMove]

        self._Mapper = vtk.vtkImageResliceMapper()
        self._Prop = vtk.vtkImageSlice()
        self._Prop._Prop = self

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToCubic()
        self._Property.SetUseLookupTableScalarRange(1)

        self._SlicePlane = vtk.vtkPlane()
        self._Mapper.SetSlicePlane(self._SlicePlane)

        self._Data = vtk.vtkImageData()
        self._BindData = self

        self._SlicePlaneOrigin = np.array([0, 0, 0])
        self._BindSlicePlaneOrigin = [self]

        self._SlicePlaneNormal = np.array([0, 0, 1])
        self._BindSlicePlaneNormal = [self]

        self._LookupTable = vtk.vtkLookupTable()
        self._BindColorWindow = [self]

        self._View = self._Visible = self._Pickable = None
        self._Color = {0: [0, 0, 0], 1: [1, 1, 1]}
        self._ColorBelowRange = [0, 0, 0]
        self._ColorAboveRange = [1, 1, 1]
        self._ColorWindow = [350, 50]
        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.setColorWindow(self._ColorWindow)
        self.setSlicePlane(self._SlicePlaneOrigin, self._SlicePlaneNormal)

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        del state['vtk']
        del state['set']
        self.__dict__.update(state)
        self.setView(self._View)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu', 'actions', '__METAOBJECT__']}

        state_set = {kw: getattr(self, kw) for kw in [
            '_Data', '_Pickable', '_Visible', '_ColorWindow', '_LookupTable', '_SlicePlaneOrigin', '_SlicePlaneNormal']}
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

    def __repr__(self):
        state = self.__getstate__()['set']
        state['_Data'] = {'GetActualMemorySize': self.data().GetActualMemorySize(),
                          'GetBounds': self.data().GetBounds(),
                          'GetCenter': self.data().GetCenter(),
                          'GetExtent': self.data().GetExtent(),
                          'GetNumberOfCells': self.data().GetNumberOfCells(),
                          'GetNumberOfPoints': self.data().GetNumberOfPoints(),
                          'GetOrigin': self.data().GetOrigin(),
                          'GetScalarRange': self.data().GetScalarRange(),
                          'GetSpacing': self.data().GetSpacing()}
        return pprint.pformat(state, width=400, compact=True)

    def view(self) -> vmi.View:
        """返回视图"""
        return self._View

    def setView(self, view) -> None:
        """设置视图"""
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)
        self.bindData()

    def updateInTime(self) -> None:
        """及时更新"""
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        """返回可见状态"""
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        """设置可见状态"""
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        """切换可见状态"""
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        """返回可交互状态"""
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        """设置可交互状态"""
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def data(self) -> vtk.vtkImageData:
        """返回数据"""
        return self._Data

    def slicePlane(self) -> vtk.vtkPlane:
        """返回断层平面"""
        return self._SlicePlane

    def slicePlaneOrigin(self) -> np.ndarray:
        """返回断层平面原点"""
        return self._SlicePlaneOrigin

    def slicePlaneNormal(self) -> np.ndarray:
        """返回断层平面法向"""
        return self._SlicePlaneNormal

    def lookupTable(self) -> vtk.vtkLookupTable:
        """返回颜色查找表"""
        return self._LookupTable

    def color(self) -> dict:
        return self._Color

    def colorAboveRange(self) -> list:
        return self._ColorAboveRange

    def colorBelowRange(self) -> list:
        return self._ColorBelowRange

    def colorWindow(self) -> list:
        return self._ColorWindow

    def bindData(self, other=None) -> None:
        """关联数据到视图，可以关联其它对象，other = self 关联自身对象，other = None 关联当前对象"""
        self.updateInTime()
        if hasattr(other, '_Data'):
            self._BindData = other
        self._Mapper.SetInputData(self._BindData.data())
        self._Prop.SetMapper(self._Mapper)

    def bindSlicePlaneOrigin(self, others: List, value: Optional[list] = None) -> None:
        """关联断层平面的原点，设置列表内的所有对象彼此关联，同时设置值为value，others = [] 取消关联"""
        binds = others.copy()
        if self not in binds:
            binds.append(self)
        for i in binds:
            i._BindSlicePlaneOrigin = binds.copy()
        if value:
            for i in binds:
                i.setSlicePlaneOrigin(self._SlicePlaneOrigin)

    def bindSlicePlaneNormal(self, others: List, value: Optional[list] = None) -> None:
        """关联断层平面的原点，设置列表内的所有对象彼此关联，同时设置值为value，others = [] 取消关联"""
        binds = others.copy()
        if self not in binds:
            binds.append(self)
        for i in binds:
            i._BindSlicePlaneNormal = binds.copy()
        if value:
            for i in binds:
                i.setSlicePlaneNormal(self._SlicePlaneNormal)

    def bindColorWindow(self, others: List, value: Optional[list] = None) -> None:
        """关联窗宽窗位，设置列表内的所有对象彼此关联，同时设置值为value，others = [] 取消关联"""
        binds = others.copy()
        if self not in binds:
            binds.append(self)
        for i in binds:
            i._BindColorWindow = binds.copy()
        if value:
            for i in binds:
                i.setColorWindow(value)

    def setLookupTable(self, lookup_table) -> None:
        """设置颜色查找表"""
        self._LookupTable = lookup_table
        self._Property.SetLookupTable(self.lookupTable())
        self.updateInTime()

    def setData(self, data) -> None:
        """设置数据，可以直接设置其它同类实例，或vtkImageData"""
        self.updateInTime()
        if hasattr(data, '_Data'):
            self.data().ShallowCopy(data.data())
        elif isinstance(data, self.data().__class__):
            self.data().ShallowCopy(data)
        else:
            self.data().ShallowCopy(self.data().__class__())
        self.bindData()

    def delete(self) -> None:
        """清除视图关联，在del之前调用"""
        self.updateInTime()
        self.data().ReleaseData()
        self.setView(None)

    def setSlicePlane(self, origin: Union[np.ndarray, List[float]], normal: Union[np.ndarray, List[float]]) -> None:
        """
        设置断层平面的原点和法向

        :param origin: 原点
        :param normal: 法向
        :return: None
        """
        for i in self._BindSlicePlaneOrigin:
            i._SlicePlaneOrigin = np.array(origin)
            i._SlicePlaneNormal = np.array(normal)
            i.slicePlane().SetOrigin(list(origin))
            i.slicePlane().SetNormal(list(normal))
            i.updateInTime()

    def setSlicePlaneOrigin(self, origin: Union[np.ndarray, List[float]]) -> None:
        """
        设置断层平面的原点，法向不变

        :param origin: 原点
        :return: None
        """
        for i in self._BindSlicePlaneOrigin:
            i._SlicePlaneOrigin = np.array(origin)
            i.slicePlane().SetOrigin(list(origin))
            i.updateInTime()

    def setSlicePlaneNormal(self, normal: Union[np.ndarray, List[float]]) -> None:
        """
        设置断层平面的法向，原点不变

        :param normal: 法向
        :return: None
        """
        for i in self._BindSlicePlaneNormal:
            i._SlicePlaneNormal = np.array(normal)
            i.slicePlane().SetNormal(normal)
            i.updateInTime()

    def setSlicePlaneOrigin_Center(self) -> None:
        """设置断层平面原点为数据中心"""
        self.setSlicePlaneOrigin(self._BindData.data().GetCenter())

    def setSlicePlaneNormal_Axial(self) -> None:
        """设置断层平面法向为横断位"""
        self.setSlicePlaneNormal([0, 0, 1])

    def setSlicePlaneNormal_Sagittal(self) -> None:
        """设置断层平面法向为矢状位"""
        self.setSlicePlaneNormal([-1, 0, 0])

    def setSlicePlaneNormal_Coronal(self) -> None:
        """设置断层平面法向为冠状位"""
        self.setSlicePlaneNormal([0, -1, 0])

    def setInterpolationType_Nearest(self) -> None:
        """设置图像显示的插值方式为邻位插值"""
        self._Property.SetInterpolationTypeToNearest()
        self.updateInTime()

    def setInterpolationType_Linear(self) -> None:
        """设置图像显示的插值方式为线性插值"""
        self._Property.SetInterpolationTypeToLinear()
        self.updateInTime()

    def setInterpolationType_Cubic(self) -> None:
        """设置图像显示的插值方式为三次插值"""
        self._Property.SetInterpolationTypeToCubic()
        self.updateInTime()

    def setColor(self, color):
        """设置色彩函数，线性映射到窗内替换默认的灰度显示"""
        self._Color = color
        self.setColorWindow(self._ColorWindow)

    def setColor_BlackWhite(self):
        """重设色彩函数为默认的灰度显示"""
        self._Color = {0: [0, 0, 0], 1: [1, 1, 1]}
        self.setColorWindow(self._ColorWindow)

    def setColorBelowRange(self, color):
        """设置体素小于最小窗值的色彩，默认为黑色"""
        self._ColorBelowRange = color
        self.setColorWindow(self._ColorWindow)

    def setColorAboveRange(self, color):
        """设置体素大于最大窗值的色彩，默认为白色"""
        self._ColorAboveRange = color
        self.setColorWindow(self._ColorWindow)

    def setColorWindow(self, color_window: List[int]) -> None:
        """设置窗宽窗位"""
        width = min(max(round(color_window[0]), 0), 65535)
        level = min(max(round(color_window[1]), -32767), 32767)

        self._ColorWindow[0] = int(width)
        self._ColorWindow[1] = int(level)

        ltr = [self._ColorWindow[1] - 0.5 * self._ColorWindow[0],
               self._ColorWindow[1] + 0.5 * self._ColorWindow[0]]
        ltr = [round(ltr[0]), round(ltr[1])]

        for bind in self._BindColorWindow:
            t = vtk.vtkLookupTable()
            t.SetNumberOfTableValues(self._ColorWindow[0])
            t.SetTableRange(ltr)
            t.SetBelowRangeColor(*self._ColorBelowRange, 1.0)
            t.SetAboveRangeColor(*self._ColorAboveRange, 1.0)
            t.SetUseBelowRangeColor(1)
            t.SetUseAboveRangeColor(1)

            ctf = vtk.vtkColorTransferFunction()
            for x in self._Color:
                r, g, b = self._Color[x]
                ctf.AddRGBPoint(x, r, g, b)
            ctfr = ctf.GetRange()

            for i in range(self._ColorWindow[0] + 1):
                try:
                    v = i / self._ColorWindow[0] * (ctfr[1] - ctfr[0]) + ctfr[0]
                except ZeroDivisionError as e:
                    v = ctfr[0]
                r, g, b = ctf.GetColor(v)
                t.SetTableValue(i, (r, g, b, 1.0))

            bind._ColorWindow[0] = self._ColorWindow[0]
            bind._ColorWindow[1] = self._ColorWindow[1]
            bind.setLookupTable(t)

    def setColorWindowWidth(self, width: int) -> None:
        """设置窗宽，窗位不变"""
        width = min(max(width, 0), 65535)
        self.setColorWindow([width, self._ColorWindow[1]])

    def setColorWindowLevel(self, level: int) -> None:
        """设置窗位，窗宽不变"""
        level = min(max(level, -32767), 32767)
        self.setColorWindow([self._ColorWindow[0], level])

    def setColorWindow_Auto(self) -> None:
        """设置窗宽窗位为适应全局"""
        r = vtk.vtkImageHistogramStatistics()
        r.SetInputData(self._BindData.data())
        r.SetAutoRangePercentiles(1, 99)
        r.SetGenerateHistogramImage(0)
        r.Update()
        r = r.GetAutoRange()
        self.setColorWindow([round(r[1] - r[0]), round(0.5 * (r[0] + r[1]))])

    def setColorWindow_Bone(self) -> None:
        """设置窗宽窗位为适应骨骼[1000, 400]"""
        self.setColorWindow([1000, 400])

    def setColorWindow_Soft(self) -> None:
        """设置窗宽窗位为适应软组织[350, 50]"""
        self.setColorWindow([350, 50])

    def slice(self, **kwargs):
        o = list(self.slicePlane().GetOrigin())
        n = self.slicePlane().GetNormal()
        dim = self._BindData.data().GetDimensions()
        dxyz = self._BindData.data().GetSpacing()

        n = [abs(_) / (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5 for _ in n]
        dn = n[0] * dxyz[0] + n[1] * dxyz[1] + n[2] * dxyz[2]

        for i in range(3):
            if dim[i] > 1:
                o[i] += kwargs['delta'] * dn * n[i]

        if vtk.vtkMath.PlaneIntersectsAABB(self._BindData.data().GetBounds(), n, o) == 0:
            self.setSlicePlaneOrigin(o)

    def windowMove(self, **kwargs):
        if self.view():
            dx, dy = self.view().pickVt_Display()
            width = self._ColorWindow[0] + 2 * dx
            level = self._ColorWindow[1] - 2 * dy
            self.setColorWindow([width, level])
            return True


class ImageVolume(QObject, vmi.Menu, vmi.Mouse):
    """图像立体，将vtkImageData通过vtkGPUVolumeRayCastMapper/vtkVolume显示"""

    def __init__(self, view: vmi.View = None, visible: bool = True, pickable: bool = False,
                 color: Dict[int, List[float]] = None, opacityScalar: Dict[int, float] = None,
                 opacityGradient: Dict[int, float] = None):
        """
        :param view: 视图
        :param visible: 可见
        :param pickable: 可交互
        :param color: 颜色方案 {scalar: [red, green, blue]}
        :param opacityScalar: 不透明度方案 {scalar: opacity}
        :param opacityGradient: 不透明度梯度方案 {scalar: opacity}
        """
        QObject.__init__(self)
        vmi.Menu.__init__(self)

        self.actions = {'Threshold': QAction('阈值 (Threshold)')}
        self.actions['Threshold'].triggered.connect(self.setOpacity_Threshold)

        def aboutToShow():
            self.menu.clear()

            menu = QMenu('风格 (Style)')
            menu.addAction(self.actions['Threshold'])
            self.menu.addMenu(menu)

        self.menu.aboutToShow.connect(aboutToShow)

        vmi.Mouse.__init__(self)

        self._Mapper = vtk.vtkGPUVolumeRayCastMapper()
        self._Prop = vtk.vtkVolume()
        self._Prop._Prop = self

        self._Mapper.SetBlendModeToComposite()
        self._Mapper.SetMaxMemoryInBytes(4096)
        self._Mapper.SetMaxMemoryFraction(1)
        self._Mapper.SetAutoAdjustSampleDistances(0)
        self._Mapper.SetLockSampleDistanceToInputSpacing(1)
        self._Mapper.SetUseJittering(1)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToLinear()
        self._Property.SetAmbient(0)
        self._Property.SetDiffuse(1)
        self._Property.SetShade(1)

        self._Data = vtk.vtkImageData()
        self._BindData = self

        self._View = self._Visible = self._Pickable = None
        self._Color = self._OpacityScalar = self._OpacityGradient = None

        self.setView(view)
        self.setVisible(visible)
        self.setPickable(pickable)
        self.setColor(color if color else {0: [1, 1, 1]})
        self.setOpacityScalar(opacityScalar if opacityScalar else {0: 0, 400: 1})
        self.setOpacityGradient(opacityGradient if opacityGradient else {})

    def __setstate__(self, state):
        self.__init__()

        for kw in state['vtk']:
            vmi.vtkInstance_sets(getattr(self, kw), state['vtk'][kw])

        for kw in state['set']:
            getattr(self, kw.replace('_', 'set', 1))(state['set'][kw])

        del state['vtk']
        del state['set']
        self.__dict__.update(state)
        self.setView(self._View)

    def __getstate__(self):
        state = self.__dict__.copy()
        state = {kw: state[kw] for kw in state if kw not in ['menu', 'actions', '__METAOBJECT__']}

        state_set = {kw: getattr(self, kw) for kw in
                     ['_Data', '_Pickable', '_Visible', '_Color', '_OpacityScalar', '_OpacityGradient']}
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

    def __repr__(self):
        state = self.__getstate__()['set']
        state['_Data'] = {'GetActualMemorySize': self.data().GetActualMemorySize(),
                          'GetBounds': self.data().GetBounds(),
                          'GetCenter': self.data().GetCenter(),
                          'GetExtent': self.data().GetExtent(),
                          'GetNumberOfCells': self.data().GetNumberOfCells(),
                          'GetNumberOfPoints': self.data().GetNumberOfPoints(),
                          'GetOrigin': self.data().GetOrigin(),
                          'GetScalarRange': self.data().GetScalarRange(),
                          'GetSpacing': self.data().GetSpacing()}
        return pprint.pformat(state, width=400, compact=True)

    def view(self) -> vmi.View:
        """返回视图"""
        return self._View

    def setView(self, view) -> None:
        """设置视图"""
        if self._View:
            self._View.renderer().RemoveActor(self._Prop)
        self._View = view
        if self._View:
            self._View.renderer().AddActor(self._Prop)
        self.bindData()

    def updateInTime(self) -> None:
        """及时刷新视图"""
        if self._View:
            self._View.updateInTime()

    def visible(self) -> bool:
        """返回可见状态"""
        return self._Visible

    def setVisible(self, visible: bool) -> None:
        """设置可见状态"""
        self.updateInTime()
        self._Visible = visible
        self._Prop.SetVisibility(1 if visible else 0)

    def visibleToggle(self) -> None:
        """切换可见状态"""
        return self.setVisible(not self.visible())

    def pickable(self) -> bool:
        """返回可交互状态"""
        return self._Pickable

    def setPickable(self, pickable: bool) -> None:
        """设置可交互状态"""
        self.updateInTime()
        self._Pickable = pickable
        self._Prop.SetPickable(1 if self._Pickable else 0)

    def data(self) -> vtk.vtkImageData:
        """返回数据"""
        return self._Data

    def delete(self) -> None:
        """清除视图关联，在del之前调用"""
        self.updateInTime()
        image = vtk.vtkImageData()
        image.SetExtent(0, 0, 0, 0, 0, 0)
        image.AllocateScalars(vtk.VTK_SHORT, 1)
        self.setData(image)
        self.setView(None)

    def bindData(self, other=None) -> None:
        """关联数据到视图，可以关联其它对象，other = self 关联自身对象，other = None 重新关联当前对象"""
        if hasattr(other, '_Data'):
            self._BindData = other
        self._Mapper.SetInputData(self._BindData.data())
        self._Prop.SetMapper(self._Mapper)
        self.updateInTime()

    def setData(self, data) -> None:
        """设置数据，可以直接设置其它同类实例，或vtkImageData"""
        self.updateInTime()
        if hasattr(data, 'data'):
            self.data().DeepCopy(data.data())
        elif isinstance(data, self.data().__class__):
            self.data().DeepCopy(data)
        else:
            self.data().DeepCopy(self.data().__class__())
        self.bindData()

    def setColor(self, color: Dict[int, List[float]]) -> None:
        """设置颜色方案 {scalar: [red, green, blue]}"""
        self.updateInTime()
        self._Color = color
        f = vtk.vtkColorTransferFunction()
        for x in self._Color:
            r, g, b = self._Color[x]
            f.AddRGBPoint(x, r, g, b)
        self._Property.SetColor(f)

    def setOpacityScalar(self, opacity_scalar: Dict[float, float]) -> None:
        self.updateInTime()
        self._OpacityScalar = opacity_scalar
        f = vtk.vtkPiecewiseFunction()
        for x in self._OpacityScalar:
            f.AddPoint(x, self._OpacityScalar[x])
        self._Property.SetScalarOpacity(f)

    def setOpacity_Threshold(self, threshold: int = None):
        """设置不透明度方案为阈值方案，threshold以上显示，threshold以下完全透明"""
        self.setOpacityScalar({threshold - 1: 0, threshold: 1})

    def setOpacityGradient(self, opacity_gradient: Dict[float, float]) -> None:
        """设置不透明度梯度方案，没啥用"""
        self.updateInTime()
        self._OpacityGradient = opacity_gradient
        f = vtk.vtkPiecewiseFunction()
        for x in self._OpacityGradient:
            f.AddPoint(x, self._OpacityGradient[x])
        self._Property.SetGradientOpacity(f)
