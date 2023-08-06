import vtk
import numpy as np

import vmi
import SimpleITK as sitk

import tempfile
import shutil
import pathlib

from PySide2.QtGui import *
from typing import List, Union


def threshold_division(image: vtk.vtkImageData, p: [np.ndarray, List[float]]):
    ext = vmi.imExtent(image)
    org = vmi.imOrigin(image)
    spc = vmi.imSpacing(image)

    image_ary = vmi.imArray_VTK(image)
    seed_pick = [int(np.floor((p[0] - org[0]) / spc[0])),
                 int(np.floor((p[1] - org[1]) / spc[1])),
                 int(np.floor((p[2] - org[2]) / spc[2]))]

    if ext[0] + 1 > seed_pick[0]:
        return
    if seed_pick[0] > ext[1] - 1:
        return
    if ext[2] + 1 > seed_pick[1]:
        return
    if seed_pick[1] > ext[3] - 1:
        return

    threshold = image_ary[seed_pick[1]][seed_pick[0]]

    seed = seed_pick.copy()
    pix = seed_pick.copy()
    pix_temp = [0, 0, 0]

    neighbors = [[-1, -1, 0],
                 [-1, 0, 0],
                 [-1, 1, 0],
                 [0, 1, 0],
                 [1, 1, 0],
                 [1, 0, 0],
                 [1, -1, 0],
                 [0, -1, 0]]

    zero_index = 0

    pts_list = []
    pts_list.append(p)

    while True:
        for s in range(8):
            pix_temp[0] = pix.copy()[0] + neighbors[(s + zero_index + 1) % 8][0]
            pix_temp[1] = pix.copy()[1] + neighbors[(s + zero_index + 1) % 8][1]
            pix_temp[2] = pix.copy()[2] + neighbors[(s + zero_index + 1) % 8][2]

            judge = [ext[0] <= pix_temp[0], pix_temp[0] <= ext[1],
                     ext[2] <= pix_temp[1], pix_temp[1] <= ext[3],
                     ext[4] <= pix_temp[2], pix_temp[2] <= ext[5]]

            if judge[0] and judge[1] and judge[2] and judge[3] and judge[4] and judge[5]:
                val = image_ary[pix_temp[1]][pix_temp[0]]

                if val >= threshold:
                    pt = [org[0] + (pix_temp[0] * spc[0]),
                          org[1] + (pix_temp[1] * spc[1]),
                          org[2] + (pix_temp[2] * spc[2])]

                    pts_list.append(pt)
                    pix = pix_temp.copy()

                    zero_index = (s + zero_index + 1 + 4) % 8
                    break
            else:
                continue

        if pix == seed:
            break

    return pts_list


def co_area(pts: List[Union[np.ndarray, List[float]]]):
    if external_slice.data():
        image = external_slice.data()
        cs = external_view.cameraCS_FPlane()
        d = vmi.imSize_Vt(image, cs.axis(1))
        pts = [pt - d * cs.axis(2) for pt in pts]
        sh = vmi.ccFace(vmi.ccWire(vmi.ccSegments(pts, True)))
        sh = vmi.ccPrism(sh, cs.axis(2), 2 * d)

        mask = vmi.imStencil_PolyData(vmi.ccPd_Sh(sh),
                                      vmi.imOrigin(image),
                                      vmi.imSpacing(image),
                                      vmi.imExtent(image))

        num = np.sum(vmi.imArray_VTK(mask)) // 255
        spc = vmi.imSpacing(image)
        area = num * spc[0] * spc[1]

        return area


def addTextActor(view, s: str, p: np.ndarray, f: vtk.vtkFollower):
    text = vtk.vtkVectorText()
    text.SetText(s)
    text.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
    mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, -66000)
    mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
    mapper.SetInputData(text.GetOutput())

    r = 5 * pt_radius
    view.renderer().RemoveActor(f)
    f.SetMapper(mapper)
    f.SetScale(r, r, r)
    f.SetPosition(p)

    view.renderer().AddActor(f)
    f.SetCamera(view.renderer().GetActiveCamera())


