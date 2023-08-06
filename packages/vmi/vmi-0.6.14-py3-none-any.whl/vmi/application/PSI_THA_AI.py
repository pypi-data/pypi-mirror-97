import warnings

import pathlib
import math
import tempfile
import time

import nibabel as nib
import numpy as np
import pydicom
import vtk

import SimpleITK
from PySide2.QtGui import *
from typing import Union, Optional, List
from numba import jit
from acetabular_segment import bulid_model, get_center, get_radius
from pelvis_mark_detection import get_pts
import vmi


def ary_flip_pre(ary: np.ndarray):
    return np.flip(np.flip(ary.swapaxes(0, 2), 1), 0)


def pre_flip_ary(ary: np.ndarray):
    return np.flip(np.flip(ary, 0), 1).swapaxes(0, 2)


def bone_win_nor(image_data):
    image_data[image_data < -100] = -100
    image_data[image_data > 900] = 900
    image_data = (image_data + 100) / 1000
    return image_data


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


def imReslice(image: vtk.vtkImageData,
              cs: Optional[vmi.CS4x4] = None,
              size: Union[np.ndarray, List[float]] = None,
              back_scalar: Union[int, float] = 0) -> vtk.vtkImageData:
    if cs is None:
        cs = vmi.CS4x4()

    if size is None:
        size = [vmi.imSize_Vt(image, cs.axis(0)) + 1,
                vmi.imSize_Vt(image, cs.axis(1)) + 1,
                vmi.imSize_Vt(image, cs.axis(2)) + 1]

    spc = np.array([1, 1, 1])

    ext = [0, int(size[0]) - 1,
           0, int(size[1]) - 1,
           0, int(size[2]) - 1]

    re = vtk.vtkImageReslice()
    re.SetInputData(image)
    re.SetInterpolationModeToCubic()
    re.SetResliceAxes(cs.matrix4x4())
    re.SetOutputOrigin([0, 0, 0])
    re.SetOutputSpacing(spc)
    re.SetOutputExtent(ext)
    re.SetBackgroundLevel(back_scalar)
    re.Update()

    return re.GetOutput()


def modelToLargestRegion(image: vtk.vtkImageData):
    fe = vtk.vtkFlyingEdges3D()
    fe.SetInputData(image)
    fe.SetValue(0, bone_value)
    fe.SetComputeNormals(0)
    fe.SetComputeGradients(0)
    fe.SetComputeScalars(0)
    fe.Update()

    pdcf = vtk.vtkPolyDataConnectivityFilter()
    pdcf.SetInputData(fe.GetOutput())
    pdcf.SetExtractionModeToLargestRegion()
    pdcf.Update()

    smooth = vtk.vtkSmoothPolyDataFilter()
    smooth.SetInputData(pdcf.GetOutput())
    smooth.SetNumberOfIterations(20)
    smooth.Update()

    sinc = vtk.vtkWindowedSincPolyDataFilter()
    sinc.SetInputData(smooth.GetOutput())
    sinc.SetNumberOfIterations(20)
    sinc.SetBoundarySmoothing(0)
    sinc.SetFeatureEdgeSmoothing(0)
    sinc.SetFeatureAngle(60)
    sinc.SetPassBand(0.1)
    sinc.SetNonManifoldSmoothing(1)
    sinc.SetNormalizeCoordinates(1)
    sinc.Update()

    return sinc.GetOutput()


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
    global LR, original_target, voi_center
    original_target = original_view.pickPt_Cell()
    voi_center = np.array([vmi.imCenter(original_slice.data())[0], original_target[1], original_target[2]])

    LR = 1 if original_target[0] > voi_center[0] else -1
    patient_LR_box.draw_text('患侧：{}'.format('左' if LR > 0 else '右'))
    patient_LR_box.setVisible(True)


def init_voi():
    global voi_image
    voi_image = original_slice.data()
    voi_volume.setData(voi_image)

    voi_view.setCamera_Axial()
    voi_view.setCamera_FitAll()


def co_mark_pts():
    global td_pts, pts_dict
    cs = vmi.CS4x4(axis0=np.array([1, 0, 0]),
                   axis1=np.array([0, 1, 0]),
                   axis2=np.array([0, 0, 1]),
                   origin=np.array([0, 0, 0]))

    image = imReslice(voi_image, cs)
    np_data = vmi.imArray_VTK(image)
    pts_dict = get_pts(np_data)

    prop_list = []

    for key in pts_dict:
        prop_list.append(vmi.pdSphere(3, pts_dict[key][0]))
        prop_list.append(vmi.pdSphere(3, pts_dict[key][1]))

    pts_prop.setData(vmi.pdAppend(prop_list))

    td_pts = pts_dict['泪滴']


