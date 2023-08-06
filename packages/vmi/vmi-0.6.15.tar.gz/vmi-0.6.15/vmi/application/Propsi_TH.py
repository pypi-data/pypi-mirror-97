import json
import pathlib
import shutil
import tempfile
import time

import cv2
import numpy as np
import pydicom
import vtk
from PySide2.QtGui import *
from numba import jit

import vmi
import vmi.application.skyward


def read_dicom():
    dcmdir = vmi.askDirectory('DICOM')  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            global series
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                with pydicom.dcmread(series.filenames()[0]) as ds:
                    global patient_name
                    patient_name = str(ds.PatientName)
                    patient_name_box.draw_text('姓名：{}'.format(patient_name))
                    patient_name_box.setVisible(True)

                    global dicom_ds
                    dicom_ds = series.toKeywordValue()
                return series.read()  # 读取DICOM系列为图像数据


def on_init_voi():
    size = vmi.askInt(1, 300, 1000, suffix='mm', title='请输入目标区域尺寸')
    if size is not None:
        global LR, original_target, voi_size, voi_center, spcut_center
        original_target = original_view.pickPt_Cell()
        voi_center = np.array([vmi.imCenter(original_slice.data())[0], original_target[1], original_target[2]])
        voi_size = np.array([vmi.imSize(original_slice.data())[0], size, size])
        init_voi()

        LR = 1 if original_target[0] > voi_center[0] else -1
        patient_LR_box.draw_text('患侧：{}'.format('左' if LR > 0 else '右'))
        patient_LR_box.setVisible(True)

        spcut_center = original_target.copy()
        update_spcut()

        voi_view.setCamera_Coronal()
        update_spcut_section()

        voi_view.setCamera_FitAll()
        for v in [voi_view, *spcut_y_views, *spcut_z_views]:
            v.setEnabled(True)


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


def init_voi():
    global voi_size, voi_center, voi_origin, voi_cs, voi_image
    voi_origin = voi_center - 0.5 * voi_size
    voi_cs = vmi.CS4x4(origin=voi_origin)

    voi_image = vmi.imReslice(original_slice.data(), voi_cs, voi_size, -1024)
    voi_image.SetOrigin(voi_cs.origin())

    voi_ary = vmi.imArray_VTK(voi_image)
    ary_pad(voi_ary, -1024)
    voi_image = vmi.imVTK_Array(voi_ary, vmi.imOrigin(voi_image), vmi.imSpacing(voi_image))
    voi_volume.setData(voi_image)

    pd = vmi.imIsosurface(voi_image, 3070)
    metal_prop.setData(pd)
    pelvis_view.setCamera_Coronal()
    pelvis_view.setCamera_FitAll()
    clear_guide_plate()


def update_line_cut():
    if len(plcut_pts) > 1:
        plcut_prop.setData(vmi.ccWire(vmi.ccSegments(plcut_pts, True)))
    else:
        plcut_prop.setData(None)
    clear_guide_plate()


@jit(nopython=True)
def ary_mask(input_ary, mask_ary, threshold, target):
    for k in range(input_ary.shape[0]):
        for j in range(input_ary.shape[1]):
            for i in range(input_ary.shape[2]):
                if mask_ary[k][j][i] != 0 and threshold <= input_ary[k][j][i]:
                    input_ary[k][j][i] = target


def plcut_voi_image():
    cs = voi_view.cameraCS_FPlane()
    d = vmi.imSize_Vt(voi_volume.data(), cs.axis(2))
    pts = [vmi.ptOnPlane(pt, vmi.imCenter(voi_volume.data()), cs.axis(2)) for pt in plcut_pts]
    pts = [pt - d * cs.axis(2) for pt in pts]
    sh = vmi.ccFace(vmi.ccWire(vmi.ccSegments(pts, True)))
    sh = vmi.ccPrism(sh, cs.axis(2), 2 * d)

    mask = vmi.imStencil_PolyData(vmi.ccPd_Sh(sh),
                                  vmi.imOrigin(voi_volume.data()),
                                  vmi.imSpacing(voi_volume.data()),
                                  vmi.imExtent(voi_volume.data()))
    mask_ary = vmi.imArray_VTK(mask)
    voi_ary = vmi.imArray_VTK(voi_volume.data())
    ary_mask(voi_ary, mask_ary, bone_value, background_value)
    voi_image = vmi.imVTK_Array(voi_ary, vmi.imOrigin(voi_volume.data()), vmi.imSpacing(voi_volume.data()))
    voi_volume.setData(voi_image)

    for v in spcut_z_views + spcut_y_views:
        v.updateInTime()
    clear_guide_plate()


def spcut_voi_image():
    spcut_image = vmi.imStencil_PolyData(spcut_prop.data(),
                                         vmi.imOrigin(voi_volume.data()),
                                         vmi.imSpacing(voi_volume.data()),
                                         vmi.imExtent(voi_volume.data()))
    spcut_ary = vmi.imArray_VTK(spcut_image)
    voi_ary = vmi.imArray_VTK(voi_volume.data())

    ary_mask(voi_ary, spcut_ary, bone_value, background_value)
    voi_image = vmi.imVTK_Array(voi_ary, vmi.imOrigin(voi_volume.data()), vmi.imSpacing(voi_volume.data()))
    voi_volume.setData(voi_image)
    clear_guide_plate()


def update_spcut():
    spcut_mesh = vmi.pdSphere(spcut_radius, spcut_center)
    spcut_prop.setData(spcut_mesh)
    clear_guide_plate()


def update_spcut_section():
    angle = 30
    y_oblique = [vmi.CS4x4().rotate(angle, [0, 0, 1]), vmi.CS4x4(), vmi.CS4x4().rotate(-angle, [0, 0, 1])]
    z_oblique = [vmi.CS4x4().rotate(-angle, [0, 1, 0]), vmi.CS4x4(), vmi.CS4x4().rotate(angle, [0, 1, 0])]

    y_normals = [cs.mvt([0, 1, 0]) for cs in y_oblique]
    z_normals = [cs.mvt([0, 0, 1]) for cs in z_oblique]

    y_cs = [vmi.CS4x4_Coronal(), vmi.CS4x4_Coronal(), vmi.CS4x4_Coronal()]
    y_cs[0] = y_cs[0].rotate(-angle, y_cs[0].axis(1))
    y_cs[2] = y_cs[2].rotate(angle, y_cs[2].axis(1))

    z_cs = [vmi.CS4x4_Axial(), vmi.CS4x4_Axial(), vmi.CS4x4_Axial()]
    z_cs[0] = z_cs[0].rotate(-angle, z_cs[0].axis(1))
    z_cs[2] = z_cs[2].rotate(angle, z_cs[2].axis(1))

    hheight = 50
    hwidth = hheight * spcut_y_views[0].width() / spcut_y_views[0].height()

    for i in range(3):
        y_cs[i].setOrigin(spcut_center - y_cs[i].mpt([hwidth, hheight, 0]))
        z_cs[i].setOrigin(spcut_center - z_cs[i].mpt([hwidth, hheight, 0]))

    for i in range(3):
        spcut_y_slices[i].setSlicePlane(spcut_center, y_normals[i])
        spcut_z_slices[i].setSlicePlane(spcut_center, z_normals[i])

    for i in range(3):
        spcut_y_props[i].setData(vmi.pdPolygon_Regular(spcut_radius, spcut_center, y_normals[i]))
        spcut_z_props[i].setData(vmi.pdPolygon_Regular(spcut_radius, spcut_center, z_normals[i]))

    for i in range(3):
        spcut_y_views[i].setCamera_FPlane(y_cs[i], 2 * hheight)
        spcut_z_views[i].setCamera_FPlane(z_cs[i], 2 * hheight)
    clear_guide_plate()


def init_pelvis():
    pd = vmi.imResample_Isotropic(voi_volume.data())
    pd = vmi.imIsosurface(pd, bone_value)
    pelvis_prop.setData(pd)

    pelvis_view.setCamera_Coronal()
    pelvis_view.setCamera_FitAll()
    pelvis_view.setEnabled(True)

    pelvis_cs.setOrigin(vmi.pdMassCenter(pelvis_prop.data()))
    cup_cs.setOrigin(original_target)
    update_pelvis_cs_prop()
    update_cup_center()
    clear_guide_plate()


def update_pelvis_MPP():
    global pelvis_cs
    vr = pelvis_view.cameraVt_Right()
    vr = vr if np.dot(vr, np.array([1, 0, 0])) >= 0 else -vr
    if vmi.vtAngle(vr, pelvis_cs.axis(1)) < 1 or vmi.vtAngle(vr, pelvis_cs.axis(1)) > 179:
        return

    pelvis_cs.setAxis(0, vr)
    pelvis_cs.orthogonalize([2, 0])
    pelvis_cs.normalize()
    update_cup_orientation()
    update_cup()

    midpt = pelvis_view.pickPt_FocalPlane([0.5 * pelvis_view.width(), 0.5 * pelvis_view.height()])
    origin = vmi.ptOnPlane(vmi.pdMassCenter(pelvis_prop.data()), midpt, pelvis_cs.axis(0))
    pelvis_cs.setOrigin(origin)
    cs = vmi.CS4x4().reflect(pelvis_cs.axis(0), pelvis_cs.origin())
    pd = vmi.pdMatrix(pelvis_prop.data(), cs.matrix4x4())
    pelvis_MPP_prop.setData(pd)

    cs = pelvis_view.cameraCS_FPlane()
    pd = vmi.pdMatrix(pelvis_prop.data(), cs.inv().matrix4x4())
    b, c = pd.GetBounds(), pd.GetCenter()
    left_top = np.array([b[0], b[2], c[2]])
    right_top = np.array([b[1], b[2], c[2]])
    left_bottom = np.array([b[0], b[3], c[2]])
    right_bottom = np.array([b[1], b[3], c[2]])
    xn = int(np.round(0.1 * (pd.GetBounds()[1] - pd.GetBounds()[0])))

    lines = []
    for i in range(xn + 1):
        pts = [left_top + i / xn * (left_bottom - left_top),
               right_top + i / xn * (right_bottom - right_top)]
        pts = [cs.mpt(pt) for pt in pts]
        line = vmi.ccEdge(vmi.ccSegment(pts[0], pts[1]))
        line = vmi.ccPd_Sh(line)
        lines.append(line)

    pd = vmi.pdAppend(lines)
    pelvis_cs_indicator_prop.setData(pd)
    update_pelvis_cs_prop()
    clear_guide_plate()


def update_pelvis_APP():
    global pelvis_cs
    vr = pelvis_view.cameraVt_Right()
    vr = vr if np.dot(vr, np.array([0, 1, 0])) >= 0 else -vr
    if vmi.vtAngle(vr, pelvis_cs.axis(0)) < 1 or vmi.vtAngle(vr, pelvis_cs.axis(0)) > 179:
        return

    pelvis_cs.setAxis(1, vr)
    pelvis_cs.orthogonalize([2, 0])
    pelvis_cs.normalize()
    update_cup_orientation()
    update_cup()

    cs = pelvis_view.cameraCS_FPlane()
    pd = vmi.pdMatrix(pelvis_prop.data(), cs.inv().matrix4x4())
    b, c = pd.GetBounds(), pd.GetCenter()
    left_top = np.array([b[0], b[2], c[2]])
    right_top = np.array([b[1], b[2], c[2]])
    left_bottom = np.array([b[0], b[3], c[2]])
    right_bottom = np.array([b[1], b[3], c[2]])
    xn = int(np.round(0.1 * (pd.GetBounds()[1] - pd.GetBounds()[0])))

    lines = []
    for i in range(xn + 1):
        pts = [left_top + i / xn * (right_top - left_top),
               left_bottom + i / xn * (right_bottom - left_bottom)]
        pts = [cs.mpt(pt) for pt in pts]
        line = vmi.ccEdge(vmi.ccSegment(pts[0], pts[1]))
        line = vmi.ccPd_Sh(line)
        lines.append(line)

    pd = vmi.pdAppend(lines)
    pelvis_cs_indicator_prop.setData(pd)
    update_pelvis_cs_prop()
    clear_guide_plate()


