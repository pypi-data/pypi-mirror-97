import vmi
import numpy as np


def read_dicom():
    dcmdir = vmi.askDirectory()  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                return series.read()  # 读取DICOM系列为图像数据


def LeftButtonPressRelease(**kwargs):
    if kwargs['picked'] is button:  # 用户点击文字框
        left_top = views[0].pickPt_FocalPlane([0, 0])  # 拾取视图左上角的焦平面点
        right_top = views[0].pickPt_FocalPlane([views[0].width(), 0])  # 拾取视图右上角的焦平面点
        left_bottom = views[0].pickPt_FocalPlane([0, views[0].height()])  # 拾取视图左下角的焦平面点

        cs = views[0].cameraCS_FPlane()  # 获得相机坐标系

        xl = np.linalg.norm(left_top - right_top)  # 视图左右方向的真实尺度
        yl = np.linalg.norm(left_top - left_bottom)  # 视图上下方向的真实尺度
        zl = vmi.imSize_Vt(image, cs.axis(2))  # 图像沿视图入射方向的最大包围盒尺寸

        pt = vmi.imCenter(image) - 0.5 * zl * cs.axis(2)  # 计算图像包围盒中心到近平面投影点
        cs.setOrigin(vmi.ptOnPlane(cs.origin(), pt, cs.axis(2)))  # 将坐标系原点投影到近平面

        # 重采样混叠，背景体素值-1024，平均密度投影，忽略-200以下的体素值
        image_blend = vmi.imReslice_Blend(image, cs, [xl, yl, zl], -1024, 'mean', -200)

        blend_prop.setData(image_blend)  # 载入混叠图像
        blend_prop.setColorWindow_Soft()  # 设置软组织窗
        views[1].setCamera_FitAll()  # 自动调整视图的视野范围


image = read_dicom()  # 读取DICOM路径
if image is None:
    vmi.appexit()

iso_value = vmi.askInt(-1000, 200, 3000, None, 'HU')  # 用户输入-1000HU至3000HU范围内的一个CT值
if iso_value is None:
    vmi.appexit()

views = [vmi.View(), vmi.View()]  # 左右视图

# 创建按钮，连接事件处理函数
button = vmi.TextBox(views[1], text='混叠', pickable=True, size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])
button.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

mesh_prop = vmi.PolyActor(views[0], color=[1, 1, 0.6])  # 左视图显示模型
mesh_prop.setData(vmi.imIsosurface(image, iso_value))  # 三维重建并显示
views[0].setCamera_Coronal()  # 设置冠状位视图
views[0].setCamera_FitAll()  # 自动调整视图的视野范围

blend_prop = vmi.ImageSlice(views[1])  # 右视图显示混叠图像

# 导入Qt用于窗口布局
from PySide2.QtWidgets import QWidget, QHBoxLayout

# 创建窗口，布局视图
widget = QWidget()
layout = QHBoxLayout(widget)
layout.addWidget(views[0])
layout.addWidget(views[1])

vmi.appexec(widget)  # 执行主程序
vmi.appexit()  # 退出主程序