def init_pelvis():
    global cup_center, cup_radius, ace_center, pre_image, pelvis_cs
    if td_pts[0].sum() != 0 and td_pts[1].sum() != 0:
        cs = vmi.CS4x4(axis0=np.array([1, 0, 0]),
                       axis1=np.array([0, 1, 0]),
                       axis2=np.array([0, 0, 1]),
                       origin=vmi.imOrigin(voi_image))

        seg_origin_pts = [td_pts[0] - 64 * cs.axis(0) - 48 * cs.axis(1) - 32 * cs.axis(2),
                          td_pts[1] - 32 * cs.axis(0) - 48 * cs.axis(1) - 32 * cs.axis(2)]

        seg_cs = [vmi.CS4x4(axis0=np.array([1, 0, 0]),
                            axis1=np.array([0, 1, 0]),
                            axis2=np.array([0, 0, 1]),
                            origin=seg_origin_pts[0]),
                  vmi.CS4x4(axis0=np.array([1, 0, 0]),
                            axis1=np.array([0, 1, 0]),
                            axis2=np.array([0, 0, 1]),
                            origin=seg_origin_pts[1])]

        size = np.array([96, 96, 96])
        seg_image = [imReslice(voi_image, seg_cs[0], size),
                     imReslice(voi_image, seg_cs[1], size)]

        seg_image[0].SetOrigin(seg_cs[0].origin())
        seg_image[1].SetOrigin(seg_cs[1].origin())

        model = bulid_model('sdf_model.h5')
        seg_ary = [vmi.imArray_VTK(seg_image[0]),
                   vmi.imArray_VTK(seg_image[1])]
        seg_pre = [np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[0]))[np.newaxis, :, :, :, np.newaxis])),
                   np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[1]))[np.newaxis, :, :, :, np.newaxis]))]
        seg_pre[0] = pre_flip_ary(seg_pre[0])
        seg_pre[1] = pre_flip_ary(seg_pre[1])

        voi_ext = np.array([vmi.imExtent(voi_image)[1] + 1,
                            vmi.imExtent(voi_image)[3] + 1,
                            vmi.imExtent(voi_image)[5] + 1])

        voi_ary = vmi.imArray_VTK(imReslice(voi_image, cs, voi_ext))

        seg_ijk_ori = [np.array((seg_origin_pts[0] - vmi.imOrigin(voi_image))).astype('int16'),
                       np.array((seg_origin_pts[1] - vmi.imOrigin(voi_image))).astype('int16')]

        voi_ary[voi_ary < bone_value] = -1024
        voi_ary[voi_ary >= bone_value] = 3200

        _cp = np.array(seg_pre.copy())
        seg_pre[0][_cp[0] < target_value] = 3200
        seg_pre[0][_cp[0] >= target_value] = -1024

        seg_pre[1][_cp[1] < target_value] = 3200
        seg_pre[1][_cp[1] >= target_value] = -1024

        voi_ary[seg_ijk_ori[0][2]:seg_ijk_ori[0][2] + 96,
        seg_ijk_ori[0][1]:seg_ijk_ori[0][1] + 96,
        seg_ijk_ori[0][0]:seg_ijk_ori[0][0] + 96] = seg_pre[0]

        voi_ary[seg_ijk_ori[1][2]:seg_ijk_ori[1][2] + 96,
        seg_ijk_ori[1][1]:seg_ijk_ori[1][1] + 96,
        seg_ijk_ori[1][0]:seg_ijk_ori[1][0] + 96] = seg_pre[1]

        pre_image = vmi.imVTK_Array(voi_ary, cs.origin(), [1, 1, 1])

        # 均值滤波
        itk_image: SimpleITK.Image = vmi.imSITK_VTK(pre_image)
        smooth = SimpleITK.MeanImageFilter()
        smooth.SetRadius([1, 1, 1])
        itk_image = smooth.Execute(itk_image)
        pre_image = vmi.imVTK_SITK(itk_image)

        original_slice.setData(pre_image)

        pd = modelToLargestRegion(pre_image)
        pelvis_prop.setData(pd)
        pelvis_view.setCamera_Coronal()
        pelvis_view.setCamera_FitAll()

        model.load_weights('placement_model.h5')
        pre = [np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[0]))[np.newaxis, :, :, :, np.newaxis])),
               np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[1]))[np.newaxis, :, :, :, np.newaxis]))]
        pre[0] = pre_flip_ary(pre[0])
        pre[1] = pre_flip_ary(pre[1])

        ace_center = [get_center(pre[0]) + seg_ijk_ori[0], get_center(pre[1]) + seg_ijk_ori[1]]
        ace_radius = [get_radius(pre[0]), get_radius(pre[1])]

        cup_prop.setData(vmi.pdAppend([vmi.pdSphere(ace_radius[0], ace_center[0]),
                                       vmi.pdSphere(ace_radius[1], ace_center[1])]))

        if LR == -1:
            cup_cs.setOrigin(ace_center[0])
            cup_radius = ace_radius[0]
            cup_radius_box.draw_text('半径：{:.0f} mm'.format(cup_radius))
        elif LR == 1:
            cup_cs.setOrigin(ace_center[1])
            cup_radius = ace_radius[1]
            cup_radius_box.draw_text('半径：{:.0f} mm'.format(cup_radius))

        update_pelvis_APP()

        # # 保存
        # nib.save(nib.Nifti1Image(bone_win_nor(ary_flip_pre(seg_ary[0])), None), 'p0.nii.gz')
        # nib.save(nib.Nifti1Image(bone_win_nor(ary_flip_pre(seg_ary[1])), None), 'p1.nii.gz')
        # nib.save(nib.Nifti1Image(seg_pre[0], None), '0.nii.gz')
        # nib.save(nib.Nifti1Image(seg_pre[1], None), '1.nii.gz')
        # nib.save(nib.Nifti1Image(pre[0], None), 's0.nii.gz')
        # nib.save(nib.Nifti1Image(pre[1], None), 's1.nii.gz')


def update_pelvis_APP():
    global pelvis_cs, pts_dict
    pelvis_cs.setAxis(0, ace_center[1] - ace_center[0])
    pelvis_cs.normalize()
    pelvis_cs.orthogonalize([2, 0])

    origin = (ace_center[0] + ace_center[1]) / 2
    pelvis_cs.setOrigin(origin)

    app_pts = vtk.vtkPoints()
    app_pts.InsertNextPoint(pts_dict['髂前上棘'][0])
    app_pts.InsertNextPoint(pts_dict['髂前上棘'][1])
    app_pts.InsertNextPoint(pts_dict['耻骨结节'][0])
    app_pts.InsertNextPoint(pts_dict['耻骨结节'][1])

    vr = -vmi.pdOBB_Pts(app_pts)['axis'][2]
    vr = vr if np.dot(vr, np.array([0, 1, 0])) >= 0 else -vr
    if vmi.vtAngle(vr, pelvis_cs.axis(0)) < 1 or vmi.vtAngle(vr, pelvis_cs.axis(0)) > 179:
        return

    pelvis_cs.setAxis(1, vr)
    pelvis_cs.orthogonalize([2, 0])

    update_cup_orientation()
    update_cup()


def update_cup_orientation():
    cs = pelvis_cs.rotate(-cup_RI, pelvis_cs.axis(1))
    cs = cs.rotate(-cup_RA, pelvis_cs.axis(0))
    cup_axis = -cs.axis(2) * np.array([LR, 1, 1])

    cup_cs.setAxis(1, pelvis_cs.axis(1))
    cup_cs.setAxis(2, cup_axis)
    cup_cs.orthogonalize([0, 1])
    cup_cs.setAxis(0, -LR * cup_cs.axis(0))
    cup_cs.normalize()

    # cup_RA = np.rad2deg(np.arctan(-cup_axis[1] / np.sqrt(1 - cup_axis[2] ** 2)))
    # cup_RI = np.rad2deg(-np.abs(cup_axis[0] / cup_axis[2]))


def update_cup():
    plane = vtk.vtkPlane()
    plane.SetNormal(cup_cs.axis(2))
    plane.SetOrigin(cup_cs.origin())

    pd = vmi.pdSphere(cup_radius, cup_cs.origin())
    pd = vmi.pdClip_Implicit(pd, plane)[1]

    pd_border = vmi.pdPolyline_Regular(cup_radius, cup_cs.origin(), cup_cs.axis(2))
    pd = vmi.pdAppend([pd, pd_border])

    # cs = vmi.CS4x4().reflect(pelvis_cs.axis(0), pelvis_cs.origin())
    # pd_MPP = vmi.pdMatrix(pd, cs.matrix4x4())
    cup_prop.setData(pd)

    if pelvis_slice_box.text() == '断层':
        pd = vmi.pdCut_Implicit(cup_prop.data(), pelvis_slice.slicePlane())
        cup_section_prop.setData(pd)


def update_cup_camera_sagittal():
    cs = vmi.CS4x4(axis1=-pelvis_cs.axis(2), axis2=-LR * pelvis_cs.axis(0))
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
    image = vmi.imReslice(pre_image, cs, size)
    image.SetOrigin(cs.origin())

    pd = modelToLargestRegion(image)
    aceta_prop.setData(pd)

    update_guide_path()
    update_cup_camera_plane()
    guide_view.setEnabled(True)


