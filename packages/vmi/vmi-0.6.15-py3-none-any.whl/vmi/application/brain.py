import random
import gc
import numpy as np
import pydicom
import vmi
import vtk
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from numba import jit
from skimage.transform import resize
from PySide2.QtCharts import QtCharts


def clear_props(prop_list):
    prop_list = np.array(prop_list)
    print(prop_list.shape, prop_list)
    if len(prop_list.shape) == 1:
        for prop in prop_list:
            prop.setData(None)
    elif len(prop_list.shape) == 2:
        for pair in prop_list:
            for prop in pair:
                prop.setData(None)


def clear_select_props():
    clear_props([angle_1_props, angle_2_props])
    clear_props([brace_props, pipe_props])
    clear_props([angle_1_line_1, angle_1_line_2])
    clear_props([angle_2_line_1, angle_2_line_2])
    clear_props([line_props])
    angle_1_pts.clear()
    angle_2_pts.clear()
    pipe_pts.clear()
    brace_pts.clear()
    line_pts.clear()
    line_measure.setData(None)


def init_voi_view():
    clear_props(tumor_f_l_props)
    clear_props(vessel_f_l_props)
    clear_props(vessel_center_props)
    clear_props(tumor_line_props)
    clear_props(vessel_line_props)
    clear_props(angle_2_props)
    clear_props(angle_1_props)
    clear_props(line_measure)
    clear_props([angle_2_line_1, angle_2_line_2])
    clear_props([angle_1_line_1, angle_1_line_2])
    clear_props([tumor_pd, vessel_pd, tumor_center_prop])
    clear_props([pipe_cline, brace_cline])
    clear_props(brace_props)
    clear_props(pipe_props)
    tumor_f_l.clear()
    vessel_f_l.clear()
    angle_1_pts.clear()
    angle_2_pts.clear()
    pipe_pts.clear()
    brace_pts.clear()
    tumor_f_l_props.clear()
    print(tumor_f_l, vessel_f_l, angle_2_pts, pipe_pts)