def update_pelvis_cs_prop():
    pelvis_csx_prop.setData(vmi.ccEdge(vmi.ccSegment(pelvis_cs.origin(), pelvis_cs.mpt([10, 0, 0]))))
    pelvis_csy_prop.setData(vmi.ccEdge(vmi.ccSegment(pelvis_cs.origin(), pelvis_cs.mpt([0, 10, 0]))))
    pelvis_csz_prop.setData(vmi.ccEdge(vmi.ccSegment(pelvis_cs.origin(), pelvis_cs.mpt([0, 0, 10]))))


def update_cup_center():
    o = pelvis_cs.inv().mpt(cup_cs.origin())
    o[0] *= LR
    cup_location_box.draw_text('{:.3f}, {:.3f}, {:.3f}'.format(o[0], o[1], o[2]))


def update_cup_orientation():
    # 用RA计算
    # cup_axis = [np.cos(np.deg2rad(cup_RA)) * np.sin(np.deg2rad(cup_RI)) * LR,
    #             -np.sin(np.deg2rad(cup_RA)),
    #             -np.cos(np.deg2rad(cup_RA)) * np.cos(np.deg2rad(cup_RI))]

    # 用AA计算
    global cup_axiss
    cup_axiss = [np.array([LR, -np.tan(np.deg2rad(cup_RA)), -1 / np.tan(np.deg2rad(cup_RI))]),
                 np.array([LR, -np.tan(np.deg2rad(cup_RA - 5)), -1 / np.tan(np.deg2rad(cup_RI))]),
                 np.array([LR, -np.tan(np.deg2rad(cup_RA + 5)), -1 / np.tan(np.deg2rad(cup_RI))])]

    cup_axis = cup_axiss[0] / np.linalg.norm(cup_axiss[0])
    cup_axiss = [vt / np.linalg.norm(vt) for vt in cup_axiss]

    RA = np.rad2deg(np.arctan(-cup_axis[1] / np.sqrt(1 - cup_axis[1] ** 2)))
    AA = np.rad2deg(np.arctan(-cup_axis[1] / np.abs(cup_axis[0])))
    OA = np.rad2deg(np.arctan(cup_axis[1] / cup_axis[2]))
    # print('RA={} AA={} OA={}'.format(RA, AA, OA))

    RI = np.rad2deg(np.arctan(-np.abs(cup_axis[0]) / cup_axis[2]))
    AI = np.rad2deg(np.arctan(-np.sqrt(1 - cup_axis[2] ** 2) / cup_axis[2]))
    OI = np.rad2deg(np.arctan(np.abs(cup_axis[0]) / np.sqrt(1 - cup_axis[0] ** 2)))
    # print('RI={} AI={} OI={}'.format(RI, AI, OI))

    # RA, AA, OA = np.deg2rad(RA), np.deg2rad(AA), np.deg2rad(OA)
    # RI, AI, OI = np.deg2rad(RI), np.deg2rad(AI), np.deg2rad(OI)
    # print(np.tan(OA), np.tan(RA) / np.cos(RI), np.sin(OI), np.sin(RI) * np.cos(RA))
    # print(np.tan(OA), np.sin(AA) * np.tan(AI), np.sin(OI), np.sin(AI) * np.cos(AA))
    # print(np.tan(AA), np.sin(OA) / np.tan(OI), np.cos(AI), np.cos(OI) * np.cos(OA))
    # print(np.tan(AA), np.tan(RA) / np.sin(RI), np.cos(AI), np.cos(RI) * np.cos(RA))
    # print(np.tan(RA), np.sin(OA) * np.cos(OI), np.tan(RI), np.tan(OI) / np.cos(OA))
    # print(np.tan(RA), np.sin(AA) * np.sin(AI), np.tan(RI), np.tan(AI) * np.cos(AA))

    cup_axis = pelvis_cs.mvt(cup_axis)
    cup_axiss = [pelvis_cs.mvt(vt) for vt in cup_axiss]

    cup_cs.setAxis(1, pelvis_cs.axis(1))
    cup_cs.setAxis(2, cup_axis)
    cup_cs.orthogonalize([0, 1])
    cup_cs.setAxis(0, -LR * cup_cs.axis(0))
    cup_cs.normalize()
    clear_guide_plate()


def update_cup(clear=True):
    plane = vtk.vtkPlane()
    plane.SetNormal(cup_cs.axis(2))
    plane.SetOrigin(cup_cs.origin())

    pd = vmi.pdSphere(cup_radius, cup_cs.origin())
    pd = vmi.pdClip_Implicit(pd, plane)[1]

    pd_border = vmi.pdPolyline_Regular(cup_radius, cup_cs.origin(), cup_cs.axis(2))
    pd = vmi.pdAppend([pd, pd_border])

    cs = vmi.CS4x4().reflect(pelvis_cs.axis(0), pelvis_cs.origin())
    pd_MPP = vmi.pdMatrix(pd, cs.matrix4x4())
    cup_prop.setData(vmi.pdAppend([pd, pd_MPP]))

    if pelvis_slice_box.text() == '断层':
        pd = vmi.pdCut_Implicit(cup_prop.data(), pelvis_slice.slicePlane())
        cup_section_prop.setData(pd)
    if clear:
        clear_guide_plate()


@jit(nopython=True)
def pt_ary_cs_mask(pt_ary: np.ndarray, cs: np.ndarray, mask: np.ndarray):
    return (pt_ary @ cs) * mask


def update_cup_camera_sagittal():
    cs = vmi.CS4x4(axis1=-pelvis_cs.axis(2), axis2=pelvis_cs.axis(0))
    cs.orthogonalize([0])
    cs.setOrigin(cup_cs.origin() - 2.25 * cup_radius * cs.axis(0) - 2.25 * cup_radius * cs.axis(1))
    pelvis_view.setCamera_FPlane(cs, 4.5 * cup_radius)
    pelvis_view.updateInTime()


def update_cup_camera_coronal():
    cs = vmi.CS4x4(axis1=-pelvis_cs.axis(2), axis2=pelvis_cs.axis(1))
    cs.orthogonalize([0])
    cs.setOrigin(cup_cs.origin() - 2.25 * cup_radius * cs.axis(0) - 2.25 * cup_radius * cs.axis(1))
    pelvis_view.setCamera_FPlane(cs, 4.5 * cup_radius)
    pelvis_view.updateInTime()


def update_cup_camera_axial():
    cs = vmi.CS4x4(axis1=pelvis_cs.axis(1), axis2=pelvis_cs.axis(2))
    cs.orthogonalize([0])
    cs.setOrigin(cup_cs.origin() - 2.25 * cup_radius * cs.axis(0) - 2.25 * cup_radius * cs.axis(1))
    pelvis_view.setCamera_FPlane(cs, 4.5 * cup_radius)
    pelvis_view.updateInTime()


def update_cup_camera_RA():
    cs = vmi.CS4x4(axis1=-cup_cs.axis(1), axis2=-cup_cs.axis(0))
    cs.orthogonalize([0])
    cs.setOrigin(cup_cs.origin() - 2.25 * cup_radius * cs.axis(0) - 2.25 * cup_radius * cs.axis(1))
    pelvis_view.setCamera_FPlane(cs, 4.5 * cup_radius)
    pelvis_view.updateInTime()


def update_cup_camera_RI():
    cs = vmi.CS4x4(axis1=-cup_cs.axis(0), axis2=cup_cs.axis(1))
    cs.orthogonalize([0])
    cs.setOrigin(cup_cs.origin() - 2.25 * cup_radius * cs.axis(0) - 2.25 * cup_radius * cs.axis(1))
    pelvis_view.setCamera_FPlane(cs, 4.5 * cup_radius)
    pelvis_view.updateInTime()


def update_cup_camera_plane():
    cs = vmi.CS4x4(axis1=-cup_cs.axis(0), axis2=-cup_cs.axis(2))
    cs.orthogonalize([0])
    cs.setOrigin(cup_cs.origin() - 2.25 * cup_radius * cs.axis(0) - 2.25 * cup_radius * cs.axis(1))
    pelvis_view.setCamera_FPlane(cs, 4.5 * cup_radius)
    pelvis_view.updateInTime()


def init_guide():
    size = np.array([5 * cup_radius, 5 * cup_radius, 5 * cup_radius])
    cs = vmi.CS4x4(origin=cup_cs.origin() - 0.5 * size)
    image = vmi.imReslice(voi_volume.data(), cs, size, -1024)
    image.SetOrigin(cs.origin())

    global aceta_image
    aceta_image = vmi.imReslice(original_slice.data(), cs, size, -1024)
    aceta_image.SetOrigin(cs.origin())

    ary = vmi.imArray_VTK(image)
    ary_pad(ary, -1024)
    image = vmi.imVTK_Array(ary, vmi.imOrigin(image), vmi.imSpacing(image))
    image = vmi.imResample_Isotropic(image)

    pd = vmi.imIsosurface(image, bone_value)
    pd = vmi.pdSmooth_WindowedSinc(pd, 20)
    aceta_prop.setData(pd)

    update_guide_path()
    update_cup_camera_plane()
    guide_view.setEnabled(True)


def update_defect_path():
    if len(defect_path_pts) > 1:
        defect_path_prop.setData(vmi.ccWire(vmi.ccSegments(defect_path_pts, closed=True)))
    else:
        defect_path_prop.setData(None)


def update_guide_path():
    global cup_cs, body_cs, large_z, small_t
    large_z, small_t = 100, 5
    body_vt_x = cup_cs.rotate(LR * (body_angle + 45), -cup_cs.axis(2)).mvt([1, 0, 0])
    body_cs = vmi.CS4x4(origin=cup_cs.mpt([body_offsetX, -LR * body_offsetY, large_z]),
                        axis0=body_vt_x, axis2=-cup_cs.axis(2))

    body_cs.orthogonalize([1, 0])
    body_cs.normalize()

    global body_xr, body_yr, head_xr, head_yr, body_x_negtive
    head_xr = 7  # 头部长径，臼缘匹配块
    head_yr = body_yr
    body_x_negtive = body_yr / np.sin(np.deg2rad(72))

    global body_wire
    body_pts = [body_cs.mpt([body_xr + head_xr, LR * -body_yr, 0]),
                body_cs.mpt([body_xr + head_xr, LR * body_yr, 0]),
                body_cs.mpt([-body_x_negtive * np.cos(np.deg2rad(72)), LR * body_yr, 0]),
                body_cs.mpt([-body_x_negtive, 0, 0]),
                body_cs.mpt([-body_x_negtive * np.cos(np.deg2rad(72)), LR * -body_yr, 0])]

    body_wire = body_cs.workplane().polyline(
        [body_cs.inv().mpt(pt)[:2].tolist() for pt in body_pts]).close().val().wrapped
    body_axis = vmi.ccEdge(vmi.ccSegment(cup_cs.mpt([0, 0, -large_z]), cup_cs.mpt([0, 0, large_z])))

    global body_hole_wire
    body_hole_radius = small_t
    body_hole_wire = vmi.ccWire(vmi.ccEdge(
        vmi.ccCircle(body_hole_radius, cup_cs.mpt([0, 0, large_z]), body_cs.axis(2), body_cs.axis(0))))

    global head_cs
    head_cs = body_cs.copy()
    head_cs.setOrigin(body_cs.mpt([body_xr, 0, 0]))

    global arm_length, arm_area_wire, shaft_radius
    shaft_radius = 5
    arm_area_pts = [head_cs.mpt([-arm_length * np.sin(np.deg2rad(t)),
                                 -LR * (arm_length * np.cos(np.deg2rad(t))), 0]) for t in range(-30, 60)]
    arm_area_wire = vmi.ccWire(vmi.ccSegments(arm_area_pts))

    defect_paths = []
    for pts in defect_path_list:
        defect_paths.append(vmi.ccWire(vmi.ccSegments(pts, closed=True)))

    global guide_path, guide_path_prop
    guide_path = vmi.ccBoolean_Union([body_wire, body_axis, body_hole_wire, arm_area_wire, *defect_paths])
    guide_path_prop.setData(guide_path)
    return


