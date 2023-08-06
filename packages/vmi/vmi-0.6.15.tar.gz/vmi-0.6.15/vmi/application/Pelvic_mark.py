import pathlib
import tempfile

import vmi
import nibabel as nib
import numpy as np
import pydicom
import vtk
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from numba import jit
import pandas as pd
import os
import pymongo
import gridfs
import pickle
import hashlib
import threading

from typing import List, Optional
from typing import Dict, Any

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QInputDialog

dic_list = ['髂翼最高点',
            '髂前上棘',
            '髂前下棘',
            '耻骨结节',
            '坐骨结节',
            '髂后上棘',
            '坐骨棘',
            '泪滴']

color_map = {
    '髂翼最高点': [128, 0, 0],
    '髂前上棘': [128, 128, 0],
    '髂前下棘': [128, 0, 128],
    '耻骨结节': [0, 255, 128],
    '坐骨结节': [0, 128, 128],
    '髂后上棘': [0, 0, 255],
    '坐骨棘': [255, 128, 255],
    '泪滴': [0, 255, 255],
}

# mark_points = {
#     '髂前上棘': [],
#     '耻骨结节': [],
#     '髂翼最高点': [],
#     '坐骨结节': [],
#     '髂后上棘': [],
#     '泪滴': []}

overlay_chart = ['正视', '侧视', '俯视']

SizePolicyMinimum = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


def upload(image: vtk.vtkImageData, kw_value: Dict[str, Any]):
    if flag == 1:
        data_db: pymongo.collection.Collection = client.THA_DB.prePelvis
        file_db = gridfs.GridFS(client.THA_DB, collection='prePelvis')

    elif flag == 2:
        data_db: pymongo.collection.Collection = client.THA_DB.postPelvis
        file_db = gridfs.GridFS(client.THA_DB, collection='postPelvis')

    # 删除已有数据
    uid = {'SeriesInstanceUID': kw_value['SeriesInstanceUID']}

    for one in file_db.find(uid):
        file_db.delete(one._id)

    for one in data_db.find(uid):
        data_db.delete_one(one)

    # 图像序列化为文件，计算特征码，上传文件项
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.nii'
        vmi.imSaveFile_NIFTI(image, str(p))
        image_bytes = p.read_bytes()
        file_id = file_db.put(image_bytes,
                              fileType='.nii',
                              scalarType=image.GetScalarTypeAsString(),
                              SeriesInstanceUID=kw_value['SeriesInstanceUID'])

    # 检查上传结果是否与本地一致
    if file_db.find_one({'_id': file_id}).md5 != hashlib.md5(image_bytes).hexdigest():
        file_db.delete(file_id)
        return print('远端MD5校验失败 {}'.format(repr(kw_value)))

    # 上传数据项
    data_db.insert_one(kw_value)


def input_dicom():
    global series_list, dcmdir
    dcmdir = vmi.askDirectory('DICOM')

    if dcmdir is not None:
        series_list = vmi.sortSeries(dcmdir)
        input_series()


def input_series():
    global series_dict, series, voi_image
    series = vmi.askSeries(series_list)
    if series is not None:
        series_dict = series.toKeywordValue()
        voi_image = series.read()
        voi_image.SetOrigin([0, 0, 0])
        input_image(voi_image)


def input_image(image: vtk.vtkImageData):
    global center_pts, mark_hash, front_img, side_img, top_img

    voi_volume.setData(image)
    voi_volume.setOpacity_Threshold(threshold)
    voi_view.setCamera_Coronal()
    voi_view.setCamera_FitAll()

    for j in center_props:
        j.setData(vmi.pdSphere(0.01, [0, 0, 0]))

    for j in image_props:
        j.setData(vmi.pdSphere(0.01, [0, 0, 0]))

    mark_hash = []
    center_pts = []
    front_img, side_img, top_img = None, None, None
    front_img = show_Front_view(voi_image)

    image_data.setData(front_img)
    image_data.setColorWindow_Auto()
    image_view.setCamera_FitAll()

    voi_view.updateAtOnce()
    vmi.appupdate()