def init_observe_view():
    observe_arr = vmi.imArray_VTK(original_image)
    re_observe_arr = resize(observe_arr,
                            [observe_arr.shape[0] // 4, observe_arr.shape[1] // 4, observe_arr.shape[2] // 4],
                            preserve_range=True)
    observe_arr = np.zeros(observe_arr.shape).astype('float32')
    observe_arr[0:observe_arr.shape[0] // 4,
    0: observe_arr.shape[1] // 4,
    0:observe_arr.shape[2] // 4, ] = re_observe_arr

    observe_image = vmi.imVTK_Array(re_observe_arr,
                                    origin=[0, 0, 0],
                                    spacing=vmi.imSpacing(original_image))
    pd = vmi.imIsosurface(observe_image, 200)  # 提取CT值为iso_value的等值面，面绘制三维重建
    observe_prop.setData(pd)  # 载入三维重建得到的面网格模型
    observe_view.setCamera_FitAll()  # 自动调整视图的视野范围


def _compute_size(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    v1 = np.linalg.norm(np.abs(p1 - p2))
    v2 = np.linalg.norm(np.abs(p1 - p3))
    v3 = np.linalg.norm(np.abs(p3 - p2))
    p = (v1 + v2 + v3) / 2
    s = pow(p * (p - v1) * (p - v2) * (p - v3), 1 / 2)
    print(s)
    return s


def compute_area_by_pts(pts):
    pts = np.array(pts)
    area = 0
    center = pts.sum(axis=0) / len(pts)
    print(pts)
    print(center)

    for i, j in enumerate(pts):
        if i < len(pts) - 1:
            part = _compute_size(pts[i], pts[i + 1], center)
            area += part
        elif i == len(pts) - 1:
            area += _compute_size(pts[i], pts[0], center)
    return round(area, 2)


def update_fill_ratio():
    fill_ratio = round((pow(pring_coil / 2 * (10 * 2.54), 2) * np.pi * filling_lenth) / tumor_pd_size, 4)
    voi_view_textboxes[-1].draw_text('填充率:{}%'.format(fill_ratio))


def compute_size(pd):
    triang = vtk.vtkTriangleFilter()
    triang.SetInputData(pd.data())
    triang.Update()
    triang_pd = vmi.PolyActor(voi_view, color=[0, 0, 0], visible=False, pickable=False)
    triang_pd.setData(triang.GetOutput())
    mass = vtk.vtkMassProperties()
    mass.SetInputData(triang_pd.data())
    mass.Update()
    return round(mass.GetVolume(), 2), round(mass.GetSurfaceArea(), 2)


def update_para_text_3_4():
    para_3_box.draw_text(
        '载瘤动脉参数:\n半径1:{}mm\n半径2:{}mm\n半径3:{}mm\n半径4:{}mm\n半径5:{}mm'.format(para_dict['radius_1'], para_dict['radius_2'],
                                                                           para_dict['radius_3'],
                                                                           para_dict['radius_4'],
                                                                           para_dict['radius_5']))
    para_4_box.draw_text('半径6:{}mm\n半径7:{}mm\n半径8:{}mm\n半径9:{}mm\n半径10:{}mm\n半径11:{}mm'.format(para_dict['radius_6'],
                                                                                               para_dict['radius_7'],
                                                                                               para_dict['radius_8'],
                                                                                               para_dict['radius_9'],
                                                                                               para_dict['radius_10'],
                                                                                               para_dict['radius_11']))


def update_para_text_1_2():
    para_1_box.draw_text(
        '动脉瘤参数:\n长:{}mm\n宽:{}mm\n高:{}mm\n体积:{}mm³'.format(para_dict['lenth'], para_dict['width'], para_dict['hight'],
                                                          para_dict['tumor_volum']))
    para_2_box.draw_text('\n截面积:{}.mm²\n瘤颈深度:{}.mm\n角一:{}°\n角二:{}°'.format(para_dict['tumor_area'], para_dict['depth'],
                                                                           para_dict['angle_1'], para_dict['angle_2']))


def compute_angle(angle_pts):
    print(angle_pts)
    angle_pts = np.array(angle_pts[:3])
    v1 = np.abs(angle_pts[1] - angle_pts[0])
    v2 = np.abs(angle_pts[2] - angle_pts[0])
    v3 = np.abs(angle_pts[2] - angle_pts[1])
    l1 = np.linalg.norm(v1)
    l2 = np.linalg.norm(v2)
    l3 = np.linalg.norm(v3)

    cos_angle = (pow(l3, 2) + pow(l1, 2) - pow(l2, 2)) / (2 * l1 * l3)
    angle = round((np.arccos(cos_angle) / np.pi) * 180, 2)
    print(v1, v2, v3, l1, l2, l3, cos_angle, angle)
    return angle


def build_brace():
    max_radius = np.array(radius_arr).max()
    if len(brace_pts) > 1:
        for i in range(len(brace_pts)):
            brace_props[i].setData(vmi.pdSphere(radius, brace_pts[i]))
            print(brace_pts)
        edge = vmi.ccEdge(vmi.ccBSpline_Kochanek(brace_pts))
        l = vmi.ccLength(edge)
        pts = vmi.ccUniformPts_Edge(edge, round(max(l / 0.01, 10)))  # 至少分割成两个点,每个点分十个
        brace_cline.setData(vmi.pdPolyline(pts))
        brace_cline_tube.SetInputData(brace_cline.data())

        brace_cline_tube.SetRadius(max_radius)
        brace_cline_tube.SetNumberOfSides(500)
        brace_cline_tube.Update()
        brace_cline.setData(brace_cline_tube.GetOutput())


def make_centers_on_top():
    for i in vessel_center_props:
        i.setAlwaysOnTop(True)
    tumor_center_prop.setAlwaysOnTop(True)


def build_pipe():
    if len(pipe_pts) > 1:
        for i in range(len(pipe_pts)):
            pipe_props[i].setData(vmi.pdSphere(radius, pipe_pts[i]))
        edge = vmi.ccEdge(vmi.ccBSpline_Kochanek(pipe_pts))
        l = vmi.ccLength(edge)
        pts = vmi.ccUniformPts_Edge(edge, round(max(l / 0.01, 10)))  # 至少分割成两个点,每个点分十个
        pipe_cline.setData(vmi.pdPolyline(pts))
        pipe_cline_tube.SetInputData(pipe_cline.data())
        pipe_cline_tube.SetRadius(0.3)
        pipe_cline_tube.SetNumberOfSides(500)
        pipe_cline_tube.Update()
        pipe_cline.setData(pipe_cline_tube.GetOutput())


def update_tumor_curve(index):
    global tumor_center
    radius = 0.3
    if len(tumor_f_l) >= 1:
        for i in range(len(tumor_f_l)):
            tumor_f_l_props[i][0].setData(vmi.pdSphere(radius, tumor_f_l[i][0]))

            tumor_f_l_props[i][1].setData(vmi.pdSphere(radius, tumor_f_l[i][1]))
            print('tumor_f_l[i]:', tumor_f_l[i])
            tumor_line_props[i].setData(vmi.ccWire(vmi.ccSegments(tumor_f_l[i], False)))

    if len(tumor_f_l_props) == 3:
        _cp = np.array(tumor_f_l)
        tumor_center = _cp.sum(axis=0).sum(axis=0) / 6
        tumor_center_prop.setData(vmi.pdSphere(radius, tumor_center))
    if index[0][0] == 0:
        para_dict['lenth'] = round(
            np.linalg.norm(np.abs(np.array(tumor_f_l[index[0][0]][0]) - np.array(tumor_f_l[index[0][0]][1]))), 2)
    if index[0][0] == 1:
        para_dict['width'] = round(
            np.linalg.norm(np.abs(np.array(tumor_f_l[index[0][0]][0]) - np.array(tumor_f_l[index[0][0]][1]))), 2)
    if index[0][0] == 2:
        para_dict['hight'] = round(
            np.linalg.norm(np.abs(np.array(tumor_f_l[index[0][0]][0]) - np.array(tumor_f_l[index[0][0]][1]))), 2)
    update_para_text_1_2()
    voi_view.updateInTime()


def update_vessel_curve():
    global vessel_centers
    vessel_centers = []
    if len(vessel_f_l) >= 1:
        for i in range(len(vessel_f_l)):
            center = (np.array(vessel_f_l[i][0]) + np.array(vessel_f_l[i][1])) / 2
            vessel_f_l_props[i][0].setData(vmi.pdSphere(radius, vessel_f_l[i][0]))

            vessel_f_l_props[i][1].setData(vmi.pdSphere(radius, vessel_f_l[i][1]))
            print(vessel_f_l[i])
            vessel_line_props[i].setData(vmi.ccWire(vmi.ccSegments(vessel_f_l[i], False)))
            vessel_center_props[i].setData(vmi.pdSphere(radius, center))
            vessel_centers.append(center)
    voi_view.updateInTime()


def seg_ary_mask(input_ary, mask_ary, threshold):
    threshold_ary = input_ary >= threshold
    logic_mask = mask_ary == 255
    input_ary[np.logical_not(np.logical_and(logic_mask, threshold_ary))] = threshold - 16
    return input_ary


def rebulid_image(plcut_pts, image_1, image_2):
    # q1:旋转视角是否有效
    global voi_image
    cs = voi_view.cameraCS_FPlane()
    d = vmi.imSize_Vt(voi_image, cs.axis(2)) * 2
    pts = [vmi.ptOnPlane(pt, vmi.imCenter(voi_image), cs.axis(2)) for pt in plcut_pts]
    pts = [pt - d * cs.axis(2) for pt in pts]
    sh = vmi.ccFace(vmi.ccWire(vmi.ccSegments(pts, True)))
    sh = vmi.ccPrism(sh, cs.axis(2), 2 * d)
    mask = vmi.imStencil_PolyData(vmi.ccPd_Sh(sh),
                                  vmi.imOrigin(voi_image),
                                  vmi.imSpacing(voi_image),
                                  vmi.imExtent(voi_image))
    mask_ary = vmi.imArray_VTK(mask)
    voi_ary = vmi.imArray_VTK(voi_image)
    tumor_ary = seg_ary_mask(voi_ary, mask_ary, window_level - 100)
    tumor_image = vmi.imVTK_Array(tumor_ary, vmi.imOrigin(voi_image), vmi.imSpacing(voi_image))

    fe3 = vtk.vtkFlyingEdges3D()
    fe3.SetInputData(tumor_image)
    fe3.SetValue(0, window_level + 50)
    fe3.SetComputeNormals(1)
    fe3.SetComputeGradients(0)
    fe3.SetComputeScalars(0)
    fe3.Update()

    pd = fe3.GetOutput()
    return pd


def ary_mask(input_ary, mask_ary, threshold, target):
    threshold_ary = input_ary >= threshold
    logic_mask = mask_ary == 255
    log_ary = np.logical_and(logic_mask, threshold_ary)
    input_ary[log_ary] = target


def update_line_width_cut(plcut_pts):
    if len(plcut_pts) > 1:
        plcut_prop.setData(vmi.ccWire(vmi.ccSegments(plcut_pts, True)))
    else:
        plcut_prop.setData(None)


def plcut_voi_image():
    global voi_image

    cs = voi_view.cameraCS_FPlane()
    d = vmi.imSize_Vt(voi_image, cs.axis(2)) * 4
    pts = [vmi.ptOnPlane(pt, vmi.imCenter(voi_image), cs.axis(2)) for pt in plcut_pts]

    pts = [pt - d * cs.axis(2) for pt in pts]

    sh = vmi.ccFace(vmi.ccWire(vmi.ccSegments(pts, True)))

    sh = vmi.ccPrism(sh, cs.axis(2), 2 * d)

    mask = vmi.imStencil_PolyData(vmi.ccPd_Sh(sh),
                                  vmi.imOrigin(voi_image),
                                  vmi.imSpacing(voi_image),
                                  vmi.imExtent(voi_image))
    mask_ary = vmi.imArray_VTK(mask)
    voi_ary = vmi.imArray_VTK(voi_image)
    ary_mask(voi_ary, mask_ary, threshold, back_value)
    voi_image = vmi.imVTK_Array(voi_ary, vmi.imOrigin(voi_image), vmi.imSpacing(voi_image))
    voi_volume.setData(voi_image)


def draw_standard_line():
    '''勾画标定区域，用于确定阈值'''
    pass


@jit(nopython=True)
def ary_pad(input_ary, constant):
    for k in [0, input_ary.shape[0] - 1]:
        for j in range(input_ary.shape[1]):
            for i in range(input_ary.shape[2]):
                input_ary[k][j][i] = constant
    for k in range(input_ary.shape[0]):
        for j in [0, input_ary.shape[1] - 1]:
            for i in range(input_ary.shape[2]):
                input_ary[k][j][i] = constant
    for k in range(input_ary.shape[0]):
        for j in range(input_ary.shape[1]):
            for i in [0, input_ary.shape[2] - 1]:
                input_ary[k][j][i] = constant


def init_voi(voi_center, voi_size):
    global voi_image, voi_ary, tumor_image_data, vessel_image_data
    '''裁剪图像区域'''
    tumor_image_data = vtk.vtkImageData()
    vessel_image_data = vtk.vtkImageData()
    voi_origin = voi_center - 0.5 * voi_size
    voi_cs = vmi.CS4x4(origin=voi_origin)
    voi_image = vmi.imReslice(original_image, voi_cs, voi_size, -1024)
    voi_image.SetOrigin(*list(voi_cs.origin()))
    voi_ary = vmi.imArray_VTK(voi_image)
    ary_pad(voi_ary, -1024)
    voi_image = vmi.imVTK_Array(voi_ary, [0, 0, 0], vmi.imSpacing(original_image))
    voi_volume.setData(voi_image)
    voi_volume.setOpacity_Threshold(window_level)
    voi_volume.setPickable(True)
    voi_view_textboxes[0].draw_text('阈值：{} HU'.format(window_level))
    tumor_image_data = tumor_image_data.DeepCopy(voi_image)
    vessel_image_data = vessel_image_data.DeepCopy(voi_image)
    init_observe_view()


def on_init_voi():
    '''弹出选择尺寸窗口'''
    size = vmi.askInt(1, 30, 100, suffix='mm', title='请输入目标区域尺寸')
    if size is not None:
        original_target = original_view.pickPt_Cell()
        voi_center = np.array([vmi.imCenter(original_image)[0], original_target[1], original_target[2]])
        voi_size = np.array([size, size, size])
        init_voi_view()
        init_voi(voi_center, voi_size)
        voi_view.setCamera_Coronal()
        voi_view.setCamera_FitAll()
        voi_view.setEnabled(True)
        print(gc.collect())


def read_dicom():
    dcmdir = vmi.askDirectory()  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                with pydicom.dcmread(series.filenames()[0]) as ds:
                    global patient_name
                    patient_name = ds.PatientName
                return series.read()  # 读取DICOM系列为图像数据


def LeftButtonPressMove(**kwargs):
    '''
    鼠标左键平移动作
    '''
    global tumor_center, section_pts, section_prop
    if kwargs['picked'] is original_slice:
        # 勾画标定区域
        if original_view_textboxes[1].text() == '正在勾画标定区域':
            pt = original_view.pickPt_FocalPlane()
            for path_pt in standard_pts:
                if (path_pt == pt).all():
                    return

            standard_pts.append(pt)  # 添加拾取路径点
            if len(standard_pts) > 1:

                standard_prop.setData(vmi.ccWire(vmi.ccSegments(standard_pts, True)))
            else:
                standard_prop.setData(None)
        else:
            pass

    elif kwargs['picked'] is voi_view:
        if voi_view_textboxes[1].text() == '请勾画切割范围':
            pt = voi_view.pickPt_FocalPlane()

            for path_pt in plcut_pts:
                if (path_pt == pt).all():
                    return

            plcut_pts.append(pt)  # 添加拾取路径点
            update_line_width_cut(plcut_pts)
            return True
        elif voi_view_textboxes[2].text() == '请勾画动脉瘤':
            pt = voi_view.pickPt_FocalPlane()

            for path_pt in tumor_pts:
                if (path_pt == pt).all():
                    return

            tumor_pts.append(pt)  # 添加拾取路径点
            update_line_width_cut(tumor_pts)
            return True
        elif voi_view_textboxes[3].text() == '请勾画载瘤动脉':
            pt = voi_view.pickPt_FocalPlane()

            for path_pt in vessel_pts:
                if (path_pt == pt).all():
                    return

            vessel_pts.append(pt)  # 添加拾取路径点
            update_line_width_cut(vessel_pts)
            return True



        elif voi_view_textboxes[8].text() == '请勾画截面':
            pt = voi_view.pickPt_FocalPlane()

            for path_pt in section_pts:
                if (path_pt == pt).all():
                    return

            section_pts.append(pt)  # 添加拾取路径点
            if len(section_pts) > 1:
                section_prop.setData(vmi.ccWire(vmi.ccSegments(section_pts, True)))
            else:
                section_prop.setData(None)
            return True

        else:
            voi_view.mouseRotateFocal()
            return True
    elif kwargs['picked'] in np.array(tumor_f_l_props):
        if voi_view_textboxes[4].text() == '正在测量动脉瘤':
            _cp = np.array(tumor_f_l_props)
            index = np.argwhere(_cp == kwargs['picked'])
            # print(tumor_f_l)
            tumor_f_l[index[0][0]][index[0][1]] += voi_view.pickVt_FocalPlane() / 2
            # print(tumor_f_l)
            update_tumor_curve(index)
    elif kwargs['picked'] in np.array(vessel_f_l_props):
        if voi_view_textboxes[5].text() == '正在测量载瘤动脉':
            _cp = np.array(vessel_f_l_props)
            index = np.argwhere(_cp == kwargs['picked'])
            vessel_f_l[index[0][0]][index[0][1]] += voi_view.pickVt_FocalPlane() / 2
            vessel_f_l_props[index[0][0]][index[0][1]].setData(
                vmi.pdSphere(radius, vessel_f_l[index[0][0]][index[0][1]]))

            vessel_centers[index[0][0]] = np.array(vessel_f_l[index[0][0]][0] + vessel_f_l[index[0][0]][1]) / 2
            vessel_line_props[index[0][0]].setData(
                vmi.ccWire(vmi.ccSegments([vessel_f_l[index[0][0]][0], vessel_f_l[index[0][0]][1]], False)))
            vessel_center_props[index[0][0]].setData(vmi.pdSphere(radius, vessel_centers[index[0][0]]))
    elif kwargs['picked'] in vessel_center_props:
        if voi_view_textboxes[5].text() == '正在测量载瘤动脉':
            i = vessel_center_props.index(kwargs['picked'])
            vessel_centers[i] += voi_view.pickVt_FocalPlane() / 2
            vessel_center_props[i].setData(vmi.pdSphere(radius, vessel_centers[i]))
    elif kwargs['picked'] is tumor_center_prop:
        if voi_view_textboxes[4].text() == '正在测量动脉瘤':
            tumor_center += voi_view.pickVt_FocalPlane() / 2
            tumor_center_prop.setData(vmi.pdSphere(radius, tumor_center))


def LeftButtonPress(**kwargs):
    pass


def LeftButtonPressMoveRelease(**kwargs):
    global tumor_pd, vessel_pd, tumor_pd_size, area, tumor_area
    if kwargs['picked'] is original_slice:
        # 勾画完目标区域提起鼠标更换文字
        if original_view_textboxes[1].text() == '正在勾画标定区域':
            original_view_textboxes[1].draw_text('标定区域')
        else:
            pass
    elif kwargs['picked'] is voi_view:
        if voi_view_textboxes[1].text() == '请勾画切割范围':
            voi_view_textboxes[1].draw_text('请耐心等待')
            plcut_voi_image()
            voi_view_textboxes[1].draw_text('线切割')

            plcut_pts.clear()
            update_line_width_cut(plcut_pts)

        elif voi_view_textboxes[2].text() == '请勾画动脉瘤':
            voi_view_textboxes[2].draw_text('请耐心等待')

            tumor_pd.setData(rebulid_image(tumor_pts, tumor_image_data, vessel_image_data))
            tumor_pd_size, tumor_area = compute_size(tumor_pd)
            para_dict['tumor_volum'] = tumor_pd_size
            update_para_text_1_2()
            voi_view_textboxes[2].draw_text('勾画动脉瘤')
            voi_view.setCamera_FitAll()
            tumor_pts.clear()
            update_line_width_cut(tumor_pts)
        elif voi_view_textboxes[3].text() == '请勾画载瘤动脉':
            voi_view_textboxes[3].draw_text('请耐心等待')
            vessel_pd.setData(rebulid_image(vessel_pts, vessel_image_data, vessel_image_data))
            voi_view_textboxes[3].draw_text('勾画载瘤动脉')

            vessel_pts.clear()
            update_line_width_cut(vessel_pts)
        elif voi_view_textboxes[8].text() == '请勾画截面':

            para_dict['tumor_area'] = compute_area_by_pts(section_pts)
            section_prop.setData(None)
            update_para_text_1_2()
            voi_view_textboxes[8].draw_text('截面测量')


def LeftButtonPressRelease(**kwargs):
    # print(kwargs['picked'])
    global pipe_props, pipe_pts, brace_pts, brace_props, \
        angle_1_pts, angle_1_props, angle_2_pts, angle_2_props, \
        angle_1_line_1, angle_1_line_2, angle_2_line_1, angle_2_line_2, \
        line, line_pts, line_props, radius_arr, section_pts, section_prop
    if kwargs['double'] is True:
        if kwargs['picked'] is voi_view:

            if voi_view_textboxes[4].text() == '正在测量动脉瘤':
                if len(tumor_f_l_props) < 3:
                    pt = voi_view.pickPt_FocalPlane()
                    look = voi_view.cameraVt_Look()
                    pt_f = pt - 2000 * look
                    pt_b = pt + 2000 * look
                    obb = vtk.vtkOBBTree()
                    obb.SetDataSet(tumor_pd.data())
                    obb.BuildLocator()

                    intersect_points = vtk.vtkPoints()
                    cell_id_list = vtk.vtkIdList()

                    interseced = obb.IntersectWithLine(pt_f, pt_b, intersect_points, cell_id_list)
                    first_pt, end_pt = [0, 0, 0], [0, 0, 0]
                    if interseced:
                        intersect_points.GetPoint(0, first_pt)
                        num = intersect_points.GetNumberOfPoints()
                        if num >= 2:
                            intersect_points.GetPoint(num - 1, end_pt)
                    if first_pt != [0, 0, 0] and end_pt != [0, 0, 0]:
                        tumor_prop_f = vmi.PolyActor(voi_view, color=[0.4, 0.4, 1], pickable=True)
                        # tumor_prop_f.setAlwaysOnTop(True)
                        tumor_prop_f.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
                        tumor_prop_f.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
                        tumor_prop_b = vmi.PolyActor(voi_view, color=[0.4, 0.4, 1], pickable=True)
                        # tumor_prop_b.setAlwaysOnTop(True)
                        tumor_prop_b.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
                        tumor_prop_b.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
                        tumor_line_prop = vmi.PolyActor(voi_view, color=[0.4, 0.4, 1], line_width=3, pickable=False)
                        tumor_f_l.append([first_pt, end_pt])
                        props_f_l = [tumor_prop_f, tumor_prop_b]
                        tumor_f_l_props.append(props_f_l)
                        tumor_line_props.append(tumor_line_prop)
                        update_tumor_curve([[5, 5]])
                        if len(tumor_f_l) == 1:
                            para_dict['lenth'] = round(
                                np.linalg.norm(np.abs(np.array(tumor_f_l[-1][0]) - np.array(tumor_f_l[-1][1]))), 2)
                        elif len(tumor_f_l) == 2:
                            para_dict['width'] = round(
                                np.linalg.norm(np.abs(np.array(tumor_f_l[-1][0]) - np.array(tumor_f_l[-1][1]))), 2)
                        elif len(tumor_f_l) == 3:
                            para_dict['hight'] = round(
                                np.linalg.norm(np.abs(np.array(tumor_f_l[-1][0]) - np.array(tumor_f_l[-1][1]))), 2)
                        update_para_text_1_2()
                    return True
            elif voi_view_textboxes[5].text() == '正在测量载瘤动脉':
                pt = voi_view.pickPt_FocalPlane()
                look = voi_view.cameraVt_Look()
                pt_f = pt - 2000 * look
                pt_b = pt + 2000 * look
                obb = vtk.vtkOBBTree()
                obb.SetDataSet(vessel_pd.data())
                obb.BuildLocator()

                intersect_points = vtk.vtkPoints()
                cell_id_list = vtk.vtkIdList()

                interseced = obb.IntersectWithLine(pt_f, pt_b, intersect_points, cell_id_list)
                first_pt, end_pt = [0, 0, 0], [0, 0, 0]
                if interseced:
                    intersect_points.GetPoint(0, first_pt)
                    num = intersect_points.GetNumberOfPoints()
                    if num >= 2:
                        intersect_points.GetPoint(num - 1, end_pt)
                if first_pt != [0, 0, 0] and end_pt != [0, 0, 0]:
                    vessel_prop_f = vmi.PolyActor(voi_view, color=[1, 0.8, 0.8], pickable=True)
                    # vessel_prop_f.setAlwaysOnTop(True)
                    vessel_prop_f.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
                    vessel_prop_f.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

                    vessel_prop_b = vmi.PolyActor(voi_view, color=[1, 0.8, 0.8], pickable=True)
                    # vessel_prop_b.setAlwaysOnTop(True)
                    vessel_prop_b.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
                    vessel_prop_b.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

                    vessel_line_prop = vmi.PolyActor(voi_view, color=[1, 0.8, 0.8], line_width=3, pickable=False)
                    vessel_line_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
                    vessel_line_prop.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

                    vessel_center_prop = vmi.PolyActor(voi_view, color=[1, 0.2, 0.2], pickable=True)
                    # vessel_center_prop.setAlwaysOnTop(True)
                    vessel_center_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
                    vessel_center_prop.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
                    vessel_center_prop.mouse['NoButton']['Wheel'] = NoButtonWheel

                    vessel_f_l.append([first_pt, end_pt])
                    props_f_l = []  # 一对表面点
                    props_f_l.append(vessel_prop_f)
                    props_f_l.append(vessel_prop_b)
                    vessel_f_l_props.append(props_f_l)  # 表面props列表[[p1,p2]]
                    vessel_line_props.append(vessel_line_prop)  # 表面两点连线prop列表
                    vessel_center_props.append(vessel_center_prop)
                    update_vessel_curve()
                    update_para_text_3_4()
                return True


    # 勾画标定区域
    elif kwargs['picked'] is original_view_textboxes[1]:
        standard_prop.setData(None)
        standard_pts.clear()
        if original_view_textboxes[1].text() == '标定区域':
            original_view_textboxes[1].draw_text('正在勾画标定区域')
            return True
        elif original_view_textboxes[1].text() == '正在勾画标定区域':
            original_view_textboxes[1].draw_text('标定区域')
            return True
    # 线切割按钮
    elif kwargs['picked'] is voi_view_textboxes[1]:
        if voi_view_textboxes[1].text() == '线切割':
            voi_view_textboxes[1].draw_text('请勾画切割范围')
            voi_view_textboxes[2].draw_text('勾画动脉瘤')
            voi_view_textboxes[3].draw_text('勾画载瘤动脉')
            return True
        elif voi_view_textboxes[1].text() == '请勾画切割范围':
            voi_view_textboxes[1].draw_text('线切割')
            return True
    # 勾画动脉瘤
    elif kwargs['picked'] is voi_view_textboxes[2]:
        if voi_view_textboxes[2].text() == '勾画动脉瘤':
            voi_view_textboxes[2].draw_text('请勾画动脉瘤')
            voi_view_textboxes[1].draw_text('线切割')
            voi_view_textboxes[3].draw_text('勾画载瘤动脉')
            return True
        elif voi_view_textboxes[2].text() == '请勾画动脉瘤':
            voi_view_textboxes[2].draw_text('勾画动脉瘤')
            return True
    # 勾画载瘤动脉
    elif kwargs['picked'] is voi_view_textboxes[3]:
        if voi_view_textboxes[3].text() == '勾画载瘤动脉':
            voi_view_textboxes[3].draw_text('请勾画载瘤动脉')
            voi_view_textboxes[1].draw_text('线切割')
            voi_view_textboxes[2].draw_text('勾画动脉瘤')
            return True
        elif voi_view_textboxes[3].text() == '请勾画载瘤动脉':
            voi_view_textboxes[3].draw_text('勾画载瘤动脉')
            return True
    # 测量动脉瘤
    elif kwargs['picked'] is voi_view_textboxes[4]:
        if voi_view_textboxes[4].text() == '测量动脉瘤':
            voi_view_textboxes[4].draw_text('正在测量动脉瘤')
            voi_view_textboxes[5].draw_text('测量载瘤动脉')
        elif voi_view_textboxes[4].text() == '正在测量动脉瘤':
            voi_view_textboxes[4].draw_text('测量动脉瘤')

        return True
    # 测量载瘤动脉
    elif kwargs['picked'] is voi_view_textboxes[5]:
        if voi_view_textboxes[5].text() == '测量载瘤动脉':
            voi_view_textboxes[5].draw_text('正在测量载瘤动脉')
            voi_view_textboxes[4].draw_text('测量动脉瘤')
            return True
        elif voi_view_textboxes[5].text() == '正在测量载瘤动脉':
            for i, f_l in enumerate(vessel_f_l):
                l = round(np.linalg.norm(abs(np.array(f_l[0]) - np.array(f_l[1]))) / 2, 2)
                para_dict['radius_' + str(i + 1)] = l
                radius_arr.append(l)

            print(para_dict)
            update_para_text_3_4()
            voi_view_textboxes[5].draw_text('测量载瘤动脉')

        return True
    # 选择导管路径
    elif kwargs['picked'] is voi_view_textboxes[6]:
        if voi_view_textboxes[6].text() == '路径规划':
            clear_select_props()
            pipe_pts, pipe_props = [], []
            voi_view_textboxes[6].draw_text('选择导管路径')
            voi_view_textboxes[7].draw_text('支撑设计')
            voi_view_textboxes[10].draw_text('选择角一')
            voi_view_textboxes[11].draw_text('选择角二')
            make_centers_on_top()
            return True
        elif voi_view_textboxes[6].text() == '选择导管路径':
            print(22222)
            voi_view_textboxes[6].draw_text('正在生成导管路径...')
            # 生成导管模型

            build_pipe()
            voi_view_textboxes[6].draw_text('路径规划')
            clear_props(pipe_props)
            pipe_props.clear()
            return True
    # 选择支撑路径
    elif kwargs['picked'] is voi_view_textboxes[7]:
        if voi_view_textboxes[7].text() == '支撑设计':
            clear_select_props()

            brace_pts, brace_props = [], []
            voi_view_textboxes[7].draw_text('选择支撑路径')
            voi_view_textboxes[6].draw_text('路径规划')
            voi_view_textboxes[10].draw_text('选择角一')
            voi_view_textboxes[11].draw_text('选择角二')
            make_centers_on_top()
            return True
        elif voi_view_textboxes[7].text() == '选择支撑路径':
            print(22222)
            voi_view_textboxes[7].draw_text('正在生成支撑...')
            # 生成支撑模型
            build_brace()
            voi_view_textboxes[7].draw_text('支撑设计')
            clear_props(brace_props)
            brace_props.clear()
        return True
    elif kwargs['picked'] is voi_view_textboxes[8]:
        if voi_view_textboxes[8].text() == '截面测量':
            clear_select_props()

            section_pts = []

            voi_view_textboxes[10].draw_text('选择角一')
            voi_view_textboxes[6].draw_text('路径规划')
            voi_view_textboxes[7].draw_text('支撑设计')
            voi_view_textboxes[8].draw_text('请勾画截面')
            voi_view_textboxes[9].draw_text('长度测量')
            voi_view_textboxes[11].draw_text('选择角二')
        elif voi_view_textboxes[8].text() == '请勾画截面':
            voi_view_textboxes[8].draw_text('截面测量')
        return True
    elif kwargs['picked'] is voi_view_textboxes[9]:
        if voi_view_textboxes[9].text() == '长度测量':
            clear_select_props()

            line, line_pts, line_props = 0, [], []
            make_centers_on_top()
            voi_view_textboxes[10].draw_text('选择角一')
            voi_view_textboxes[6].draw_text('路径规划')
            voi_view_textboxes[7].draw_text('支撑设计')
            voi_view_textboxes[8].draw_text('截面测量')
            voi_view_textboxes[9].draw_text('任选两点测量长度')
            voi_view_textboxes[11].draw_text('选择角二')
        elif voi_view_textboxes[9].text() == '任选两点测量长度':
            voi_view_textboxes[9].draw_text('长度测量')
            clear_props(line_props)
        return True
    elif kwargs['picked'] is voi_view_textboxes[10]:
        if voi_view_textboxes[10].text() == '选择角一':
            clear_select_props()

            angle_1_pts, angle_1_props = [], []
            voi_view_textboxes[10].draw_text('选择角一顶点')
            voi_view_textboxes[6].draw_text('路径规划')
            voi_view_textboxes[7].draw_text('支撑设计')
            voi_view_textboxes[8].draw_text('截面测量')
            voi_view_textboxes[9].draw_text('长度测量')
            voi_view_textboxes[11].draw_text('选择角二')
            make_centers_on_top()
        elif voi_view_textboxes[10].text() == '选择角一顶点':
            voi_view_textboxes[10].draw_text('正在计算角一...')
            # 生成支撑模型
            if len(angle_1_pts) == 3:
                angle_1 = compute_angle(angle_1_pts)
                para_dict['angle_1'] = angle_1
                update_para_text_1_2()
            voi_view_textboxes[10].draw_text('选择角一')
            clear_props(angle_1_props)
            clear_props([angle_1_line_1, angle_1_line_2])

        return True
    elif kwargs['picked'] is voi_view_textboxes[11]:
        if voi_view_textboxes[11].text() == '选择角二':
            clear_select_props()
            angle_2_pts, angle_2_props = [], []
            voi_view_textboxes[11].draw_text('选择角二顶点')
            voi_view_textboxes[6].draw_text('路径规划')
            voi_view_textboxes[7].draw_text('支撑设计')
            voi_view_textboxes[8].draw_text('截面测量')
            voi_view_textboxes[9].draw_text('长度测量')
            voi_view_textboxes[10].draw_text('选择角一')
            make_centers_on_top()
            return True
        if voi_view_textboxes[11].text() == '选择角二顶点':
            voi_view_textboxes[11].draw_text('正在计算角二...')
            # 生成支撑模型
            if len(angle_2_pts) == 3:
                angle_2 = compute_angle(angle_2_pts)
                para_dict['angle_2'] = angle_2
                update_para_text_1_2()
            voi_view_textboxes[11].draw_text('选择角二')
            clear_props(angle_2_props)
            clear_props([angle_2_line_1, angle_2_line_2])
            return True


    # 隐藏体数据
    elif kwargs['picked'] is voi_view_textboxes[12]:
        if voi_view_textboxes[12].text() == '隐藏整体数据':
            voi_volume.setVisible(False)
            voi_view_textboxes[12].draw_text('显示整体数据')
            return True
        else:
            voi_volume.setVisible(True)
            voi_view_textboxes[12].draw_text('隐藏整体数据')
            return True
    # 隐藏动脉瘤
    elif kwargs['picked'] is voi_view_textboxes[13]:
        if voi_view_textboxes[13].text() == '隐藏动脉瘤':
            tumor_pd.setVisible(False)
            voi_view_textboxes[13].draw_text('显示动脉瘤')
            return True

        else:
            tumor_pd.setVisible(True)
            voi_view_textboxes[13].draw_text('隐藏动脉瘤')

            return True

    # 隐藏载瘤动脉
    elif kwargs['picked'] is voi_view_textboxes[14]:
        if voi_view_textboxes[14].text() == '隐藏载瘤动脉':
            vessel_pd.setVisible(False)
            voi_view_textboxes[14].draw_text('显示载瘤动脉')
            return True

        else:
            vessel_pd.setVisible(True)
            voi_view_textboxes[14].draw_text('隐藏载瘤动脉')
            return True

    # 隐藏表面点
    elif kwargs['picked'] is voi_view_textboxes[15]:
        if voi_view_textboxes[15].text() == '隐藏表面点':
            for tumor_prop_f_l in tumor_f_l_props:
                for j in tumor_prop_f_l:
                    j.setVisible(False)
            for tumor_line in tumor_line_props:
                tumor_line.setVisible(False)
            for vessel_prop_f_l in vessel_f_l_props:
                for j in vessel_prop_f_l:
                    j.setVisible(False)
            for vessel_line in vessel_line_props:
                vessel_line.setVisible(False)
            voi_view_textboxes[15].draw_text('显示表面点')


        elif voi_view_textboxes[15].text() == '显示表面点':
            for tumor_prop_f_l in tumor_f_l_props:
                for j in tumor_prop_f_l:
                    j.setVisible(True)
            for tumor_line in tumor_line_props:
                tumor_line.setVisible(True)
            for vessel_prop_f_l in vessel_f_l_props:
                for j in vessel_prop_f_l:
                    j.setVisible(True)
            for vessel_line in vessel_line_props:
                vessel_line.setVisible(True)
            voi_view_textboxes[15].draw_text('隐藏表面点')
        return True
    elif kwargs['picked'] is voi_view_textboxes[16]:
        if voi_view_textboxes[16].text() == '隐藏导管路径':
            pipe_cline.setVisible(False)
            voi_view_textboxes[16].draw_text('显示导管路径')
        elif voi_view_textboxes[16].text() == '显示导管路径':
            pipe_cline.setVisible(True)
            voi_view_textboxes[16].draw_text('隐藏导管路径')
        return True
    elif kwargs['picked'] is voi_view_textboxes[17]:
        if voi_view_textboxes[17].text() == '隐藏支撑':
            brace_cline.setVisible(False)
            voi_view_textboxes[17].draw_text('显示支撑')
        elif voi_view_textboxes[17].text() == '显示支撑':
            brace_cline.setVisible(True)
            voi_view_textboxes[17].draw_text('隐藏支撑')
        return True
    # 选择路径，添加绿色的点实时刷新，点生成路径不显示
    if voi_view_textboxes[6].text() == '选择导管路径':
        if kwargs['picked'] in vessel_center_props:
            i = vessel_center_props.index(kwargs['picked'])
            print(vessel_centers[i], vessel_centers)
            if np.array(vessel_centers[i]) not in np.array(pipe_pts):
                pipe_pts.append(vessel_centers[i])
                pipe_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                pipe_props.append(pipe_prop)
                pipe_props[-1].setData(vmi.pdSphere(radius, vessel_centers[i]))
            return True
        elif kwargs['picked'] is tumor_center_prop:
            if np.array(tumor_center) not in np.array(pipe_pts):
                pipe_pts.append(tumor_center)
                pipe_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                pipe_props.append(pipe_prop)
                pipe_props[-1].setData(vmi.pdSphere(radius, tumor_center))
            return True
    if voi_view_textboxes[7].text() == '选择支撑路径':
        if kwargs['picked'] in vessel_center_props:
            i = vessel_center_props.index(kwargs['picked'])
            # print(vessel_centers[i], vessel_centers)
            if np.array(vessel_centers[i]) not in np.array(brace_pts):
                brace_pts.append(vessel_centers[i])
                brace_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                brace_props.append(brace_prop)
                brace_props[-1].setData(vmi.pdSphere(radius, vessel_centers[i]))
        elif kwargs['picked'] is tumor_center_prop:
            if np.array(tumor_center) not in np.array(brace_pts):
                brace_pts.append(tumor_center)
                brace_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                brace_props.append(brace_prop)
                brace_props[-1].setData(vmi.pdSphere(radius, tumor_center))
        return True
    if voi_view_textboxes[9].text() == '任选两点测量长度':
        print('line_pts', line_pts)
        if len(line_pts) < 2:
            print(kwargs['picked'])
            if kwargs['picked'] in vessel_center_props:
                print(11111)
                i = vessel_center_props.index(kwargs['picked'])
                # print(vessel_centers[i], vessel_centers)
                if np.array(vessel_centers[i]) not in np.array(line_pts):
                    line_pts.append(vessel_centers[i])
                    line_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                    line_props.append(line_prop)
                    line_props[-1].setData(vmi.pdSphere(radius, vessel_centers[i]))
            elif kwargs['picked'] is tumor_center_prop:
                if np.array(tumor_center) not in np.array(line_pts):
                    line_pts.append(tumor_center)
                    line_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                    line_props.append(line_prop)
                    line_props[-1].setData(vmi.pdSphere(radius, tumor_center))
        if len(line_pts) == 2:
            print(line_pts)
            line_measure.setData(vmi.ccWire(vmi.ccSegments(np.array(line_pts), False)))
            line = round(np.linalg.norm(np.abs(np.array(line_pts[0]) - np.array(line_pts[1]))), 2)
            para_dict['depth'] = line
            update_para_text_1_2()
        return True

    if voi_view_textboxes[10].text() == '选择角一顶点':
        print('angle_1_pts', angle_1_pts)

        if len(angle_1_pts) < 3:

            if kwargs['picked'] in vessel_center_props:
                i = vessel_center_props.index(kwargs['picked'])
                if np.array(vessel_centers[i]) not in np.array(angle_1_pts):
                    angle_1_pts.append(vessel_centers[i])
                    angle_1_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                    angle_1_props.append(angle_1_prop)
                    angle_1_props[-1].setData(vmi.pdSphere(radius, vessel_centers[i]))
                    print(111)
            elif kwargs['picked'] is tumor_center_prop:
                if np.array(tumor_center) not in np.array(angle_1_pts):
                    angle_1_pts.append(tumor_center)
                    angle_1_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                    angle_1_props.append(angle_1_prop)
                    angle_1_props[-1].setData(vmi.pdSphere(radius, tumor_center))
                    print(222)
        if len(angle_1_pts) == 2:
            # print('angle_1_pts:', angle_1_pts)
            angle_1_line_1 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)
            angle_1_line_1.setData(vmi.ccWire(vmi.ccSegments(angle_1_pts, False)))
            print(333, angle_1_line_1)
        if len(angle_1_pts) == 3:
            # print('angle_1_pts_2:', angle_1_pts)

            angle_1_line_2 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)
            angle_1_line_2.setData(vmi.ccWire(vmi.ccSegments(angle_1_pts[1:3], False)))

        return True
    if voi_view_textboxes[11].text() == '选择角二顶点':
        print('angle_2_pts', angle_2_pts)

        if len(angle_2_pts) < 3:

            if kwargs['picked'] in vessel_center_props:
                i = vessel_center_props.index(kwargs['picked'])
                if np.array(vessel_centers[i]) not in np.array(angle_2_pts):
                    angle_2_pts.append(vessel_centers[i])
                    angle_2_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                    angle_2_props.append(angle_2_prop)
                    angle_2_props[-1].setData(vmi.pdSphere(radius, vessel_centers[i]))
                    print(111)
            elif kwargs['picked'] is tumor_center_prop:
                if np.array(tumor_center) not in np.array(angle_2_pts):
                    angle_2_pts.append(tumor_center)
                    angle_2_prop = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], pickable=True, always_on_top=True)
                    angle_2_props.append(angle_2_prop)
                    angle_2_props[-1].setData(vmi.pdSphere(radius, tumor_center))
                    print(222)
        if len(angle_2_pts) == 2:
            # print('angle_2_pts:', angle_2_pts)
            angle_2_line_1 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)
            angle_2_line_1.setData(vmi.ccWire(vmi.ccSegments(angle_2_pts, False)))
            print(333, angle_2_line_1)
        if len(angle_2_pts) == 3:
            # print('angle_2_pts_2:', angle_2_pts)

            angle_2_line_2 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)
            angle_2_line_2.setData(vmi.ccWire(vmi.ccSegments(angle_2_pts[1:3], False)))
            print(444, angle_2_line_2)

        return True


