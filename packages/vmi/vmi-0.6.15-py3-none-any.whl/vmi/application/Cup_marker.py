import glob
import vtk
import numpy as np
import pandas as pd

import vmi

from PySide2.QtCore import *
from PySide2.QtWidgets import *

SizePolicyMinimum = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


def input_dir():
    global file_dir

    s = QSettings()
    title = '请选择文件夹 (Please select directory)'

    d = QFileDialog(None, title, str(s.value('Last' + title, defaultValue=vmi.desktopPath)))
    d.setAcceptMode(QFileDialog.AcceptOpen)
    d.setFileMode(QFileDialog.Directory)
    d.setViewMode(QFileDialog.Detail)
    d.setFilter(QDir.AllEntries | QDir.NoSymLinks | QDir.NoDotAndDotDot)

    if d.exec_() != QDialog.Accepted or len(d.selectedFiles()) < 1:
        return

    s.setValue('Last' + title, d.selectedFiles()[0])
    file_dir = d.selectedFiles()[0]

    input_list()


def input_list():
    global file_list, file_name, cup_origin, cup_radius, cup_cs, cup_angle

    if file_dir:
        file_list = glob.glob(r'{}/*.nii.gz'.format(file_dir))

        npy_dir = str(file_dir[:-6]) + '/npy'
        npy_list = glob.glob(r'{}/*.npy'.format(npy_dir))

        mark_dir = str(file_dir[:-6]) + '/mark/npy'
        mark_list = glob.glob(r'{}/*.npy'.format(mark_dir))

        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(['File Names'])

        for x in file_list:
            suffix = str('\\' + x.split('\\')[1])[:-7]
            index = npy_dir + suffix + '.npy'
            mark_index = npy_dir[:-3] + 'mark/npy' + suffix + '_mark.npy'

            if index in npy_list:
                if mark_index not in mark_list:
                    item = QTreeWidgetItem()
                    item.setText(0, x)
                    tree.addTopLevelItem(item)

        dialog = QDialog()
        dialog.setSizePolicy(SizePolicyMinimum)
        dialog.setWindowTitle('选择文件')
        dialog.setLayout(QVBoxLayout())
        dialog.setMinimumWidth(500)
        dialog.layout().addWidget(tree)

        button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button.setSizePolicy(SizePolicyMinimum)
        button.accepted.connect(dialog.accept)
        button.rejected.connect(dialog.reject)
        dialog.layout().addWidget(button)

        if dialog.exec_() == QDialog.Accepted:
            file_name = tree.currentItem().text(0)

            cup_origin, cup_radius, cup_cs, cup_angle = [[0, 0, 0], [0, 0, 0]], [24, 24], [[], []], [[20, 40], [20, 40]]

            radius_boxes[0].draw_text('右侧半径 {:.1f}'.format(cup_radius[0]))
            radius_boxes[1].draw_text('左侧半径 {:.1f}'.format(cup_radius[1]))
            angle_boxes[0].draw_text('右侧前倾 {:.1f}'.format(cup_angle[0][0]))
            angle_boxes[1].draw_text('右侧外展 {:.1f}'.format(cup_angle[0][1]))
            angle_boxes[2].draw_text('左侧前倾 {:.1f}'.format(cup_angle[1][0]))
            angle_boxes[3].draw_text('左侧外展 {:.1f}'.format(cup_angle[1][1]))

            init_pcs()
            input_image()