def update_guide_plate():
    global UDI, UDI_time
    UDI_time = time.localtime()
    UDI = '{}{}'.format('TH', vmi.convert_base(round(time.time() * 100)).upper())

    time_start, time_prev = time.time(), time.time()

    global kirs_radius, kirs_hole_radius
    kirs_hole_radius = kirs_radius + 0.05 + 0.15

    global body_cs, body_xr, body_yr, head_cs, head_xr, head_yr, large_z, small_t, arm_length, shaft_radius
    global psi_match, psi_match_prop
    global head_height, head_z
    head_height = 15

    mold_xr = body_xr + head_xr
    mold_yr = arm_length + kirs_hole_radius + 2
    res = 1
    nx, ny = int(np.ceil(mold_xr / res)) + 1, int(np.ceil(mold_yr / res)) + 1
    body_mold, body_z_array = [], []

    defect_centers, defect_radiuss = [], []
    for pts in defect_path_list:
        pts = np.array([np.array([1, 1, 0]) * body_cs.inv().mpt(pt) for pt in pts])
        c = np.sum(pts, axis=0) / len(pts)
        defect_centers.append(c)
        r = np.mean([np.linalg.norm(c - pt) for pt in pts])
        defect_radiuss.append(r)

    def z_filter(x_array: np.ndarray, y_array: np.ndarray, z_array: np.ndarray) -> np.ndarray:
        # 邻域均值光顺
        for k in range(int(1e4)):
            delta_max = 0
            z_array_ = z_array.copy()
            for j in range(0, 2 * ny + 1):
                for i in range(0, 2 * nx + 1):
                    pt = np.array([x_array[j][i], y_array[j][i], 0])
                    defect = False
                    for c, r in zip(defect_centers, defect_radiuss):
                        if np.linalg.norm(pt - c) < r:
                            defect = True
                            break

                    jmin, jmax = min(max(j - 1, 0), 2 * ny), min(max(j + 1, 0), 2 * ny)
                    imin, imax = min(max(i - 1, 0), 2 * nx), min(max(i + 1, 0), 2 * nx)
                    neighbors = z_array_[jmin:(jmax + 1), imin:(imax + 1)]

                    delta = (z_array_[j][i] - neighbors.mean()) * (10 if defect else 1)
                    delta_max = max(delta_max, delta)
                    if delta > 1:
                        z_array[j][i] = neighbors.mean()

            if delta_max < 1 + 1e-6:
                break

        if not len(body_mold):
            # 统计髋臼边缘最高点
            global head_z
            head_z = large_z
            for j in range(0, 2 * ny + 1):
                for i in range(0, 2 * nx + 1):
                    if x_array[j][i] > body_xr - head_xr:
                        head_z = min(head_z, z_array[j][i])
            head_z = head_z - small_t

            # 边缘外深度截断
            for j in range(0, 2 * ny + 1):
                for i in range(0, 2 * nx + 1):
                    if x_array[j][i] > body_xr - 1e-3:
                        if z_array[j][i] > head_z - small_t + head_depth:
                            z_array[j][i] = head_z - small_t + head_depth
        return z_array

    body = vmi.ccMatchSolid_Rect(
        aceta_prop.data(), body_cs, nx, ny, res, small_t, 2 * large_z - small_t, z_filter, body_mold)

    vmi.ccMatchSolid_Rect(
        aceta_prop.data(), body_cs, nx, ny, res, small_t, 2 * large_z - small_t, z_filter, body_mold)

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('match body', time_stop)

    global psi_mold, psi_mold_prop
    mold_max_z = small_t + vmi.pdRayDistance_Pt(body_cs.origin(), body_cs.axis(2), aceta_prop.data())
    if not mold_max_z:
        mold_max_z = head_z + small_t + body_xr + head_xr
    body_top_z = mold_max_z - small_t - 15

    mold_wire = body_cs.workplane([0, -LR * 0.5 * (mold_yr - mold_xr), 0]).rect(
        2 * mold_xr, mold_xr + mold_yr).val().wrapped
    mold_box = vmi.ccPrism(vmi.ccFace(mold_wire), body_cs.axis(2), mold_max_z)
    psi_mold = vmi.ccBoolean_Intersection([body_mold[0], mold_box])

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('psi_mold', time_stop)

    label_cs = vmi.CS4x4(origin=body_cs.mpt([0, LR * 0.5 * (mold_xr - mold_yr), mold_max_z - 1]),
                         axis1=-LR * body_cs.axis(1), axis2=-body_cs.axis(2))
    label_cs.orthogonalize([0])

    label_wire = label_cs.workplane().rect(2 * mold_xr, mold_xr + mold_yr + small_t * 4).val().wrapped
    label_box = vmi.ccPrism(vmi.ccFace(label_wire), body_cs.axis(2), 2)
    psi_mold = vmi.ccBoolean_Union([psi_mold, label_box])

    label_cs = vmi.CS4x4(origin=body_cs.mpt([0, -LR * (mold_yr + small_t), mold_max_z]),
                         axis1=-LR * body_cs.axis(1), axis2=-body_cs.axis(2))
    label_cs.orthogonalize([0])
    text = '{} {}'.format(patient_name, 'L' if LR > 0 else 'R')
    label_text = label_cs.workplane().text(text, small_t, 3, font='DengXian', kind='bold').val().wrapped
    psi_mold = vmi.ccBoolean_Union([psi_mold, label_text])

    label_cs = vmi.CS4x4(origin=body_cs.mpt([0, LR * (mold_xr + small_t), mold_max_z]),
                         axis1=-LR * body_cs.axis(1), axis2=-body_cs.axis(2))
    label_cs.orthogonalize([0])
    label_text = label_cs.workplane().text(UDI, small_t, 3, font='DengXian', kind='bold').val().wrapped
    psi_mold = vmi.ccBoolean_Union([psi_mold, label_text])

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('psi_label', time_stop)

    global body_x_negtive
    body_pts = [[body_xr + head_xr, LR * -body_yr, head_z],
                [body_xr + head_xr, LR * body_yr, head_z],
                [-body_x_negtive * np.cos(np.deg2rad(72)), LR * body_yr, head_z],
                [-body_x_negtive, 0, head_z],
                [-body_x_negtive * np.cos(np.deg2rad(72)), LR * -body_yr, head_z]]
    body_wire = vmi.ccWire(vmi.ccSegments([body_cs.mpt(pt) for pt in body_pts], True))
    body_box = vmi.ccPrism(vmi.ccFace(body_wire), body_cs.axis(2), 2 * large_z)
    body = vmi.ccBoolean_Intersection([body, body_box])

    if match_style == '下沉式':
        body_pts = [[body_xr + head_xr, LR * body_yr, 2 * large_z],
                    [body_xr + head_xr, LR * body_yr, head_z],
                    [body_xr - head_xr, LR * body_yr, head_z],
                    [0, LR * body_yr, body_top_z],
                    [-body_x_negtive, LR * body_yr, body_top_z],
                    [-body_x_negtive, LR * body_yr, 2 * large_z]]
        body_wire = vmi.ccWire(vmi.ccSegments([body_cs.mpt(pt) for pt in body_pts], True))
        body_box = vmi.ccPrism(vmi.ccFace(body_wire), -LR * body_cs.axis(1), 2 * body_yr)
        body = vmi.ccBoolean_Intersection([body, body_box])
    else:
        body_pts = [[body_xr + head_xr, LR * body_yr, large_z * 2],
                    [body_xr + head_xr, LR * body_yr, head_z],
                    [-body_x_negtive, LR * body_yr, head_z],
                    [-body_x_negtive, LR * body_yr, head_z + small_t],
                    [body_xr - head_xr * 2, LR * body_yr, head_z + small_t],
                    [body_xr - head_xr * 2, LR * body_yr, 2 * large_z]]
        body_wire = vmi.ccWire(vmi.ccSegments([body_cs.mpt(pt) for pt in body_pts], True))
        body_box = vmi.ccPrism(vmi.ccFace(body_wire), -LR * body_cs.axis(1), 2 * body_yr)
        body = vmi.ccBoolean_Intersection([body, body_box])

    global shaft
    cone_height = head_height + 1 - 3
    dr = cone_height * np.tan(np.deg2rad(5.675))
    shaft_wire0 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(
        shaft_radius, head_cs.mpt([0, 0, head_z + 1]), head_cs.axis(2), head_cs.axis(0))))
    shaft_wire1 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(
        shaft_radius - dr, head_cs.mpt([0, 0, head_z + 1 - cone_height]), head_cs.axis(2), head_cs.axis(0))))
    shaft_face0 = vmi.ccFace(shaft_wire0)
    shaft_face1 = vmi.ccFace(shaft_wire1)
    shaft = vmi.ccSolid(vmi.ccSew([vmi.ccLoft([shaft_wire0, shaft_wire1]), shaft_face0, shaft_face1]))
    body = vmi.ccBoolean_Union([body, shaft])

    global shaft_hole
    shaft_hole_wire = vmi.ccWire(vmi.ccEdge(
        vmi.ccCircle(kirs_hole_radius, head_cs.mpt([0, 0, head_z + 200]), head_cs.axis(2), head_cs.axis(0))))
    shaft_hole = vmi.ccPrism(vmi.ccFace(shaft_hole_wire), -head_cs.axis(2), 2000)
    body = vmi.ccBoolean_Difference([body, shaft_hole])

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('psi_body', time_stop)

    global body_hole_wire
    body_hole = vmi.ccPrism(vmi.ccFace(body_hole_wire), body_cs.axis(2), 2 * large_z)

    global psi_arm, psi_arm_short, psi_arm_long
    psi_arms, arm_lengths = [0, 0, 0], [arm_length - 5, arm_length, arm_length + 5]
    for i in range(3):
        arm_pts = [[kirs_hole_radius + 2, -LR * (arm_lengths[i] + kirs_hole_radius + 2), head_z],
                   [kirs_hole_radius + 2, -LR * (arm_lengths[i] - kirs_hole_radius - 2), head_z],
                   [head_xr, LR * -head_xr, head_z],
                   [head_xr, LR * head_xr, head_z],
                   [-head_xr, LR * head_xr, head_z],
                   [-head_xr, LR * -head_xr, head_z],
                   [-kirs_hole_radius - 2, -LR * (arm_lengths[i] - kirs_hole_radius - 2), head_z],
                   [-kirs_hole_radius - 2, -LR * (arm_lengths[i] + kirs_hole_radius + 2), head_z]]
        arm_pts = [head_cs.mpt(pt) for pt in arm_pts]
        arm_wire = vmi.ccWire(vmi.ccSegments(arm_pts, True))
        psi_arms[i] = vmi.ccPrism(vmi.ccFace(arm_wire), -head_cs.axis(2), head_height + 2)

        cone_height = head_height + 1 - 2
        dr = cone_height * np.tan(np.deg2rad(5.675))

        c = head_cs.mpt([0, 0, head_z + 1 - cone_height])
        cone_wire0 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(
            shaft_radius, c + cone_height * head_cs.axis(2), head_cs.axis(2), head_cs.axis(0))))
        cone_wire1 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(
            shaft_radius - dr, c, head_cs.axis(2), head_cs.axis(0))))

        cone_face0, cone_face1 = vmi.ccFace(cone_wire0), vmi.ccFace(cone_wire1)
        cone = vmi.ccSolid(vmi.ccSew([vmi.ccLoft([cone_wire0, cone_wire1]), cone_face0, cone_face1]))
        psi_arms[i] = vmi.ccBoolean_Difference([psi_arms[i], cone])

        kirs_hole_center = head_cs.mpt([0, -LR * arm_lengths[i], head_z + 200])
        kirs_hole = vmi.ccPrism(vmi.ccFace(vmi.ccWire(vmi.ccCircle(
            kirs_hole_radius, kirs_hole_center, head_cs.axis(2)))), -head_cs.axis(2), 2000)
        psi_arms[i] = vmi.ccBoolean_Difference([psi_arms[i], shaft_hole, cone, kirs_hole])

    psi_arm_short, psi_arm, psi_arm_long = psi_arms[0], psi_arms[1], psi_arms[2]
    psi_arm_prop.setData(psi_arm)
    # psi_arm_prop.setData(vmi.pdTriangle(vmi.ccPd_Sh(psi_arm), 0, 0))

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('psi_arm', time_stop)

    center_hole_wire = vmi.ccWire(vmi.ccEdge(
        vmi.ccCircle(kirs_hole_radius, body_cs.mpt([0, 0, 0]), body_cs.axis(2), body_cs.axis(0))))
    center_hole = vmi.ccPrism(vmi.ccFace(center_hole_wire), body_cs.axis(2), 2 * large_z)

    psi_mold = vmi.ccBoolean_Difference([psi_mold, center_hole])
    psi_mold = vmi.ccBoolean_Difference([psi_mold, shaft_hole])
    psi_mold_prop.setData(psi_mold)
    # mold_prop.setData(vmi.pdTriangle(vmi.ccPd_Sh(mold), 0, 0))

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('mold_hole', time_stop)

    psi_match = vmi.ccBoolean_Difference([body, body_hole])
    psi_match_prop.setData(psi_match)
    # psi_match_prop.setData(vmi.pdTriangle(vmi.ccPd_Sh(psi_match), 0, 0))

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('psi_match', time_stop)
    print(time.time() - time_start)


