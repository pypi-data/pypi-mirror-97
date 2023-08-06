import hashlib
import gridfs
import pymongo
import pickle
import vtk

import vmi

import SimpleITK


def from_image_to_stl():
    # 获取图像信息
    uid = "1.2.840.113704.1.111.9620.1487668799.1"
    search_dict = {'StudyInstanceUID': uid}
    md5_key = image_data_db.find_one(search_dict)
    data_image = image_file_db.find_one({'md5': md5_key['predicted_md5'][-1]})

    pelvis_image = pickle.loads(data_image.read())

    # 中值滤波
    res = 1
    spc = vmi.imSpacing(pelvis_image)
    size = [int(0.5 + res / spc[0]),
            int(0.5 + res / spc[1]),
            int(0.5 + res / spc[2])]

    itk_image: SimpleITK.Image = vmi.imSITK_VTK(pelvis_image)
    smooth = SimpleITK.BinaryMedianImageFilter()
    smooth.SetRadius(size)
    itk_image = smooth.Execute(itk_image)
    pelvis_image = vmi.imVTK_SITK(itk_image)

    # 等值面提取
    fe = vtk.vtkFlyingEdges3D()
    fe.SetInputData(pelvis_image)
    fe.SetValue(0, 1)
    fe.SetComputeNormals(0)
    fe.SetComputeGradients(0)
    fe.SetComputeScalars(0)
    fe.Update()

    # 光滑处理
    smooth = vtk.vtkWindowedSincPolyDataFilter()
    smooth.SetInputData(fe.GetOutput())
    smooth.SetNumberOfIterations(20)
    smooth.SetBoundarySmoothing(0)
    smooth.SetFeatureEdgeSmoothing(0)
    smooth.SetFeatureAngle(60)
    smooth.SetPassBand(0.1)
    smooth.SetNonManifoldSmoothing(1)
    smooth.SetNormalizeCoordinates(1)
    smooth.Update()

    pd = smooth.GetOutput()

    # 保存STL文件
    stl_filename = uid + '.stl'
    w = vtk.vtkSTLWriter()
    w.SetInputData(pd)
    w.SetFileName(stl_filename)
    w.SetFileTypeToBinary()
    w.Update()

    # 上传STL文件
    stl_file = open(stl_filename, 'rb')
    file_data = stl_file.read()
    model_md5 = hashlib.md5(file_data).hexdigest()

    if not model_file_db.exists({'md5': model_md5}):
        file_id = model_file_db.put(file_data,
                                    fileType='.stl',
                                    StudyInstanceUID=uid,
                                    type='model')

        # 检查上传结果是否与本地一致
        if model_file_db.find_one({'_id': file_id}).md5 != model_md5:
            model_file_db.delete(file_id)
            return print('文件上传失败')
        else:
            # 替换旧数据,增加STL数据的md5
            if not model_data_db.find_one(search_dict):
                model_data_db.insert_one(search_dict)

            key_data_dict = model_data_db.find_one(search_dict)
            value_data_dict = {**key_data_dict,
                               'model_md5': model_md5,
                               'type': 'model'}
            model_data_db.find_one_and_replace(key_data_dict, value_data_dict)

    return pd


def from_cup_data_to_stl():
    pt_dict = {'臼杯中心': [107.93227321, 179.52647828, 157.30932222],
               '臼杯半径': 25.0,
               '朝向': [1, 0, 0]}

    o, r, n = pt_dict['臼杯中心'], pt_dict['臼杯半径'], pt_dict['朝向']

    plane = vtk.vtkPlane()
    plane.SetNormal(n)
    plane.SetOrigin(o)

    pd = vmi.pdSphere(r, o)
    pd = vmi.pdClip_Implicit(pd, plane)[1]
    pd_border = vmi.pdPolyline_Regular(r, o, n)
    pd = vmi.pdAppend([pd, pd_border])

    return pd


def return_globals():
    return globals()


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://root:medraw123@192.168.11.122:27017/admin', 27017)

    image_data_db: pymongo.collection.Collection = client.xj_testDB.pelvisPredict
    image_file_db = gridfs.GridFS(client.xj_testDB, collection='pelvisPredict')

    model_data_db: pymongo.collection.Collection = client.xj_testDB.pelvisSTL
    model_file_db = gridfs.GridFS(client.xj_testDB, collection='pelvisSTL')

    view = vmi.View()

    # 骨盆模型
    pelvis_data = from_image_to_stl()
    pelvis_prop = vmi.PolyActor(view)
    pelvis_prop.setData(pelvis_data)

    # 臼杯
    cup_data = from_cup_data_to_stl()
    cup_prop = vmi.PolyActor(view)
    cup_prop.setData(cup_data)

    view.setCamera_FitAll()

    main = vmi.Main(return_globals)
    main.setAppName('image_to_stl')
    main.setAppVersion(vmi.version)
    main.excludeKeys += ['main']

    main.layout().addWidget(view, 0, 0, 1, 1)
    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