def check_list():
    global file_list, file_name, cup_origin, cup_radius, cup_angle

    if file_dir:
        file_list = glob.glob(r'{}/*.nii.gz'.format(file_dir))

        npy_dir = str(file_dir[:-6]) + '/npy'
        npy_list = glob.glob(r'{}/*.npy'.format(npy_dir))

        mark_dir = str(file_dir[:-6]) + '/mark/npy'
        mark_list = glob.glob(r'{}/*.npy'.format(mark_dir))

        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(['File Names'])

        for x in file_list:
            suffix = str('\\' + x.split('\\')[1])[:-7]
            index = npy_dir + suffix + '.npy'
            mark_index = npy_dir[:-3] + 'mark/npy' + suffix + '_mark.npy'

            if index in npy_list:
                if mark_index in mark_list:
                    item = QTreeWidgetItem()
                    item.setText(0, x)
                    tree.addTopLevelItem(item)

        dialog = QDialog()
        dialog.setSizePolicy(SizePolicyMinimum)
        dialog.setWindowTitle('选择文件')
        dialog.setLayout(QVBoxLayout())
        dialog.setMinimumWidth(500)
        dialog.layout().addWidget(tree)

        button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button.setSizePolicy(SizePolicyMinimum)
        button.accepted.connect(dialog.accept)
        button.rejected.connect(dialog.reject)
        dialog.layout().addWidget(button)

        if dialog.exec_() == QDialog.Accepted:
            file_name = tree.currentItem().text(0)

            init_pcs()
            input_image()

            npy_name = str(file_name).split('image')[0] + 'mark/npy'
            suffix = str(file_name).split('image')[1][:-7]

            mark_dict = np.load(npy_name + suffix + '_mark.npy', allow_pickle=True).item()

            cup_origin = [mark_dict['右侧臼杯中心'], mark_dict['左侧臼杯中心']]
            cup_radius = [mark_dict['右侧臼杯半径'], mark_dict['左侧臼杯半径']]

            if '右侧前倾角' in mark_dict.keys():
                cup_angle = [[mark_dict['右侧前倾角'], mark_dict['右侧外展角']],
                             [mark_dict['左侧前倾角'], mark_dict['左侧外展角']]]

            update_slice_view()
            update_cup()

            radius_boxes[0].draw_text('右侧半径 {:.1f}'.format(cup_radius[0]))
            radius_boxes[1].draw_text('左侧半径 {:.1f}'.format(cup_radius[1]))
            angle_boxes[0].draw_text('右侧前倾 {:.1f}'.format(cup_angle[0][0]))
            angle_boxes[1].draw_text('右侧外展 {:.1f}'.format(cup_angle[0][1]))
            angle_boxes[2].draw_text('左侧前倾 {:.1f}'.format(cup_angle[1][0]))
            angle_boxes[3].draw_text('左侧外展 {:.1f}'.format(cup_angle[1][1]))


def input_image():
    global series_image, cup_origin

    if file_name:
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(file_name)
        reader.Update()

        series_image = reader.GetOutput()
        series_volume.setData(series_image)
        series_view.setCamera_FitAll()
        series_view.updateAtOnce()

        # 初始化臼杯中心
        x_offset = 0.25 * (vmi.imBounds(series_image)[1] - vmi.imBounds(series_image)[0])
        y_offset = 0.25 * (vmi.imBounds(series_image)[3] - vmi.imBounds(series_image)[2])
        cup_origin[0] = vmi.imCenter(series_image) - x_offset * pelvis_cs.axis(0) + y_offset * pelvis_cs.axis(2)
        cup_origin[1] = vmi.imCenter(series_image) + x_offset * pelvis_cs.axis(0) + y_offset * pelvis_cs.axis(2)

        init_slice_view()
        update_cup()

        for v in right_views + left_views:
            v.setCamera_FitAll()

        vmi.appupdate()