def pdSplineKochanek(pts: List[Union[np.ndarray, List[float]]], ptn: int, closed: bool = False):
    if len(pts) < 2:
        return

    points = vtk.vtkPoints()
    for pt in pts:
        points.InsertNextPoint([pt[0], pt[1], pt[2]])

    xSpline = vtk.vtkKochanekSpline()
    ySpline = vtk.vtkKochanekSpline()
    zSpline = vtk.vtkKochanekSpline()

    pSpline = vtk.vtkParametricSpline()
    pSpline.SetXSpline(xSpline)
    pSpline.SetYSpline(ySpline)
    pSpline.SetZSpline(zSpline)
    pSpline.SetPoints(points)
    pSpline.SetClosed(closed)
    pSpline.SetParameterizeByLength(1)
    pSpline.SetLeftConstraint(1)
    pSpline.SetRightConstraint(1)

    pfSource = vtk.vtkParametricFunctionSource()
    pfSource.SetParametricFunction(pSpline)
    pfSource.SetUResolution(ptn - 1)
    pfSource.SetVResolution(ptn - 1)
    pfSource.SetWResolution(ptn - 1)
    pfSource.Update()

    return pfSource.GetOutput()


def ask_enhance_image_format():
    global external_image
    select = vmi.askButtons(['JPG', 'Dicom'])

    if select == 'JPG':
        external_image = input_image()
    elif select == 'Dicom':
        external_image = input_dicom()

    if external_image:
        external_slice.setData(external_image)
        external_slice.setColorWindow_Auto()
        external_slice.setSlicePlaneOrigin_Center()
        external_slice.setSlicePlaneNormal_Axial()
        external_view.setCamera_Axial()
        external_view.setCamera_FitAll()


def ask_normal_image_format():
    global internal_image
    select = vmi.askButtons(['JPG', 'Dicom'])

    if select == 'JPG':
        internal_image = input_image()
    elif select == 'Dicom':
        internal_image = input_dicom()

    internal_slice.setData(internal_image)
    internal_slice.setColorWindow_Auto()
    internal_slice.setSlicePlaneOrigin_Center()
    internal_slice.setSlicePlaneNormal_Axial()
    internal_view.setCamera_Axial()
    internal_view.setCamera_FitAll()


def input_dicom():
    file = vmi.askOpenFile('*.dcm', '请选择打开图像 (Please select open Dicom)')

    if file is None:
        return
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.dcm'
        shutil.copyfile(file, p)
        r = sitk.ImageFileReader()
        r.SetFileName(str(p))

        image = vmi.imVTK_SITK(r.Execute())
        image_ary = vmi.imArray_VTK(image)

        ori, spc = [0, 0, 0], [1, 1, 1]
        return vmi.imVTK_Array(np.array([image_ary]), ori, spc)


def input_image():
    file = vmi.askOpenFile('*.JPG', '请选择打开图像 (Please select open image)')

    if file is None:
        return

    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.jpg'
        shutil.copyfile(file, p)
        r = vtk.vtkJPEGReader()
        r.SetFileName(str(p))
        r.Update()

        image_ary = vmi.imArray_VTK(r.GetOutput())
        image_ary = np.flipud(image_ary)

        ori, spc = [0, 0, 0], [1, 1, 1]
        return vmi.imVTK_Array(np.array([image_ary]), ori, spc)


def bu_mark():
    global mark_list
    if external_image:
        pt = external_view.pickPt_Cell()
        mark_list.append(pt)
        pd_list = vmi.pdSphere(pt_radius, pt)

        for p in mark_list:
            pd_list = vmi.pdAppend([pd_list, vmi.pdSphere(pt_radius, p)])
        if len(mark_list) > 1:
            mark_line.setData(pdSplineKochanek(mark_list, 100 * len(mark_list)))

        mark_prop.setData(pd_list)


