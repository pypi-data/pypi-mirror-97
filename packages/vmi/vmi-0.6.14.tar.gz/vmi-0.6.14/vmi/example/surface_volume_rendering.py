import vmi


def read_dicom():
    dcmdir = vmi.askDirectory()  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                return series.read()  # 读取DICOM系列为图像数据


def view_surface(view, image, iso_value):
    pd = vmi.imIsosurface(image, iso_value)  # 提取CT值为iso_value的等值面，面绘制三维重建
    actor = vmi.PolyActor(view)  # 面绘制显示
    actor.setData(pd)  # 载入三维重建得到的面网格模型
    view.setCamera_FitAll()  # 自动调整视图的视野范围
    return actor


def view_volume(view, image, iso_value):
    volume = vmi.ImageVolume(view)  # 体绘制显示
    volume.setData(image)  # 载入读取到的DICOM图像
    volume.setOpacityScalar({iso_value - 1: 0, iso_value: 1})  # 设置像素和透明度之间的函数关系
    view.setCamera_FitAll()  # 自动调整视图的视野范围
    return view, volume


# 导入Qt用于窗口布局
from PySide2.QtWidgets import QWidget, QHBoxLayout

image = read_dicom()  # 读取DICOM图像

if image is None:  # 图像无效则退出主程序
    vmi.appexit()

# 输入一个CT值用于等值面提取
iso_value = vmi.askInt(-1000, 200, 3000, None, 'HU')
if iso_value is None:
    vmi.appexit()

surface_view = vmi.View()  # 面绘制视图
view_surface(surface_view, image, iso_value)

volume_view = vmi.View()  # 体绘制视图
view_volume(volume_view, image, iso_value)

# 创建窗口，布局视图
widget = QWidget()
layout = QHBoxLayout(widget)
layout.addWidget(surface_view)
layout.addWidget(volume_view)

vmi.appexec(widget)  # 执行主程序
vmi.appexit()  # 退出主程序
