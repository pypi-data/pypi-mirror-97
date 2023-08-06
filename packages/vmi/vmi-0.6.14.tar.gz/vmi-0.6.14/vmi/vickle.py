import copyreg
import pathlib
import tempfile
from typing import Dict, Any

import numpy as np
import vtk
from OCC.Core.IFSelect import *
from OCC.Core.STEPControl import *
from OCC.Core.TopoDS import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import vmi

vtkget_ignore = ('GetDebug', 'GetGlobalReleaseDataFlag', 'GetGlobalWarningDisplay', 'GetReferenceCount',
                 'GetAAFrames', 'GetFDFrames', 'GetSubFrames', 'GetUseConstantFDOffsets', 'GetStereoCapableWindow',
                 'GetForceCompileOnly', 'GetGlobalImmediateModeRendering', 'GetImmediateModeRendering',
                 'GetScalarMaterialMode', 'GetReleaseDataFlag')


def vtkInstance_gets(instance) -> Dict[str, Any]:
    """
    返回vtk类型实例的所有Set/Get状态值

    :param instance: vtk类型实例
    :return: 状态值{'GetXXX': Any}
    """
    gets = {}
    for get_name in dir(instance):
        if get_name.startswith('Get'):
            set_name = get_name.replace('Get', 'Set', 1)
            if hasattr(instance, set_name) and get_name not in vtkget_ignore:
                try:
                    a = getattr(instance, get_name)()
                    if 'vtk' not in str(type(a)):
                        gets[get_name] = a
                except TypeError:
                    pass
    return gets


def vtkInstance_sets(instance, gets) -> None:
    """
    设置vtk类型实例的所有Set/Get状态值
    :param instance: vtk类型实例
    :param gets: 状态值{'GetXXX': Any}
    :return: None
    """
    for get_name in gets:
        set_name = get_name.replace('Get', 'Set', 1)
        try:
            getattr(instance, set_name)(gets[get_name])
        except TypeError:
            pass


def pickle_vtkImageData(instance: vtk.vtkImageData):
    gets = vtkInstance_gets(instance)
    if instance.GetNumberOfPoints() == 0:
        data = bytes()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vti'
            vmi.imSaveFile_XML(instance, str(p))
            data = p.read_bytes()
    return unpickle_vtkImageData, (gets, data,)


def unpickle_vtkImageData(gets, data):
    if len(data) == 0:
        instance = vtk.vtkImageData()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vti'
            p.write_bytes(data)
            instance = vmi.imOpenFile_XML(str(p))
    vtkInstance_sets(instance, gets)
    return instance


def pickle_vtkLookupTable(instance: vtk.vtkLookupTable):
    gets = vtkInstance_gets(instance)
    data = []
    for i in range(instance.GetNumberOfTableValues()):
        data.append(instance.GetTableValue(i))
    return unpickle_vtkLookupTable, (gets, data,)


def unpickle_vtkLookupTable(gets, data):
    instance = vtk.vtkLookupTable()
    vtkInstance_sets(instance, gets)
    instance.SetNumberOfTableValues(len(data))
    for i in range(len(data)):
        instance.SetTableValue(i, data[i])
    instance.Build()
    return instance


def pickle_vtkMatrix4x4(instance: vtk.vtkMatrix4x4):
    gets = vtkInstance_gets(instance)
    data = np.zeros((4, 4))
    for j in range(4):
        for i in range(4):
            data[i, j] = instance.GetElement(j, i)
    return unpickle_vtkMatrix4x4, (gets, data,)


def unpickle_vtkMatrix4x4(gets, data):
    instance = vtk.vtkMatrix4x4()
    vtkInstance_sets(instance, gets)
    for j in range(4):
        for i in range(4):
            instance.SetElement(j, i, data[i, j])
    return instance


