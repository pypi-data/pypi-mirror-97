import vmi


def read_dicom():
    dcmdir = vmi.askDirectory()  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                return series.read()  # 读取DICOM系列为图像数据


image = read_dicom()  # 读取DICOM图像

if image is None:  # 图像无效则退出主程序
    vmi.appexit()

view = vmi.View()  # 创建视图

slice = vmi.ImageSlice(view)  # 创建图像断层
slice.setData(image)  # 载入图像
slice.setSlicePlaneOrigin_Center()  # 设置图像断层位置居中
slice.setSlicePlaneNormal_Axial()  # 设置图像断层显示横断面
slice.setColor({0: [0, 0, 1], 1: [0, 1, 1], 2: [1, 1, 0], 3: [1, 0, 0]})
slice.setColorAboveRange([1, 0, 0])
view.setCamera_FitAll()  # 重置相机适应场景大小

vmi.appexec(view)  # 执行主窗口程序
vmi.appexit()  # 清理并退出程序