def map_mark():
    global mark_prop_data, draw_prop_data
    if internal_image:
        mark_prop_data = vmi.pdAppend([mark_prop.data(), mark_line.data()])
        for i, prop in enumerate(color_prop):
            draw_prop_data[i] = prop.data()

        c = mark_prop_data.GetCenter()
        if external_scale and internal_scale is not None:
            s = external_scale / internal_scale

            t = vtk.vtkTransform()
            t.Identity()
            t.PreMultiply()
            t.Translate(c[0], c[1], 0)
            t.Scale(s, s, s)
            t.Translate(-c[0], -c[1], 0)
            t.Update()
            mark_prop_data = vmi.pdTransform(mark_prop_data, t)

        if external_scale and internal_scale is not None:
            for i, data in enumerate(draw_prop_data):
                s = external_scale / internal_scale

                t = vtk.vtkTransform()
                t.Identity()
                t.PreMultiply()
                t.Translate(c[0], c[1], 0)
                t.Scale(s, s, s)
                t.Translate(-c[0], -c[1], 0)
                t.Update()
                draw_prop_data[i] = vmi.pdTransform(data, t)

        map_mark_prop.setData(mark_prop_data)
        mark_list.clear()
        update_map()


def draw_range():
    global draw_list
    if external_image:
        pt = external_view.pickPt_Cell()
        draw_list.append(pt)
        if len(draw_list) > 1:
            draw_prop.setData(vmi.pdPolyline(draw_list, closed=True))


def map_draw():
    global mark_prop_data, draw_prop_data
    if internal_image:
        for i, prop in enumerate(color_prop):
            draw_prop_data[i] = prop.data()

    mark_prop_data = vmi.pdAppend([mark_prop.data(), mark_line.data()])

    c = mark_prop_data.GetCenter()
    if external_scale and internal_scale is not None:
        s = external_scale / internal_scale

        t = vtk.vtkTransform()
        t.Identity()
        t.PreMultiply()
        t.Translate(c[0], c[1], 0)
        t.Scale(s, s, s)
        t.Translate(-c[0], -c[1], 0)
        t.Update()
        mark_prop_data = vmi.pdTransform(mark_prop_data, t)

    if external_scale and internal_scale is not None:
        for i, data in enumerate(draw_prop_data):
            s = external_scale / internal_scale

            t = vtk.vtkTransform()
            t.Identity()
            t.PreMultiply()
            t.Translate(c[0], c[1], 0)
            t.Scale(s, s, s)
            t.Translate(-c[0], -c[1], 0)
            t.Update()
            draw_prop_data[i] = vmi.pdTransform(data, t)
            map_color_prop[i].setData(draw_prop_data[i])

    update_map()


def update_map():
    global mark_prop_data, draw_prop_data
    if internal_image:
        c = map_mark_prop.data().GetCenter()
        if map_mark_prop:
            t = vtk.vtkTransform()
            t.Identity()
            t.PreMultiply()
            t.Translate(c[0], c[1], 0)
            t.Scale(scale, scale, scale)
            t.RotateZ(rotate)
            t.Translate(-c[0], -c[1], 0)
            t.Update()
            map_mark_prop.setData(vmi.pdTransform(mark_prop_data, t))

        if map_color_prop:
            for i, data in enumerate(draw_prop_data):
                t = vtk.vtkTransform()
                t.Identity()
                t.PreMultiply()
                t.Translate(c[0], c[1], 0)
                t.Scale(scale, scale, scale)
                t.RotateZ(rotate)
                t.Translate(-c[0], -c[1], 0)
                t.Update()

                map_color_prop[i].setData(vmi.pdTransform(data, t))


def init_map():
    global rotate, scale
    rotate, scale = 0, 1
    rotate_box.draw_text('旋转 {:.1f}'.format(rotate))
    scale_box.draw_text('缩放 {:.2f}'.format(scale))
    map_mark()
    map_draw()


def init_external_scale():
    global external_scale_list, external_pix_dis, external_real_dis, external_scale
    if external_image:
        pt = external_view.pickPt_Cell()
        external_scale_list.append(pt)

        if len(external_scale_list) == 1:
            external_scale_prop_pts[0].setData(vmi.pdSphere(pt_radius, pt))
            external_scale_prop_pts[1].setData(None)
            external_scale_prop_line.setData(None)
            external_view.renderer().RemoveActor(external_scale_follower)

        elif len(external_scale_list) == 2:
            external_pix_dis = np.linalg.norm(external_scale_list[1] - external_scale_list[0])
            external_scale_prop_pts[1].setData(vmi.pdSphere(pt_radius, pt))
            external_scale_prop_line.setData(pdSplineKochanek(external_scale_list, int(external_pix_dis)))

            mid_pt = (external_scale_list[0] + external_scale_list[1]) / 2
            external_scale_list.clear()

            real_dis = vmi.askInt(1, 50, 10000, 5, suffix=' mm', title='输入实际距离')
            if real_dis:
                external_real_dis = real_dis
                addTextActor(external_view, str(external_real_dis) + ' mm', mid_pt, external_scale_follower)

                external_scale = external_real_dis / external_pix_dis
                external_scale_prop_box.draw_text('确定标尺位置')

                update_area_scale()
                init_map()


