from numba import jit

import vmi


def read_dicom():
    dcmdir = vmi.askDirectory()  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                return series.read()  # 读取DICOM系列为图像数据


# 路径更新函数
def update_line_cut():
    if len(plcut_pts) > 1:  # 如果路径点不少于2个
        plcut_prop.setData(vmi.ccWire(vmi.ccSegments(plcut_pts, True)))  # 构造闭合折线段
    else:
        plcut_prop.setData(None)  # 清空显示


@jit(nopython=True)  # 进阶技巧：因为python循环写入体素值的效率比C++低很多，所以采用numba多线程加速
def ary_mask(input_ary, mask_ary, threshold, target):
    """
    编辑图像数值的遍历过程

    :param input_ary: 输入图像
    :param mask_ary: 标记图像
    :param threshold: 阈值
    :param target: 编辑目标值
    :return: None
    """
    for k in range(input_ary.shape[0]):
        for j in range(input_ary.shape[1]):
            for i in range(input_ary.shape[2]):
                # 遍历所有体素，将标记范围内的体素改写为目标值
                if mask_ary[k][j][i] != 0 and threshold <= input_ary[k][j][i]:
                    input_ary[k][j][i] = target


# 编辑图像数值
def plcut_voi_image():
    cs = voi_view.cameraCS_FPlane()  # 取当前相机坐标系
    d = vmi.imSize_Vt(voi_volume.data(), cs.axis(2))  # 计算图像体数据在垂直屏幕方向的深度
    pts = [vmi.ptOnPlane(pt, vmi.imCenter(voi_volume.data()), cs.axis(2)) for pt in plcut_pts]  # 投影路径点到图像体中心平面
    pts = [pt - d * cs.axis(2) for pt in pts]  # 平移路径点到图像体最近位置，构建一个包围盒端面
    sh = vmi.ccFace(vmi.ccWire(vmi.ccSegments(pts, True)))  # 构造面单元
    sh = vmi.ccPrism(sh, cs.axis(2), 2 * d)  # 拉伸构造包围盒实体

    # 利用路径构造的包围盒实体，计算模板图像体，在路径范围内的图像值非零，在路径范围外的图像值为零
    mask = vmi.imStencil_PolyData(vmi.ccPd_Sh(sh),
                                  vmi.imOrigin(voi_volume.data()),
                                  vmi.imSpacing(voi_volume.data()),
                                  vmi.imExtent(voi_volume.data()))

    # 转换为numpy数组
    mask_ary = vmi.imArray_VTK(mask)
    voi_ary = vmi.imArray_VTK(voi_volume.data())

    # 编辑图像
    ary_mask(voi_ary, mask_ary, bone_value, target_value)

    # 转换回vtk图像更新显示
    voi_image = vmi.imVTK_Array(voi_ary, vmi.imOrigin(voi_volume.data()), vmi.imSpacing(voi_volume.data()))
    voi_volume.setData(voi_image)


# 数值框的滚轮响应函数
def on_bone_value():
    global bone_value
    bone_value = bone_value_box.value()  # 更新全局骨CT值
    voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})  # 设置体素和透明度之间的函数关系


def LeftButtonPress(**kwargs):
    if kwargs['picked'] is voi_view:
        if plcut_box.text() == '请勾画切割范围':
            pt = voi_view.pickPt_FocalPlane()  # 取第一个路径点
            plcut_pts.clear()  # 清空路径点列表
            plcut_pts.append(pt)  # 加入路径点列表
            update_line_cut()  # 更新路径显示
        return True  # 事件处理终止


def LeftButtonPressMove(**kwargs):
    global spcut_center, pelvis_cs
    if kwargs['picked'] is voi_view:
        if plcut_box.text() == '请勾画切割范围':
            pt = voi_view.pickPt_FocalPlane()  # 取当前路径点

            for path_pt in plcut_pts:  # 遍历已存在的路径点
                if (path_pt == pt).all():  # 如果发现重复
                    return  # 取点无效

            plcut_pts.append(pt)  # 添加路径点
            update_line_cut()  # 更新路径显示
        else:
            voi_view.mouseRotateFocal(**kwargs)  # 执行视图默认行为
        return True  # 事件处理终止


def LeftButtonPressMoveRelease(**kwargs):
    if kwargs['picked'] is voi_view:
        if plcut_box.text() == '请勾画切割范围':
            plcut_box.draw_text('请耐心等待')
            plcut_voi_image()
            plcut_box.draw_text('线切割')

            plcut_pts.clear()
            update_line_cut()
        return True  # 事件处理终止


def LeftButtonPressRelease(**kwargs):
    if kwargs['picked'] is plcut_box:
        if plcut_box.text() == '线切割':
            plcut_box.draw_text('请勾画切割范围')
        elif plcut_box.text() == '请勾画切割范围':
            plcut_box.draw_text('线切割')
        return True  # 事件处理终止


if __name__ == '__main__':
    image = read_dicom()  # 读取DICOM图像

    if image is None:  # 图像无效则退出主程序
        vmi.appexit()

    # 体绘制视图
    voi_view = vmi.View()
    voi_view.mouse['LeftButton']['Press'] = [LeftButtonPress]
    voi_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    voi_view.mouse['LeftButton']['PressMoveRelease'] = [LeftButtonPressMoveRelease]

    # 调整到冠状位正视
    voi_view.setCamera_Coronal()
    voi_view.setCamera_FitAll()  # 自动调整视图的视野范围

    # 骨CT值和编辑目标CT值
    bone_value, target_value = 200, -1100

    # 体绘制显示
    voi_volume = vmi.ImageVolume(voi_view)
    voi_volume.setData(image)  # 载入读取到的DICOM图像
    voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})  # 设置体素和透明度之间的函数关系

    # 骨CT数值框，调节三维显示效果
    bone_value_box = vmi.ValueBox(voi_view, value_format='骨阈值：{:.0f} HU',
                                  value_min=-1000, value=bone_value, value_max=3000,
                                  value_decimals=0, value_step=10, value_update=on_bone_value,
                                  size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)

    # 线切割路径点列表
    plcut_pts = []

    # 路径
    plcut_prop = vmi.PolyActor(voi_view, color=[1, 0.6, 0.6], line_width=3, always_on_top=True)

    # 激活按钮，切换鼠标交互
    plcut_box = vmi.TextBox(voi_view, text='线切割', size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0], pickable=True)
    plcut_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    vmi.appexec(voi_view)  # 执行主程序
    vmi.appexit()  # 退出主程序