def update_guide_path():
    global cup_cs, body_cs, large_z, small_t
    large_z, small_t = 100, 5
    body_vt_x = cup_cs.rotate(LR * (body_angle + 45), -cup_cs.axis(2)).mvt([1, 0, 0])
    body_cs = vmi.CS4x4(origin=cup_cs.mpt([0, 0, large_z]), axis0=body_vt_x, axis2=-cup_cs.axis(2))
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
    body_axis = vmi.ccEdge(vmi.ccSegment(body_cs.mpt([0, 0, 0]), body_cs.mpt([0, 0, 2 * large_z])))

    global body_hole_wire
    body_hole_radius = small_t
    body_hole_wire = vmi.ccWire(vmi.ccEdge(
        vmi.ccCircle(body_hole_radius, body_cs.origin(), body_cs.axis(2), body_cs.axis(0))))

    global head_cs
    head_cs = body_cs.copy()
    head_cs.setOrigin(body_cs.mpt([body_xr, 0, 0]))

    global arm_length, arm_area_wire, shaft_radius
    shaft_radius = 5
    arm_area_pts = [head_cs.mpt([-arm_length * np.sin(np.deg2rad(t)),
                                 -LR * (arm_length * np.cos(np.deg2rad(t))), 0]) for t in range(-30, 60)]
    arm_area_wire = vmi.ccWire(vmi.ccSegments(arm_area_pts))

    global guide_path, guide_path_prop
    guide_path = vmi.ccBoolean_Union([body_wire, body_axis, body_hole_wire, arm_area_wire])
    guide_path_prop.setData(guide_path)
    return


def update_guide_plate():
    global UDI, UDI_time
    UDI_time = time.localtime()
    UDI = '{}{}'.format('TH', vmi.convert_base(round(time.time() * 100)).upper())

    time_start, time_prev = time.time(), time.time()

    global kirs_radius, kirs_hole_radius
    kirs_hole_radius = kirs_radius + 0.2

    global body_cs, body_xr, body_yr, head_cs, head_xr, head_yr, large_z, small_t, arm_length, shaft_radius
    mold_xr = body_xr + head_xr
    mold_yr = arm_length + kirs_hole_radius + 2
    res = 1
    xn, yn = int(np.ceil(mold_xr / res)) + 1, int(np.ceil(mold_yr / res)) + 1
    body_mold, body_z_array = [], []
    body = vmi.ccMatchSolid_Rect(
        aceta_prop.data(), body_cs, xn, yn, res, small_t, 2 * large_z - small_t, 0.2, body_mold, body_z_array)

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('match body', time_stop)

    nx, ny = int(np.ceil(head_xr / res)) + 1, int(np.ceil(head_yr / res)) + 1
    head_z_array = []
    vmi.ccMatchSolid_Rect(
        aceta_prop.data(), head_cs, nx, ny, res, small_t, 2 * large_z - small_t, 0.2, None, head_z_array)

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('match head', time_stop)

    global head_height
    head_height = 15
    head_z = np.min(head_z_array[0]) - small_t

    global psi_mold, psi_mold_prop
    mold_max_z = head_z + small_t + body_xr + head_xr
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
    print('label', time_stop)

    global body_x_negtive
    body_pts = [[body_xr + head_xr, LR * -body_yr, head_z],
                [body_xr + head_xr, LR * body_yr, head_z],
                [-body_x_negtive * np.cos(np.deg2rad(72)), LR * body_yr, head_z],
                [-body_x_negtive, 0, head_z],
                [-body_x_negtive * np.cos(np.deg2rad(72)), LR * -body_yr, head_z]]
    body_wire = vmi.ccWire(vmi.ccSegments([body_cs.mpt(pt) for pt in body_pts], True))
    body_box = vmi.ccPrism(vmi.ccFace(body_wire), body_cs.axis(2), 2 * large_z)
    body = vmi.ccBoolean_Intersection([body, body_box])

    body_pts = [[body_xr + head_xr, LR * body_yr, 2 * large_z],
                [body_xr + head_xr, LR * body_yr, head_z],
                [body_xr - head_xr, LR * body_yr, head_z],
                [0, LR * body_yr, head_z + (body_xr - head_xr) * np.tan(np.deg2rad(45))],
                [-body_x_negtive, LR * body_yr, head_z + (body_xr - head_xr) * np.tan(np.deg2rad(45))],
                [-body_x_negtive, LR * body_yr, 2 * large_z]]
    body_wire = vmi.ccWire(vmi.ccSegments([body_cs.mpt(pt) for pt in body_pts], True))
    body_box = vmi.ccPrism(vmi.ccFace(body_wire), -LR * body_cs.axis(1), 2 * body_yr)
    body = vmi.ccBoolean_Intersection([body, body_box])

    # body_pts = [[body_xr + head_xr, LR * body_yr, large_z * 2],
    #             [body_xr + head_xr, LR * body_yr, head_z],
    #             [-body_x_negtive, LR * body_yr, head_z],
    #             [-body_x_negtive, LR * body_yr, head_z + small_t],
    #             [body_xr - head_xr * 2, LR * body_yr, head_z + small_t],
    #             [body_xr - head_xr * 2, LR * body_yr, 2 * large_z]]
    # body_wire = vmi.ccWire(vmi.ccSegments([body_cs.mpt(pt) for pt in body_pts], True))
    # body_box = vmi.ccPrism(vmi.ccFace(body_wire), -LR * body_cs.axis(1), 2 * body_yr)
    # body = vmi.ccBoolean_Intersection([body, body_box])

    global shaft
    h = head_height + 1 - 3
    dr = h * np.tan(np.deg2rad(5.675))
    shaft_wire0 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(
        shaft_radius, head_cs.mpt([0, 0, head_z + 1]), head_cs.axis(2), head_cs.axis(0))))
    shaft_wire1 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(
        shaft_radius - dr, head_cs.mpt([0, 0, head_z + 1 - h]), head_cs.axis(2), head_cs.axis(0))))
    shaft_face0 = vmi.ccFace(shaft_wire0)
    shaft_face1 = vmi.ccFace(shaft_wire1)
    shaft = vmi.ccSolid(vmi.ccSew([vmi.ccLoft([shaft_wire0, shaft_wire1]), shaft_face0, shaft_face1]))
    body = vmi.ccBoolean_Union([body, shaft])

    global shaft_hole
    shaft_hole_wire = vmi.ccWire(vmi.ccEdge(
        vmi.ccCircle(kirs_hole_radius, head_cs.mpt([0, 0, 0]), head_cs.axis(2), head_cs.axis(0))))
    shaft_hole = vmi.ccPrism(vmi.ccFace(shaft_hole_wire), head_cs.axis(2), 2 * large_z)
    body = vmi.ccBoolean_Difference([body, shaft_hole])

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('body', time_stop)

    global body_hole_wire
    body_hole = vmi.ccPrism(vmi.ccFace(body_hole_wire), body_cs.axis(2), 2 * large_z)

    global psi_arm
    arm_pts = [[kirs_hole_radius + 2, -LR * (arm_length + kirs_hole_radius + 2), head_z],
               [kirs_hole_radius + 2, -LR * (arm_length - kirs_hole_radius - 2), head_z],
               [head_xr, LR * -head_xr, head_z],
               [head_xr, LR * head_xr, head_z],
               [-head_xr, LR * head_xr, head_z],
               [-head_xr, LR * -head_xr, head_z],
               [-kirs_hole_radius - 2, -LR * (arm_length - kirs_hole_radius - 2), head_z],
               [-kirs_hole_radius - 2, -LR * (arm_length + kirs_hole_radius + 2), head_z]]
    arm_pts = [head_cs.mpt(pt) for pt in arm_pts]
    arm_wire = vmi.ccWire(vmi.ccSegments(arm_pts, True))
    psi_arm = vmi.ccPrism(vmi.ccFace(arm_wire), -head_cs.axis(2), head_height + 2)

    h = head_height + 1 - 2
    dr = h * np.tan(np.deg2rad(5.675))
    hole_wire0 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(shaft_radius, head_cs.mpt([0, 0, head_z + 1]),
                                                    head_cs.axis(2), head_cs.axis(0))))
    hole_wire1 = vmi.ccWire(vmi.ccEdge(vmi.ccCircle(shaft_radius - dr, head_cs.mpt([0, 0, head_z + 1 - h]),
                                                    head_cs.axis(2), head_cs.axis(0))))
    hole_face0 = vmi.ccFace(hole_wire0)
    hole_face1 = vmi.ccFace(hole_wire1)
    hole = vmi.ccSolid(vmi.ccSew([vmi.ccLoft([hole_wire0, hole_wire1]), hole_face0, hole_face1]))
    psi_arm = vmi.ccBoolean_Difference([psi_arm, hole])

    arm_hole_center = head_cs.mpt([0, -LR * arm_length, 0])
    arm_hole = vmi.ccPrism(vmi.ccFace(vmi.ccWire(vmi.ccCircle(
        kirs_hole_radius, arm_hole_center, head_cs.axis(2), head_cs.axis(0)))), head_cs.axis(2), 2 * large_z)
    psi_arm = vmi.ccBoolean_Difference([psi_arm, arm_hole])
    psi_arm = vmi.ccBoolean_Difference([psi_arm, shaft_hole])

    psi_arm_prop.setData(psi_arm)
    # psi_arm_prop.setData(vmi.pdTriangle(vmi.ccPd_Sh(psi_arm), 0, 0))

    center_hole_wire = vmi.ccWire(vmi.ccEdge(
        vmi.ccCircle(kirs_hole_radius, body_cs.mpt([0, 0, 0]), body_cs.axis(2), body_cs.axis(0))))
    center_hole = vmi.ccPrism(vmi.ccFace(center_hole_wire), body_cs.axis(2), 2 * large_z)

    psi_mold = vmi.ccBoolean_Difference([psi_mold, center_hole])
    psi_mold = vmi.ccBoolean_Difference([psi_mold, shaft_hole])
    psi_mold_prop.setData(psi_mold)
    # mold_prop.setData(vmi.pdTriangle(vmi.ccPd_Sh(mold), 0, 0))

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('arm', time_stop)

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('arm', time_stop)

    global psi_match, psi_match_prop
    psi_match = vmi.ccBoolean_Difference([body, body_hole])
    psi_match_prop.setData(psi_match)
    # psi_match_prop.setData(vmi.pdTriangle(vmi.ccPd_Sh(psi_match), 0, 0))

    time_stop = time.time() - time_prev
    time_prev = time.time()
    print('body cut', time_stop)
    print(time.time() - time_start)