def init_internal_scale():
    global internal_scale_list, internal_pix_dis, internal_real_dis, internal_scale
    if internal_image:
        pt = internal_view.pickPt_Cell()
        internal_scale_list.append(pt)

        if len(internal_scale_list) == 1:
            internal_scale_prop_pts[0].setData(vmi.pdSphere(pt_radius, pt))
            internal_scale_prop_pts[1].setData(None)
            internal_scale_prop_line.setData(None)
            internal_view.renderer().RemoveActor(internal_scale_follower)

        elif len(internal_scale_list) == 2:
            internal_pix_dis = np.linalg.norm(internal_scale_list[1] - internal_scale_list[0])
            internal_scale_prop_pts[1].setData(vmi.pdSphere(pt_radius, pt))
            internal_scale_prop_line.setData(pdSplineKochanek(internal_scale_list, int(internal_pix_dis)))

            mid_pt = (internal_scale_list[0] + internal_scale_list[1]) / 2
            internal_scale_list.clear()

            real_dis = vmi.askInt(1, 50, 10000, 5, suffix=' mm', title='输入实际距离')
            if real_dis:
                internal_real_dis = real_dis
                addTextActor(internal_view, str(internal_real_dis) + ' mm', mid_pt, internal_scale_follower)

                internal_scale = internal_real_dis / internal_pix_dis
                internal_scale_prop_box.draw_text('确定标尺位置')
                init_map()


def update_area_scale():
    global area_list
    if external_scale is not None:
        s = external_scale
        for i, area in enumerate(area_list):
            area_boxes[i].draw_text('{:.2f} mm2'.format(area * s * s))

        total_area = np.sum(np.array(area_list))
        total_box.draw_text('总计： {:.2f} mm2'.format(total_area * s * s))
    else:
        for i, area in enumerate(area_list):
            area_boxes[i].draw_text('{:.2f} mm2'.format(0))


def NoButtonEnter(**kwargs):
    if kwargs['picked'] in area_boxes:
        index = area_boxes.index(kwargs['picked'])
        area_boxes[index].draw_text('清除')
        return


def NoButtonMove(**kwargs):
    global external_image, draw_list, move_flag, move_list
    if kwargs['picked'] is external_slice:
        if draw_box.text() == '选择填充颜色':
            if move_flag:
                pt = external_view.pickPt_Cell()
                move_list = threshold_division(external_image, pt)
                if len(move_list) > 1:
                    draw_prop.setData(vmi.pdPolyline(move_list, closed=True))
                    return True


def NoButtonLeave(**kwargs):
    if kwargs['picked'] in area_boxes:
        update_area_scale()
        return


def LeftButtonPress(**kwargs):
    if kwargs['picked'] is external_slice:
        if draw_box.text() == '选择填充颜色':
            draw_list.clear()
            return True


def LeftButtonPressMove(**kwargs):
    global mark_prop_data, draw_prop_data, move_flag
    if kwargs['picked'] is external_slice:
        if draw_box.text() == '选择填充颜色':
            move_flag = False
            draw_range()
            return True
    if kwargs['picked'] in [map_mark_prop]:
        c = np.zeros(3)
        c += kwargs['picked'].view().pickVt_FocalPlane()

        t = vtk.vtkTransform()
        t.Identity()
        t.PreMultiply()
        t.Translate(c[0], c[1], 0)
        t.Update()

        map_mark_prop.setData(vmi.pdTransform(map_mark_prop.data(), t))
        mark_prop_data = vmi.pdTransform(mark_prop_data, t)

        for i, data in enumerate(draw_prop_data):
            map_color_prop[i].setData(vmi.pdTransform(map_color_prop[i].data(), t))
            draw_prop_data[i] = vmi.pdTransform(data, t)

            return True


