import hashlib
import pickle
import threading
from typing import Dict, Any

import gridfs
import pydicom
import pymongo
import requests
import vmi
import vtk
from PySide2.QtCore import *
from PySide2.QtWidgets import *


def input_dicom():
    global series_list, dcmdir
    dcmdir = vmi.askDirectory('DICOM')

    if dcmdir is not None:
        series_list = vmi.sortSeries(dcmdir)
        input_series()


def input_series():
    global series_dict, series
    series = vmi.askSeries(series_list)
    if series:
        series_dict = series.toKeywordValue()
        input_image(series.read())


def input_image(image: vtk.vtkImageData):
    series_volume.setData(image)
    series_view.setCamera_FitAll()
    series_view.updateAtOnce()
    vmi.appupdate()


def update_series_opcity():
    series_volume.setOpacityScalar({series_opacity_range[0] - 1: 0,
                                    series_opacity_range[0]: 1,
                                    series_opacity_range[1]: 1,
                                    series_opacity_range[1] + 1: 0})
    series_volume.setColor({series_opacity_range[0]: [1, 1, 0.9],
                            series_opacity_range[1]: [1, 1, 0.1]})


def output_nifti():
    if series_dict:
        vmi.imSaveFile_NIFTI(series_volume.data())


def upload_dcm():
    if series:
        file_names = series.filenames()

        tag_list = []
        for i in file_names:
            d = {}
            with pydicom.dcmread(i) as ds:
                for e in ds.iterall():
                    if e.value.__class__ in [None, bool, int, float, str]:
                        d[e.keyword] = e.value
                    elif e.value.__class__ in [bytes]:
                        d[e.keyword] = '{} bytes'.format(len(e.value))
                    else:
                        d[e.keyword] = str(e.value)
            d = {kw: d[kw] for kw in sorted(d)}
            tag_list.append(d)

        if not file_db.exists({'StudyInstanceUID': tag_list[0]['StudyInstanceUID']}):
            for i, val in enumerate(file_names):
                single_file = open(val, 'rb').read()
                single_md5 = hashlib.md5(single_file).hexdigest()
                if not file_db.exists({'md5': single_md5}):
                    file_db.put(single_file, **tag_list[i])


def output_upload():
    if series:
        # 上传原始数据
        upload_dcm()

        # 查找用户账号
        user_list = []
        user_db: pymongo.collection.Collection = client.wby_testDB.DoctorCollection
        for x in user_db.find({'doctor_userName': {'$exists': True}}):
            user_list.append(x['doctor_userName'])

        # 标注信息
        label = [QLabel('销售姓名:'), QLabel('销售电话:'), QLabel('手术时间:')]
        text = []

        size_policy_min = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        dialog = QDialog()
        dialog.setSizePolicy(size_policy_min)
        dialog.setWindowTitle('Upload')
        dialog.setLayout(QVBoxLayout())
        dialog.setMinimumWidth(200)

        combo_box = [QComboBox(), QComboBox()]
        combo_box[0].addItem("导板名称：THA手术导板")
        combo_box[0].addItem("导板名称：TKA手术导板")
        dialog.layout().addWidget(combo_box[0])

        for i in user_list:
            combo_box[1].addItem('用户姓名： ' + i)
        dialog.layout().addWidget(combo_box[1])

        for i in range(len(label)):
            text.append(QLineEdit())
            dialog.layout().addWidget(label[i])
            dialog.layout().addWidget(text[i])

        button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button.setSizePolicy(size_policy_min)
        button.accepted.connect(dialog.accept)
        button.rejected.connect(dialog.reject)
        dialog.layout().addWidget(button)

        if dialog.exec_() == QDialog.Accepted:
            if series_dict:
                # Web通讯
                data = {
                    "uuid": QUuid.createUuid().toString(),
                    "patientName": series_dict["PatientName"],
                    "patientGender": series_dict["PatientSex"],
                    "patientAge": series_dict["PatientAge"],
                    "guideType": 'THA',
                    "userName": '1'
                }

                response = requests.post("http://192.168.11.185:3333/sys/newUID", data=str(data))

                case_type = []
                if combo_box[0].currentIndex() == 0:
                    case_type = 'THA'
                elif combo_box[0].currentIndex() == 1:
                    case_type = 'TKA'

                case_userName = user_list[combo_box[1].currentIndex()]

                if response.text != "-1":
                    # 上传案例数据
                    case_uid = {'case_uid': response.text}
                    key_dict = case_db.find_one(case_uid)
                    val_dict = {**key_dict,
                                'case_studyInstanceUID': series_dict['StudyInstanceUID'],
                                'case_userName': case_userName,
                                'case_salesName': text[0].text(),
                                'case_salesPhoneNumber': text[1].text(),
                                'case_operationDate': text[2].text(),
                                'case_type': case_type}
                    case_db.find_one_and_replace(key_dict, val_dict)