def clear_guide_plate():
    global psi_match, psi_arm, psi_mold
    psi_match = vmi.TopoDS_Shape()
    psi_arm = vmi.TopoDS_Shape()
    psi_mold = vmi.TopoDS_Shape()
    psi_match_prop.setData(vtk.vtkPolyData())
    psi_arm_prop.setData(vtk.vtkPolyData())
    psi_mold_prop.setData(vtk.vtkPolyData())


def case_snapshot(video=False):
    snapshots = []
    visibles = [aceta_prop.visible(),
                guide_path_prop.visible(),
                psi_match_prop.visible(),
                psi_arm_prop.visible(),
                psi_mold_prop.visible()]

    with tempfile.TemporaryDirectory() as p:
        f = pathlib.Path(p) / '.png'

        original_slice.setVisible(True)
        original_slice.setSlicePlaneNormal_Coronal()
        original_slice.setSlicePlaneOrigin(original_target)
        original_view.setCamera_Coronal()
        original_view.setCamera_FitAll()
        main.scrollArea().ensureWidgetVisible(original_view)
        if video:
            delta = vmi.imSpacing(original_slice.data())[0]
            n = int(round(30 / delta))
            delta = 30 / n
            for _ in range(n):
                original_slice.slice(delta=-delta)
                original_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(2 * n):
                original_slice.slice(delta=delta)
                original_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(n):
                original_slice.slice(delta=-delta)
                original_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(50):
                snapshots.append(snapshots[-1])
        else:
            original_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

        voi_volume.setVisible(True)
        spcut_prop.setVisible(False)
        voi_view.setCamera_Coronal()
        voi_view.setCamera_FitAll()
        main.scrollArea().ensureWidgetVisible(voi_view)
        if video:
            pass
        else:
            voi_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

        # 前平面
        main.scrollArea().ensureWidgetVisible(pelvis_view)
        pelvis_cs_indicator_prop.setVisible(True)
        global pelvis_MPP_camera_cs, pelvis_APP_camera_cs
        pelvis_view.setCamera_FPlane(pelvis_APP_camera_cs, pelvis_APP_camera_height)
        if video:
            pelvis_view.camera().Roll(-LR * 15)
            pelvis_view.camera().OrthogonalizeViewUp()
            for _ in range(15):
                pelvis_view.camera().Roll(LR * 1)
                pelvis_view.camera().OrthogonalizeViewUp()

                cs = pelvis_view.cameraCS_FPlane()
                pd = vmi.pdMatrix(pelvis_prop.data(), cs.inv().matrix4x4())
                b, c = pd.GetBounds(), pd.GetCenter()
                left_top = np.array([b[0], b[2], c[2]])
                right_top = np.array([b[1], b[2], c[2]])
                left_bottom = np.array([b[0], b[3], c[2]])
                right_bottom = np.array([b[1], b[3], c[2]])
                xn = int(np.round(0.1 * (pd.GetBounds()[1] - pd.GetBounds()[0])))

                lines = []
                for i in range(xn + 1):
                    pts = [left_top + i / xn * (right_top - left_top),
                           left_bottom + i / xn * (right_bottom - left_bottom)]
                    pts = [cs.mpt(pt) for pt in pts]
                    line = vmi.ccEdge(vmi.ccSegment(pts[0], pts[1]))
                    line = vmi.ccPd_Sh(line)
                    lines.append(line)

                pd = vmi.pdAppend(lines)
                pelvis_cs_indicator_prop.setData(pd)

                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(50):
                snapshots.append(snapshots[-1])
        else:
            cs = pelvis_view.cameraCS_FPlane()
            pd = vmi.pdMatrix(pelvis_prop.data(), cs.inv().matrix4x4())
            b, c = pd.GetBounds(), pd.GetCenter()
            left_top = np.array([b[0], b[2], c[2]])
            right_top = np.array([b[1], b[2], c[2]])
            left_bottom = np.array([b[0], b[3], c[2]])
            right_bottom = np.array([b[1], b[3], c[2]])
            xn = int(np.round(0.1 * (pd.GetBounds()[1] - pd.GetBounds()[0])))

            lines = []
            for i in range(xn + 1):
                pts = [left_top + i / xn * (right_top - left_top),
                       left_bottom + i / xn * (right_bottom - left_bottom)]
                pts = [cs.mpt(pt) for pt in pts]
                line = vmi.ccEdge(vmi.ccSegment(pts[0], pts[1]))
                line = vmi.ccPd_Sh(line)
                lines.append(line)

            pd = vmi.pdAppend(lines)
            pelvis_cs_indicator_prop.setData(pd)

            pelvis_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

        # 对称面
        pelvis_MPP_prop.setVisible(True)
        pelvis_view.setCamera_FPlane(pelvis_MPP_camera_cs, pelvis_MPP_camera_height)
        if video:
            pelvis_view.camera().Roll(-LR * 15)
            pelvis_view.camera().OrthogonalizeViewUp()
            for _ in range(15):
                pelvis_view.camera().Roll(LR * 1)
                pelvis_view.camera().OrthogonalizeViewUp()

                origin = pelvis_view.pickPt_FocalPlane([0.5 * pelvis_view.width(), 0.5 * pelvis_view.height()])
                cs = vmi.CS4x4().reflect(pelvis_view.cameraCS_FPlane().axis(0), origin)
                pd = vmi.pdMatrix(pelvis_prop.data(), cs.matrix4x4())
                pelvis_MPP_prop.setData(pd)

                cs = pelvis_view.cameraCS_FPlane()
                pd = vmi.pdMatrix(pelvis_prop.data(), cs.inv().matrix4x4())
                b, c = pd.GetBounds(), pd.GetCenter()
                left_top = np.array([b[0], b[2], c[2]])
                right_top = np.array([b[1], b[2], c[2]])
                left_bottom = np.array([b[0], b[3], c[2]])
                right_bottom = np.array([b[1], b[3], c[2]])
                xn = int(np.round(0.1 * (pd.GetBounds()[1] - pd.GetBounds()[0])))

                lines = []
                for i in range(xn + 1):
                    pts = [left_top + i / xn * (left_bottom - left_top),
                           right_top + i / xn * (right_bottom - right_top)]
                    pts = [cs.mpt(pt) for pt in pts]
                    line = vmi.ccEdge(vmi.ccSegment(pts[0], pts[1]))
                    line = vmi.ccPd_Sh(line)
                    lines.append(line)

                pd = vmi.pdAppend(lines)
                pelvis_cs_indicator_prop.setData(pd)

                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(50):
                snapshots.append(snapshots[-1])
        else:
            origin = pelvis_view.pickPt_FocalPlane([0.5 * pelvis_view.width(), 0.5 * pelvis_view.height()])
            cs = vmi.CS4x4().reflect(pelvis_view.cameraCS_FPlane().axis(0), origin)
            pd = vmi.pdMatrix(pelvis_prop.data(), cs.matrix4x4())
            pelvis_MPP_prop.setData(pd)

            cs = pelvis_view.cameraCS_FPlane()
            pd = vmi.pdMatrix(pelvis_prop.data(), cs.inv().matrix4x4())
            b, c = pd.GetBounds(), pd.GetCenter()
            left_top = np.array([b[0], b[2], c[2]])
            right_top = np.array([b[1], b[2], c[2]])
            left_bottom = np.array([b[0], b[3], c[2]])
            right_bottom = np.array([b[1], b[3], c[2]])
            xn = int(np.round(0.1 * (pd.GetBounds()[1] - pd.GetBounds()[0])))

            lines = []
            for i in range(xn + 1):
                pts = [left_top + i / xn * (left_bottom - left_top),
                       right_top + i / xn * (right_bottom - right_top)]
                pts = [cs.mpt(pt) for pt in pts]
                line = vmi.ccEdge(vmi.ccSegment(pts[0], pts[1]))
                line = vmi.ccPd_Sh(line)
                lines.append(line)

            pd = vmi.pdAppend(lines)
            pelvis_cs_indicator_prop.setData(pd)

            pelvis_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())
        pelvis_cs_indicator_prop.setVisible(False)
        pelvis_MPP_prop.setVisible(False)

        # 横断
        update_cup_camera_axial()

        pelvis_slice_box.draw_text('断层')
        cup_prop.setVisible(False)
        pelvis_prop.setVisible(False)
        cup_section_prop.setVisible(True)
        cup_section_prop.setLineWidth(10)
        pelvis_slice.setVisible(True)

        pelvis_slice.setSlicePlane(cup_cs.origin(), pelvis_view.cameraVt_Look())
        pd = vmi.pdCut_Implicit(cup_prop.data(), pelvis_slice.slicePlane())
        cup_section_prop.setData(pd)

        if video:
            delta = vmi.imSpacing(pelvis_slice.data())[0]
            n = int(round(30 / delta))
            delta = 30 / n
            for _ in range(n):
                pelvis_slice.slice(delta=-delta)
                update_cup(False)
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(2 * n):
                pelvis_slice.slice(delta=delta)
                update_cup(False)
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(n):
                pelvis_slice.slice(delta=-delta)
                update_cup(False)
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(50):
                snapshots.append(snapshots[-1])
        else:
            pelvis_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

        # 冠状
        update_cup_camera_coronal()

        pelvis_slice_box.draw_text('断层')
        cup_prop.setVisible(False)
        pelvis_prop.setVisible(False)
        cup_section_prop.setVisible(True)
        pelvis_slice.setVisible(True)

        pelvis_slice.setSlicePlane(cup_cs.origin(), pelvis_view.cameraVt_Look())
        pd = vmi.pdCut_Implicit(cup_prop.data(), pelvis_slice.slicePlane())
        cup_section_prop.setData(pd)

        if video:
            delta = vmi.imSpacing(pelvis_slice.data())[1]
            n = int(round(30 / delta))
            delta = 30 / n
            for _ in range(n):
                pelvis_slice.slice(delta=-delta)
                update_cup(False)
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(2 * n):
                pelvis_slice.slice(delta=delta)
                update_cup(False)
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(n):
                pelvis_slice.slice(delta=-delta)
                update_cup(False)
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(50):
                snapshots.append(snapshots[-1])
        else:
            pelvis_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

        pelvis_slice_box.draw_text('三维')
        cup_prop.setVisible(True)
        pelvis_prop.setVisible(True)
        cup_section_prop.setVisible(False)
        cup_section_prop.setLineWidth(3)
        pelvis_slice.setVisible(False)

        # 正视
        if video:
            update_cup_camera_plane()
            for _ in range(30):
                pelvis_view.camera().Elevation(-1)
                pelvis_view.camera().OrthogonalizeViewUp()
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(60):
                pelvis_view.camera().Elevation(1)
                pelvis_view.camera().OrthogonalizeViewUp()
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(30):
                pelvis_view.camera().Elevation(-1)
                pelvis_view.camera().OrthogonalizeViewUp()
                pelvis_view.snapshot_PNG(str(f))
                snapshots.append(f.read_bytes())
            for _ in range(50):
                snapshots.append(snapshots[-1])
        else:
            aceta_prop.setVisible(True)
            guide_path_prop.setVisible(False)
            psi_match_prop.setVisible(False)
            psi_arm_prop.setVisible(False)
            psi_mold_prop.setVisible(False)
            update_cup_camera_plane()
            main.scrollArea().ensureWidgetVisible(pelvis_view)
            pelvis_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())
            main.scrollArea().ensureWidgetVisible(guide_view)
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

            aceta_prop.setVisible(True)
            guide_path_prop.setVisible(True)
            psi_match_prop.setVisible(True)
            psi_arm_prop.setVisible(False)
            psi_mold_prop.setVisible(False)
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

            aceta_prop.setVisible(True)
            guide_path_prop.setVisible(False)
            psi_match_prop.setVisible(True)
            psi_arm_prop.setVisible(True)
            psi_mold_prop.setVisible(False)
            guide_view.camera().Elevation(-30)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

            aceta_prop.setVisible(True)
            guide_path_prop.setVisible(False)
            psi_match_prop.setVisible(True)
            psi_arm_prop.setVisible(True)
            psi_mold_prop.setVisible(False)
            guide_view.camera().Elevation(-60)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.camera().Azimuth(LR * 90)
            guide_view.camera().Elevation(30)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

            aceta_prop.setVisible(False)
            guide_path_prop.setVisible(False)
            psi_match_prop.setVisible(True)
            psi_arm_prop.setVisible(True)
            psi_mold_prop.setVisible(False)
            guide_view.camera().Elevation(-90)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.setCamera_FitAll()
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

            aceta_prop.setVisible(False)
            guide_path_prop.setVisible(False)
            psi_match_prop.setVisible(True)
            psi_arm_prop.setVisible(True)
            psi_mold_prop.setVisible(True)
            update_cup_camera_plane()
            guide_view.camera().Elevation(-30)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.setCamera_FitAll()
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

            aceta_prop.setVisible(False)
            guide_path_prop.setVisible(False)
            psi_match_prop.setVisible(True)
            psi_arm_prop.setVisible(False)
            psi_mold_prop.setVisible(True)
            update_cup_camera_plane()
            guide_view.camera().Elevation(30)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.camera().Dolly(30)
            guide_view.camera().OrthogonalizeViewUp()
            guide_view.setCamera_FitAll()
            guide_view.snapshot_PNG(str(f))
            snapshots.append(f.read_bytes())

        aceta_prop.setVisible(visibles[0])
        guide_path_prop.setVisible(visibles[1])
        psi_match_prop.setVisible(visibles[2])
        psi_arm_prop.setVisible(visibles[3])
        psi_mold_prop.setVisible(visibles[4])
    return snapshots