def pickle_vtkPolyData(instance: vtk.vtkPolyData):
    gets = vtkInstance_gets(instance)
    if instance.GetNumberOfPoints() == 0:
        data = bytes()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vtp'
            vmi.pdSaveFile_XML(instance, str(p))
            data = p.read_bytes()
    return unpickle_vtkPolyData, (gets, data,)


def unpickle_vtkPolyData(gets, data):
    if len(data) == 0:
        instance = vtk.vtkPolyData()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vtp'
            p.write_bytes(data)
            instance = vmi.pdOpenFile_XML(str(p))
    vtkInstance_sets(instance, gets)
    return instance


copyreg.pickle(vtk.vtkImageData, pickle_vtkImageData)
copyreg.pickle(vtk.vtkLookupTable, pickle_vtkLookupTable)
copyreg.pickle(vtk.vtkMatrix4x4, pickle_vtkMatrix4x4)
copyreg.pickle(vtk.vtkPolyData, pickle_vtkPolyData)


def pickle_TopoDS_Shape(instance: TopoDS_Shape):
    if instance.IsNull():
        data = bytes()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.stp'
            w = STEPControl_Writer()
            w.Transfer(instance, STEPControl_AsIs)
            status = w.Write(str(p))
            if status == IFSelect_RetDone:
                data = p.read_bytes()
            else:
                data = bytes()
    return unpickle_TopoDS_Shape, (data,)


def unpickle_TopoDS_Shape(data):
    if len(data) == 0:
        instance = TopoDS_Shape()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.stp'
            p.write_bytes(data)
            r = STEPControl_Reader()
            status = r.ReadFile(str(p))
            if status == IFSelect_RetDone:
                r.TransferRoots()
                instance = r.OneShape()
            else:
                instance = TopoDS_Shape()
    return instance


copyreg.pickle(TopoDS_Shape, pickle_TopoDS_Shape)


def pickle_QImage(instance: QImage):
    ba = QByteArray()
    buffer = QBuffer(ba)
    buffer.open(QIODevice.WriteOnly)
    instance.save(buffer, 'PNG')
    return unpickle_QImage, (ba.data(), instance.format().name.decode())


def unpickle_QImage(data, format):
    ba = QByteArray(data)
    instance = QImage.fromData(ba, format)
    return instance


copyreg.pickle(QImage, pickle_QImage)


def contains_zh_CN(text) -> bool:
    """判断字符串是否包含中文"""
    return text.encode() != text.encode('cp936')


def read_Medraw(file_name: str) -> Dict:
    """
    读取.medraw文件，输出

    :param file_name: 文件路径
    :return: {'appName', 'appVersion', 'origin', 'spacing', 'extent', 'aryRef', 'aryEdi', 'imageRef', 'imageEdi'}
    """
    f = QFile(file_name)
    f.open(QIODevice.ReadOnly)
    s = QDataStream(f)

    appName = s.readQString()
    appVersion = s.readQString()
    origin = [s.readDouble(), s.readDouble(), s.readDouble()]
    spacing = [s.readDouble(), s.readDouble(), s.readDouble()]
    extent = [s.readInt32(), s.readInt32(), s.readInt32(), s.readInt32(), s.readInt32(), s.readInt32()]
    shape = [extent[5] - extent[4] + 1, extent[3] - extent[2] + 1, extent[1] - extent[0] + 1]

    aryRef = np.zeros(shape)
    aryEdi = np.zeros(shape)

    for k in range(aryRef.shape[0]):
        for j in range(aryRef.shape[1]):
            for i in range(aryRef.shape[2]):
                aryRef[k][j][i] = s.readInt16()
                aryEdi[k][j][i] = s.readUInt8()

    imageRef = vmi.imVTK_Array(aryRef, origin, spacing)
    imageEdi = vmi.imVTK_Array(aryEdi, origin, spacing)

    return {'appName': appName, 'appVersion': appVersion, 'origin': origin, 'spacing': spacing, 'extent': extent,
            'aryRef': aryRef, 'aryEdi': aryEdi, 'imageRef': imageRef, 'imageEdi': imageEdi}