def LeftButtonPressRelease(**kwargs):
    global move_flag, draw_list, area_list
    if kwargs['picked'] is mark_box:
        if mark_box.text() == '标记参照范围':
            if external_scale_prop_box.text() == '确定标尺位置':
                if draw_box.text() == '绘制目标区域':
                    mark_box.draw_text('确定')
        elif mark_box.text() == '确定':
            mark_box.draw_text('标记参照范围')
            init_map()
            return True
    elif kwargs['picked'] is draw_box:
        if draw_box.text() == '绘制目标区域':
            if external_scale_prop_box.text() == '确定标尺位置':
                draw_box.draw_text('选择填充颜色')
                move_flag = True
                return True
    elif kwargs['picked'] is external_slice:
        if mark_box.text() == '确定':
            bu_mark()
        elif external_scale_prop_box.text() == '定位标注':
            init_external_scale()
        elif draw_box.text() == '选择填充颜色':
            if move_flag:
                move_flag = False
                return True
    elif kwargs['picked'] is internal_slice:
        if internal_scale_prop_box.text() == '定位标注':
            init_internal_scale()
            return True
    elif kwargs['picked'] is external_scale_prop_box:
        if external_scale_prop_box.text() == '确定标尺位置':
            if mark_box.text() == '标记参照范围':
                if draw_box.text() == '绘制目标区域':
                    external_scale_prop_box.draw_text('定位标注')
    elif kwargs['picked'] is internal_scale_prop_box:
        if internal_scale_prop_box.text() == '确定标尺位置':
            internal_scale_prop_box.draw_text('定位标注')
            return True
    elif kwargs['picked'] in color_boxes:
        if draw_box.text() == '选择填充颜色':
            index = color_boxes.index(kwargs['picked'])
            color_prop[index].setData(draw_prop)
            map_color_prop[index].setData(draw_prop)

            if len(draw_list) == 0:
                draw_list = move_list

            area_list[index] = co_area(draw_list)
            update_area_scale()

            draw_prop.setData(None)
            draw_list.clear()
            draw_box.draw_text('绘制目标区域')
            init_map()
            return True
    elif kwargs['picked'] in area_boxes:
        index = area_boxes.index(kwargs['picked'])
        color_prop[index].setData(None)
        map_color_prop[index].setData(None)

        area_list[index] = 0
        update_area_scale()
        return True


def NoButtonWheel(**kwargs):
    global rotate, scale
    if kwargs['picked'] is rotate_box:
        rotate = min(max(rotate + 0.5 * kwargs['delta'],
                         -180), 180)
        rotate_box.draw_text('旋转 {:.1f}'.format(rotate))
        update_map()
        return True
    elif kwargs['picked'] is scale_box:
        scale = min(max(scale + 0.01 * kwargs['delta'],
                        0.5), 100)
        scale_box.draw_text('缩放 {:.2f}'.format(scale))
        update_map()
        return True


def return_globals():
    return globals()


