import warnings

import pathlib
import math
import tempfile
import time

import numpy as np
import pydicom
import vtk
import requests
import pickle
import json
import base64
import SimpleITK
from PySide2.QtGui import *
from typing import Union, Optional, List
from numba import jit
import vmi


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


def init_voi():
    global voi_image
    voi_image = original_slice.data()
    voi_volume.setData(voi_image)

    voi_view.setCamera_Axial()
    voi_view.setCamera_FitAll()


def overlay_image():
    np_data = vmi.imArray_VTK(voi_image)
    np_data = np_data.swapaxes(0, 2)
    np_data[np_data < 100] = 100
    np_data[np_data > 400] = 400

    overlay_f = np_data.sum(axis=1)
    overlay_t = np_data.sum(axis=2)

    url = "http://192.168.11.70:5000/pelvis_markpoints"
    data = {'overlay_f': base64.b64encode(pickle.dumps(overlay_f)),
            'overlay_t':  base64.b64encode(pickle.dumps(overlay_t))}

    res = requests.post(url=url, data=data)
    print(res)
    print('zzzzzzzzzzz',res.text)
    print('zzzzzzzzzzz',pickle.loads(base64.b64decode(res.text)))


def LeftButtonPressRelease(**kwargs):
    global spcut_radius, pelvis_cs, cup_radius, cup_cs, cup_RA, cup_RI, bone_value, LR
    global body_angle, body_xr, body_yr, kirs_radius
    if kwargs['picked'] is dicom_box:
        original_image = read_dicom()

        if original_image is not None:
            original_image.SetOrigin(0, 0, 0)
            original_slice.setData(original_image)
            original_slice.setSlicePlaneOrigin_Center()
            original_slice.setSlicePlaneNormal_Coronal()
            original_view.setCamera_Coronal()
            original_view.setCamera_FitAll()
            init_voi()
            overlay_image()

            # side = vmi.askButtons(['患右', '患左'], title='选择患侧')
            # if side == '患右':
            #     LR = -1
            # elif side == '患左':
            #     LR = 1
            return True
    elif kwargs['picked'] is bone_value_box:
        v = vmi.askInt(-1000, bone_value, 3000)
        if v is not None:
            bone_value = v
            bone_value_box.draw_text('骨阈值：{:.0f} HU'.format(bone_value))
            voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
            return True


def NoButtonWheel(**kwargs):
    global bone_value
    if kwargs['picked'] is bone_value_box:
        bone_value = min(max(bone_value + 10 * kwargs['delta'], -1000), 3000)
        bone_value_box.draw_text('骨阈值：{:.0f} HU'.format(bone_value))
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
        return True


def return_globals():
    return globals()


if __name__ == '__main__':
    global original_view, voi_view
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

        dicom_box = vmi.TextBox(original_view, text='DICOM', pickable=True,
                                size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0])
        dicom_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        patient_name_box = vmi.TextBox(original_view, text='姓名', visible=False,
                                       size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])

        # 1 目标区域
        voi_view = vmi.View()

        bone_value, target_value = 200, 0

        bone_value_box = vmi.TextBox(voi_view, text='骨阈值：{:.0f} HU'.format(bone_value),
                                     size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)
        bone_value_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        bone_value_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        voi_image = vtk.vtkImageData()
        voi_volume = vmi.ImageVolume(voi_view, pickable=True)
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
        voi_volume.setColor({bone_value: [1, 1, 0.6]})

    # 视图布局
    for v in [original_view, voi_view]:
        v.setMinimumWidth(round(0.5 * main.screenWidth()))

    original_view.setParent(main.scrollArea())
    main.layout().addWidget(original_view, 0, 0, 1, 1)
    main.layout().addWidget(voi_view, 0, 1, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