def NoButtonWheel(**kwargs):
    global window_level, window_width, filling_lenth, pring_coil
    # 修改窗位
    if kwargs['picked'] is original_view_textboxes[2]:
        window_level = min(max(window_level + 25 * kwargs['delta'], -1000), 3000)
        original_slice.setColorWindowLevel(window_level)
        original_view_textboxes[2].draw_text('窗位：{}'.format(window_level))
        return True
    # 修改窗宽
    elif kwargs['picked'] is original_view_textboxes[3]:
        window_width = min(max(window_width + 25 * kwargs['delta'], 0), 3000)
        original_slice.setColorWindowWidth(window_width)
        original_view_textboxes[3].draw_text('窗宽：{}'.format(window_width))
        return True
    elif kwargs['picked'] is voi_view_textboxes[-3]:
        pring_coil = round(min(max(pring_coil + 0.0001 * kwargs['delta'], 0), 3000), 5)
        voi_view_textboxes[-3].draw_text('弹簧圈直径:{}in'.format(pring_coil))
        update_fill_ratio()
    elif kwargs['picked'] is voi_view_textboxes[-2]:
        filling_lenth = min(max(filling_lenth + 1 * kwargs['delta'], 0), 3000)
        voi_view_textboxes[-2].draw_text('填充长度:{}mm'.format(filling_lenth))
        update_fill_ratio()