def case_sync():
    global cup_radius, cup_RA, cup_RI
    import vmi.application.skyward
    with tempfile.TemporaryDirectory() as p:
        case_vtp = {'pelvis_vtp': pelvis_prop.data(),
                    'psi_match_vtp': psi_match_prop.data(),
                    'psi_arm_vtp': psi_arm_prop.data(),
                    'psi_mold_vtp': psi_mold_prop.data()}
        for kw in case_vtp:
            f = str(pathlib.Path(p) / '{}.vtp'.format(kw))
            vmi.pdSaveFile_XML(case_vtp[kw], f)
            case_vtp[kw] = f

        case_stl = {'psi_match_stl': psi_match_prop.data(),
                    'psi_arm_stl': psi_arm_prop.data(),
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

        case = vmi.application.skyward.case(product_model='TH', order_uid=UDI,
                                            order_files=['psi_match_stl', 'psi_arm_stl', 'psi_mold_stl'],
                                            patient_name=dicom_ds['PatientName'],
                                            patient_sex=dicom_ds['PatientSex'],
                                            patient_age=dicom_ds['PatientAge'],
                                            dicom_files={'pelvis_dicom': series.filenames()},
                                            vti_files={},
                                            vtp_files=case_vtp,
                                            stl_files=case_stl,
                                            pelvis_dicom_info=pelvis_dicom_info,
                                            surgical_side='left' if LR > 0 else 'right',
                                            pelvis_cs=pelvis_cs.array4x4().tolist(),
                                            head_cs=head_cs.array4x4().tolist(),
                                            cup_cs=cup_cs.array4x4().tolist(),
                                            cup_radius=round(cup_radius * 100) / 100,
                                            cup_RA=round(cup_RA * 100) / 100,
                                            cup_RI=round(cup_RI * 100) / 100)

        case = vmi.application.skyward.case_sync(case, ['pelvis_dicom', 'order_model', 'surgical_side'])

        if case is True:
            vmi.askInfo('同步完成')
        elif case:
            cup_radius = case['cup_radius']
            cup_RA = case['cup_RA']
            cup_RI = case['cup_RI']
            cup_radius_box.draw_text('半径：{:.0f} mm'.format(cup_radius))
            cup_RA_box.draw_text('前倾角：{:.1f}°'.format(cup_RA))
            cup_RI_box.draw_text('外展角：{:.1f}°'.format(cup_RI))
            update_cup_orientation()
            update_cup()

            if case['customer_confirmed']:
                init_guide()
            vmi.askInfo('同步完成')


def save_docx(file):
    global UDI, UDI_time

    with tempfile.TemporaryDirectory() as p:
        png = str(pathlib.Path(p) / '.png')

        doc = vmi.docx_document('设计确认单')
        vmi.docx_section_landscape_A4(doc.sections[0])
        vmi.docx_section_margin_middle(doc.sections[0])
        vmi.docx_section_header(doc.sections[0])

        s_title = vmi.docx_style(doc, '影为标题', 'Normal', size=26, alignment='CENTER')
        s_header = vmi.docx_style(doc, '影为页眉', 'Header', size=10)
        s_body_left = vmi.docx_style(doc, '影为正文', 'Body Text')
        s_body_left_indent = vmi.docx_style(doc, '影为正文首行缩进', 'Body Text', first_line_indent=2)
        s_body_center = vmi.docx_style(doc, '影为正文居中', 'Body Text', alignment='CENTER')
        s_table = vmi.docx_style(doc, '影为表格', 'Table Grid', alignment='CENTER')

        doc.sections[0].header.paragraphs[0].text = '影为医疗科技（上海）有限公司\t\t\t\t{}'.format('[表单号]')
        doc.sections[0].header.paragraphs[0].style = s_header

        def add_row_text(table, texts, styles, merge=None):
            r = len(table.add_row().table.rows) - 1
            if merge is not None:
                table.cell(r, merge[0]).merge(table.cell(r, merge[1]))
            for c in range(min(len(table.columns), len(texts))):
                table.cell(r, c).paragraphs[0].text = texts[c]
                table.cell(r, c).paragraphs[0].style = styles[c]

        def add_row_picture(table, text, styles, pic_file):
            r = len(table.add_row().table.rows) - 1
            table.cell(r, 1).merge(table.cell(r, 3))
            table.cell(r, 0).paragraphs[0].text = text
            table.cell(r, 0).paragraphs[0].style = styles[0]
            table.cell(r, 1).paragraphs[0].style = styles[1]

            with open(pic_file, 'rb') as pic:
                table.cell(r, 1).paragraphs[0].add_run().add_picture(pic, width=table.cell(r, 1).width * 0.7)

        doc_table = doc.add_table(1, 4, s_table)
        doc_table.autofit = True
        doc_table.alignment = vmi.docx.enum.table.WD_TABLE_ALIGNMENT.CENTER

        doc_table.cell(0, 0).merge(doc_table.cell(0, 3))
        doc_table.cell(0, 0).paragraphs[0].text = '设计确认单\nDesign Confirmation'
        doc_table.cell(0, 0).paragraphs[0].style = s_title

        add_row_text(doc_table, ['顾客姓名\nCustomer name', '',
                                 '顾客编号\nCustomer UID', ''], [s_body_center] * 4)
        add_row_text(doc_table, ['单位\nOrganization', '',
                                 '电邮\nEmail', ''], [s_body_center] * 4)
        add_row_text(doc_table, ['邮寄信息\nMailing information', ''], [s_body_center, s_body_left], [1, 3])

        text = '顾客收货视为已阅读并接受：'
        text += '\n1）所述产品属于个性化医疗器械；'
        text += '\n2）确认设计输入已包含顾客要求；'
        text += '\n3）确认设计输出符合顾客要求，同意进行生产制造；'
        text += '\n4）当顾客要求与产品上市信息冲突时，不作为设计输入。'
        add_row_text(doc_table, ['销售条款\nTerms of sale', text], [s_body_center, s_body_left], [1, 3])

        add_row_text(doc_table, ['销售工程师\nSales engineer', '',
                                 '电话\nTelephone', ''], [s_body_center] * 4)

        add_row_text(doc_table, ['产品名称\nProduct name', '全髋关节置换手术导板',
                                 '序列号\nSerial number', UDI], [s_body_center] * 4)
        add_row_text(doc_table, ['型号\nModel', 'TH',
                                 '规格\nSpecification', '定制式'], [s_body_center] * 4)
        add_row_text(doc_table, [
            '患者\nPatient',
            '{}\n{} {}'.format(dicom_ds['PatientName'], dicom_ds['PatientSex'], dicom_ds['PatientAge']),
            '手术侧\nSurgical side', '左' if LR > 0 else '右'], [s_body_center] * 4)

        spc, dim = vmi.imSpacing(original_slice.data()), vmi.imDimensions(original_slice.data())
        text = '描述：{}，{}，{}'.format(dicom_ds['StudyDate'], dicom_ds['Modality'], dicom_ds['StudyDescription'])
        text += '\n参数：{}×{}×{}，{}×{}×{} mm'.format(dim[0], dim[1], dim[2], spc[0], spc[1], spc[2])
        text += '\n系列：{}'.format(dicom_ds['SeriesInstanceUID'])
        add_row_text(doc_table, ['影像输入\nRadiological input', text], [s_body_center, s_body_left], [1, 3])

        text = '影像学前倾角：{:.1f}°\n影像学外展角：{:.1f}°'.format(cup_RA, cup_RI)
        add_row_text(doc_table, ['临床输入\nClinical input', text], [s_body_center, s_body_left], [1, 3])

        text = '骨阈值：{:.0f} HU'.format(bone_value)
        text += '\n主体方位：{:.0f}°，主体长径：{:.0f} mm，主体短径：{:.0f} mm'.format(body_angle, body_xr, body_yr)
        text += '\n旋臂长度：{:.0f} mm'.format(arm_length)
        text += '\n导针半径：{:.1f} mm'.format(kirs_radius)
        add_row_text(doc_table, ['造型输入\nModeling input', text], [s_body_center, s_body_left], [1, 3])

        add_row_text(doc_table, ['设计时间\nDesign time', '{}年{}月{}日{}'.format(
            UDI_time.tm_year, UDI_time.tm_mon, UDI_time.tm_mday, time.strftime('%H:%M:%S', UDI_time))],
                     [s_body_center, s_body_left], [1, 3])

        text = '{} {}'.format(UDI, '定位板.stl')
        text += '\n{} {}'.format(UDI, '旋臂.stl')
        text += '\n{} {}'.format(UDI, '配模.stl')
        add_row_text(doc_table, ['设计输出\nDesign output', text], [s_body_center, s_body_left], [1, 3])

        visibles = [aceta_prop.visible(),
                    guide_path_prop.visible(),
                    psi_match_prop.visible(),
                    psi_arm_prop.visible(),
                    psi_mold_prop.visible()]

        aceta_prop.setVisible(True)
        guide_path_prop.setVisible(False)
        psi_match_prop.setVisible(False)
        psi_arm_prop.setVisible(False)
        psi_mold_prop.setVisible(False)
        update_cup_camera_plane()
        guide_view.snapshot_PNG(png)
        add_row_picture(doc_table, '快照（1/6）\nSnapshot', [s_body_center, s_body_center], png)

        aceta_prop.setVisible(True)
        guide_path_prop.setVisible(True)
        psi_match_prop.setVisible(True)
        psi_arm_prop.setVisible(False)
        psi_mold_prop.setVisible(False)
        guide_view.snapshot_PNG(png)
        add_row_picture(doc_table, '快照（2/6）\nSnapshot', [s_body_center, s_body_center], png)

        aceta_prop.setVisible(True)
        guide_path_prop.setVisible(False)
        psi_match_prop.setVisible(True)
        psi_arm_prop.setVisible(True)
        psi_mold_prop.setVisible(False)
        guide_view.camera().Elevation(-30)
        guide_view.camera().OrthogonalizeViewUp()
        guide_view.snapshot_PNG(png)
        add_row_picture(doc_table, '快照（3/6）\nSnapshot', [s_body_center, s_body_center], png)

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
        guide_view.snapshot_PNG(png)
        add_row_picture(doc_table, '快照（4/6）\nSnapshot', [s_body_center, s_body_center], png)

        aceta_prop.setVisible(False)
        guide_path_prop.setVisible(False)
        psi_match_prop.setVisible(True)
        psi_arm_prop.setVisible(True)
        psi_mold_prop.setVisible(False)
        guide_view.camera().Elevation(-90)
        guide_view.camera().OrthogonalizeViewUp()
        guide_view.setCamera_FitAll()
        guide_view.snapshot_PNG(png)
        add_row_picture(doc_table, '快照（5/6）\nSnapshot', [s_body_center, s_body_center], png)

        aceta_prop.setVisible(False)
        guide_path_prop.setVisible(False)
        psi_match_prop.setVisible(True)
        psi_arm_prop.setVisible(True)
        psi_mold_prop.setVisible(True)
        update_cup_camera_plane()
        guide_view.camera().Elevation(-30)
        guide_view.camera().OrthogonalizeViewUp()
        guide_view.snapshot_PNG(png)
        add_row_picture(doc_table, '快照（6/6）\nSnapshot', [s_body_center, s_body_center], png)

        aceta_prop.setVisible(visibles[0])
        guide_path_prop.setVisible(visibles[1])
        psi_match_prop.setVisible(visibles[2])
        psi_arm_prop.setVisible(visibles[3])
        psi_mold_prop.setVisible(visibles[4])
        doc.save(file)


def LeftButtonPressMove(**kwargs):
    global spcut_center, pelvis_cs
    if kwargs['picked'] in [cup_prop, cup_section_prop]:
        pt = pelvis_view.pickPt_FocalPlane()
        pt = vmi.ptOnPlane(pt, pelvis_cs.origin(), pelvis_view.cameraVt_Look())

        over = kwargs['picked'].view().pickVt_FocalPlane()
        if np.dot(pt - pelvis_cs.origin(), cup_cs.origin() - pelvis_cs.origin()) < 0:
            over = pelvis_cs.inv().mvt(over)
            over[0] *= -1
            over = pelvis_cs.mvt(over)

        cup_cs.setOrigin(cup_cs.origin() + over)
        update_cup()
        return True
    elif kwargs['picked'] is pelvis_view:
        pelvis_view.mouseRotateFocal(**kwargs)
    elif kwargs['picked'] is psi_arm_prop:
        pass  # TODO 是否支持鼠标拖动旋臂自由移动旋转？


def LeftButtonPressRelease(**kwargs):
    global spcut_radius, pelvis_cs, cup_radius, cup_cs, cup_RA, cup_RI, bone_value, LR
    global body_angle, body_xr, body_yr, kirs_radius
    if kwargs['picked'] is dicom_box:
        original_image = read_dicom()
        original_image.SetOrigin(0, 0, 0)

        if original_image is not None:
            original_slice.setData(original_image)
            original_slice.setSlicePlaneOrigin_Center()
            original_slice.setSlicePlaneNormal_Coronal()
            original_view.setCamera_Coronal()
            original_view.setCamera_FitAll()
            init_voi()

            side = vmi.askButtons(['患右', '患左'], title='选择患侧')
            if side == '患右':
                LR = -1
            elif side == '患左':
                LR = 1

            co_mark_pts()
            init_pelvis()
            init_guide()
            return True
    elif kwargs['picked'] is original_slice:
        # on_init_voi()
        return True
    elif kwargs['picked'] is bone_value_box:
        v = vmi.askInt(-1000, bone_value, 3000)
        if v is not None:
            bone_value = v
            bone_value_box.draw_text('骨阈值：{:.0f} HU'.format(bone_value))
            voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
            return True

    elif kwargs['picked'] is cup_RA_box:
        r = vmi.askFloat(-15.0, cup_RA, 45.0, 1, 0.1)
        if r is not None:
            cup_RA = r
            cup_RA_box.draw_text('前倾角：{:.1f}°'.format(cup_RA))

            update_cup_orientation()
            update_cup()
            return True
    elif kwargs['picked'] is cup_RI_box:
        r = vmi.askFloat(0.0, cup_RI, 60.0, 1, 0.1)
        if r is not None:
            cup_RI = r
            cup_RI_box.draw_text('外展角：{:.1f}°'.format(cup_RI))

            update_cup_orientation()
            update_cup()
            return True
    elif kwargs['picked'] is cup_camera_sagittal_box:
        update_cup_camera_sagittal()
        return True
    elif kwargs['picked'] is cup_camera_coronal_box:
        update_cup_camera_coronal()
        return True
    elif kwargs['picked'] is cup_camera_axial_box:
        update_cup_camera_axial()
        return True
    elif kwargs['picked'] is cup_camera_RA_box:
        update_cup_camera_RA()
        return True
    elif kwargs['picked'] is cup_camera_RI_box:
        update_cup_camera_RI()
        return True
    elif kwargs['picked'] is cup_camera_plane_box:
        update_cup_camera_plane()
        return True
    elif kwargs['picked'] is pelvis_visible_box:
        pelvis_prop.visibleToggle()
        pelvis_visible_box.draw_text(
            back_color=QColor().fromRgbF(1, 1, 0.6) if pelvis_prop.visible() else QColor('black'))
        return True
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
            return True
        elif pelvis_slice_box.text() == '断层':
            pelvis_slice_box.draw_text('三维')
            cup_prop.setVisible(True)
            pelvis_prop.setVisible(True)
            cup_section_prop.setVisible(False)
            pelvis_slice.setVisible(False)
            return True

    elif kwargs['picked'] is init_guide_box:
        init_guide_box.draw_text('请耐心等待')
        init_guide()
        init_guide_box.draw_text('创建导板')
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
    elif kwargs['picked'] is guide_update_box:
        guide_update_box.draw_text('请耐心等待')
        update_guide_path()
        update_guide_plate()
        guide_update_box.draw_text('更新导板')
    elif kwargs['picked'] is body_angle_box:
        r = vmi.askInt(-45, body_angle, 45)
        if r is not None:
            body_angle = r
            body_angle_box.draw_text('主体方位：{}°'.format(body_angle))
            update_guide_path()
    elif kwargs['picked'] is body_xr_box:
        r = vmi.askInt(10, body_xr, 50)
        if r is not None:
            body_xr = r
            body_xr_box.draw_text('主体长径：{:.0f} mm'.format(body_xr))
            update_guide_path()
    elif kwargs['picked'] is body_yr_box:
        r = vmi.askInt(10, body_yr, 50)
        if r is not None:
            body_yr = r
            body_yr_box.draw_text('主体宽径：{:.0f} mm'.format(body_yr))
            update_guide_path()
    elif kwargs['picked'] is arm_length_box:
        global arm_length
        r = vmi.askInt(10, arm_length, 90)
        if r is not None:
            arm_length = r
            arm_length_box.draw_text('旋臂长度：{:.0f} mm'.format(arm_length))
            update_guide_path()
    elif kwargs['picked'] is kirs_radius_box:
        r = vmi.askFloat(0.5, kirs_radius, 2.5, 1, 0.1)
        if r is not None:
            kirs_radius = r
            kirs_radius_box.draw_text('导针半径：{:.1f} mm'.format(kirs_radius))
            update_guide_path()
    # elif kwargs['picked'] is output_box:
    #     p = vmi.askDirectory('vmi')
    #     if p is not None:
    #         global UDI, UDI_time
    #
    #         try:
    #             vmi.pdSaveFile_STL(aceta_prop.data(), str(pathlib.Path(p) / ('{} {}'.format(UDI, ' 髋臼.stl'))))
    #             vmi.pdSaveFile_STL(mold_prop.data(), str(pathlib.Path(p) / ('{} {}'.format(UDI, ' 配模.stl'))))
    #             vmi.pdSaveFile_STL(psi_match_prop.data(), str(pathlib.Path(p) / ('{} {}'.format(UDI, ' 定位板.stl'))))
    #             vmi.pdSaveFile_STL(psi_arm_prop.data(), str(pathlib.Path(p) / ('{} {}'.format(UDI, ' 旋臂.stl'))))
    #             save_docx(str(pathlib.Path(p) / ('{} {} {} {} {}.docx'.format(
    #                 UDI, '设计确认单', patient_name, 'L' if LR > 0 else 'R', time.strftime('%Y-%m-%d %H-%M-%S', UDI_time)))))
    #         except Exception as e:
    #             vmi.askInfo(str(e))


def MidButtonPressMove(**kwargs):
    if kwargs['picked'] in [pelvis_view, pelvis_slice]:
        pelvis_view.mousePan()


def RightButtonPressMove(**kwargs):
    if kwargs['picked'] in [pelvis_view, pelvis_slice]:
        pelvis_view.mouseZoom()


def NoButtonWheel(**kwargs):
    global bone_value, spcut_radius, cup_radius, cup_RA, cup_RI
    global body_angle, body_xr, body_yr, kirs_radius
    if kwargs['picked'] is bone_value_box:
        bone_value = min(max(bone_value + 10 * kwargs['delta'], -1000), 3000)
        bone_value_box.draw_text('骨阈值：{:.0f} HU'.format(bone_value))
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
        return True
    elif kwargs['picked'] is pelvis_view:
        pelvis_view.mouseRotateLook(**kwargs)
        return True
    elif kwargs['picked'] is cup_radius_box:
        cup_radius = min(max(cup_radius + kwargs['delta'], 5), 50)
        cup_radius_box.draw_text('半径：{:.0f} mm'.format(cup_radius))
        update_cup()
        return True
    elif kwargs['picked'] is cup_RA_box:
        cup_RA = min(max(cup_RA + 0.1 * kwargs['delta'], -15), 45)
        cup_RA_box.draw_text('前倾角：{:.1f}°'.format(cup_RA))
        update_cup_orientation()
        update_cup()
        return True
    elif kwargs['picked'] is cup_RI_box:
        cup_RI = min(max(cup_RI + 0.1 * kwargs['delta'], 0), 60)
        cup_RI_box.draw_text('外展角：{:.1f}°'.format(cup_RI))
        update_cup_orientation()
        update_cup()
        return True
    elif kwargs['picked'] is pelvis_slice:
        update_cup()
        return True
    elif kwargs['picked'] is body_angle_box:
        body_angle = min(max(body_angle + kwargs['delta'], -45), 45)
        body_angle_box.draw_text('主体方位：{}°'.format(body_angle))
        update_guide_path()
    elif kwargs['picked'] is body_xr_box:
        body_xr = min(max(body_xr + kwargs['delta'], 10), 50)
        body_xr_box.draw_text('主体长径：{:.0f} mm'.format(body_xr))
        update_guide_path()
    elif kwargs['picked'] is body_yr_box:
        body_yr = min(max(body_yr + kwargs['delta'], 10), 50)
        body_yr_box.draw_text('主体宽径：{:.0f} mm'.format(body_yr))
        update_guide_path()
    elif kwargs['picked'] is arm_length_box:
        global arm_length
        arm_length = min(max(arm_length + kwargs['delta'], 10), 90)
        arm_length_box.draw_text('旋臂长度：{:.0f} mm'.format(arm_length))
        update_guide_path()
    elif kwargs['picked'] is kirs_radius_box:
        kirs_radius = min(max(kirs_radius + 0.1 * kwargs['delta'], 0.5), 2.5)
        kirs_radius_box.draw_text('导针半径：{:.1f} mm'.format(kirs_radius))
        update_guide_path()


def return_globals():
    return globals()


if __name__ == '__main__':
    global original_view, voi_view, pelvis_view, guide_view
    warnings.filterwarnings("ignore")

    main = vmi.Main(return_globals)
    main.setAppName('全髋关节置换(THA)规划')
    main.setAppVersion(vmi.version)
    main.excludeKeys += ['main', 'i', 'box', 'prop', 'voi_image']

    select = vmi.askButtons(['新建', '打开'], title=main.appName())
    if select is None:
        vmi.appexit()

    if select == '打开':
        open_file = vmi.askOpenFile(nameFilter='*.vmi', title='打开存档')
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

        bone_value, target_value = 200, 0

        bone_value_box = vmi.TextBox(voi_view, text='骨阈值：{:.0f} HU'.format(bone_value),
                                     size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)
        bone_value_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        bone_value_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        voi_size, voi_center, voi_origin, voi_cs = np.zeros(3), np.zeros(3), np.zeros(3), vmi.CS4x4()
        voi_image = vtk.vtkImageData()

        voi_volume = vmi.ImageVolume(voi_view, pickable=True)
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
        voi_volume.setColor({bone_value: [1, 1, 0.6]})

        # 骨盆标记点
        pts_prop = vmi.PolyActor(voi_view, color=[0.4, 0.6, 1], line_width=3, pickable=True)
        td_pts = np.zeros((2, 3))
        pts_dict = []

        # 5 骨盆视图
        pelvis_view = vmi.View()
        pelvis_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        pelvis_view.mouse['MidButton']['PressMove'] = [MidButtonPressMove]
        pelvis_view.mouse['RightButton']['PressMove'] = [RightButtonPressMove]
        pelvis_view.mouse['NoButton']['Wheel'] = [NoButtonWheel]
        pelvis_prop = vmi.PolyActor(pelvis_view, color=[1, 1, 0.6])

        pelvis_cs, cup_cs = vmi.CS4x4(), vmi.CS4x4()
        cup_radius, cup_RA, cup_RI = 22, 20, 40
        cup_center = np.zeros((2, 3)), np.zeros((2, 3))
        cup_prop = vmi.PolyActor(pelvis_view, color=[0.4, 0.6, 1], line_width=3, pickable=True)
        cup_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        cup_radius_box = vmi.TextBox(pelvis_view, text='半径：{:.0f} mm'.format(cup_radius), pickable=True,
                                     size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0])
        cup_radius_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        cup_radius_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        cup_RA_box = vmi.TextBox(pelvis_view, text='前倾角：{:.1f}°'.format(cup_RA), pickable=True,
                                 size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])
        cup_RA_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        cup_RA_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        cup_RI_box = vmi.TextBox(pelvis_view, text='外展角：{:.1f}°'.format(cup_RI), pickable=True,
                                 size=[0.2, 0.04], pos=[0, 0.14], anchor=[0, 0])
        cup_RI_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        cup_RI_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        pelvis_slice = vmi.ImageSlice(pelvis_view, visible=False)
        pelvis_slice.bindData(voi_volume)
        pelvis_slice.mouse['MidButton']['PressMove'] = [MidButtonPressMove]
        pelvis_slice.mouse['RightButton']['PressMove'] = [RightButtonPressMove]
        pelvis_slice.mouse['NoButton']['Wheel'] += [NoButtonWheel]

        original_slice.bindColorWindow([pelvis_slice])

        cup_section_prop = vmi.PolyActor(pelvis_view, color=[0.4, 0.6, 1], line_width=3, visible=False, pickable=True)
        cup_section_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        pelvis_slice_box = vmi.TextBox(pelvis_view, text='三维', pickable=True,
                                       size=[0.2, 0.04], pos=[0, 0.2], anchor=[0, 0])
        pelvis_slice_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_sagittal_box = vmi.TextBox(pelvis_view, text='矢状', pickable=True,
                                              size=[0.06, 0.04], pos=[0, 0.36], anchor=[0, 0])
        cup_camera_sagittal_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_coronal_box = vmi.TextBox(pelvis_view, text='冠状', pickable=True,
                                             size=[0.06, 0.04], pos=[0.06, 0.36], anchor=[0, 0])
        cup_camera_coronal_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_axial_box = vmi.TextBox(pelvis_view, text='横断', pickable=True,
                                           size=[0.06, 0.04], pos=[0.12, 0.36], anchor=[0, 0])
        cup_camera_axial_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_RA_box = vmi.TextBox(pelvis_view, text='前倾', pickable=True,
                                        size=[0.06, 0.04], pos=[0, 0.4], anchor=[0, 0])
        cup_camera_RA_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_RI_box = vmi.TextBox(pelvis_view, text='外展', pickable=True,
                                        size=[0.06, 0.04], pos=[0.06, 0.4], anchor=[0, 0])
        cup_camera_RI_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        cup_camera_plane_box = vmi.TextBox(pelvis_view, text='正视', pickable=True,
                                           size=[0.06, 0.04], pos=[0.12, 0.4], anchor=[0, 0])
        cup_camera_plane_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        pelvis_visible_box = vmi.TextBox(pelvis_view, size=[0.02, 0.04], pos=[0.18, 0.36], anchor=[0, 0],
                                         back_color=QColor().fromRgbF(1, 1, 0.6), pickable=True)
        pelvis_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        init_guide_box = vmi.TextBox(pelvis_view, text='创建导板', pickable=True,
                                     fore_color=QColor('white'), back_color=QColor('crimson'),
                                     bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0])
        init_guide_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        # 8 导板
        guide_view = vmi.View()
        guide_view.bindCamera([pelvis_view])

        aceta_prop = vmi.PolyActor(guide_view, color=[1, 1, 0.6])

        guide_path = vmi.TopoDS_Shape()  # 引导线
        guide_path_prop = vmi.PolyActor(guide_view, color=[0.4, 1, 0.4], line_width=3)

        psi_match = vmi.TopoDS_Shape()  # 主板
        psi_match_prop = vmi.PolyActor(guide_view, color=[0.4, 0.6, 1])

        psi_arm = vmi.TopoDS_Shape()  # 旋臂
        psi_arm_prop = vmi.PolyActor(guide_view, color=[0.6, 0.8, 1])
        psi_arm_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        psi_mold = vmi.TopoDS_Shape()  # 配模
        psi_mold_prop = vmi.PolyActor(guide_view, color=[1, 0.4, 0.4])

        body_angle = 0  # 主体方位
        body_xr, body_yr = 20, 15  # 主体长径宽径，臼窝匹配块
        arm_length = 50  # 旋臂长度
        kirs_radius = 1  # 导向孔半径

        body_angle_box = vmi.TextBox(guide_view, text='主体方位：{}°'.format(body_angle), pickable=True,
                                     size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0])
        body_angle_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        body_angle_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        body_xr_box = vmi.TextBox(guide_view, text='主体长径：{:.0f} mm'.format(body_xr), pickable=True,
                                  size=[0.2, 0.04], pos=[0, 0.08], anchor=[0, 0])
        body_xr_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        body_xr_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        body_yr_box = vmi.TextBox(guide_view, text='主体宽径：{:.0f} mm'.format(body_yr), pickable=True,
                                  size=[0.2, 0.04], pos=[0, 0.12], anchor=[0, 0])
        body_yr_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        body_yr_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        arm_length_box = vmi.TextBox(guide_view, text='旋臂长度：{:.0f} mm'.format(arm_length), pickable=True,
                                     size=[0.2, 0.04], pos=[0, 0.16], anchor=[0, 0])
        arm_length_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        arm_length_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        kirs_radius_box = vmi.TextBox(guide_view, text='导针半径：{:.1f} mm'.format(kirs_radius), pickable=True,
                                      size=[0.2, 0.04], pos=[0, 0.20], anchor=[0, 0])
        kirs_radius_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        kirs_radius_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        guide_update_box = vmi.TextBox(guide_view, text='更新导板', pickable=True,
                                       size=[0.10, 0.04], pos=[0, 0.26], anchor=[0, 0])
        guide_update_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        aceta_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(1, 1, 0.6),
                                        size=[0.02, 0.04], pos=[0.10, 0.26], anchor=[0, 0])
        aceta_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        guide_path_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(0.4, 1, 0.4),
                                             size=[0.02, 0.04], pos=[0.12, 0.26], anchor=[0, 0])
        guide_path_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        psi_match_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(0.4, 0.6, 1),
                                            size=[0.02, 0.04], pos=[0.14, 0.26], anchor=[0, 0])
        psi_match_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        psi_arm_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(0.6, 0.8, 1),
                                          size=[0.02, 0.04], pos=[0.16, 0.26], anchor=[0, 0])
        psi_arm_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        mold_visible_box = vmi.TextBox(guide_view, pickable=True, back_color=QColor().fromRgbF(1, 0.4, 0.4),
                                       size=[0.02, 0.04], pos=[0.18, 0.26], anchor=[0, 0])
        mold_visible_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        case_sync_box = vmi.TextBox(guide_view, text='同步', pickable=True,
                                    fore_color=QColor('white'), back_color=QColor('crimson'),
                                    bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0])
        case_sync_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        # output_box = vmi.TextBox(guide_view, text='导出方案', fore_color=QColor('white'), back_color=QColor('crimson'),
        #                          bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0], pickable=True)
        # output_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    # 视图布局
    for v in [original_view, voi_view, pelvis_view, guide_view]:
        v.setMinimumWidth(round(0.5 * main.screenWidth()))

    original_view.setParent(main.scrollArea())
    main.layout().addWidget(original_view, 0, 0, 1, 1)
    main.layout().addWidget(voi_view, 0, 1, 1, 1)
    main.layout().addWidget(pelvis_view, 0, 2, 1, 1)
    main.layout().addWidget(guide_view, 0, 3, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