def bind_props(axis):
    global image_props
    x_offset = vmi.imExtent(voi_image)[1] - vmi.imExtent(voi_image)[0] + 1
    y_offset = vmi.imExtent(voi_image)[3] - vmi.imExtent(voi_image)[2] + 1
    z_offset = vmi.imExtent(voi_image)[5] - vmi.imExtent(voi_image)[4] + 1
    x_spacing = vmi.imSpacing(voi_image)[0]
    y_spacing = vmi.imSpacing(voi_image)[1]
    z_spacing = vmi.imSpacing(voi_image)[2]

    image_front_cs = vmi.CS4x4(axis0=[1, 0, 0],
                               axis1=[0, 0, -1],
                               axis2=[0, 1, 0],
                               origin=[0, 0, z_offset * z_spacing])
    image_side_cs = vmi.CS4x4(axis0=[0, -1, 0],
                              axis1=[0, 0, -1],
                              axis2=[1, 0, 0],
                              origin=[0, y_offset * y_spacing, z_offset * z_spacing])
    image_top_cs = vmi.CS4x4(axis0=[1, 0, 0],
                             axis1=[0, 1, 0],
                             axis2=[0, 0, 1],
                             origin=[0, 0, 0])

    ith = -1

    for i in range(len(center_pts)):
        if i % 2 == 0:
            ith += 1
            if ith >= 5:
                ith = 5
        rbg = np.array(color_map[dic_list[ith]]) / 255
        image_props[i].setColor(rbg)
        if axis == 1:
            image_props[i].setData(vmi.pdSphere(radius, [image_front_cs.inv().mpt(center_pts[i])[0],
                                                         image_front_cs.inv().mpt(center_pts[i])[1], 0]))
        elif axis == 2:
            side_pt = [image_side_cs.inv().mpt(center_pts[i])[0], image_side_cs.inv().mpt(center_pts[i])[1], 0]
            image_props[i].setData(vmi.pdSphere(radius, side_pt))
        elif axis == 0:
            image_props[i].setData(vmi.pdSphere(radius, [image_top_cs.inv().mpt(center_pts[i])[0],
                                                         image_top_cs.inv().mpt(center_pts[i])[1], 0]))
        image_props[i].alwaysOnTop()


def _dialog_ok_cancel(widgets, title, ok_cancel=True) -> QDialog:
    dialog = QDialog()
    dialog.setSizePolicy(SizePolicyMinimum)
    dialog.setWindowTitle(title)
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(800)

    for w in widgets:
        w.setParent(dialog)
        dialog.layout().addWidget(w)

    if ok_cancel:
        button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button.setSizePolicy(SizePolicyMinimum)
        button.accepted.connect(dialog.accept)
        button.rejected.connect(dialog.reject)
        dialog.layout().addWidget(button)
    return dialog


# 访问数据列表
def load_by_list():
    global case_uid, case_info, case_image_data, voi_image, mark_hash, center_props, center_pts, front_img, side_img, top_img

    data_db: pymongo.collection.Collection = client.testDB.spinePelvis
    file_db = gridfs.GridFS(client.testDB, collection='spinePelvis')
    markData_db: pymongo.collection.Collection = client.testDB.spinePelvisMF

    tree = QTreeWidget()
    tree.setColumnCount(5)
    tree.setHeaderLabels(['姓名', '年龄', '模态', '层数', '序列'])

    for x in data_db.find({"SeriesInstanceUID": {'$exists': True}}).sort(
            "PatientName", pymongo.ASCENDING):
        if not markData_db.find_one({'SeriesInstanceUID': x["SeriesInstanceUID"]}):
            item = QTreeWidgetItem()
            item.setText(0, str(x["PatientName"]))
            item.setText(1, str(x["PatientAge"]))
            item.setText(2, str(x["Modality"]))
            item.setText(3, str(x["Slices"]))
            item.setText(4, str(x["SeriesInstanceUID"]))
            tree.addTopLevelItem(item)

    d = _dialog_ok_cancel([tree], "list")
    if d.exec_() == QDialog.Accepted:
        case_uid = tree.currentItem().text(4)
        search_dict = {'SeriesInstanceUID': case_uid}

        if not file_db.exists(search_dict):
            return 'case_uid not found'
        else:
            case_info = data_db.find_one({'SeriesInstanceUID': case_uid})
            case_image_data = file_db.find_one(search_dict)

            # 清空所有点
            for i in center_props:
                i.setData(vmi.pdSphere(0.01, [0, 0, 0]))

            mark_hash = []
            center_pts = []
            front_img, side_img, top_img = None, None, None

            for j in image_props:
                j.setData(vmi.pdSphere(0.01, [0, 0, 0]))
            # 反序列化并将数据传至voi_volum
            voi_image = pickle.loads(case_image_data.read())
            voi_image.SetOrigin([0, 0, 0])

            front_img = show_Front_view(voi_image)

            voi_volume.setData(voi_image)
            voi_volume.setOpacity_Threshold(threshold)
            voi_view.setCamera_FitAll()
            voi_view.setCamera_Coronal()

            image_data.setData(front_img)
            image_data.setColorWindow_Auto()
            image_view.setCamera_FitAll()