def init_pcs():
    global pcs, pelvis_cs

    if file_name:
        npy_name = str(file_name).split('image')[0] + 'npy'
        suffix = str(file_name).split('image')[1][:-7]

        pt_dict = np.load(npy_name + suffix + '.npy', allow_pickle=True).item()

        # # 验证标志点
        # test_prop = vmi.PolyActor(series_view, color=[0.4, 0.6, 1], line_width=3, pickable=True)
        # test_prop.setData(vmi.pdAppend([vmi.pdSphere(2.5, pt_dict['髂前上棘'][0]),
        #                                 vmi.pdSphere(2.5, pt_dict['髂前上棘'][1]),
        #                                 vmi.pdSphere(2.5, pt_dict['耻骨结节'][0]),
        #                                 vmi.pdSphere(2.5, pt_dict['耻骨结节'][1]),
        #                                 vmi.pdSphere(2.5, pt_dict['髂翼最高点'][0]),
        #                                 vmi.pdSphere(2.5, pt_dict['髂翼最高点'][1]),
        #                                 vmi.pdSphere(2.5, pt_dict['坐骨结节'][0]),
        #                                 vmi.pdSphere(2.5, pt_dict['坐骨结节'][1])]))

        pcs = {'x': [1, 0, 0],
               'y': [0, 1, 0],
               'z': [0, 0, 1]}

        # APP
        app_pts = vtk.vtkPoints()
        app_pts.InsertNextPoint(pt_dict['髂前上棘'][0])
        app_pts.InsertNextPoint(pt_dict['髂前上棘'][1])
        app_pts.InsertNextPoint(pt_dict['耻骨结节'][0])
        app_pts.InsertNextPoint(pt_dict['耻骨结节'][1])

        pcs['y'] = -vmi.pdOBB_Pts(app_pts)['axis'][2]

        # MPP
        mpp_pts = [[pt_dict['髂前上棘'][0], pt_dict['髂前上棘'][1]],
                   [pt_dict['髂后上棘'][0], pt_dict['髂后上棘'][1]],
                   [pt_dict['坐骨棘'][0], pt_dict['坐骨棘'][1]],
                   [pt_dict['泪滴'][0], pt_dict['泪滴'][1]]]

        for j in range(4):
            if mpp_pts[j][0][0] > mpp_pts[j][1][0]:
                n = mpp_pts[j][1][0]
                mpp_pts[j][1][0] = mpp_pts[j][0][0]
                mpp_pts[j][0][0] = n

        mpp_vec = [(mpp_pts[0][1] - mpp_pts[0][0]) / vtk.vtkMath.Normalize(mpp_pts[0][1] - mpp_pts[0][0]),
                   (mpp_pts[1][1] - mpp_pts[1][0]) / vtk.vtkMath.Normalize(mpp_pts[1][1] - mpp_pts[1][0]),
                   (mpp_pts[2][1] - mpp_pts[2][0]) / vtk.vtkMath.Normalize(mpp_pts[2][1] - mpp_pts[2][0]),
                   (mpp_pts[3][1] - mpp_pts[3][0]) / vtk.vtkMath.Normalize(mpp_pts[3][1] - mpp_pts[3][0])]

        pcs['x'] = (mpp_vec[0] + mpp_vec[1] + mpp_vec[2] + mpp_vec[3]) / vtk.vtkMath.Normalize(
            mpp_vec[0] + mpp_vec[1] + mpp_vec[2] + mpp_vec[3])
        pcs['x'] = vmi.vtOnPlane(pcs['x'], pcs['y'])

        vtk.vtkMath.Cross(pcs['x'], pcs['y'], pcs['z'])

        if vtk.vtkMath.DegreesFromRadians(
                vtk.vtkMath.AngleBetweenVectors(pcs['x'], [1, 0, 0])) > 90:
            pcs['x'] = [-pcs['x'][0], -pcs['x'][1], -pcs['x'][2]]

        if vtk.vtkMath.DegreesFromRadians(
                vtk.vtkMath.AngleBetweenVectors(pcs['y'], [0, 1, 0])) > 90:
            pcs['y'] = [-pcs['y'][0], -pcs['y'][1], -pcs['y'][2]]

        if vtk.vtkMath.DegreesFromRadians(
                vtk.vtkMath.AngleBetweenVectors(pcs['z'], [0, 0, 1])) > 90:
            pcs['z'] = [-pcs['z'][0], -pcs['z'][1], -pcs['z'][2]]

        pelvis_cs = vmi.CS4x4(axis0=np.array(pcs['x']),
                              axis1=np.array(pcs['y']),
                              axis2=np.array(pcs['z']),
                              origin=[0, 0, 0])


def output_data():
    global file_name, series_image

    if series_image is not None:
        if file_name:
            save_name = str(file_name).split('image')[0] + 'mark/'
            suffix = str(file_name).split('image')[1][:-7]

            origin = vmi.imOrigin(series_image)
            spacing = vmi.imSpacing(series_image)
            extent = vmi.imExtent(series_image)

            stencil = [vmi.imStencil_PolyData(cup_prop[0].data(), origin, spacing, extent),
                       vmi.imStencil_PolyData(cup_prop[1].data(), origin, spacing, extent)]

            image = np.zeros(vmi.imArray_VTK(stencil[0]).shape).astype('uint8')
            image[vmi.imArray_VTK(stencil[0]) != 0] = 1
            image[vmi.imArray_VTK(stencil[1]) != 0] = 2

            vmi.imSaveFile_NIFTI(vmi.imVTK_Array(image, origin, spacing),
                                 save_name + '/image' + suffix + '_image.nii.gz')

            cup_data = {
                '右侧臼杯中心': cup_origin[0],
                '左侧臼杯中心': cup_origin[1],
                '右侧臼杯半径': cup_radius[0],
                '左侧臼杯半径': cup_radius[1],
                '右侧前倾角': cup_angle[0][0],
                '右侧外展角': cup_angle[0][1],
                '左侧前倾角': cup_angle[1][0],
                '左侧外展角': cup_angle[1][1]
            }

            np.save(save_name + '/npy' + suffix + '_mark.npy', cup_data)
            vmi.askInfo('标注文件已保存')