def case_sync():
    global cup_radius, cup_RA, cup_RI
    with tempfile.TemporaryDirectory() as p:
        case_vti = {'pelvis_vti': original_slice.data(),
                    'acetabulum_vti': aceta_image}
        for kw in case_vti:
            f = str(pathlib.Path(p) / '{}.vtp'.format(kw))
            vmi.imSaveFile_XML(case_vti[kw], f)
            case_vti[kw] = f

        case_vtp = {'pelvis_vtp': pelvis_prop.data(),
                    'acetabulum_vtp': aceta_prop.data(),
                    'psi_match_vtp': psi_match_prop.data(),
                    'psi_arm_vtp': psi_arm_prop.data(),
                    'psi_arm_short_vtp': vmi.ccPd_Sh(psi_arm_short),
                    'psi_arm_long_vtp': vmi.ccPd_Sh(psi_arm_long),
                    'psi_mold_vtp': psi_mold_prop.data()}
        for kw in case_vtp:
            f = str(pathlib.Path(p) / '{}.vtp'.format(kw))
            vmi.pdSaveFile_XML(case_vtp[kw], f)
            case_vtp[kw] = f

        case_stl = {'psi_match_stl': psi_match_prop.data(),
                    'psi_arm_stl': psi_arm_prop.data(),
                    'psi_arm_short_stl': vmi.ccPd_Sh(psi_arm_short),
                    'psi_arm_long_stl': vmi.ccPd_Sh(psi_arm_long),
                    'psi_mold_stl': psi_mold_prop.data()}
        for kw in case_stl:
            f = str(pathlib.Path(p) / '{}.stl'.format(kw))
            vmi.pdSaveFile_STL(case_stl[kw], f)
            case_stl[kw] = f

        spc, dim = vmi.imSpacing(original_slice.data()), vmi.imDimensions(original_slice.data())
        pelvis_dicom_info = {'Modality': dicom_ds['Modality'],
                             'StudyDate': dicom_ds['StudyDate'],
                             'StudyDescription': dicom_ds['StudyDescription'],
                             'Resolution': dim.tolist(),
                             'Spacing': spc.tolist()}

        order_files = ['psi_match_stl', 'psi_arm_stl', 'psi_arm_short_stl', 'psi_arm_long_stl', 'psi_mold_stl']

        case = vmi.application.skyward.case(product_name='髋关节手术导板', product_model='TH',
                                            product_specification='定制式',
                                            app_name=main.appName(),
                                            app_version=main.appVersion(),
                                            order_uid=UDI,
                                            order_files=order_files,
                                            patient_name=dicom_ds['PatientName'],
                                            patient_sex=dicom_ds['PatientSex'],
                                            patient_age=dicom_ds['PatientAge'],
                                            dicom_files={'pelvis_dicom': series.filenames()},
                                            vti_files=case_vti,
                                            vtp_files=case_vtp,
                                            stl_files=case_stl,
                                            snapshot_list=case_snapshot(),
                                            pelvis_dicom_info=pelvis_dicom_info,
                                            surgical_side='L' if LR > 0 else 'R',
                                            pelvis_cs=pelvis_cs.array4x4().tolist(),
                                            body_cs=body_cs.array4x4().tolist(),
                                            head_cs=head_cs.array4x4().tolist(),
                                            cup_cs=cup_cs.array4x4().tolist(),
                                            cup_radius=round(cup_radius * 100) / 100,
                                            cup_RA=round(cup_RA * 100) / 100,
                                            cup_RI=round(cup_RI * 100) / 100,
                                            bone_value=bone_value,
                                            body_angle=body_angle,
                                            body_xr=body_xr,
                                            body_yr=body_yr,
                                            arm_length=arm_length,
                                            match_style=match_style)

        case = vmi.application.skyward.case_sync(case, [
            'product_name', 'product_model', 'pelvis_dicom', 'surgical_side'])

        if case is True:
            vmi.askInfo('同步完成')
        elif case:
            cup_radius = case['cup_radius']
            cup_RA = case['cup_RA']
            cup_RI = case['cup_RI']
            cup_radius_box.draw_value(cup_radius)
            cup_RA_box.draw_value(cup_RA)
            cup_RI_box.draw_value(cup_RI)
            on_cup()
            vmi.askInfo('同步完成')


def LeftButtonPress(**kwargs):
    if kwargs['picked'] is voi_view:
        if plcut_box.text() == '请勾画切割范围':
            pt = voi_view.pickPt_FocalPlane()
            plcut_pts.clear()
            plcut_pts.append(pt)
            update_line_cut()


def LeftButtonPressMove(**kwargs):
    global spcut_center, pelvis_cs
    if kwargs['picked'] is voi_view:
        if plcut_box.text() == '请勾画切割范围':
            pt = voi_view.pickPt_Cell()

            for path_pt in plcut_pts:
                if (path_pt == pt).all():
                    return

            plcut_pts.append(pt)  # 添加拾取路径点
            update_line_cut()
        else:
            voi_view.mouseRotateFocal(**kwargs)
        return True
    elif kwargs['picked'] is aceta_prop:
        if defect_path_box.text() == '请勾画缺陷范围':
            pt = guide_view.pickPt_Cell()

            for path_pt in defect_path_pts:
                if (path_pt == pt).all():
                    return

            defect_path_pts.append(pt)
            update_defect_path()
            return True
    elif kwargs['picked'] in [pelvis_view, pelvis_prop]:
        pelvis_view.mouseRotateFocal(**kwargs)
        if pelvis_MPP_box.text() == '确定':
            update_pelvis_MPP()
        elif pelvis_APP_box.text() == '确定':
            update_pelvis_APP()
        return True
    elif kwargs['picked'] in [spcut_prop, *spcut_y_props, *spcut_z_props]:
        spcut_center += kwargs['picked'].view().pickVt_FocalPlane()
        update_spcut()
        update_spcut_section()
        return True
    elif kwargs['picked'] in [cup_prop, cup_section_prop]:
        pt = pelvis_view.pickPt_FocalPlane()
        pt = vmi.ptOnPlane(pt, pelvis_cs.origin(), pelvis_view.cameraVt_Look())

        over = kwargs['picked'].view().pickVt_FocalPlane()
        if np.dot(pt - pelvis_cs.origin(), cup_cs.origin() - pelvis_cs.origin()) < 0:
            over = pelvis_cs.inv().mvt(over)
            over[0] *= -1
            over = pelvis_cs.mvt(over)

        cup_cs.setOrigin(cup_cs.origin() + over)
        update_cup_center()
        update_cup()
        return True
    elif kwargs['picked'] is pelvis_csx_prop:
        vt = pelvis_view.pickVt_FocalPlane()
        vt = vmi.vtOnVector(vt, pelvis_cs.axis(0))
        pelvis_cs.setOrigin(pelvis_cs.origin() + vt)
        update_pelvis_cs_prop()
        update_cup_center()
        return True
    elif kwargs['picked'] is pelvis_csy_prop:
        vt = pelvis_view.pickVt_FocalPlane()
        vt = vmi.vtOnVector(vt, pelvis_cs.axis(1))
        pelvis_cs.setOrigin(pelvis_cs.origin() + vt)
        update_pelvis_cs_prop()
        update_cup_center()
        return True
    elif kwargs['picked'] is pelvis_csz_prop:
        vt = pelvis_view.pickVt_FocalPlane()
        vt = vmi.vtOnVector(vt, pelvis_cs.axis(2))
        pelvis_cs.setOrigin(pelvis_cs.origin() + vt)
        update_pelvis_cs_prop()
        update_cup_center()
        return True


def LeftButtonPressMoveRelease(**kwargs):
    if kwargs['picked'] is voi_view:
        if plcut_box.text() == '请勾画切割范围':
            plcut_box.draw_text('请耐心等待')
            plcut_voi_image()
            plcut_box.draw_text('线切割')

            plcut_pts.clear()
            update_line_cut()
    elif kwargs['picked'] is aceta_prop:
        if defect_path_box.text() == '请勾画缺陷范围':
            global defect_path_pts
            if len(defect_path_pts) > 1:
                defect_path_list.append(defect_path_pts.copy())
            defect_path_pts.clear()
            update_defect_path()
            update_guide_path()
            clear_guide_plate()