def LeftButtonPressRelease(**kwargs):
    global series_opacity_range
    if kwargs['picked'] is series_opacity_range_box[0]:
        v = vmi.askInt(-10000, series_opacity_range[0], series_opacity_range[1])
        if v is not None:
            series_opacity_range[0] = v
        series_opacity_range_box[0].draw_text('min {:.0f}'.format(series_opacity_range[0]))
        update_series_opcity()
    elif kwargs['picked'] is series_opacity_range_box[1]:
        v = vmi.askInt(series_opacity_range[0], series_opacity_range[0], 10000)
        if v is not None:
            series_opacity_range[1] = v
        series_opacity_range_box[1].draw_text('min {:.0f}'.format(series_opacity_range[1]))
        update_series_opcity()


def NoButtonWheel(**kwargs):
    global series_opacity_range
    if kwargs['picked'] is series_opacity_range_box[0]:
        series_opacity_range[0] = min(max(series_opacity_range[0] + kwargs['delta'],
                                          -10000), series_opacity_range[1])
        series_opacity_range_box[0].draw_text('min {:.0f}'.format(series_opacity_range[0]))
        update_series_opcity()
    elif kwargs['picked'] is series_opacity_range_box[1]:
        series_opacity_range[1] = min(max(series_opacity_range[1] + kwargs['delta'],
                                          series_opacity_range[0]), 10000)
        series_opacity_range_box[1].draw_text('max {:.0f}'.format(series_opacity_range[1]))
        update_series_opcity()


def return_globals():
    return globals()


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://root:medraw123@192.168.11.122:27017/admin', 27017)
    case_db: pymongo.collection.Collection = client.wby_testDB.case
    file_db = gridfs.GridFS(client.SkywardDB, collection='Dicom')

    dcmdir, series = [], []

    main = vmi.Main(return_globals)
    main.setAppName('dicom_uoloader')
    main.setAppVersion(vmi.version)
    main.excludeKeys += ['main']

    menu_input = main.menuBar().addMenu('输入')
    menu_input.addAction('DICOM').triggered.connect(input_dicom)
    menu_input.addAction('Series').triggered.connect(input_series)

    menu_output = main.menuBar().addMenu('输出')
    menu_output.addAction('NIFTI').triggered.connect(output_nifti)
    menu_output.addAction('上传').triggered.connect(output_upload)

    series_list, series_dict = [], {}
    series_view = vmi.View()
    series_view.setCamera_Coronal()
    series_volume = vmi.ImageVolume(series_view)

    series_opacity_range = [200, 3000]
    update_series_opcity()

    series_opacity_range_box = [vmi.TextBox(series_view, text='min {:.0f}'.format(series_opacity_range[0]),
                                            size=[0.1, 0.03], pos=[0, 0.03], anchor=[0, 0], pickable=True),
                                vmi.TextBox(series_view, text='max {:.0f}'.format(series_opacity_range[1]),
                                            size=[0.1, 0.03], pos=[0.1, 0.03], anchor=[0, 0], pickable=True)]

    for box in series_opacity_range_box:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    main.layout().addWidget(series_view, 0, 0, 1, 1)
    vmi.appexec(main)
    vmi.appexit()