# 上传文件
def output_upload():
    global case_uid
    if flag == 0:
        markData_db: pymongo.collection.Collection = client.testDB.spinePelvisMF
        markFile_db = gridfs.GridFS(client.testDB, collection='spinePelvisMF')

    elif flag == 1:
        markData_db: pymongo.collection.Collection = client.THA_DB.prePelvisMF
        markFile_db = gridfs.GridFS(client.THA_DB, collection='prePelvisMF')

        if series:
            tags = series.toKeywordValue()
            case_uid = tags['SeriesInstanceUID']
            upload(voi_image, tags)

    elif flag == 2:
        markData_db: pymongo.collection.Collection = client.THA_DB.postPelvisMF
        markFile_db = gridfs.GridFS(client.THA_DB, collection='postPelvisMF')

        if series:
            tags = series.toKeywordValue()
            case_uid = tags['SeriesInstanceUID']
            upload(voi_image, tags)

    if center_pts:
        mark_dict = {
            '髂翼最高点': [center_pts[0], center_pts[1]],
            '髂前上棘': [center_pts[2], center_pts[3]],
            '髂前下棘': [center_pts[4], center_pts[5]],
            '耻骨结节': [center_pts[6], center_pts[7]],
            '坐骨结节': [center_pts[8], center_pts[9]],
            '髂后上棘': [center_pts[10], center_pts[11]],
            '坐骨棘': [center_pts[12], center_pts[13]],
            '泪滴': [center_pts[14], center_pts[15]],
        }

        mark_bytes = pickle.dumps(mark_dict)
        mark_hash.append(hashlib.md5(mark_bytes).hexdigest())

        # 上传文件，避免重复上传完全一样的文件
        if not markFile_db.exists({'markData': mark_hash}):
            markFile_db.put(mark_bytes, fileType='.json')

            if not markData_db.find_one({'SeriesInstanceUID': case_uid}):
                markData_db.insert_one({'SeriesInstanceUID': case_uid})

            # 替换旧数据,增加marked数据的md5
            unmarked_data_dict = markData_db.find_one({'SeriesInstanceUID': case_uid})
            marked_data_dict = {**unmarked_data_dict, 'markData': mark_hash}
            markData_db.find_one_and_replace(unmarked_data_dict, marked_data_dict)

            data_id = mark_hash[-1]

            # 记录上传的id
            if vmi.askYesNo('上传成功 {} 复制到剪贴板？'.format(str(data_id))):
                vmi.app.clipboard().setText(str(data_id))


def _Overlay(image_data, axis):
    np_data = vmi.imArray_VTK(image_data)
    np_data[np_data < 100] = 0
    if axis == 0:
        overlay_data = np_data.sum(axis=0)
        return vmi.imVTK_Array(overlay_data, origin=[0, 0, 0],
                               spacing=[vmi.imSpacing(image_data)[1], vmi.imSpacing(image_data)[0],
                                        vmi.imSpacing(image_data)[2]])
    elif axis == 1:
        overlay_data = np.flip(np.flip(np.sum(np_data, axis)), axis=1) / 100
        return vmi.imVTK_Array(overlay_data, origin=[0, 0, 0],
                               spacing=[vmi.imSpacing(image_data)[0], vmi.imSpacing(image_data)[2],
                                        vmi.imSpacing(image_data)[1]])
    elif axis == 2:
        overlay_data = np.fliplr(np.flip(np.flip(np.sum(np_data, axis)), axis=1) / 100)
    return vmi.imVTK_Array(overlay_data, origin=[0, 0, 0],
                           spacing=[vmi.imSpacing(image_data)[0], vmi.imSpacing(image_data)[2],
                                    vmi.imSpacing(image_data)[1]])


