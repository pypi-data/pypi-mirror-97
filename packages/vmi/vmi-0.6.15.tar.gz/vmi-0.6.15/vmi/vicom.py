import datetime
import os
import pathlib
import shutil
import tempfile
import threading
from typing import List, Optional, Dict

import SimpleITK as sitk
import numpy as np
import pydicom
import vtk
from PySide2.QtCore import *

import vmi


class SeriesData(QObject, vmi.Menu):
    """DICOM系列数据"""

    def __init__(self, filenames=None, name=None):
        QObject.__init__(self)

        self.name = name if name else self.tr('系列 (Series)')
        vmi.Menu.__init__(self)

        self._Filenames = filenames
        self._Directory = tempfile.TemporaryDirectory()

        if self._Filenames and len(self._Filenames) > 0:
            self._Filenames = [shutil.copy2(f, self._Directory.name) for f in self._Filenames]

    def __setstate__(self, s):
        self.__init__(name=s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Filenames = []
        self._Directory = tempfile.TemporaryDirectory()
        for kw in s['_Bytes']['_Files']:
            p = pathlib.Path(self._Directory.name) / kw
            p.write_bytes(s['_Bytes']['_Files'][kw])
            self._Filenames.append(str(p))

        del s['_Bytes']

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['_Filenames', '_Directory', 'menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Bytes'] = {'_Files': {pathlib.Path(f).name: pathlib.Path(f).read_bytes() for f in self._Filenames}}
        return s

    def __str__(self):
        with pydicom.dcmread(self._Filenames[0]) as ds:
            r = ['', '', '', '', '']
            for e in [_ for _ in ds if _.VR != 'SQ']:
                e.showVR = False
                if e.name in ['Modality', 'Slice Thickness', 'Rows', 'Columns', 'Pixel Spacing', 'Pixel Data']:
                    r[0] += repr(e) + '\n'
                elif e.name.startswith('Patient'):
                    r[1] += repr(e) + '\n'
                elif e.name.startswith('Study'):
                    r[2] += repr(e) + '\n'
                elif e.name.startswith('Series'):
                    r[3] += repr(e) + '\n'
                elif e.name.startswith('Image'):
                    r[4] += repr(e) + '\n'
            return 'Slices: {}\n'.format(len(self._Filenames)) + r[0] + r[1] + r[2] + r[3] + r[4]

    def __repr__(self):
        return self.__str__()

    def toKeywordValue(self) -> Dict[str, str]:
        d = {'Slices': len(self._Filenames)}
        with pydicom.dcmread(self._Filenames[0]) as ds:
            for e in ds.iterall():
                if e.value.__class__ in [None, bool, int, float, str]:
                    d[e.keyword] = e.value
                elif e.value.__class__ in [bytes]:
                    d[e.keyword] = '{} bytes'.format(len(e.value))
                else:
                    d[e.keyword] = str(e.value)
        d = {kw: d[kw] for kw in sorted(d)}
        return d

    def filenames(self) -> List[str]:
        """返回文件列表"""
        return self._Filenames

    def readITK(self) -> sitk.Image:
        """读取系列为SimpleITK图像"""
        r = sitk.ImageSeriesReader()
        r.SetFileNames(self._Filenames)
        image = r.Execute()
        return image

    def read(self) -> Optional[vtk.vtkImageData]:
        """读取系列为vtkImageData图像"""
        image = None

        def func():
            nonlocal image
            image = vmi.imVTK_SITK(self.readITK())

        t = threading.Thread(target=func)
        t.start()
        vmi.appwait(t)
        return image


def sortSeries(dcmdir: str, recursive: bool = True) -> List[SeriesData]:
    """
    识别并排序DICOM文件，返回SeriesData对象的列表

    :param dcmdir: DICOM文件夹
    :param recursive: 递归搜索
    :return: [SeriesData]
    """
    dcmdir = str(pathlib.Path(dcmdir))
    series = []

    def func():
        roots = [dcmdir]
        if recursive:
            roots = [root for root, *_ in os.walk(dcmdir)]
            roots.sort()
        for root in roots:
            with tempfile.TemporaryDirectory() as p:
                if vmi.contains_zh_CN(root):
                    for f in os.listdir(root):
                        f = os.path.join(root, f)
                        if os.path.isfile(f):
                            shutil.copy2(f, p)
                    root = p

                for i in sitk.ImageSeriesReader.GetGDCMSeriesIDs(root):
                    filenames = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(root, i)
                    series.append(SeriesData(filenames))

    t = threading.Thread(target=func)
    t.start()
    vmi.appwait(t)
    return series


def sortFilenames(dcmdir: str, recursive: bool = True) -> List[List[str]]:
    """
    识别并排序DICOM文件，返回Series的文件名列表的列表

    :param dcmdir: DICOM文件夹
    :param recursive: 递归搜索
    :return: [[filenames]]
    """
    dcmdir = str(pathlib.Path(dcmdir))
    filenames_list = []

    roots = [dcmdir]
    if recursive:
        roots = [root for root, *_ in os.walk(dcmdir)]
        roots.sort()
    for root in roots:
        with tempfile.TemporaryDirectory() as p:
            if vmi.contains_zh_CN(root):
                for f in os.listdir(root):
                    f = os.path.join(root, f)
                    if os.path.isfile(f):
                        shutil.copy2(f, p)
                directory = p
            else:
                directory = root

            for i in sitk.ImageSeriesReader.GetGDCMSeriesIDs(directory):
                filenames = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(directory, i)
                filenames = [str(pathlib.Path(root) / pathlib.Path(f).name) for f in filenames]
                filenames_list.append(filenames)
                print('sortFilenames {}'.format(len(filenames_list)))
    return filenames_list


def imSaveDICOM_SeriesCT(image: vtk.vtkImageData, path=None) -> None:
    """保存vtkImageData到DICOM文件"""
    if path is None:
        path = vmi.askDirectory('导出 (Export) DICOM Series')
        if path is None:
            return

    date = datetime.datetime.now().strftime('%Y%m%d')
    time = datetime.datetime.now().strftime('%H%M%S.%f')
    pixel_array = vmi.imArray_VTK(image)
    origin = np.array(image.GetOrigin())
    dimensions = np.array(image.GetDimensions())

    for k in pixel_array.shape[0]:
        suffix = '.dcm'
        filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
        filename_big_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

        file_meta = pydicom.Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"

        ds = pydicom.FileDataset(filename_little_endian, {}, file_meta=file_meta, preamble=b"\0" * 128)
        ds.is_little_endian = True
        ds.is_implicit_VR = True

        ds.PatientName = 'anonymous'
        ds.PatientID = '000000'

        ds.AccessionNumber = '0000000000000'
        ds.AcquisitionDate = date
        ds.AcquisitionDateTime = date + time
        ds.AcquisitionNumber = ''
        ds.AcquisitionTime = time

        ds.BitsAllocated = 16
        ds.BitsStored = 12
        ds.HighBit = 11

        ds.ContentDate = date
        ds.ContentTime = time

        ds.ImageOrientationPatient = ['1', '0', '0', '0', '1', '0']
        ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL', 'HELIX']

        ds.Rows = dimensions[0]
        ds.Columns = dimensions[1]
        print(pixel_array.dtype)
        ds.PixelData = pixel_array.tobytes()

        ds.InstanceCreationDate = date
        ds.InstanceCreationTime = time
