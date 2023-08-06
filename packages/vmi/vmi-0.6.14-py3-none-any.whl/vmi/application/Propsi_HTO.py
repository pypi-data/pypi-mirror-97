import json
import pathlib
import shutil
import tempfile
import time

import numpy as np
import pydicom
import vtk
from PySide2.QtGui import *
from PySide2.QtCore import QLineF, QPointF
from numba import jit
import SimpleITK as sitk
from typing import List, Union

import vmi


def pd_polygon(pt_list: List[Union[np.ndarray, List[float]]]):
    n = len(pt_list)

    if n < 3:
        return
    pts = vtk.vtkPoints()

    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(n);

    for i in range(n):
        pts.InsertNextPoint(pt_list[i])
        polygon.GetPointIds().SetId(i, i)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polygon)

    pd = vtk.vtkPolyData()
    pd.SetPoints(pts)
    pd.SetPolys(cells)

    return pd


def input_dicom():
    file = vmi.askOpenFile('*.*', '请选择打开图像 (Please select open Dicom)')

    if file is None:
        return
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.dcm'
        shutil.copyfile(file, p)
        r = sitk.ImageFileReader()
        r.SetFileName(str(p))

        global patient_name
        patient_name = str(pydicom.dcmread(str(p)).PatientName)
        patient_name_box.draw_text('姓名：{}'.format(patient_name))
        patient_name_box.setVisible(True)

        image = vmi.imVTK_SITK(r.Execute())
        image_ary = vmi.imArray_VTK(image)

        ori, spc = [0, 0, 0], [1, 1, 1]
        return vmi.imVTK_Array(np.array([image_ary]), ori, spc)


def init_rect_prop():
    global rect_size, rect_pos, hip_cir_center, hip_cir_radius, ankle_pt, femur_distal_pt, tibia_proximal_pt, tibia_cut_pt
    data = xray_slice.data()
    if data.GetNumberOfPoints() > 0:
        center = vmi.imCenter(data)
        bounds = vmi.imBounds(data)
        rect_size[0] = 0.3 * (bounds[1] - bounds[0])
        rect_size[1] = rect_size[0] * xray_view.height() / xray_view.width()

        rect_pos = [[center[0] - 0.5 * rect_size[0], center[1] - 2.5 * rect_size[1], 0],
                    [center[0] - 0.5 * rect_size[0], center[1] - 0.5 * rect_size[1], 0],
                    [center[0] - 0.5 * rect_size[0], center[1] + 1.5 * rect_size[1], 0]]

        for i in range(3):
            pts = [rect_pos[i],
                   [rect_pos[i][0] + rect_size[0], rect_pos[i][1], 0],
                   [rect_pos[i][0] + rect_size[0], rect_pos[i][1] + rect_size[1], 0],
                   [rect_pos[i][0], rect_pos[i][1] + rect_size[1], 0]]

            rect_prop[i].setData(pd_polygon(pts))

    # 髋关节初始化
    hip_cir_center = [rect_pos[0][0] + 0.5 * rect_size[0], rect_pos[0][1] + 0.5 * rect_size[1], 0]
    hip_cir_radius = 0.25 * rect_size[0]

    # 踝关节初始化
    ankle_pt = [[rect_pos[2][0] + 1 / 3. * rect_size[0], rect_pos[2][1] + 0.5 * rect_size[1], 0],
                [rect_pos[2][0] + 2 / 3. * rect_size[0], rect_pos[2][1] + 0.5 * rect_size[1], 0]]

    # 膝关节初始化
    femur_distal_pt = [[rect_pos[1][0] + 1 / 3. * rect_size[0], rect_pos[1][1] + 1 / 3. * rect_size[1], 0],
                       [rect_pos[1][0] + 2 / 3. * rect_size[0], rect_pos[1][1] + 1 / 3. * rect_size[1], 0]]

    tibia_proximal_pt = [[rect_pos[1][0] + 1 / 3. * rect_size[0], rect_pos[1][1] + 4 / 9. * rect_size[1], 0],
                         [rect_pos[1][0] + 2 / 3. * rect_size[0], rect_pos[1][1] + 4 / 9. * rect_size[1], 0]]

    tibia_cut_pt = [[rect_pos[1][0] + 1 / 3. * rect_size[0], rect_pos[1][1] + 5 / 9. * rect_size[1], 0],
                    [rect_pos[1][0] + 2 / 3. * rect_size[0], rect_pos[1][1] + 5 / 9. * rect_size[1], 0],
                    [rect_pos[1][0] + 2 / 3. * rect_size[0], rect_pos[1][1] + 5 / 9. * rect_size[1], 0]]

    return