if __name__ == '__main__':
    main = vmi.Main(return_globals)
    main.setAppName('KidneyImageRegistration')
    main.excludeKeys += ['main']

    menu_input = main.menuBar().addMenu('输入')
    menu_input.addAction('选择图像1').triggered.connect(ask_enhance_image_format)
    menu_input.addAction('选择图像2').triggered.connect(ask_normal_image_format)

    # 普通视图
    external_view = vmi.View()
    external_view.mouse['LeftButton']['PressMove'] = [external_view.mouseBlock]
    external_view.mouse['NoButton']['Wheel'] = [external_view.mouseBlock]

    external_image = []
    external_slice = vmi.ImageSlice(external_view)
    external_slice.mouse['LeftButton']['Press'] = [LeftButtonPress]
    external_slice.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    external_slice.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    external_slice.mouse['NoButton']['Move'] = [NoButtonMove]
    external_slice.mouse['RightButton']['PressRelease'] = [external_slice.mouseBlock]

    mark_box = vmi.TextBox(external_view, text='标记参照范围',
                           size=[0.2, 0.06], pos=[0, 0.21], anchor=[0, 0], pickable=True)
    draw_box = vmi.TextBox(external_view, text='绘制目标区域',
                           size=[0.2, 0.06], pos=[0, 0.27], anchor=[0, 0], pickable=True)
    mark_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    draw_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    color_list = [[1, 0, 0], [1, 0.4, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1],
                  [0, 1, 1], [0, 0.1, 0.4], [1, 0.4, 1], [0.4, 0, 0.4], [0.4, 0, 0]]

    color_boxes = [
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[0][0], color_list[0][1], color_list[0][2]),
                    size=[0.04, 0.04], pos=[0, 0.33], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[1][0], color_list[1][1], color_list[1][2]),
                    size=[0.04, 0.04], pos=[0, 0.37], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[2][0], color_list[2][1], color_list[2][2]),
                    size=[0.04, 0.04], pos=[0, 0.41], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[3][0], color_list[3][1], color_list[3][2]),
                    size=[0.04, 0.04], pos=[0, 0.45], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[4][0], color_list[4][1], color_list[4][2]),
                    size=[0.04, 0.04], pos=[0, 0.49], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[5][0], color_list[5][1], color_list[5][2]),
                    size=[0.04, 0.04], pos=[0, 0.53], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[6][0], color_list[6][1], color_list[6][2]),
                    size=[0.04, 0.04], pos=[0, 0.57], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[7][0], color_list[7][1], color_list[7][2]),
                    size=[0.04, 0.04], pos=[0, 0.61], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[8][0], color_list[8][1], color_list[8][2]),
                    size=[0.04, 0.04], pos=[0, 0.65], anchor=[0, 0], pickable=True),
        vmi.TextBox(external_view, back_color=QColor.fromRgbF(color_list[9][0], color_list[9][1], color_list[9][2]),
                    size=[0.04, 0.04], pos=[0, 0.69], anchor=[0, 0], pickable=True)]

    area_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    area_boxes = [vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[0]),
                              size=[0.16, 0.04], pos=[0.04, 0.33], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[1]),
                              size=[0.16, 0.04], pos=[0.04, 0.37], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[2]),
                              size=[0.16, 0.04], pos=[0.04, 0.41], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[3]),
                              size=[0.16, 0.04], pos=[0.04, 0.45], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[4]),
                              size=[0.16, 0.04], pos=[0.04, 0.49], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[5]),
                              size=[0.16, 0.04], pos=[0.04, 0.53], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[6]),
                              size=[0.16, 0.04], pos=[0.04, 0.57], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[7]),
                              size=[0.16, 0.04], pos=[0.04, 0.61], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[8]),
                              size=[0.16, 0.04], pos=[0.04, 0.65], anchor=[0, 0], pickable=True),
                  vmi.TextBox(external_view, text='{:.2f} mm2'.format(area_list[9]),
                              size=[0.16, 0.04], pos=[0.04, 0.69], anchor=[0, 0], pickable=True)]
    total_box = vmi.TextBox(external_view, text='总计： {:.2f} mm2'.format(0),
                            size=[0.2, 0.04], pos=[0, 0.73], anchor=[0, 0], pickable=False)

    for box in color_boxes:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    for box in area_boxes:
        box.mouse['NoButton']['Enter'].insert(0, NoButtonEnter)
        box.mouse['NoButton']['Leave'].insert(0, NoButtonLeave)
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    move_flag = False

    pt_radius = 12
    mark_list = []
    mark_line = vmi.PolyActor(external_view, color=[0.4, 0.6, 1], line_width=3, pickable=False, always_on_top=True)
    mark_prop = vmi.PolyActor(external_view, color=[0.4, 0.6, 1], line_width=3, pickable=False, always_on_top=True)

    move_list = []
    draw_list = []
    draw_prop = vmi.PolyActor(external_view, color=[1, 1, 1], line_width=3, pickable=False, always_on_top=True)

    mark_prop_data = vtk.vtkPolyData
    draw_prop_data = [vtk.vtkPolyData, vtk.vtkPolyData, vtk.vtkPolyData, vtk.vtkPolyData, vtk.vtkPolyData,
                      vtk.vtkPolyData, vtk.vtkPolyData, vtk.vtkPolyData, vtk.vtkPolyData, vtk.vtkPolyData]

    color_prop = [vmi.PolyActor(external_view, color=color_list[0], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[1], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[2], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[3], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[4], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[5], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[6], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[7], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[8], line_width=3, pickable=False, always_on_top=True),
                  vmi.PolyActor(external_view, color=color_list[9], line_width=3, pickable=False, always_on_top=True)]

    # 普通视图比例尺
    external_scale, external_real_dis, external_pix_dis = None, None, None

    external_scale_list = []
    external_scale_prop_line = vmi.PolyActor(
        external_view, color=[0.4, 1, 0.6], line_width=3, pickable=False, always_on_top=True)
    external_scale_prop_pts = [
        vmi.PolyActor(external_view, color=[0.4, 1, 0.6], line_width=3, pickable=True, always_on_top=True),
        vmi.PolyActor(external_view, color=[0.4, 1, 0.6], line_width=3, pickable=True, always_on_top=True)]

    external_scale_prop_box = vmi.TextBox(external_view, text='确定标尺位置',
                                          size=[0.2, 0.06], pos=[0, 0.15], anchor=[0, 0], pickable=True)
    external_scale_prop_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    external_scale_follower = vtk.vtkFollower()
    external_scale_follower.SetPickable(False)

    # 增强视图
    internal_view = vmi.View()
    internal_view.mouse['LeftButton']['PressMove'] = [internal_view.mouseBlock]
    internal_view.mouse['NoButton']['Wheel'] = [internal_view.mouseBlock]

    internal_image = []
    internal_slice = vmi.ImageSlice(internal_view)
    internal_slice.mouse['LeftButton']['PressMove'] = [internal_slice.mouseBlock]
    internal_slice.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
    internal_slice.mouse['RightButton']['PressRelease'] = [internal_slice.mouseBlock]

    rotate, scale = 0, 1
    rotate_box = vmi.TextBox(internal_view, text='旋转 {:.1f}'.format(rotate),
                             size=[0.2, 0.06], pos=[0, 0.21], anchor=[0, 0], pickable=True)
    scale_box = vmi.TextBox(internal_view, text='缩放 {:.2f}'.format(scale),
                            size=[0.2, 0.06], pos=[0, 0.27], anchor=[0, 0], pickable=True)
    for box in [rotate_box] + [scale_box]:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    map_mark_prop = vmi.PolyActor(internal_view, color=[0.4, 0.6, 1], line_width=3, pickable=True, always_on_top=True)
    map_draw_prop = vmi.PolyActor(internal_view, color=[1, 1, 0.6], line_width=3, pickable=False, always_on_top=True)

    for p in [map_mark_prop, map_draw_prop]:
        p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

    map_color_prop = [
        vmi.PolyActor(internal_view, color=color_list[0], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[1], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[2], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[3], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[4], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[5], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[6], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[7], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[8], line_width=3, pickable=False, always_on_top=True),
        vmi.PolyActor(internal_view, color=color_list[9], line_width=3, pickable=False, always_on_top=True)]

    # 增强视图比例尺
    internal_scale, internal_real_dis, internal_pix_dis = None, None, None

    internal_scale_list = []
    internal_scale_prop_line = vmi.PolyActor(
        internal_view, color=[0.4, 1, 0.6], line_width=3, pickable=False, always_on_top=True)
    internal_scale_prop_pts = [
        vmi.PolyActor(internal_view, color=[0.4, 1, 0.6], line_width=3, pickable=True, always_on_top=True),
        vmi.PolyActor(internal_view, color=[0.4, 1, 0.6], line_width=3, pickable=True, always_on_top=True)]

    internal_scale_prop_box = vmi.TextBox(internal_view, text='确定标尺位置',
                                          size=[0.2, 0.06], pos=[0, 0.15], anchor=[0, 0], pickable=True)
    internal_scale_prop_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    internal_scale_follower = vtk.vtkFollower()
    internal_scale_follower.SetPickable(False)

    # 视图布局
    main.layout().addWidget(external_view, 0, 1, 1, 1)
    main.layout().addWidget(internal_view, 0, 2, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