def LeftButtonPressRelease(**kwargs):
    global spcut_radius, pelvis_cs, cup_radius, cup_cs, cup_RA, cup_RI, bone_value
    global body_angle, body_xr, body_yr, match_style, arm_length
    global pelvis_MPP_camera_cs, pelvis_APP_camera_cs, pelvis_MPP_camera_height, pelvis_APP_camera_height
    global defect_path_pts
    if kwargs['picked'] is dicom_box:
        image = read_dicom()
        if image:
            original_image = image
            clear_guide_plate()
            if original_image is not None:
                original_slice.setData(original_image)
                original_slice.setSlicePlaneOrigin_Center()
                original_slice.setSlicePlaneNormal_Coronal()
                original_view.setCamera_Coronal()
                original_view.setCamera_FitAll()
    elif kwargs['picked'] is original_slice:
        on_init_voi()
    elif kwargs['picked'] is plcut_box:
        if plcut_box.text() == '线切割':
            plcut_box.draw_text('请勾画切割范围')
        elif plcut_box.text() == '请勾画切割范围':
            plcut_box.draw_text('线切割')
    elif kwargs['picked'] is spcut_box:
        spcut_box.draw_text('请耐心等待')
        spcut_voi_image()
        spcut_box.draw_text('球切割')
        update_spcut_section()
    elif kwargs['picked'] is spcut_visible_box:
        spcut_prop.visibleToggle()
        spcut_visible_box.draw_text(
            back_color=QColor().fromRgbF(0.4, 0.6, 1) if spcut_prop.visible() else QColor('black'))
    elif kwargs['picked'] is spcut_radius_box:
        r = vmi.askInt(5, spcut_radius, 50)
        if r is not None:
            spcut_radius = r
            spcut_radius_box.draw_text('球半径：{:.0f} mm'.format(spcut_radius))
            update_spcut()
            update_spcut_section()
    elif kwargs['picked'] is init_pelvis_box:
        init_pelvis_box.draw_text('请耐心等待')
        init_pelvis()
        update_cup_orientation()
        update_cup()
        init_pelvis_box.draw_text('创建骨盆')
    elif kwargs['picked'] is cup_camera_sagittal_box:
        update_cup_camera_sagittal()
    elif kwargs['picked'] is cup_camera_coronal_box:
        update_cup_camera_coronal()
    elif kwargs['picked'] is cup_camera_axial_box:
        update_cup_camera_axial()
    elif kwargs['picked'] is cup_camera_RA_box:
        update_cup_camera_RA()
    elif kwargs['picked'] is cup_camera_RI_box:
        update_cup_camera_RI()
    elif kwargs['picked'] is cup_camera_plane_box:
        update_cup_camera_plane()
    elif kwargs['picked'] is pelvis_visible_box:
        pelvis_prop.visibleToggle()
        pelvis_visible_box.draw_text(
            back_color=QColor().fromRgbF(1, 1, 0.6) if pelvis_prop.visible() else QColor('black'))
    elif kwargs['picked'] is metal_visible_box:
        metal_prop.visibleToggle()
        metal_visible_box.draw_text(
            back_color=QColor().fromRgbF(1, 0.4, 0.4) if metal_prop.visible() else QColor('black'))
    elif kwargs['picked'] is pelvis_slice_box:
        if pelvis_slice_box.text() == '三维':
            pelvis_slice_box.draw_text('断层')
            cup_prop.setVisible(False)
            pelvis_prop.setVisible(False)
            cup_section_prop.setVisible(True)
            pelvis_slice.setVisible(True)

            pelvis_slice.setSlicePlane(cup_cs.origin(), pelvis_view.cameraVt_Look())
            pd = vmi.pdCut_Implicit(cup_prop.data(), pelvis_slice.slicePlane())
            cup_section_prop.setData(pd)
        elif pelvis_slice_box.text() == '断层':
            pelvis_slice_box.draw_text('三维')
            cup_prop.setVisible(True)
            pelvis_prop.setVisible(True)
            cup_section_prop.setVisible(False)
            pelvis_slice.setVisible(False)
    elif kwargs['picked'] is pelvis_MPP_box:
        if pelvis_MPP_box.text() == '标记对称面':
            pelvis_MPP_box.draw_text('确定')
            if pelvis_MPP_camera_cs:
                pelvis_view.setCamera_FPlane(pelvis_MPP_camera_cs, pelvis_MPP_camera_height)
            update_pelvis_MPP()
            pelvis_MPP_prop.setVisible(True)
            pelvis_cs_indicator_prop.setVisible(True)
        elif pelvis_MPP_box.text() == '确定':
            pelvis_MPP_box.draw_text('标记对称面')
            pelvis_MPP_camera_cs = pelvis_view.cameraCS_FPlane()
            pelvis_MPP_camera_height = pelvis_view.cameraCS_Height()
            pelvis_MPP_prop.setVisible(False)
            pelvis_cs_indicator_prop.setVisible(False)
    elif kwargs['picked'] is pelvis_APP_box:
        if pelvis_APP_box.text() == '标记前平面':
            pelvis_APP_box.draw_text('确定')
            if pelvis_APP_camera_cs:
                pelvis_view.setCamera_FPlane(pelvis_APP_camera_cs, pelvis_APP_camera_height)
            update_pelvis_APP()
            pelvis_cs_indicator_prop.setVisible(True)
        elif pelvis_APP_box.text() == '确定':
            pelvis_APP_box.draw_text('标记前平面')
            pelvis_APP_camera_cs = pelvis_view.cameraCS_FPlane()
            pelvis_APP_camera_height = pelvis_view.cameraCS_Height()
            pelvis_cs_indicator_prop.setVisible(False)
    elif kwargs['picked'] is init_guide_box:
        init_guide_box.draw_text('请耐心等待')
        init_guide()
        init_guide_box.draw_text('创建髋臼')
    elif kwargs['picked'] is case_sync_box:
        case_sync_box.draw_text('请耐心等待')
        case_sync()
        case_sync_box.draw_text('同步')
    elif kwargs['picked'] is aceta_visible_box:
        aceta_prop.visibleToggle()
        aceta_visible_box.draw_text(
            back_color=QColor().fromRgbF(1, 1, 0.6) if aceta_prop.visible() else QColor('black'))
    elif kwargs['picked'] is psi_match_visible_box:
        psi_match_prop.visibleToggle()
        psi_match_visible_box.draw_text(
            back_color=QColor().fromRgbF(0.4, 0.6, 1) if psi_match_prop.visible() else QColor('black'))
    elif kwargs['picked'] is guide_path_visible_box:
        guide_path_prop.visibleToggle()
        guide_path_visible_box.draw_text(
            back_color=QColor().fromRgbF(0.4, 1, 0.4) if guide_path_prop.visible() else QColor('black'))
    elif kwargs['picked'] is psi_arm_visible_box:
        psi_arm_prop.visibleToggle()
        psi_arm_visible_box.draw_text(
            back_color=QColor().fromRgbF(0.6, 0.8, 1) if psi_arm_prop.visible() else QColor('black'))
    elif kwargs['picked'] is mold_visible_box:
        psi_mold_prop.visibleToggle()
        mold_visible_box.draw_text(
            back_color=QColor().fromRgbF(1, 0.4, 0.4) if psi_mold_prop.visible() else QColor('black'))
    elif kwargs['picked'] is defect_path_box:
        if defect_path_box.text() == '标记缺陷':
            defect_path_box.draw_text('请勾画缺陷范围')
        elif defect_path_box.text() == '请勾画缺陷范围':
            defect_path_pts.clear()
            update_defect_path()
            defect_path_box.draw_text('标记缺陷')
    elif kwargs['picked'] is defect_path_clear_box:
        defect_path_pts.clear()
        update_defect_path()
        defect_path_list.clear()
        update_guide_path()
        clear_guide_plate()
    elif kwargs['picked'] is guide_update_box:
        guide_update_box.draw_text('请耐心等待')
        update_guide_path()
        update_guide_plate()
        guide_update_box.draw_text('更新导板')
    elif kwargs['picked'] is match_style_box:
        match_style = '上浮式' if match_style == '下沉式' else '下沉式'
        match_style_box.draw_text('匹配方式：{}'.format(match_style))
        update_guide_path()
        clear_guide_plate()
    elif kwargs['picked'] is skydio_box:
        savedir = vmi.askDirectory()
        if savedir is None:
            return

        if psi_match_prop.data().GetNumberOfCells():
            vmi.pdSaveFile_STL(psi_match_prop.data(), str(pathlib.Path(savedir) / '匹配板.stl'))
        if psi_mold_prop.data().GetNumberOfCells():
            vmi.pdSaveFile_STL(psi_mold_prop.data(), str(pathlib.Path(savedir) / '配模.stl'))
        if psi_arm_prop.data().GetNumberOfCells():
            vmi.pdSaveFile_STL(psi_arm_prop.data(), str(pathlib.Path(savedir) / '旋臂.stl'))
        if aceta_prop.data().GetNumberOfCells():
            vmi.pdSaveFile_STL(aceta_prop.data(), str(pathlib.Path(savedir) / '髋臼.stl'))
        if pelvis_prop.data().GetNumberOfCells():
            vmi.pdSaveFile_STL(pelvis_prop.data(), str(pathlib.Path(savedir) / '骨盆.stl'))
        if metal_prop.data().GetNumberOfCells():
            vmi.pdSaveFile_STL(metal_prop.data(), str(pathlib.Path(savedir) / '金属.stl'))

        c = head_cs.mpt([0, -LR * arm_length, head_z])
        kirs = vmi.ccPrism(vmi.ccFace(vmi.ccWire(vmi.ccCircle(
            kirs_hole_radius, c, head_cs.axis(2)))), -head_cs.axis(2), 200)
        vmi.pdSaveFile_STL(vmi.ccPd_Sh(kirs), str(pathlib.Path(savedir) / '导向针.stl'))

        c = head_cs.mpt([0, 0, head_z])
        kirs = vmi.ccPrism(vmi.ccFace(vmi.ccWire(vmi.ccCircle(
            kirs_hole_radius, c, head_cs.axis(2)))), -head_cs.axis(2), 200)
        vmi.pdSaveFile_STL(vmi.ccPd_Sh(kirs), str(pathlib.Path(savedir) / '固定针.stl'))

        cs = pelvis_cs.copy()
        (pathlib.Path(savedir) / '骨盆坐标系.json').write_text(json.dumps(cs.array4x4().tolist()))
        cs = body_cs.copy()
        cs.setOrigin(body_cs.mpt([0, 0, head_z]))
        (pathlib.Path(savedir) / '髋臼坐标系.json').write_text(json.dumps(cs.array4x4().tolist()))
        cs = head_cs.copy()
        cs.setOrigin(head_cs.mpt([0, 0, head_z]))
        (pathlib.Path(savedir) / '旋臂坐标系.json').write_text(json.dumps(cs.array4x4().tolist()))

        snapshots = case_snapshot(True)
        with tempfile.TemporaryDirectory() as p:
            xvid_writer = cv2.VideoWriter(str(pathlib.Path(p) / '.mp4'),
                                          cv2.VideoWriter_fourcc(*'XVID'),
                                          20, (guide_view.width(), guide_view.height()))

            for ba in snapshots:
                f = pathlib.Path(p) / '.png'
                f.write_bytes(ba)
                xvid_writer.write(cv2.imread(str(f)))
            xvid_writer.release()

            shutil.copy2(pathlib.Path(p) / '.mp4',
                         pathlib.Path(savedir) / '{} {}.mp4'.format(patient_name, 'L' if LR else 'R'))


def MidButtonPressMove(**kwargs):
    if kwargs['picked'] in [pelvis_view, pelvis_prop, pelvis_slice]:
        pelvis_view.mousePan()
        if pelvis_MPP_box.text() == '确定':
            update_pelvis_MPP()
        elif pelvis_APP_box.text() == '确定':
            update_pelvis_APP()
        return True