def update_rect_prop():
    for i in range(3):
        pts = [rect_pos[i],
               [rect_pos[i][0] + rect_size[0], rect_pos[i][1], 0],
               [rect_pos[i][0] + rect_size[0], rect_pos[i][1] + rect_size[1], 0],
               [rect_pos[i][0], rect_pos[i][1] + rect_size[1], 0]]

        rect_prop[i].setData(pd_polygon(pts))
    return


def update_joint_slice():
    global LR
    image = xray_slice.data()
    for s in joint_slice:
        s.setData(image)

    b = [[rect_pos[0][0], rect_pos[0][0] + rect_size[0], rect_pos[0][1], rect_pos[0][1] + rect_size[1], 0, 0],
         [rect_pos[1][0], rect_pos[1][0] + rect_size[0], rect_pos[1][1], rect_pos[1][1] + rect_size[1], 0, 0],
         [rect_pos[2][0], rect_pos[2][0] + rect_size[0], rect_pos[2][1], rect_pos[2][1] + rect_size[1], 0, 0]]

    for i, view in enumerate(joint_view):
        w = view.width()
        h = view.height()
        x, y, z = b[i][1] - b[i][0], b[i][3] - b[i][2], b[i][5] - b[i][4]

        scale = [y * h / w if y / w > z / h else z,
                 x * h / w if x / w > z / h else z,
                 x * h / w if x / w > y / h else y]

        view.renderer().ResetCamera(b[i])
        view.renderer().ResetCameraClippingRange()
        view.renderer().GetActiveCamera().SetParallelScale(0.5 * scale[2])

    xray_view.setCamera_FitAll()

    center = vmi.imCenter(image)
    LR = 1 if rect_pos[1][0] + 0.5 * rect_size[0] > center[0] else -1
    patient_LR_box.draw_text('患侧：{}'.format('左' if LR > 0 else '右'))
    patient_LR_box.setVisible(True)

    return


def update_view_line():
    pt = [[hip_cir_center,
           [0.5 * (ankle_pt[0][0] + ankle_pt[1][0]),
            0.5 * (ankle_pt[0][1] + ankle_pt[1][1]), 0]],
          [hip_cir_center,
           [0.5 * (femur_distal_pt[0][0] + femur_distal_pt[1][0]),
            0.5 * (femur_distal_pt[0][1] + femur_distal_pt[1][1]), 0]],
          [[0.5 * (tibia_proximal_pt[0][0] + tibia_proximal_pt[1][0]),
            0.5 * (tibia_proximal_pt[0][1] + tibia_proximal_pt[1][1]), 0],
           [0.5 * (ankle_pt[0][0] + ankle_pt[1][0]),
            0.5 * (ankle_pt[0][1] + ankle_pt[1][1]), 0]]]

    for prop in hip_ankle_line_prop:
        prop.setData(vmi.pdPolyline(pt[0]))
    for prop in hip_femur_line_prop:
        prop.setData(vmi.pdPolyline(pt[1]))
    for prop in ankle_tibia_line_prop:
        prop.setData(vmi.pdPolyline(pt[2]))
    return


def update_hip_prop():
    hip_cir_prop.setData(vmi.pdPolygon_Regular(hip_cir_radius, hip_cir_center, [0, 0, 1]))
    return