def show_Front_view(image_data, axis=1):
    fount_img = _Overlay(image_data, axis)
    return fount_img


def show_Side_view(image_data, axis=2):
    side_img = _Overlay(image_data, axis)
    return side_img


def show_Top_view(image_data, axis=0):
    top_img = _Overlay(image_data, axis)
    return top_img


# 查看已上传数据
def check_upload():
    global case_uid, case_info, case_image_data, voi_image, mark_hash, center_pts, front_img, side_img, top_img

    if flag == 0:
        data_db: pymongo.collection.Collection = client.testDB.spinePelvis
        file_db = gridfs.GridFS(client.testDB, collection='spinePelvis')
        markData_db: pymongo.collection.Collection = client.testDB.spinePelvisMF
        markFile_db = gridfs.GridFS(client.testDB, collection='spinePelvisMF')

    elif flag == 1:
        data_db: pymongo.collection.Collection = client.THA_DB.prePelvis
        file_db = gridfs.GridFS(client.THA_DB, collection='prePelvis')
        markData_db: pymongo.collection.Collection = client.THA_DB.prePelvisMF
        markFile_db = gridfs.GridFS(client.THA_DB, collection='prePelvisMF')

    elif flag == 2:
        data_db: pymongo.collection.Collection = client.THA_DB.postPelvis
        file_db = gridfs.GridFS(client.THA_DB, collection='postPelvis')
        markData_db: pymongo.collection.Collection = client.THA_DB.postPelvisMF
        markFile_db = gridfs.GridFS(client.THA_DB, collection='postPelvisMF')

    tree = QTreeWidget()
    tree.setColumnCount(5)
    tree.setHeaderLabels(['姓名', '年龄', '模态', '层数', '序列'])

    for x in markData_db.find({"SeriesInstanceUID": {'$exists': True}}):
        if data_db.find_one({"SeriesInstanceUID": x["SeriesInstanceUID"]}):
            k = data_db.find_one({"SeriesInstanceUID": x["SeriesInstanceUID"]})

            item = QTreeWidgetItem()
            item.setText(0, str(k["PatientName"]))
            item.setText(1, str(k["PatientAge"]))
            item.setText(2, str(k["Modality"]))
            # item.setText(3, str(k["slices"]))
            item.setText(3, str('111'))
            item.setText(4, str(k["SeriesInstanceUID"]))
            tree.addTopLevelItem(item)

    d = _dialog_ok_cancel([tree], "list")
    if d.exec_() == QDialog.Accepted:
        case_uid = tree.currentItem().text(4)
        search_dict = {'SeriesInstanceUID': case_uid}
        if not file_db.exists(search_dict):
            return 'case_uid not found'
        else:
            case_info = data_db.find_one({'SeriesInstanceUID': case_uid})
            case_image_data = file_db.find_one(search_dict)

            # 反序列化并将数据传至voi_volum
            voi_image = pickle.loads(case_image_data.read())
            voi_image.SetOrigin([0, 0, 0])
            voi_volume.setData(voi_image)
            voi_volume.setOpacity_Threshold(threshold)
            voi_view.setCamera_FitAll()
            voi_view.setCamera_Coronal()

            mark_hash = markData_db.find_one({"SeriesInstanceUID": case_uid})["markData"]
            pts_info = markFile_db.find_one({"md5": mark_hash[-1]})
            pts_dict = pickle.loads(pts_info.read())

            center_pts = []
            front_img, side_img, top_img = None, None, None
            front_img = show_Front_view(voi_image)
            image_data.setData(front_img)
            image_data.setColorWindow_Auto()
            image_view.setCamera_FitAll()
            for j in image_props:
                j.setData(vmi.pdSphere(0.01, [0, 0, 0]))
            for name in pts_dict:
                center_pts.append(pts_dict[name][0])
                center_pts.append(pts_dict[name][1])

            render_all_pts()
            bind_props(axis=1)


# 添加并更新所有标记点
def render_all_pts():
    ith = -1
    global center_props, center_pts
    for i in range(len(center_pts)):
        if i % 2 == 0:
            ith += 1
            rbg = np.array(color_map[dic_list[ith]]) / 255
        center_props[i].setColor(rbg)
        center_props[i].setData(vmi.pdSphere(radius, center_pts[i]))
    voi_view.updateAtOnce()