def RightButtonPressMove(**kwargs):
    if kwargs['picked'] in [pelvis_view, pelvis_prop, pelvis_slice]:
        pelvis_view.mouseZoom()
        if pelvis_MPP_box.text() == '确定':
            update_pelvis_MPP()
        elif pelvis_APP_box.text() == '确定':
            update_pelvis_APP()
        return True


def NoButtonWheel(**kwargs):
    global bone_value, spcut_radius, cup_radius, cup_RA, cup_RI
    global body_angle, body_xr, body_yr, kirs_radius
    if kwargs['picked'] is spcut_radius_box:
        spcut_radius = min(max(spcut_radius + kwargs['delta'], 5), 50)
        spcut_radius_box.draw_text('球半径：{:.0f} mm'.format(spcut_radius))
        update_spcut()
        update_spcut_section()
    elif kwargs['picked'] in [pelvis_view, pelvis_prop]:
        pelvis_view.mouseRotateLook(**kwargs)
        if pelvis_MPP_box.text() == '确定':
            update_pelvis_MPP()
        elif pelvis_APP_box.text() == '确定':
            update_pelvis_APP()
        return True
    elif kwargs['picked'] is pelvis_slice:
        update_cup()


def on_bone_value():
    global bone_value
    bone_value = bone_value_box.value()
    voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
    clear_guide_plate()


def on_cup():
    global cup_radius, cup_RA, cup_RI
    cup_radius = cup_radius_box.value()
    cup_RA = cup_RA_box.value()
    cup_RI = cup_RI_box.value()
    update_cup_orientation()
    update_cup()
    clear_guide_plate()


def on_guide():
    global body_offsetX, body_offsetY, body_angle, body_xr, body_yr, arm_length, head_depth
    body_offsetX = body_offsetX_box.value()
    body_offsetY = body_offsetY_box.value()
    body_angle = body_angle_box.value()
    body_xr = body_xr_box.value()
    body_yr = body_yr_box.value()
    head_depth = head_depth_box.value()
    arm_length = arm_length_box.value()
    update_guide_path()
    clear_guide_plate()


def return_globals():
    return globals()