def update_ankle_prop():
    ankle_line_prop.setData(vmi.pdPolyline(ankle_pt))
    for i in range(2):
        r = point_size
        pt = [[ankle_pt[i][0] - r, ankle_pt[i][1] + r, 0],
              [ankle_pt[i][0] + r, ankle_pt[i][1] - r, 0],
              [ankle_pt[i][0] + r, ankle_pt[i][1] + r, 0],
              [ankle_pt[i][0] - r, ankle_pt[i][1] - r, 0]]

        ankle_pt_prop[i].setData(vmi.pdAppend([vmi.pdPolyline([pt[0], pt[1]]),
                                               vmi.pdPolyline([pt[2], pt[3]])]))
    return


def update_knee_prop():
    femur_distal_line_prop.setData(vmi.pdPolyline(femur_distal_pt))
    tibia_proximal_line_prop.setData(vmi.pdPolyline(tibia_proximal_pt))
    tibia_cut_line_prop[0].setData(vmi.pdPolyline([tibia_cut_pt[0], tibia_cut_pt[1]]))

    r = point_size
    for i in range(2):
        pt = [[femur_distal_pt[i][0] - r, femur_distal_pt[i][1] + r, 0],
              [femur_distal_pt[i][0] + r, femur_distal_pt[i][1] - r, 0],
              [femur_distal_pt[i][0] + r, femur_distal_pt[i][1] + r, 0],
              [femur_distal_pt[i][0] - r, femur_distal_pt[i][1] - r, 0]]

        femur_distal_pt_prop[i].setData(vmi.pdAppend([vmi.pdPolyline([pt[0], pt[1]]),
                                                      vmi.pdPolyline([pt[2], pt[3]])]))

    for i in range(2):
        pt = [[tibia_proximal_pt[i][0] - r, tibia_proximal_pt[i][1] + r, 0],
              [tibia_proximal_pt[i][0] + r, tibia_proximal_pt[i][1] - r, 0],
              [tibia_proximal_pt[i][0] + r, tibia_proximal_pt[i][1] + r, 0],
              [tibia_proximal_pt[i][0] - r, tibia_proximal_pt[i][1] - r, 0]]

        tibia_proximal_pt_prop[i].setData(vmi.pdAppend([vmi.pdPolyline([pt[0], pt[1]]),
                                                        vmi.pdPolyline([pt[2], pt[3]])]))

    pt = [[tibia_cut_pt[1][0] - r, tibia_cut_pt[1][1] + r, 0],
          [tibia_cut_pt[1][0] + r, tibia_cut_pt[1][1] - r, 0],
          [tibia_cut_pt[1][0] + r, tibia_cut_pt[1][1] + r, 0],
          [tibia_cut_pt[1][0] - r, tibia_cut_pt[1][1] - r, 0]]
    tibia_cut_pt_prop[0].setData(vmi.pdPolygon_Regular(point_size, tibia_cut_pt[0], [0, 0, 1]))
    tibia_cut_pt_prop[1].setData(vmi.pdAppend([vmi.pdPolyline([pt[0], pt[1]]),
                                               vmi.pdPolyline([pt[2], pt[3]])]))

    return


def update_tibia_cut():
    global post_ankle_pt
    t = vtk.vtkTransform()
    t.Identity()
    t.PreMultiply()
    t.Translate(tibia_cut_pt[0][0], tibia_cut_pt[0][1], 0)
    t.RotateZ(tibia_cut_angle)
    t.Translate(-tibia_cut_pt[0][0], -tibia_cut_pt[0][1], 0)
    t.Update()

    # 术后截骨线
    t.TransformPoint(tibia_cut_pt[1], tibia_cut_pt[2])
    tibia_cut_line_prop[1].setData(vmi.pdPolyline([tibia_cut_pt[0], tibia_cut_pt[2]]))

    # 术后力线
    if tibia_cut_angle == 0:
        post_line_prop.setData(None)
    else:
        post_ankle_pt = [0.5 * (ankle_pt[0][0] + ankle_pt[1][0]), 0.5 * (ankle_pt[0][1] + ankle_pt[1][1]), 0]
        tibia_center = [0.5 * (tibia_proximal_pt[0][0] + tibia_proximal_pt[1][0]),
                        0.5 * (tibia_proximal_pt[0][1] + tibia_proximal_pt[1][1]), 0]
        t.TransformPoint(post_ankle_pt, post_ankle_pt)
        post_line_prop.setData(vmi.pdAppend([vmi.pdPolyline([hip_cir_center, post_ankle_pt]),
                                             vmi.pdPolyline([tibia_center, post_ankle_pt])]))

    return