def LeftButtonPressRelease(**kwargs):
    global center_pts, image_display_method
    if kwargs['picked'] in [voi_view]:
        if kwargs['double'] is True:
            if len(center_pts) < 16:
                center_pts.append(voi_view.pickPt_Cell())
                render_all_pts()
                bind_props(axis=image_display_method)
            else:
                pass
    else:
        image_view.pickPt_FocalPlane()


def LeftButtonPress(**kwargs):
    global visable, image_data, front_img, side_img, top_img, image_view, image_display_method, center_pts, flag
    if kwargs['picked'] is features_box_list[0]:
        output_upload()

    elif kwargs['picked'] is features_box_list[1]:
        load_by_list()

    elif kwargs['picked'] is features_box_list[3]:
        # 显示/隐藏体数据
        visable = not (visable)
        voi_volume.setVisible(visable)
        if visable:
            features_box_list[3].draw_text(text='显示体数据')
        else:
            features_box_list[3].draw_text(text='隐藏体数据')

    elif kwargs['picked'] is overlay_chart_text_box_list[0]:
        if front_img is None:
            front_img = show_Front_view(voi_image)
        image_data.setData(front_img)
        bind_props(axis=1)
        image_data.setColorWindow_Auto()
        image_view.setCamera_FitAll()
        image_display_method = 1

    elif kwargs['picked'] is overlay_chart_text_box_list[1]:
        if side_img is None:
            side_img = show_Side_view(voi_image)

        image_data.setData(side_img)
        bind_props(axis=2)
        image_view.setCamera_FitAll()
        image_data.setColorWindow_Auto()
        image_display_method = 2

    elif kwargs['picked'] is overlay_chart_text_box_list[2]:
        if top_img is None:
            top_img = show_Top_view(voi_image)
        image_data.setData(top_img)
        bind_props(axis=0)
        image_view.setCamera_FitAll()
        image_data.setColorWindow_Auto()
        image_display_method = 0

    elif kwargs['picked'] is features_box_list[4]:
        check_upload()

    elif kwargs['picked'] is features_box_list[5]:
        flag = 1
        d = vmi.askYesNo('是否确认上传术前数据？')
        if d:
            output_upload()

    elif kwargs['picked'] is features_box_list[6]:
        flag = 2
        d = vmi.askYesNo('是否确认上传术后数据？')
        if d:
            output_upload()

    elif kwargs['picked'] is features_box_list[7]:
        flag = 1
        check_upload()

    elif kwargs['picked'] is features_box_list[8]:
        flag = 2
        check_upload()


def LeftButtonPressMove(**kwargs):
    if kwargs['picked'] in center_props:
        i = center_props.index(kwargs['picked'])
        #     center_pts[i] += voi_view.pickVt_FocalPlane()
        #     center_props[i].setData(vmi.pdSphere(radius, center_pts[i]))
        # else:
        #     voi_view.mouseRotateFocal(**kwargs)

        center_pts[i] += voi_view.pickVt_FocalPlane()

        center_props[i].setData(vmi.pdSphere(radius, center_pts[i]))
        bind_props(axis=image_display_method)

    else:
        voi_view.mouseRotateFocal(**kwargs)


def NoButtonWheel(**kwargs):
    if kwargs['picked'] is features_box_list[2]:
        global threshold
        threshold = min(max(threshold + 10 * kwargs['delta'], -1000), 3000)
        features_box_list[2].draw_text('阈值：{} HU'.format(threshold))
        voi_volume.setOpacityScalar({threshold - 1: 0, threshold: 1})


class Main(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)
        brush = QBrush(QColor(255, 255, 255, 255))
        palette = QPalette()
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.setPalette(palette)
        self.setWidgetResizable(True)

    def closeEvent(self, ev: QCloseEvent):
        ev.accept() if vmi.askYesNo('退出程序？') else ev.ignore()