if __name__ == '__main__':
    global original_view, voi_view, spcut_y_views, spcut_z_views, pelvis_view, guide_view
    main = vmi.Main(return_globals)
    main.setAppName('Propsi TH')
    main.setAppVersion('1.2.3')
    main.excludeKeys += ['main', 'i', 'box', 'prop', 'voi_image']

    select = vmi.askButtons(['新建', '打开'], title=main.appName())
    if select is None:
        vmi.appexit()

    if select == '打开':
        open_file = vmi.askOpenFile(nameFilter='*.vmi', title='存档')
        if open_file is not None:
            main.loads(pathlib.Path(open_file).read_bytes())
        else:
            vmi.appexit()
    elif select == '新建':
        patient_name = str()

        # 0 原始图像
        original_target, LR = np.zeros(3), 1
        original_view = vmi.View()

        original_slice = vmi.ImageSlice(original_view)  # 断层显示
        original_slice.setColorWindow_Bone()
        original_slice.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        dicom_box = vmi.TextBox(original_view, text='DICOM', pickable=True,
                                size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0])
        dicom_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        patient_name_box = vmi.TextBox(original_view, text='姓名', visible=False,
                                       size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])
        patient_LR_box = vmi.TextBox(original_view, text='患侧', visible=False,
                                     size=[0.2, 0.04], pos=[0, 0.14], anchor=[0, 0])

        # 1 目标区域
        voi_view = vmi.View()
        voi_view.mouse['LeftButton']['Press'] = [LeftButtonPress]
        voi_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        voi_view.mouse['LeftButton']['PressMoveRelease'] = [LeftButtonPressMoveRelease]

        bone_value, background_value = 200, -1100

        bone_value_box = vmi.ValueBox(voi_view, value_format='骨阈值：{:.0f} HU',
                                      value_min=-1000, value=bone_value, value_max=3000,
                                      value_decimals=0, value_step=1, value_update=on_bone_value,
                                      size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)

        voi_size, voi_center, voi_origin, voi_cs = np.zeros(3), np.zeros(3), np.zeros(3), vmi.CS4x4()
        voi_image = vtk.vtkImageData()

        voi_volume = vmi.ImageVolume(voi_view, pickable=True)
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
        voi_volume.setColor({bone_value: [1, 1, 0.6]})

        # 线切割
        plcut_pts = []
        plcut_prop = vmi.PolyActor(voi_view, color=[1, 0.6, 0.6], line_width=3, always_on_top=True)

        # 球切割
        spcut_center, spcut_radius, spcut_length = np.zeros(3), 22, 200
        spcut_prop = vmi.PolyActor(voi_view, color=[0.4, 0.6, 1], pickable=True)
        spcut_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        plcut_box = vmi.TextBox(voi_view, text='线切割', size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0], pickable=True)
        plcut_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        spcut_box = vmi.TextBox(voi_view, text='球切割', size=[0.2, 0.04], pos=[0, 0.16], anchor=[0, 0], pickable=True)
        spcut_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        spcut_visible_box = vmi.TextBox(voi_view, size=[0.01, 0.04], pos=[0.2, 0.16], anchor=[1, 0],
                                        back_color=QColor().fromRgbF(0.4, 0.6, 1), pickable=True)
        spcut_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        spcut_radius_box = vmi.TextBox(voi_view, text='球半径：{:.0f} mm'.format(spcut_radius),
                                       size=[0.2, 0.04], pos=[0, 0.20], anchor=[0, 0], pickable=True)
        spcut_radius_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        spcut_radius_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        # 234 球切割局部
        spcut_y_views = [vmi.View(), vmi.View(), vmi.View()]
        spcut_z_views = [vmi.View(), vmi.View(), vmi.View()]

        for i in spcut_y_views + spcut_z_views:
            i.mouse['LeftButton']['PressMove'] = [i.mouseBlock]

        spcut_y_boxs = [vmi.TextBox(spcut_y_views[i], text=['斜冠状位', '正冠状位', '斜冠状位'][i],
                                    size=[0.2, 0.1], pos=[1, 1], anchor=[1, 1]) for i in range(3)]
        spcut_z_boxs = [vmi.TextBox(spcut_z_views[i], text=['斜横断位', '正横断位', '斜横断位'][i],
                                    size=[0.2, 0.1], pos=[1, 1], anchor=[1, 1]) for i in range(3)]

        spcut_y_slices = [vmi.ImageSlice(v) for v in spcut_y_views]
        spcut_z_slices = [vmi.ImageSlice(v) for v in spcut_z_views]

        for i in spcut_y_slices + spcut_z_slices:
            i.bindData(voi_volume)
            i.mouse['NoButton']['Wheel'] = [i.mouseBlock]

        spcut_y_props = [vmi.PolyActor(v, color=[0.4, 0.6, 1], opacity=0.5, pickable=True) for v in spcut_y_views]
        spcut_z_props = [vmi.PolyActor(v, color=[0.4, 0.6, 1], opacity=0.5, pickable=True) for v in spcut_z_views]

        for i in spcut_y_props + spcut_z_props:
            i.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        init_pelvis_box = vmi.TextBox(voi_view, text='创建骨盆', fore_color=QColor('white'), back_color=QColor('crimson'),
                                      bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0], pickable=True)
        init_pelvis_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        # 5 骨盆规划
        pelvis_view = vmi.View()
        pelvis_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        pelvis_view.mouse['MidButton']['PressMove'] = [MidButtonPressMove]
        pelvis_view.mouse['RightButton']['PressMove'] = [RightButtonPressMove]
        pelvis_view.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        pelvis_prop = vmi.PolyActor(pelvis_view, pickable=True, highlightable=False)
        pelvis_prop.setColor(QColor(250, 246, 222))
        pelvis_prop.prop_property().SetAmbient(0.2)
        pelvis_prop.prop_property().SetDiffuse(0.8)
        pelvis_prop.prop_property().SetSpecular(0.1)
        pelvis_prop.prop_property().SetSpecularPower(10)
        pelvis_prop.mouse['LeftButton']['PressMove'] = pelvis_view.mouse['LeftButton']['PressMove']
        pelvis_prop.mouse['MidButton']['PressMove'] = pelvis_view.mouse['MidButton']['PressMove']
        pelvis_prop.mouse['RightButton']['PressMove'] = pelvis_view.mouse['RightButton']['PressMove']
        pelvis_prop.mouse['NoButton']['Wheel'] = pelvis_view.mouse['NoButton']['Wheel']

        metal_prop = vmi.PolyActor(pelvis_view, color=[1, 0.4, 0.4])

        pelvis_csx_prop = vmi.PolyActor(pelvis_view, color=[1, 0, 0], line_width=3, always_on_top=True, pickable=True)
        pelvis_csx_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        pelvis_csy_prop = vmi.PolyActor(pelvis_view, color=[0, 1, 0], line_width=3, always_on_top=True, pickable=True)
        pelvis_csy_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        pelvis_csz_prop = vmi.PolyActor(pelvis_view, color=[0, 0, 1], line_width=3, always_on_top=True, pickable=True)
        pelvis_csz_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        pelvis_cs, cup_cs = vmi.CS4x4(), vmi.CS4x4()
        pelvis_APP_camera_cs, pelvis_MPP_camera_cs = None, None
        pelvis_APP_camera_height, pelvis_MPP_camera_height = 300, 300
        cup_radius, cup_RA, cup_RI = 22, 20, 40
        cup_prop = vmi.PolyActor(pelvis_view, color=[0.4, 0.6, 1], line_width=3, pickable=True)
        cup_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        cup_location_box = vmi.TextBox(pelvis_view, text='{:.3f}, {:.3f}, {:.3f}'.format(0, 0, 0),
                                       size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=False)

        cup_radius_box = vmi.ValueBox(pelvis_view, value_format='半径：{:.0f} mm',
                                      value_min=15, value=cup_radius, value_max=40,
                                      value_decimals=0, value_step=1, value_update=on_cup,
                                      size=[0.2, 0.04], pos=[0, 0.08], anchor=[0, 0], pickable=True)

        cup_RA_box = vmi.ValueBox(pelvis_view, value_format='前倾角：{:.1f}°',
                                  value_min=-30, value=cup_RA, value_max=60,
                                  value_decimals=1, value_step=0.1, value_update=on_cup,
                                  size=[0.2, 0.04], pos=[0, 0.14], anchor=[0, 0], pickable=True)

        cup_RI_box = vmi.ValueBox(pelvis_view, value_format='外展角：{:.1f}°',
                                  value_min=10, value=cup_RI, value_max=70,
                                  value_decimals=1, value_step=0.1, value_update=on_cup,
                                  size=[0.2, 0.04], pos=[0, 0.18], anchor=[0, 0], pickable=True)

        pelvis_slice = vmi.ImageSlice(pelvis_view, visible=False)
        pelvis_slice.bindData(voi_volume)
        pelvis_slice.mouse['MidButton']['PressMove'] = [MidButtonPressMove]
        pelvis_slice.mouse['RightButton']['PressMove'] = [RightButtonPressMove]
        pelvis_slice.mouse['NoButton']['Wheel'] += [NoButtonWheel]

        original_slice.bindColorWindow(spcut_y_slices + spcut_z_slices + [pelvis_slice], original_slice.colorWindow())

        cup_section_prop = vmi.PolyActor(pelvis_view, color=[0.4, 0.6, 1], line_width=3, visible=False, pickable=True)
        cup_section_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        pelvis_slice_box = vmi.TextBox(pelvis_view, text='三维', pickable=True,
                                       size=[0.16, 0.04], pos=[0, 0.24], anchor=[0, 0])
        pelvis_slice_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        pelvis_visible_box = vmi.TextBox(pelvis_view, size=[0.02, 0.04], pos=[0.16, 0.24], anchor=[0, 0],
                                         back_color=QColor().fromRgbF(1, 1, 0.6), pickable=True)
        pelvis_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        metal_visible_box = vmi.TextBox(pelvis_view, size=[0.02, 0.04], pos=[0.18, 0.24], anchor=[0, 0],
                                        back_color=QColor().fromRgbF(1, 0.4, 0.4), pickable=True)
        metal_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        pelvis_APP_box = vmi.TextBox(pelvis_view, text='标记前平面', pickable=True,
                                     size=[0.2, 0.04], pos=[0, 0.3], anchor=[0, 0])
        pelvis_APP_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        pelvis_MPP_box = vmi.TextBox(pelvis_view, text='标记对称面', pickable=True,
                                     size=[0.2, 0.04], pos=[0, 0.34], anchor=[0, 0])
        pelvis_MPP_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_sagittal_box = vmi.TextBox(pelvis_view, text='矢状', pickable=True,
                                              size=[0.06, 0.04], pos=[0.32, 0.04], anchor=[0, 0])
        cup_camera_sagittal_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_coronal_box = vmi.TextBox(pelvis_view, text='冠状', pickable=True,
                                             size=[0.06, 0.04], pos=[0.38, 0.04], anchor=[0, 0])
        cup_camera_coronal_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_axial_box = vmi.TextBox(pelvis_view, text='横断', pickable=True,
                                           size=[0.06, 0.04], pos=[0.44, 0.04], anchor=[0, 0])
        cup_camera_axial_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_RA_box = vmi.TextBox(pelvis_view, text='前倾', pickable=True,
                                        size=[0.06, 0.04], pos=[0.5, 0.04], anchor=[0, 0])
        cup_camera_RA_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_RI_box = vmi.TextBox(pelvis_view, text='外展', pickable=True,
                                        size=[0.06, 0.04], pos=[0.56, 0.04], anchor=[0, 0])
        cup_camera_RI_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_plane_box = vmi.TextBox(pelvis_view, text='正视', pickable=True,
                                           size=[0.06, 0.04], pos=[0.62, 0.04], anchor=[0, 0])
        cup_camera_plane_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        pelvis_MPP_prop = vmi.PolyActor(pelvis_view, visible=False, color=[1, 0.4, 0.4], repres='points')
        pelvis_cs_indicator_prop = vmi.PolyActor(pelvis_view, visible=False, color=[1, 0.4, 0.4], line_width=3,
                                                 always_on_top=True)

        init_guide_box = vmi.TextBox(pelvis_view, text='创建髋臼', pickable=True,
                                     fore_color=QColor('white'), back_color=QColor('crimson'),
                                     bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0])
        init_guide_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        # 8 导板
        guide_view = vmi.View()
        guide_view.bindCamera([pelvis_view])

        aceta_image = vtk.vtkImageData()

        aceta_prop = vmi.PolyActor(guide_view, pickable=True, highlightable=False)
        aceta_prop.setColor(QColor(250, 246, 222))
        aceta_prop.prop_property().SetAmbient(0.2)
        aceta_prop.prop_property().SetDiffuse(0.8)
        aceta_prop.prop_property().SetSpecular(0.1)
        aceta_prop.prop_property().SetSpecularPower(10)
        aceta_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        aceta_prop.mouse['LeftButton']['PressMoveRelease'] = [LeftButtonPressMoveRelease]
        aceta_prop.mouse['MidButton']['PressMove'] = guide_view.mouse['MidButton']['PressMove']
        aceta_prop.mouse['RightButton']['PressMove'] = guide_view.mouse['RightButton']['PressMove']
        aceta_prop.mouse['NoButton']['Wheel'] = guide_view.mouse['NoButton']['Wheel']

        guide_path = vmi.TopoDS_Shape()  # 引导线
        guide_path_prop = vmi.PolyActor(guide_view, color=[0.4, 1, 0.4], line_width=3)

        psi_match = vmi.TopoDS_Shape()  # 主板
        psi_match_prop = vmi.PolyActor(guide_view)
        psi_match_prop.setColor(QColor(127, 160, 212))
        psi_match_prop.prop_property().SetAmbient(0.2)
        psi_match_prop.prop_property().SetDiffuse(0.8)
        psi_match_prop.prop_property().SetSpecular(0.1)
        psi_match_prop.prop_property().SetSpecularPower(10)

        psi_arm = vmi.TopoDS_Shape()  # 旋臂
        psi_arm_short = vmi.TopoDS_Shape()
        psi_arm_long = vmi.TopoDS_Shape()
        psi_arm_prop = vmi.PolyActor(guide_view)
        psi_arm_prop.setColor(QColor(180, 202, 234))
        psi_arm_prop.prop_property().SetAmbient(0.2)
        psi_arm_prop.prop_property().SetDiffuse(0.8)
        psi_arm_prop.prop_property().SetSpecular(0.1)
        psi_arm_prop.prop_property().SetSpecularPower(10)
        psi_arm_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        psi_mold = vmi.TopoDS_Shape()  # 配模
        psi_mold_prop = vmi.PolyActor(guide_view)
        psi_mold_prop.setColor(QColor(233, 124, 132))
        psi_mold_prop.prop_property().SetAmbient(0.2)
        psi_mold_prop.prop_property().SetDiffuse(0.8)
        psi_mold_prop.prop_property().SetSpecular(0.1)
        psi_mold_prop.prop_property().SetSpecularPower(10)

        body_offsetX, body_offsetY = 0, 0
        body_angle = 0  # 主体方位
        body_xr, body_yr = 20, 15  # 主体长径宽径，臼窝匹配块
        head_depth = 25  # 边缘深度
        arm_length = 35  # 旋臂长度
        match_style = '下沉式'
        kirs_radius = 1  # 导向孔半径

        body_offset_box = vmi.TextBox(guide_view, text='偏移：', pickable=False,
                                      size=[0.08, 0.04], pos=[0, 0.04], anchor=[0, 0])
        body_offsetX_box = vmi.ValueBox(guide_view, value_format='{:.0f} mm',
                                        value_min=-100, value=body_offsetX, value_max=100,
                                        value_decimals=0, value_step=1, value_update=on_guide,
                                        size=[0.06, 0.04], pos=[0.08, 0.04], anchor=[0, 0], pickable=True)
        body_offsetY_box = vmi.ValueBox(guide_view, value_format='{:.0f} mm',
                                        value_min=-100, value=body_offsetY, value_max=100,
                                        value_decimals=0, value_step=1, value_update=on_guide,
                                        size=[0.06, 0.04], pos=[0.14, 0.04], anchor=[0, 0], pickable=True)

        body_angle_box = vmi.ValueBox(guide_view, value_format='主体方位：{:.0f}°',
                                      value_min=-45, value=body_angle, value_max=45,
                                      value_decimals=0, value_step=1, value_update=on_guide,
                                      size=[0.2, 0.04], pos=[0, 0.08], anchor=[0, 0], pickable=True)
        body_xr_box = vmi.ValueBox(guide_view, value_format='主体长径：{:.0f} mm',
                                   value_min=10, value=body_xr, value_max=60,
                                   value_decimals=0, value_step=1, value_update=on_guide,
                                   size=[0.2, 0.04], pos=[0, 0.12], anchor=[0, 0], pickable=True)
        body_yr_box = vmi.ValueBox(guide_view, value_format='主体宽径：{:.0f} mm',
                                   value_min=10, value=body_yr, value_max=60,
                                   value_decimals=0, value_step=1, value_update=on_guide,
                                   size=[0.2, 0.04], pos=[0, 0.16], anchor=[0, 0], pickable=True)
        head_depth_box = vmi.ValueBox(guide_view, value_format='边缘深度：{:.0f} mm',
                                      value_min=5, value=head_depth, value_max=50,
                                      value_decimals=0, value_step=1, value_update=on_guide,
                                      size=[0.2, 0.04], pos=[0, 0.2], anchor=[0, 0], pickable=True)
        arm_length_box = vmi.ValueBox(guide_view, value_format='旋臂长度：{:.0f} mm',
                                      value_min=10, value=arm_length, value_max=60,
                                      value_decimals=0, value_step=1, value_update=on_guide,
                                      size=[0.2, 0.04], pos=[0, 0.24], anchor=[0, 0], pickable=True)

        match_style_box = vmi.TextBox(guide_view, text='匹配方式：{}'.format(match_style), pickable=True,
                                      size=[0.2, 0.04], pos=[0, 0.28], anchor=[0, 0])
        match_style_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        defect_path_pts, defect_path_list = [], []
        defect_path_prop = vmi.PolyActor(guide_view, color=[1, 1, 0])

        defect_path_box = vmi.TextBox(guide_view, text='标记缺陷', pickable=True,
                                      size=[0.10, 0.04], pos=[0, 0.34], anchor=[0, 0])
        defect_path_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        defect_path_clear_box = vmi.TextBox(guide_view, text='清空', pickable=True,
                                            size=[0.10, 0.04], pos=[0.10, 0.34], anchor=[0, 0])
        defect_path_clear_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        guide_update_box = vmi.TextBox(guide_view, text='更新导板', pickable=True,
                                       size=[0.10, 0.04], pos=[0, 0.38], anchor=[0, 0])
        guide_update_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        aceta_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(1, 1, 0.6),
                                        size=[0.02, 0.04], pos=[0.10, 0.38], anchor=[0, 0])
        aceta_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        guide_path_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(0.4, 1, 0.4),
                                             size=[0.02, 0.04], pos=[0.12, 0.38], anchor=[0, 0])
        guide_path_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        psi_match_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(0.4, 0.6, 1),
                                            size=[0.02, 0.04], pos=[0.14, 0.38], anchor=[0, 0])
        psi_match_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        psi_arm_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(0.6, 0.8, 1),
                                          size=[0.02, 0.04], pos=[0.16, 0.38], anchor=[0, 0])
        psi_arm_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        mold_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(1, 0.4, 0.4),
                                       size=[0.02, 0.04], pos=[0.18, 0.38], anchor=[0, 0])
        mold_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        case_sync_box = vmi.TextBox(guide_view, text='同步', pickable=True,
                                    fore_color=QColor('white'), back_color=QColor('crimson'),
                                    bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0])
        case_sync_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        skydio_box = vmi.TextBox(guide_view, text='skydio', pickable=True,
                                 size=[0.2, 0.04], pos=[1, 0.10], anchor=[1, 0])
        skydio_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        # output_box = vmi.TextBox(guide_view, text='导出方案', fore_color=QColor('white'), back_color=QColor('crimson'),
        #                          bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0], pickable=True)
        # output_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        for v in [original_view, voi_view, *spcut_y_views, *spcut_z_views, pelvis_view, guide_view]:
            v.setEnabled(False)
        original_view.setEnabled(True)

    # 视图布局
    for v in [original_view, voi_view, *spcut_y_views, *spcut_z_views, pelvis_view, guide_view]:
        v.setMinimumWidth(round(0.5 * main.screenWidth()))

    for v in spcut_y_views + spcut_z_views:
        v.setMinimumWidth(round(0.25 * main.screenWidth()))

    original_view.setParent(main.scrollArea())
    main.layout().addWidget(original_view, 0, 0, 3, 1)
    main.layout().addWidget(voi_view, 0, 1, 3, 1)
    main.layout().addWidget(spcut_y_views[0], 0, 2, 1, 1)
    main.layout().addWidget(spcut_y_views[1], 1, 2, 1, 1)
    main.layout().addWidget(spcut_y_views[2], 2, 2, 1, 1)
    main.layout().addWidget(spcut_z_views[0], 0, 3, 1, 1)
    main.layout().addWidget(spcut_z_views[1], 1, 3, 1, 1)
    main.layout().addWidget(spcut_z_views[2], 2, 3, 1, 1)
    main.layout().addWidget(pelvis_view, 0, 4, 3, 1)
    main.layout().addWidget(guide_view, 0, 5, 3, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