def update_parameter():
    pt = [[hip_cir_center,
           [0.5 * (femur_distal_pt[0][0] + femur_distal_pt[1][0]),
            0.5 * (femur_distal_pt[0][1] + femur_distal_pt[1][1]), 0]],
          [[0.5 * (tibia_proximal_pt[0][0] + tibia_proximal_pt[1][0]),
            0.5 * (tibia_proximal_pt[0][1] + tibia_proximal_pt[1][1]), 0],
           [0.5 * (ankle_pt[0][0] + ankle_pt[1][0]),
            0.5 * (ankle_pt[0][1] + ankle_pt[1][1]), 0]]]

    lines = [QLineF(QPointF(pt[0][0][0], pt[0][0][1]), QPointF(pt[0][1][0], pt[0][1][1])),
             QLineF(QPointF(pt[1][1][0], pt[1][1][1]), QPointF(pt[1][0][0], pt[1][0][1]))]

    deformity_angle = 180 - lines[0].angleTo(lines[1])
    deformity_angle *= LR
    if deformity_angle > 0:
        deformity_angle_box.draw_text('{:.2f} ° 膝内翻'.format(np.abs(deformity_angle)))
    elif deformity_angle < 0:
        deformity_angle_box.draw_text('{:.2f} ° 膝外翻'.format(np.abs(deformity_angle)))
    deformity_angle_box.setVisible(True)

    return


def LeftButtonPressMove(**kwargs):
    global rect_pos, hip_cir_center, femur_distal_pt, tibia_proximal_pt, ankle_pt, tibia_cut_pt
    if kwargs['picked'] in rect_prop:
        index = rect_prop.index(kwargs['picked'])
        rect_pos[index] += kwargs['picked'].view().pickVt_FocalPlane()

        update_rect_prop()
        update_joint_slice()

        if index == 0:
            hip_cir_center += kwargs['picked'].view().pickVt_FocalPlane()
            update_hip_prop()
            update_tibia_cut()
        elif index == 1:
            femur_distal_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
            femur_distal_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
            tibia_proximal_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
            tibia_proximal_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
            tibia_cut_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
            tibia_cut_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
            tibia_cut_pt[2] += kwargs['picked'].view().pickVt_FocalPlane()
            update_knee_prop()
            update_tibia_cut()
        elif index == 2:
            ankle_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
            ankle_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
            update_ankle_prop()
            update_tibia_cut()

        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is hip_cir_prop:
        hip_cir_center += kwargs['picked'].view().pickVt_FocalPlane()
        update_hip_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is femur_distal_pt_prop[0]:
        femur_distal_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is femur_distal_pt_prop[1]:
        femur_distal_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is femur_distal_line_prop:
        femur_distal_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        femur_distal_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is tibia_proximal_pt_prop[0]:
        tibia_proximal_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is tibia_proximal_pt_prop[1]:
        tibia_proximal_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is tibia_proximal_line_prop:
        tibia_proximal_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        tibia_proximal_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is ankle_pt_prop[0]:
        ankle_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        update_ankle_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is ankle_pt_prop[1]:
        ankle_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_ankle_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is ankle_line_prop:
        ankle_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        ankle_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_ankle_prop()
        update_tibia_cut()
        update_view_line()
        update_parameter()
        return True
    elif kwargs['picked'] is tibia_cut_pt_prop[0]:
        tibia_cut_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_tibia_cut()
        update_parameter()
        return True
    elif kwargs['picked'] is tibia_cut_pt_prop[1]:
        tibia_cut_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_tibia_cut()
        update_parameter()
        return True
    elif kwargs['picked'] is tibia_cut_line_prop[0]:
        tibia_cut_pt[0] += kwargs['picked'].view().pickVt_FocalPlane()
        tibia_cut_pt[1] += kwargs['picked'].view().pickVt_FocalPlane()
        tibia_cut_pt[2] += kwargs['picked'].view().pickVt_FocalPlane()
        update_knee_prop()
        update_tibia_cut()
        update_parameter()
        return True