def return_globals():
    return globals()


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://root:medraw123@192.168.11.122:27017/admin', 27017)

    visable = True
    threshold = 200
    image_display_method = 1
    front_img, side_img, top_img = None, None, None
    radius = 2.5
    center_props = []
    center_pts = []

    case_uid = []
    case_info = []
    case_image_data = []
    image_props = []
    mark_hash = []

    voi_image = []
    dcmdir, series, series_list = [], [], []
    flag = 0

    voi_view = vmi.View()

    for i in range(16):
        center_props.append(vmi.PolyActor(voi_view, color=[0, 0, 0], pickable=True, always_on_top=True))
    voi_volume = vmi.ImageVolume(voi_view, pickable=True)

    voi_view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    voi_view.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    textBox_list = []
    for i, key in enumerate(color_map):
        if i % 2 == 0:

            textBox_list.append(vmi.TextBox(voi_view, back_color=QColor.fromRgbF([np.array(color_map[key]) / 255][0][0],
                                                                                 [np.array(color_map[key]) / 255][0][1],
                                                                                 [np.array(color_map[key]) / 255][0][
                                                                                     2]),
                                            size=[0.02, 0.04], pos=[0, i // 2 * 0.06], anchor=[0, 0]))
            textBox_list.append(vmi.TextBox(voi_view, text=key, size=[0.1, 0.04], pos=[0.02, i // 2 * 0.06],
                                            anchor=[0, 0]))
        elif i % 2 == 1:
            textBox_list.append(vmi.TextBox(voi_view, back_color=QColor.fromRgbF([np.array(color_map[key]) / 255][0][0],
                                                                                 [np.array(color_map[key]) / 255][0][1],
                                                                                 [np.array(color_map[key]) / 255][0][
                                                                                     2]),
                                            size=[0.02, 0.04], pos=[0.12, i // 2 * 0.06], anchor=[0, 0]))
            textBox_list.append(vmi.TextBox(voi_view, text=key, size=[0.1, 0.04], pos=[0.14, i // 2 * 0.06],
                                            anchor=[0, 0]))

    features_box_list = [vmi.TextBox(voi_view, pickable=True, text='上传标记数据', size=[0.12, 0.04], pos=[0.12, 0.3],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='下载原始数据', size=[0.12, 0.04], pos=[0, 0.3],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='阈值：200 HU', size=[0.12, 0.04], pos=[0, 0.24],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='显示体数据', size=[0.12, 0.04], pos=[0.12, 0.24],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='查看已上传数据', size=[0.12, 0.04], pos=[0, 0.36],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='上传术前数据', size=[0.12, 0.04], pos=[0, 0.3],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='上传术后数据', size=[0.12, 0.04], pos=[0.12, 0.3],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='查看术前数据', size=[0.12, 0.04], pos=[0, 0.36],
                                     anchor=[0, 0]),
                         vmi.TextBox(voi_view, pickable=True, text='查看术后数据', size=[0.12, 0.04], pos=[0.12, 0.36],
                                     anchor=[0, 0])
                         ]

    features_box_list[0].setVisible(False)
    features_box_list[1].setVisible(False)
    features_box_list[4].setVisible(False)

    for box in features_box_list:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPress]

    features_box_list[2].mouse['NoButton']['Wheel'] = [NoButtonWheel]

    image_view = vmi.View()
    image_data = vmi.ImageSlice(image_view, pickable=True)
    for i in range(16):
        image_props.append(vmi.PolyActor(image_view, color=[0, 0, 0], pickable=True, always_on_top=True))
    overlay_chart_text_box_list = []
    overlay_chart_text_box = vmi.TextBox(image_view, text='叠加图', size=[0.24, 0.04], pos=[0, 0],
                                         anchor=[0, 0])

    for i, text in enumerate(overlay_chart):
        overlay_chart_text_box_list.append(
            vmi.TextBox(image_view, text=text, pickable=True, size=[0.08, 0.04], pos=[0.08 * i, 0.06],
                        anchor=[0, 0]))
        overlay_chart_text_box_list[i].mouse['LeftButton']['Press'] = [LeftButtonPress]

    main = vmi.Main(return_globals)
    main.setAppName('pelvic_mark')
    main.excludeKeys += ['main']

    menu_input = main.menuBar().addMenu('输入')
    menu_input.addAction('DICOM').triggered.connect(input_dicom)
    menu_input.addAction('Series').triggered.connect(input_series)

    main.layout().addWidget(voi_view, 0, 0, 3, 1)

    main.layout().addWidget(image_view, 0, 1, 3, 1)
    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