class Main(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)
        brush = QBrush(QColor(255, 255, 255, 255))
        palette = QPalette()
        desktop = QApplication.desktop()
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.screenWidth = desktop.width()
        self.screenHeight = desktop.height()
        self.setPalette(palette)
        self.setWidgetResizable(False)

    def closeEvent(self, ev: QCloseEvent):
        ev.accept() if vmi.askYesNo('退出程序？') else ev.ignore()

    # vtk.vtkKdTreePointLocator


if __name__ == '__main__':
    patient_name = str()
    original_image = read_dicom()  # 读取DICOM路径
    if original_image is None:
        vmi.appexit()
    radius = 0.3
    radius_arr = []
    pring_coil = 0.0108
    filling_lenth = 0
    fill_ratio = 0

    color_dict = {'标定线': [0.2, 0.2, 1],
                  '线切割': [0.4, 0.4, 0.4],
                  '动脉瘤': [1, 0.4, 0.4],

                  '载瘤动脉': [0.4, 1, 0.4],

                  '路径点': [1, 0.2, 1],

                  '路径线': [0., 0.2, 1],

                  '角1': [0.2, 0.2, 1],
                  '角2': [0.2, 0.2, 1],
                  }
    para_dict = {'lenth': 0.0, 'width': 0.0, 'hight': 0.0, 'tumor_volum': 0.0, 'tumor_area': 0.0, 'depth': 0.0,
                 'angle_1': 0.0, 'angle_2': 0.0, 'radius_1': 0.0, 'radius_2': 0.0, 'radius_3': 0.0, 'radius_4': 0.0,
                 'radius_5': 0.0, 'radius_6': 0.0, 'radius_7': 0.0, 'radius_8': 0.0, 'radius_9': 0.0, 'radius_10': 0.0,
                 'radius_11': 0.0}
    window_level = 400
    window_width = 1000
    original_view = vmi.View()
    original_slice = vmi.ImageSlice(original_view)  # 断层显示
    original_slice.setData(original_image)  # 载入读取到的DICOM图像
    original_slice.setColorWindow_Bone()
    original_slice.setSlicePlaneOrigin_Center()
    original_slice.setSlicePlaneNormal_Coronal()
    original_view.setCamera_Coronal()
    original_view.setCamera_FitAll()

    original_slice_menu = vmi.Menu()
    original_slice_menu.menu.addAction('定位目标区域').triggered.connect(on_init_voi)
    original_slice_menu.menu.addSeparator()
    original_slice_menu.menu.addMenu(original_slice.menu)
    original_slice.mouse['RightButton']['PressRelease'] = [original_slice_menu.menuexec]
    original_slice.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    original_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    original_view.mouse['LeftButton']['PressMoveRelease'] = [LeftButtonPressMoveRelease]

    original_view_text = ['姓名：{}', '标定区域', '窗宽:{}', '窗位:{}']
    original_view_text_format = [patient_name, '', window_level, window_width]
    original_view_textboxes = []
    for i, text in enumerate(original_view_text):
        original_view_textboxes.append(vmi.TextBox(original_view, text=text.format(original_view_text_format[i]),
                                                   size=[0.24, 0.04], pos=[0, (i + 1) * 0.04], anchor=[0, 0],
                                                   pickable=True))
    # 标定目标区域

    standard_pts = []
    standard_prop = vmi.PolyActor(original_view, color=[1, 0.4, 0.4], line_width=3)
    standard_prop.setAlwaysOnTop(True)
    original_view_textboxes[1].mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    # 调整窗宽窗位
    original_view_textboxes[2].mouse['NoButton']['Wheel'] = [NoButtonWheel]
    original_view_textboxes[3].mouse['NoButton']['Wheel'] = [NoButtonWheel]

    voi_view = vmi.View()
    voi_view.mouse['LeftButton']['Press'] = [LeftButtonPress]
    voi_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    voi_view.mouse['LeftButton']['PressMoveRelease'] = [LeftButtonPressMoveRelease]
    voi_view.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    threshold, back_value = window_level, -1024

    voi_image = vtk.vtkImageData()
    voi_volume = vmi.ImageVolume(voi_view, pickable=True)
    voi_volume.setOpacity_Threshold(threshold)
    voi_volume.setColor({threshold: [1, 0.4, 0.4]})

    voi_view_textboxes = [vmi.TextBox(voi_view, text='阈值：{} HU'.format(threshold),
                                      size=[0.24, 0.04], pos=[0, 0.04], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='线切割'.format(threshold),
                                      size=[0.24, 0.04], pos=[0, 0.1], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='勾画动脉瘤'.format(threshold),
                                      size=[0.12, 0.04], pos=[0, 0.16], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='勾画载瘤动脉'.format(threshold),
                                      size=[0.12, 0.04], pos=[0.12, 0.16], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='测量动脉瘤'.format(threshold),
                                      size=[0.12, 0.04], pos=[0, 0.22], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='测量载瘤动脉'.format(threshold),
                                      size=[0.12, 0.04], pos=[0.12, 0.22], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='路径规划'.format(threshold),
                                      size=[0.12, 0.04], pos=[0, 0.28], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='支撑设计'.format(threshold),
                                      size=[0.12, 0.04], pos=[0.12, 0.28], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='截面测量',
                                      size=[0.12, 0.04], pos=[0, 0.34], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='长度测量',
                                      size=[0.12, 0.04], pos=[0.12, 0.34], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='选择角一',
                                      size=[0.12, 0.04], pos=[0, 0.4], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='选择角二',
                                      size=[0.12, 0.04], pos=[0.12, 0.4], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='隐藏整体数据',
                                      size=[0.12, 0.04], pos=[0, 0.46], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='隐藏动脉瘤',
                                      size=[0.12, 0.04], pos=[0.12, 0.46], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='隐藏载瘤动脉',
                                      size=[0.12, 0.04], pos=[0, 0.52], anchor=[0, 0],
                                      pickable=True),

                          vmi.TextBox(voi_view, text='隐藏表面点',
                                      size=[0.12, 0.04], pos=[0.12, 0.52], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='隐藏导管路径',
                                      size=[0.12, 0.04], pos=[0, 0.58], anchor=[0, 0],
                                      pickable=True),
                          vmi.TextBox(voi_view, text='隐藏支撑',
                                      size=[0.12, 0.04], pos=[0.12, 0.58], anchor=[0, 0],
                                      pickable=True,
                                      ),
                          vmi.TextBox(voi_view, text='弹簧圈一'.format(pring_coil),
                                      size=[0.24, 0.04], pos=[0, 0.64], anchor=[0, 0],
                                      pickable=True,
                                      ),
                          vmi.TextBox(voi_view, text='填充长度:{}mm'.format(filling_lenth),
                                      size=[0.24, 0.04], pos=[0.0, 0.70], anchor=[0, 0],
                                      pickable=True,
                                      ),
                          vmi.TextBox(voi_view, text='填充率:{}%'.format(fill_ratio),
                                      size=[0.24, 0.04], pos=[0.0, 0.76], anchor=[0, 0],
                                      pickable=True,
                                      ),
                          ]
    for text_box in voi_view_textboxes:
        text_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    voi_view_textboxes[-3].mouse['NoButton']['Wheel'] = [NoButtonWheel]
    voi_view_textboxes[-2].mouse['NoButton']['Wheel'] = [NoButtonWheel]
    voi_view_textboxes[-1].mouse['NoButton']['Wheel'] = [NoButtonWheel]

    para_1_box = vmi.TextBox(voi_view, text='动脉瘤参数:\n长:{}mm\n宽:{}mm\n高:{}mm\n体积:{}mm³'.format(0.00, 0.00, 0.00, 0.00),
                             size=[0.18, 0.15], pos=[0.26, 0.04], anchor=[0, 0])
    para_2_box = vmi.TextBox(voi_view, text='\n截面积:{}.mm²\n瘤颈深度:{}.mm\n角一:{}°\n角二:{}°'.format(0.00, 0.00, 0.00, 0.00),
                             size=[0.18, 0.15], pos=[0.43, 0.04], anchor=[0, 0])
    para_3_box = vmi.TextBox(voi_view,
                             text='载瘤动脉参数:\n半径1:{}mm\n半径2:{}mm\n半径3:{}mm\n半径4:{}mm\n半径5:{}mm'.format(0.00, 0.00, 0.00,
                                                                                                     0.00, 0.00),
                             size=[0.18, 0.15], pos=[0.62, 0.04], anchor=[0, 0])
    para_4_box = vmi.TextBox(voi_view,
                             text='半径6:{}mm\n半径7:{}mm\n半径8:{}mm\n半径9:{}mm\n半径10:{}mm\n半径11:{}mm'.format(0.00, 0.00,
                                                                                                        0.00, 0.00,
                                                                                                        0.00, 0.00),
                             size=[0.18, 0.15], pos=[0.79, 0.04], anchor=[0, 0])
    # tumor pd ,vessel_pd
    tumor_pd = vmi.PolyActor(voi_view, repres='wireframe', color=[0.8, 0.8, 1])  # 面绘制显示
    vessel_pd = vmi.PolyActor(voi_view, repres='wireframe', color=[1, 0.8, 0.8])  # 面绘制显示
    plcut_pts = []
    plcut_prop = vmi.PolyActor(voi_view, color=[1, 0.4, 0.4], line_width=3)
    plcut_prop.setAlwaysOnTop(True)
    tumor_pts = []
    tumor_cline_prop = vmi.PolyActor(voi_view, color=[1, 0.4, 0.4], line_width=3)
    tumor_cline_prop.setAlwaysOnTop(True)
    vessel_pts = []
    vessel_cline_prop = vmi.PolyActor(voi_view, color=[1, 0.4, 0.4], line_width=3)
    vessel_cline_prop.setAlwaysOnTop(True)
    # 中心点和中心线 载瘤动脉和动脉瘤
    vessel_f_l, vessel_f_l_props, vessel_line_props, vessel_centers, vessel_center_props, radius_arr = [], [], [], [], [], []

    tumor_f_l, tumor_f_l_props, tumor_line_props = [], [], []

    tumor_center_prop = vmi.PolyActor(voi_view, color=[0.8, 0.8, 1], pickable=True)
    tumor_center_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    tumor_center_prop.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    pipe_pts, pipe_props = [], []
    pipe_cline = vmi.PolyActor(voi_view, color=[0.7, 0.7, 0.7], line_width=3)
    pipe_cline_tube = vtk.vtkTubeFilter()

    brace_pts, brace_props = [], []
    brace_cline = vmi.PolyActor(voi_view, color=[0.9, 0.9, 0.9], line_width=3)
    brace_cline_tube = vtk.vtkTubeFilter()
    # line, line_pts, line_props = 0, [], []

    angle_1, angle_1_pts, angle_1_props = 0, [], []
    angle_1_line_1 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)
    angle_1_line_2 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)

    angle_2, angle_2_pts, angle_2_props = 0, [], []
    angle_2_line_1 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)
    angle_2_line_2 = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)

    section_pts = []
    section_prop = vmi.PolyActor(voi_view, color=[1, 0.4, 0.4], line_width=3, always_on_top=True)
    line_props, line_pts = [], []
    line_measure = vmi.PolyActor(voi_view, color=[0.2, 1, 0.2], line_width=3, always_on_top=True)

    observe_view = vmi.View()
    observe_view.bindCamera([voi_view])
    observe_prop = vmi.PolyActor(observe_view)  # 面绘制显示

    # observe_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout_0 = QVBoxLayout(widget)
    layout_2 = QVBoxLayout(widget)
    main = Main()

    print(main.screenWidth, main.screenHeight)
    # voi_view.setFixedHeight(int(main.screenHeight*0.9))
    # voi_view.setFixedWidth(int(main.screenWidth*0.8))
    # original_view.setFixedHeight(int(main.screenHeight*0.6))
    original_view.setMinimumWidth(int(main.screenHeight * 0.6))

    # test_view.setFixedHeight(int(main.screenHeight*0.3))
    # test_view.setFixedWidth(int(main.screenHeight*0.3))
    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    voi_view.setFixedSize(int(main.screenHeight * 0.6), int(main.screenHeight * 0.6))
    observe_view.setFixedSize(int(main.screenHeight * 0.6), int(main.screenHeight * 0.3))
    voi_view.setFixedSize(int(main.screenHeight * 1.2), int(main.screenHeight * 0.9))
    layout_0.addWidget(original_view)
    layout_0.addWidget(observe_view)

    layout.addLayout(layout_0)

    layout.addWidget(voi_view)

    main.setWidget(widget)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