def output_parameter():
    if file_dir:
        file_list = glob.glob(r'{}/*.nii.gz'.format(file_dir))

        npy_dir = str(file_dir[:-6]) + '/npy'
        npy_list = glob.glob(r'{}/*.npy'.format(npy_dir))

        mark_dir = str(file_dir[:-6]) + '/mark/npy'
        mark_list = glob.glob(r'{}/*.npy'.format(mark_dir))

        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(['File Names'])

        data = [[], [], [], [], [], []]
        name_list = []
        dis_list = [[], [], [], [], [], []]

        for x in file_list:
            suffix = str('\\' + x.split('\\')[1])[:-7]
            index = npy_dir + suffix + '.npy'
            mark_index = npy_dir[:-3] + 'mark/npy' + suffix + '_mark.npy'
            pt_index = npy_dir[:-3] + 'npy' + suffix + '.npy'

            if index in npy_list:
                if mark_index in mark_list:
                    mark_dict = np.load(mark_index, allow_pickle=True).item()
                    pt_dict = np.load(pt_index, allow_pickle=True).item()

                    # 遍历骨盆坐标系
                    pcs = {'x': [1, 0, 0],
                           'y': [0, 1, 0],
                           'z': [0, 0, 1]}

                    # APP
                    app_pts = vtk.vtkPoints()
                    app_pts.InsertNextPoint(pt_dict['髂前上棘'][0])
                    app_pts.InsertNextPoint(pt_dict['髂前上棘'][1])
                    app_pts.InsertNextPoint(pt_dict['耻骨结节'][0])
                    app_pts.InsertNextPoint(pt_dict['耻骨结节'][1])

                    pcs['y'] = -vmi.pdOBB_Pts(app_pts)['axis'][2]

                    # MPP
                    mpp_pts = [[pt_dict['髂前上棘'][0], pt_dict['髂前上棘'][1]],
                               [pt_dict['髂后上棘'][0], pt_dict['髂后上棘'][1]],
                               [pt_dict['坐骨棘'][0], pt_dict['坐骨棘'][1]],
                               [pt_dict['泪滴'][0], pt_dict['泪滴'][1]]]

                    for j in range(4):
                        if mpp_pts[j][0][0] > mpp_pts[j][1][0]:
                            n = mpp_pts[j][1][0]
                            mpp_pts[j][1][0] = mpp_pts[j][0][0]
                            mpp_pts[j][0][0] = n

                    mpp_vec = [(mpp_pts[0][1] - mpp_pts[0][0]) / vtk.vtkMath.Normalize(mpp_pts[0][1] - mpp_pts[0][0]),
                               (mpp_pts[1][1] - mpp_pts[1][0]) / vtk.vtkMath.Normalize(mpp_pts[1][1] - mpp_pts[1][0]),
                               (mpp_pts[2][1] - mpp_pts[2][0]) / vtk.vtkMath.Normalize(mpp_pts[2][1] - mpp_pts[2][0]),
                               (mpp_pts[3][1] - mpp_pts[3][0]) / vtk.vtkMath.Normalize(mpp_pts[3][1] - mpp_pts[3][0])]

                    pcs['x'] = (mpp_vec[0] + mpp_vec[1] + mpp_vec[2] + mpp_vec[3]) / vtk.vtkMath.Normalize(
                        mpp_vec[0] + mpp_vec[1] + mpp_vec[2] + mpp_vec[3])
                    pcs['x'] = vmi.vtOnPlane(pcs['x'], pcs['y'])

                    vtk.vtkMath.Cross(pcs['x'], pcs['y'], pcs['z'])

                    # 计算距离
                    dis = {'右侧臼杯中心-APP':
                               (vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['y'], pt_dict['耻骨结节'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['y'], pt_dict['耻骨结节'][1]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['y'], pt_dict['髂前上棘'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['y'], pt_dict['髂前上棘'][1])) / 4,
                           '右侧臼杯中心-MPP':
                               (vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['x'], pt_dict['耻骨结节'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['x'], pt_dict['耻骨结节'][1])) / 2,
                           '右侧臼杯中心-泪滴':
                               (vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['z'], pt_dict['泪滴'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['右侧臼杯中心'], pcs['z'], pt_dict['泪滴'][1])) / 2,
                           '左侧臼杯中心-APP':
                               (vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['y'], pt_dict['耻骨结节'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['y'], pt_dict['耻骨结节'][1]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['y'], pt_dict['髂前上棘'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['y'], pt_dict['髂前上棘'][1])) / 4,
                           '左侧臼杯中心-MPP':
                               (vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['x'], pt_dict['耻骨结节'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['x'], pt_dict['耻骨结节'][1])) / 2,
                           '左侧臼杯中心-泪滴':
                               (vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['z'], pt_dict['泪滴'][0]) +
                                vtk.vtkPlane.DistanceToPlane(mark_dict['左侧臼杯中心'], pcs['z'], pt_dict['泪滴'][1])) / 2}

                    # 添加数据
                    name_list.append(mark_index.split('/npy\\')[1].split('_')[0])
                    data[0].append(mark_dict['右侧臼杯半径'])
                    data[1].append(mark_dict['左侧臼杯半径'])
                    data[2].append(mark_dict['右侧前倾角'])
                    data[3].append(mark_dict['右侧外展角'])
                    data[4].append(mark_dict['左侧前倾角'])
                    data[5].append(mark_dict['左侧外展角'])

                    dis_list[0].append(dis['右侧臼杯中心-APP'])
                    dis_list[1].append(dis['右侧臼杯中心-MPP'])
                    dis_list[2].append(dis['右侧臼杯中心-泪滴'])
                    dis_list[3].append(dis['左侧臼杯中心-APP'])
                    dis_list[4].append(dis['左侧臼杯中心-MPP'])
                    dis_list[5].append(dis['左侧臼杯中心-泪滴'])

        data_df = pd.DataFrame({'患者姓名': name_list,
                                '右侧臼杯半径': data[0],
                                '左侧臼杯半径': data[1],
                                '右侧前倾角': data[2],
                                '右侧外展角': data[3],
                                '左侧前倾角': data[4],
                                '左侧外展角': data[5],
                                '右侧臼杯中心-APP': dis_list[0],
                                '右侧臼杯中心-MPP': dis_list[1],
                                '右侧臼杯中心-泪滴': dis_list[2],
                                '左侧臼杯中心-APP': dis_list[3],
                                '左侧臼杯中心-MPP': dis_list[4],
                                '左侧臼杯中心-泪滴': dis_list[5]})

        file = vmi.askSaveFile('xlsx', '*.xlsx', '导出 (Export) 数据')
        if file is None:
            return
        writer = pd.ExcelWriter(file)
        data_df.to_excel(writer)
        writer.save()


def update_series_opacity():
    series_volume.setOpacityScalar({series_opacity_range[0] - 1: 0,
                                    series_opacity_range[0]: 1,
                                    series_opacity_range[1]: 1,
                                    series_opacity_range[1] + 1: 0})
    series_volume.setColor({series_opacity_range[0]: [1, 1, 0.9],
                            series_opacity_range[1]: [1, 1, 0.1]})


def init_slice_view():
    if series_image is not None:
        right_slices[0].setSlicePlaneNormal(pcs['y'])
        right_slices[1].setSlicePlaneNormal(pcs['x'])
        right_slices[2].setSlicePlaneNormal(pcs['z'])
        left_slices[0].setSlicePlaneNormal(pcs['y'])
        left_slices[1].setSlicePlaneNormal(pcs['x'])
        left_slices[2].setSlicePlaneNormal(pcs['z'])

        o = np.array([0, 0, 0])
        coronal_cs = vmi.CS4x4(axis0=np.array(pcs['x']),
                               axis1=-np.array(pcs['z']),
                               axis2=np.array(pcs['y']),
                               origin=o)
        axial_cs = vmi.CS4x4(axis0=np.array(pcs['x']),
                             axis1=np.array(pcs['y']),
                             axis2=np.array(pcs['z']),
                             origin=o)

        sagittal_cs = [vmi.CS4x4(axis0=-np.array(pcs['y']),
                                 axis1=-np.array(pcs['z']),
                                 axis2=np.array(pcs['x']),
                                 origin=o),
                       vmi.CS4x4(axis0=np.array(pcs['y']),
                                 axis1=-np.array(pcs['z']),
                                 axis2=-np.array(pcs['x']),
                                 origin=o)]

        right_views[0].setCamera_FPlane(coronal_cs, 1)
        right_views[1].setCamera_FPlane(sagittal_cs[0], 1)
        right_views[2].setCamera_FPlane(axial_cs, 1)

        left_views[0].setCamera_FPlane(coronal_cs, 1)
        left_views[1].setCamera_FPlane(sagittal_cs[1], 1)
        left_views[2].setCamera_FPlane(axial_cs, 1)

        for s in right_slices:
            s.setSlicePlaneOrigin(cup_origin[0])
            s.setData(series_image)

        for s in left_slices:
            s.setSlicePlaneOrigin(cup_origin[1])
            s.setData(series_image)


def update_slice_view():
    if series_image is not None:
        for s in right_slices:
            s.setSlicePlaneOrigin(cup_origin[0])

        for s in left_slices:
            s.setSlicePlaneOrigin(cup_origin[1])


def update_cup():
    global cup_cs
    cup_cs[0] = pelvis_cs.rotate(cup_angle[0][0], pelvis_cs.axis(0))
    cup_cs[0] = cup_cs[0].rotate(cup_angle[0][1] - 180, pelvis_cs.axis(1))
    cup_cs[1] = pelvis_cs.rotate(cup_angle[1][0], pelvis_cs.axis(0))
    cup_cs[1] = cup_cs[1].rotate(180 - cup_angle[1][1], pelvis_cs.axis(1))

    cup_cs[0].setOrigin(cup_origin[0])
    cup_cs[1].setOrigin(cup_origin[1])

    right_plane = vtk.vtkPlane()
    right_plane.SetNormal(cup_cs[0].axis(2))
    right_plane.SetOrigin(cup_cs[0].origin())

    left_plane = vtk.vtkPlane()
    left_plane.SetNormal(cup_cs[1].axis(2))
    left_plane.SetOrigin(cup_cs[1].origin())

    right_pd = vmi.pdSphere(cup_radius[0], cup_cs[0].origin())
    right_pd = vmi.pdClip_Implicit(right_pd, right_plane)[1]

    left_pd = vmi.pdSphere(cup_radius[1], cup_cs[1].origin())
    left_pd = vmi.pdClip_Implicit(left_pd, left_plane)[1]

    right_pd_border = vmi.pdPolyline_Regular(cup_radius[0], cup_cs[0].origin(), cup_cs[0].axis(2))
    right_pd = vmi.pdAppend([right_pd, right_pd_border])

    left_pd_border = vmi.pdPolyline_Regular(cup_radius[1], cup_cs[1].origin(), cup_cs[1].axis(2))
    left_pd = vmi.pdAppend([left_pd, left_pd_border])

    cup_prop[0].setData(right_pd)
    cup_prop[1].setData(left_pd)

    r = 2
    pd = [vmi.pdAppend([vmi.pdCut_Implicit(cup_prop[0].data(), right_slices[0].slicePlane()),
                        vmi.pdSphere(r, cup_cs[0].origin())]),
          vmi.pdAppend([vmi.pdCut_Implicit(cup_prop[0].data(), right_slices[1].slicePlane()),
                        vmi.pdSphere(r, cup_cs[0].origin())]),
          vmi.pdAppend([vmi.pdCut_Implicit(cup_prop[0].data(), right_slices[2].slicePlane()),
                        vmi.pdSphere(r, cup_cs[0].origin())]),
          vmi.pdAppend([vmi.pdCut_Implicit(cup_prop[1].data(), left_slices[0].slicePlane()),
                        vmi.pdSphere(r, cup_cs[1].origin())]),
          vmi.pdAppend([vmi.pdCut_Implicit(cup_prop[1].data(), left_slices[1].slicePlane()),
                        vmi.pdSphere(r, cup_cs[1].origin())]),
          vmi.pdAppend([vmi.pdCut_Implicit(cup_prop[1].data(), left_slices[2].slicePlane()),
                        vmi.pdSphere(r, cup_cs[1].origin())])]
    for r in range(6):
        cup_section_prop[r].setData(pd[r])


def LeftButtonPressMove(**kwargs):
    global cup_origin
    if kwargs['picked'] in [cup_prop[0], cup_section_prop[0], cup_section_prop[1], cup_section_prop[2]]:
        cup_origin[0] += kwargs['picked'].view().pickVt_FocalPlane()
        update_slice_view()
        update_cup()
        return True

    elif kwargs['picked'] in [cup_prop[1], cup_section_prop[3], cup_section_prop[4], cup_section_prop[5]]:
        cup_origin[1] += kwargs['picked'].view().pickVt_FocalPlane()
        update_slice_view()
        update_cup()
        return True


def LeftButtonPressRelease(**kwargs):
    global series_opacity_range, cup_radius
    if kwargs['picked'] is series_opacity_range_box[0]:
        v = vmi.askInt(-10000, series_opacity_range[0], series_opacity_range[1])
        if v is not None:
            series_opacity_range[0] = v
        series_opacity_range_box[0].draw_text('min {:.0f}'.format(series_opacity_range[0]))
        update_series_opacity()

    elif kwargs['picked'] is series_opacity_range_box[1]:
        v = vmi.askInt(series_opacity_range[0], series_opacity_range[0], 10000)
        if v is not None:
            series_opacity_range[1] = v
        series_opacity_range_box[1].draw_text('min {:.0f}'.format(series_opacity_range[1]))
        update_series_opacity()

    elif kwargs['picked'] is radius_boxes[0]:
        v = vmi.askInt(0, cup_radius[0], 90, 1)
        if v is not None:
            cup_radius[0] = v
        radius_boxes[0].draw_text('右侧半径 {:.1f}'.format(cup_radius[0]))
        update_cup()

    elif kwargs['picked'] is radius_boxes[1]:
        v = vmi.askInt(0, cup_radius[1], 90, 1)
        if v is not None:
            cup_radius[1] = v
        radius_boxes[1].draw_text('左侧半径 {:.1f}'.format(cup_radius[1]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[0]:
        v = vmi.askFloat(0, cup_angle[0][0], 180, 1)
        if v is not None:
            cup_angle[0][0] = v
        angle_boxes[0].draw_text('右侧前倾 {:.1f}'.format(cup_angle[0][0]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[1]:
        v = vmi.askFloat(0, cup_angle[0][1], 180, 1)
        if v is not None:
            cup_angle[0][1] = v
        angle_boxes[1].draw_text('右侧外展 {:.1f}'.format(cup_angle[0][1]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[2]:
        v = vmi.askFloat(0, cup_angle[1][0], 180, 1)
        if v is not None:
            cup_angle[1][0] = v
        angle_boxes[2].draw_text('左侧前倾 {:.1f}'.format(cup_angle[1][0]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[3]:
        v = vmi.askFloat(0, cup_angle[1][1], 180, 1)
        if v is not None:
            cup_angle[1][1] = v
        angle_boxes[3].draw_text('左侧外展 {:.1f}'.format(cup_angle[1][1]))
        update_cup()


def NoButtonWheel(**kwargs):
    global series_opacity_range, cup_radius
    if kwargs['picked'] is series_opacity_range_box[0]:
        series_opacity_range[0] = min(max(series_opacity_range[0] + kwargs['delta'],
                                          -10000), series_opacity_range[1])
        series_opacity_range_box[0].draw_text('min {:.0f}'.format(series_opacity_range[0]))
        update_series_opacity()

    elif kwargs['picked'] is series_opacity_range_box[1]:
        series_opacity_range[1] = min(max(series_opacity_range[1] + kwargs['delta'],
                                          series_opacity_range[0]), 10000)
        series_opacity_range_box[1].draw_text('max {:.0f}'.format(series_opacity_range[1]))
        update_series_opacity()

    elif kwargs['picked'] is radius_boxes[0]:
        cup_radius[0] = min(max(cup_radius[0] + 1 * kwargs['delta'],
                                0), 90)
        radius_boxes[0].draw_text('右侧半径 {:.1f}'.format(cup_radius[0]))
        update_cup()

    elif kwargs['picked'] is radius_boxes[1]:
        cup_radius[1] = min(max(cup_radius[1] + 1 * kwargs['delta'],
                                0), 90)
        radius_boxes[1].draw_text('左侧半径 {:.1f}'.format(cup_radius[1]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[0]:
        cup_angle[0][0] = min(max(cup_angle[0][0] + 0.5 * kwargs['delta'],
                                  0), 180)
        angle_boxes[0].draw_text('右侧前倾 {:.1f}'.format(cup_angle[0][0]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[1]:
        cup_angle[0][1] = min(max(cup_angle[0][1] + 0.5 * kwargs['delta'],
                                  0), 180)
        angle_boxes[1].draw_text('右侧外展 {:.1f}'.format(cup_angle[0][1]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[2]:
        cup_angle[1][0] = min(max(cup_angle[1][0] + 0.5 * kwargs['delta'],
                                  0), 180)
        angle_boxes[2].draw_text('左侧前倾 {:.1f}'.format(cup_angle[1][0]))
        update_cup()

    elif kwargs['picked'] is angle_boxes[3]:
        cup_angle[1][1] = min(max(cup_angle[1][1] + 0.5 * kwargs['delta'],
                                  0), 180)
        angle_boxes[3].draw_text('左侧外展 {:.1f}'.format(cup_angle[1][1]))
        update_cup()


def return_globals():
    return globals()


if __name__ == '__main__':
    main = vmi.Main(return_globals)
    main.setAppName('Cup_marker')
    main.setAppVersion(vmi.version)
    main.excludeKeys += ['main']

    menu_input = main.menuBar().addMenu('输入')
    menu_input.addAction('选择文件夹').triggered.connect(input_dir)
    menu_input.addAction('未标注列表').triggered.connect(input_list)
    menu_input.addAction('查看已标注').triggered.connect(check_list)

    menu_output = main.menuBar().addMenu('输出')
    menu_output.addAction('完成标注').triggered.connect(output_data)
    menu_output.addAction('导出数据').triggered.connect(output_parameter)

    file_name, file_dir, file_list = [], [], []

    # 骨盆坐标系
    pcs = {'x': [1, 0, 0],
           'y': [0, 1, 0],
           'z': [0, 0, 1]}
    vtk.vtkMath.Cross(pcs['x'], pcs['y'], pcs['z'])
    pelvis_cs = vmi.CS4x4(axis0=np.array(pcs['x']),
                          axis1=np.array(pcs['y']),
                          axis2=np.array(pcs['z']),
                          origin=[0, 0, 0])

    # 体绘制视图
    series_dict = []
    series_image = []
    series_view = vmi.View()
    series_view.setCamera_Coronal()
    series_volume = vmi.ImageVolume(series_view)

    series_opacity_range = [200, 3000]
    update_series_opacity()

    series_opacity_range_box = [vmi.TextBox(series_view, text='min {:.0f}'.format(series_opacity_range[0]),
                                            size=[0.2, 0.06], pos=[0, 0.03], anchor=[0, 0], pickable=True),
                                vmi.TextBox(series_view, text='max {:.0f}'.format(series_opacity_range[1]),
                                            size=[0.2, 0.06], pos=[0.2, 0.03], anchor=[0, 0], pickable=True)]

    for box in series_opacity_range_box:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    # 二维视图
    right_views = [vmi.View(), vmi.View(), vmi.View()]
    left_views = [vmi.View(), vmi.View(), vmi.View()]

    for i in right_views + left_views:
        i.mouse['LeftButton']['PressMove'] = [i.mouseBlock]
        i.mouse['NoButton']['Wheel'] = [i.mouseBlock]

    right_boxes = [vmi.TextBox(right_views[i], text=['冠状位', '矢状位', '横断位'][i],
                               size=[0.2, 0.06], pos=[0, 0.03], anchor=[0, 0]) for i in range(3)]
    left_boxes = [vmi.TextBox(left_views[i], text=['冠状位', '矢状位', '横断位'][i],
                              size=[0.2, 0.06], pos=[0, 0.03], anchor=[0, 0]) for i in range(3)]

    right_slices = [vmi.ImageSlice(v) for v in right_views]
    left_slices = [vmi.ImageSlice(v) for v in left_views]

    for i in right_slices + left_slices:
        i.mouse['NoButton']['Wheel'] = [i.mouseBlock]
        i.setColorWindow_Bone()

    # 臼杯参数
    cup_origin, cup_radius, cup_cs, cup_angle = [[0, 0, 0], [0, 0, 0]], [24, 24], [[], []], [[20, 40], [20, 40]]

    box_size = [0.2, 0.06]
    radius_boxes = [vmi.TextBox(series_view, text='右侧半径 {:.1f}'.format(cup_radius[0]),
                                size=box_size, pos=[0, 0.09], anchor=[0, 0], pickable=True),
                    vmi.TextBox(series_view, text='左侧半径 {:.1f}'.format(cup_radius[1]),
                                size=box_size, pos=[0.2, 0.09], anchor=[0, 0], pickable=True)]

    angle_boxes = [vmi.TextBox(series_view, text='右侧前倾 {:.1f}'.format(cup_angle[0][0]),
                               size=box_size, pos=[0, 0.15], anchor=[0, 0], pickable=True),
                   vmi.TextBox(series_view, text='右侧外展 {:.1f}'.format(cup_angle[0][1]),
                               size=box_size, pos=[0, 0.21], anchor=[0, 0], pickable=True),
                   vmi.TextBox(series_view, text='左侧前倾 {:.1f}'.format(cup_angle[1][0]),
                               size=box_size, pos=[0.2, 0.15], anchor=[0, 0], pickable=True),
                   vmi.TextBox(series_view, text='左侧外展 {:.1f}'.format(cup_angle[1][1]),
                               size=box_size, pos=[0.2, 0.21], anchor=[0, 0], pickable=True)]

    for box in radius_boxes + angle_boxes:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    cup_prop = [vmi.PolyActor(series_view, color=[0.4, 0.6, 1], line_width=3, pickable=True),
                vmi.PolyActor(series_view, color=[0.4, 0.6, 1], line_width=3, pickable=True)]
    for p in cup_prop:
        p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

    cup_section_prop = [vmi.PolyActor(right_views[0], color=[0.4, 0.6, 1], line_width=3, pickable=True),
                        vmi.PolyActor(right_views[1], color=[0.4, 0.6, 1], line_width=3, pickable=True),
                        vmi.PolyActor(right_views[2], color=[0.4, 0.6, 1], line_width=3, pickable=True),
                        vmi.PolyActor(left_views[0], color=[0.4, 0.6, 1], line_width=3, pickable=True),
                        vmi.PolyActor(left_views[1], color=[0.4, 0.6, 1], line_width=3, pickable=True),
                        vmi.PolyActor(left_views[2], color=[0.4, 0.6, 1], line_width=3, pickable=True)]
    for p in cup_section_prop:
        p.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]

    # 视图布局
    main.layout().addWidget(series_view, 0, 2, 3, 1)
    main.layout().addWidget(right_views[0], 0, 1, 1, 1)
    main.layout().addWidget(right_views[1], 1, 1, 1, 1)
    main.layout().addWidget(right_views[2], 2, 1, 1, 1)
    main.layout().addWidget(left_views[0], 0, 3, 1, 1)
    main.layout().addWidget(left_views[1], 1, 3, 1, 1)
    main.layout().addWidget(left_views[2], 2, 3, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