def LeftButtonPressRelease(**kwargs):
    if kwargs['picked'] is xray_box:
        image = input_dicom()
        if image:
            xray_slice.setData(image)

            init_rect_prop()
            update_joint_slice()
            update_hip_prop()
            update_ankle_prop()
            update_knee_prop()
            update_view_line()

            xray_slice.bindColorWindow(joint_slice)
            xray_slice.setColorWindow_Auto()
            xray_view.setCamera_FitAll()
        return True


def NoButtonWheel(**kwargs):
    global hip_cir_radius, tibia_cut_angle
    if kwargs['picked'] is hip_cir_prop:
        hip_cir_radius += kwargs['delta']
        update_hip_prop()
        update_view_line()
        return True
    elif kwargs['picked'] is tibia_cut_pt_prop[0]:
        tibia_cut_angle += 0.1 * kwargs['delta']
        update_tibia_cut()
        return True


def return_globals():
    return globals()


if __name__ == '__main__':
    global xray_view, joint_view
    main = vmi.Main(return_globals)
    main.setAppName('Propsi HTO')
    main.setAppVersion('1.0')
    main.excludeKeys += ['main', 'i', 'box', 'prop']

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
        LR = 1
        point_size = 10
        xray_view = vmi.View()
        xray_view.mouse['LeftButton']['PressMove'] = [xray_view.mouseBlock]
        xray_view.mouse['MidButton']['PressMove'] = [xray_view.mouseBlock]
        xray_view.mouse['RightButton']['PressMove'] = [xray_view.mouseBlock]

        xray_slice = vmi.ImageSlice(xray_view)  # 断层显示
        xray_slice.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        xray_box = vmi.TextBox(xray_view, text='DICOM', pickable=True,
                               size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0])
        xray_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        patient_name_box = vmi.TextBox(xray_view, text='姓名', visible=False,
                                       size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])
        patient_LR_box = vmi.TextBox(xray_view, text='患侧', visible=False,
                                     size=[0.2, 0.04], pos=[0, 0.14], anchor=[0, 0])

        rect_size = [0, 0]
        rect_pos = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        rect_prop = [vmi.PolyActor(xray_view, color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True, pickable=True,
                                   opacity=0.3),
                     vmi.PolyActor(xray_view, color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True, pickable=True,
                                   opacity=0.3),
                     vmi.PolyActor(xray_view, color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True, pickable=True,
                                   opacity=0.3)]

        for p in rect_prop:
            p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        # 123 局部图像
        joint_view = [vmi.View(), vmi.View(), vmi.View()]

        for v in joint_view:
            v.mouse['MidButton']['PressMove'] = [v.mouseBlock]
            v.mouse['RightButton']['PressMove'] = [v.mouseBlock]

        joint_slice = [vmi.ImageSlice(joint_view[0]),
                       vmi.ImageSlice(joint_view[1]),
                       vmi.ImageSlice(joint_view[2])]

        hip_ankle_line_prop = [vmi.PolyActor(xray_view, color=[1, 0, 0], line_width=3, always_on_top=True),
                               vmi.PolyActor(joint_view[0], color=[1, 0, 0], line_width=3, always_on_top=True),
                               vmi.PolyActor(joint_view[1], color=[1, 0, 0], line_width=3, always_on_top=True),
                               vmi.PolyActor(joint_view[2], color=[1, 0, 0], line_width=3, always_on_top=True)]

        hip_femur_line_prop = [vmi.PolyActor(xray_view, color=[1, 0, 0], line_width=3, always_on_top=True),
                               vmi.PolyActor(joint_view[0], color=[1, 0, 0], line_width=3, always_on_top=True),
                               vmi.PolyActor(joint_view[1], color=[1, 0, 0], line_width=3, always_on_top=True),
                               vmi.PolyActor(joint_view[2], color=[1, 0, 0], line_width=3, always_on_top=True)]

        ankle_tibia_line_prop = [vmi.PolyActor(xray_view, color=[1, 0, 0], line_width=3, always_on_top=True),
                                 vmi.PolyActor(joint_view[0], color=[1, 0, 0], line_width=3, always_on_top=True),
                                 vmi.PolyActor(joint_view[1], color=[1, 0, 0], line_width=3, always_on_top=True),
                                 vmi.PolyActor(joint_view[2], color=[1, 0, 0], line_width=3, always_on_top=True)]

        # # 术后力线
        post_ankle_pt = [0, 0, 0]
        post_line_prop = vmi.PolyActor(xray_view, color=[0.6, 0.8, 0.4], line_width=3, always_on_top=True)

        # # 参数计算
        deformity_angle_box = vmi.TextBox(xray_view, text='', visible=False,
                                          size=[0.2, 0.04], pos=[0, 0.18], anchor=[0, 0])

        # 髋视图
        hip_cir_center, hip_cir_radius = [0, 0, 0], 0
        hip_cir_prop = vmi.PolyActor(joint_view[0], color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True,
                                     pickable=True, opacity=0.3)
        hip_cir_prop.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        hip_cir_prop.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        # 膝视图
        # # 股骨远端连线
        femur_distal_pt = [[0, 0, 0], [0, 0, 0]]
        femur_distal_line_prop = vmi.PolyActor(joint_view[1], color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True,
                                               pickable=True)
        femur_distal_pt_prop = [vmi.PolyActor(joint_view[1], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                              pickable=True),
                                vmi.PolyActor(joint_view[1], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                              pickable=True)]
        # # 胫骨近端连线
        tibia_proximal_pt = [[0, 0, 0], [0, 0, 0]]
        tibia_proximal_line_prop = vmi.PolyActor(joint_view[1], color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True,
                                                 pickable=True)
        tibia_proximal_pt_prop = [vmi.PolyActor(joint_view[1], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                                pickable=True),
                                  vmi.PolyActor(joint_view[1], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                                pickable=True)]
        # # 胫骨截骨连线
        tibia_cut_pt = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        tibia_cut_angle = 0
        tibia_cut_line_prop = [vmi.PolyActor(joint_view[1], color=[0, 0.7, 0.8], line_width=3, always_on_top=True,
                                             pickable=True),
                               vmi.PolyActor(joint_view[1], color=[0, 0.7, 0.8], line_width=3, always_on_top=True,
                                             pickable=False)]
        tibia_cut_pt_prop = [vmi.PolyActor(joint_view[1], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                           pickable=True, opacity=0.3),
                             vmi.PolyActor(joint_view[1], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                           pickable=True)]

        tibia_cut_pt_prop[0].mouse['NoButton']['Wheel'] = [NoButtonWheel]
        for p in femur_distal_pt_prop + tibia_proximal_pt_prop + tibia_cut_pt_prop:
            p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
        for p in [femur_distal_line_prop, tibia_proximal_line_prop, tibia_cut_line_prop[0]]:
            p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

        # 踝视图
        ankle_pt = [[0, 0, 0], [0, 0, 0]]
        ankle_line_prop = vmi.PolyActor(joint_view[2], color=[0.2, 0.3, 0.7], line_width=3, always_on_top=True,
                                        pickable=True)
        ankle_pt_prop = [vmi.PolyActor(joint_view[2], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                       pickable=True),
                         vmi.PolyActor(joint_view[2], color=[1, 0.8, 0.2], line_width=3, always_on_top=True,
                                       pickable=True)]
        for p in ankle_pt_prop + [ankle_line_prop]:
            p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

    # 视图布局
    for v in [xray_view, joint_view[0], joint_view[1], joint_view[2]]:
        v.setMinimumWidth(round(0.2 * main.screenWidth()))
        v.renderer().SetBackground(0, 0, 0)

    xray_view.setParent(main.scrollArea())
    main.layout().addWidget(xray_view, 0, 0, 2, 1)
    main.layout().addWidget(joint_view[0], 0, 2, 1, 1)
    main.layout().addWidget(joint_view[1], 0, 1, 2, 1)
    main.layout().addWidget(joint_view[2], 1, 2, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
