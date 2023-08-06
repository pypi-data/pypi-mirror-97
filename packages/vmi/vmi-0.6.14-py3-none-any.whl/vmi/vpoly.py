import pathlib
import shutil
import tempfile
from typing import Union, List, Optional, Dict, Any

import numpy as np
import vtk

import vmi


def pdOpenFile_STL(file=None) -> Optional[vtk.vtkPolyData]:
    """读取STL文件返回vtkPolyData，读取失败则返回None"""
    if file is None:
        file = vmi.askOpenFile('*.stl', '导入 (Import) STL')
        if file is None:
            return
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.stl'
        shutil.copyfile(file, p)
        r = vtk.vtkSTLReader()
        r.SetFileName(str(p))
        r.Update()
        return r.GetOutput()


def pdSaveFile_STL(pd: vtk.vtkPolyData, file=None) -> None:
    """保存vtkPolyData到STL文件"""
    if file is None:
        file = vmi.askSaveFile('stl', '*.stl', '导出 (Export) STL')
        if file is None:
            return
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.stl'
        w = vtk.vtkSTLWriter()
        w.SetInputData(pd)
        w.SetFileName(str(p))
        w.SetFileTypeToBinary()
        w.Update()
        shutil.copyfile(p, file)


def pdSaveFile_XML(pd: vtk.vtkPolyData, file=None) -> None:
    """保存vtkPolyData到vtp文件"""
    if file is None:
        file = vmi.askSaveFile('vtp', '*.vtp', '导出 (Export) XML')
        if file is None:
            return

    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.vtp'
        w = vtk.vtkXMLPolyDataWriter()
        w.SetFileName(str(p))
        w.SetInputData(pd)
        w.SetDataModeToBinary()
        w.SetCompressorTypeToZLib()
        w.Update()
        shutil.copyfile(p, file)


def pdOpenFile_XML(file=None) -> Optional[vtk.vtkPolyData]:
    """读取vtp文件返回vtkPolyData，读取失败则返回None"""
    if file is None:
        file = vmi.askOpenFile('*.vtp', '导入 (Import) XML')
        if file is None:
            return
    with tempfile.TemporaryDirectory() as p:
        p = pathlib.Path(p) / '.vtp'
        shutil.copyfile(file, p)
        r = vtk.vtkXMLPolyDataReader()
        r.SetFileName(str(p))
        r.Update()
        return r.GetOutput()


def pdBounds(pd: vtk.vtkPolyData):
    """返回边界[xmin, xmax, ymin, ymax, zmin, zmax]"""
    return np.array(pd.GetBounds())


def pdCenter(pd: vtk.vtkPolyData):
    """返回包围盒中心[x, y, z]"""
    b = pdBounds(pd)
    return 0.5 * np.array([b[0] + b[1], b[2] + b[3], b[4] + b[5]])


def pdMassCenter(pd: vtk.vtkPolyData) -> np.ndarray:
    """返回密度中心"""
    mass = vtk.vtkCenterOfMass()
    mass.SetInputData(pd)
    mass.Update()
    return np.array(mass.GetCenter())


def pdSize(pd: vtk.vtkPolyData):
    """返回轴向包围盒尺寸"""
    b = pdBounds(pd)
    return np.linalg.norm(np.array([b[1] - b[0], b[3] - b[2], b[5] - b[4]]))


def pdPolyline(pts: List[Union[np.ndarray, List[float]]], closed=False) -> Optional[vtk.vtkPolyData]:
    """
    构造折线段

    :param pts: 节点
    :param closed: 闭合
    :return: vtkPolyData，构造失败则返回None
    """
    if len(pts) < 2:
        return

    points = vtk.vtkPoints()
    for pt in pts:
        points.InsertNextPoint([pt[0], pt[1], pt[2]])

    ids = vtk.vtkIdList()

    for i in range(points.GetNumberOfPoints()):
        ids.InsertNextId(i)

    if closed:
        ids.InsertNextId(0)

    lines = vtk.vtkCellArray()
    lines.InsertNextCell(ids)

    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    pd.SetLines(lines)
    return pd


def pdPolyline_Regular(radius: float, center: Union[np.ndarray, List[float]], normal: Union[np.ndarray, List[float]],
                       resolution: float = 120) -> vtk.vtkPolyData:
    """
    构造无面正多边形

    :param radius: 节点半径
    :param center: 中心坐标
    :param normal: 所在平面的法向
    :param resolution: 边数
    :return: vtkPolyData，构造失败则返回None
    """
    polyline = vtk.vtkRegularPolygonSource()
    polyline.SetCenter(*list(center[:3]))
    polyline.SetNormal(*list(normal[:3]))
    polyline.SetRadius(radius)
    polyline.SetNumberOfSides(resolution)
    polyline.SetGeneratePolygon(0)
    polyline.Update()
    return polyline.GetOutput()


def pdPolygon_Regular(radius: float, center: Union[np.ndarray, List[float]], normal: Union[np.ndarray, List[float]],
                      resolution: float = 120) -> vtk.vtkPolyData:
    """
    构造有面正多边形

    :param radius: 节点半径
    :param center: 中心坐标
    :param normal: 所在平面的法向
    :param resolution: 边数
    :return: vtkPolyData，构造失败则返回None
    """
    polyline = vtk.vtkRegularPolygonSource()
    polyline.SetCenter(*list(center[:3]))
    polyline.SetNormal(*list(normal[:3]))
    polyline.SetRadius(radius)
    polyline.SetNumberOfSides(resolution)
    polyline.SetGeneratePolygon(1)
    polyline.Update()
    return polyline.GetOutput()


def pdPolygon(pt_list: List[Union[np.ndarray, List[float]]]):
    n = len(pt_list)

    if n < 3:
        return
    pts = vtk.vtkPoints()

    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(n)

    for i in range(n):
        pts.InsertNextPoint(pt_list[i])
        polygon.GetPointIds().SetId(i, i)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polygon)

    pd = vtk.vtkPolyData()
    pd.SetPoints(pts)
    pd.SetPolys(cells)

    return pd


def pdSphere(radius: float, center: Union[np.ndarray, List[float]], resolution: float = 120) -> vtk.vtkPolyData:
    """
    构造球体

    :param radius: 半径
    :param center: 中心
    :param resolution: 边数
    :return: vtkPolyData，构造失败则返回None
    """
    source = vtk.vtkSphereSource()
    source.SetCenter(list(center[:3]))
    source.SetRadius(radius)
    source.SetPhiResolution(resolution)
    source.SetThetaResolution(resolution)
    source.Update()
    return source.GetOutput()


def pdExtract_Largest(pd: vtk.vtkPolyData) -> vtk.vtkPolyData:
    """提取最大的相连网格"""
    connectivity = vtk.vtkPolyDataConnectivityFilter()
    connectivity.SetInputData(pd)
    connectivity.SetExtractionModeToLargestRegion()
    connectivity.Update()
    return connectivity.GetOutput()


def pdExtract_Closest(pd: vtk.vtkPolyData, pt) -> vtk.vtkPolyData:
    """提取距离pt最近的相连网格"""
    connectivity = vtk.vtkPolyDataConnectivityFilter()
    connectivity.SetInputData(pd)
    connectivity.SetExtractionModeToClosestPointRegion()
    connectivity.SetClosestPoint([pt[i] for i in range(3)])
    connectivity.Update()
    return connectivity.GetOutput()


def pdSmooth_WindowedSinc(pd: vtk.vtkPolyData, iter_num=10) -> vtk.vtkPolyData:
    """光顺网格，窗函数法，迭代次数iter_num越大则光顺程度越高"""
    smooth = vtk.vtkWindowedSincPolyDataFilter()
    smooth.SetInputData(pd)
    smooth.SetNumberOfIterations(iter_num)
    smooth.SetPassBand(0.1)
    smooth.SetNonManifoldSmoothing(1)
    smooth.SetNormalizeCoordinates(1)
    smooth.SetFeatureAngle(60)
    smooth.SetBoundarySmoothing(0)
    smooth.SetFeatureEdgeSmoothing(0)
    smooth.Update()
    return smooth.GetOutput()


def pdSmooth_Laplacian(pd: vtk.vtkPolyData, iter_num=10) -> vtk.vtkPolyData:
    """光顺网格，拉普拉斯函数法，迭代次数iter_num越大则光顺程度越高"""
    smooth = vtk.vtkSmoothPolyDataFilter()
    smooth.SetInputData(pd)
    smooth.SetNumberOfIterations(iter_num)
    smooth.SetConvergence(0)
    smooth.SetRelaxationFactor(0.33)
    smooth.SetFeatureAngle(60)
    smooth.SetBoundarySmoothing(0)
    smooth.SetFeatureEdgeSmoothing(0)
    smooth.Update()
    return smooth.GetOutput()


def pdNormals(pd: vtk.vtkPolyData) -> vtk.vtkPolyData:
    """计算网格单元法向"""
    if pd.GetPointData().GetNormals() is None or pd.GetCellData().GetNormals() is None:
        normals = vtk.vtkPolyDataNormals()
        normals.SetInputData(pd)
        normals.SetComputePointNormals(1)
        normals.SetComputeCellNormals(1)
        normals.Update()
        return normals.GetOutput()
    return pd


def pdTriangle(pd: vtk.vtkPolyData, pass_verts=1, pass_lines=1) -> vtk.vtkPolyData:
    """
    三角网格化

    :param pd: 输入网格
    :param pass_verts: 是否保留点单元
    :param pass_lines: 是否保留线单元
    :return: vtkPolyData
    """
    triangle = vtk.vtkTriangleFilter()
    triangle.SetPassVerts(pass_verts)
    triangle.SetPassLines(pass_lines)
    triangle.SetInputData(pd)
    triangle.Update()
    return triangle.GetOutput()


def pdClip_Implicit(pd: vtk.vtkPolyData, f: vtk.vtkImplicitFunction) -> List[vtk.vtkPolyData]:
    """
    隐函数裁剪网格

    :param pd: 输入网格
    :param f: 隐函数
    :return: [vtkPolyData (隐函数大于0), vtkPolyData (隐函数小于0)]
    """
    clip = vtk.vtkClipPolyData()
    clip.SetClipFunction(f)
    clip.SetInputData(pdNormals(pd))
    clip.SetGenerateClippedOutput(1)
    clip.Update()
    return [clip.GetOutput(), clip.GetClippedOutput()]


def pdClip_Pd(pd: vtk.vtkPolyData, clip_pd: vtk.vtkPolyData) -> List[vtk.vtkPolyData]:
    """
    网格裁剪网格

    :param pd: 输入网格
    :param clip_pd: 裁剪网格
    :return: [vtkPolyData (裁剪网格外侧), vtkPolyData (裁剪网格内侧)]
    """
    clip_function = vtk.vtkImplicitPolyDataDistance()
    clip_function.SetInput(pdNormals(clip_pd))
    return pdClip_Implicit(pd, clip_function)


def pdCut_Implicit(pd: vtk.vtkPolyData, f: vtk.vtkImplicitFunction) -> vtk.vtkPolyData:
    """
    隐函数切割网格

    :param pd: 输入网格
    :param f: 隐函数
    :return: vtkPolyData (隐函数等于0)
    """
    cut = vtk.vtkCutter()
    cut.SetCutFunction(f)
    cut.SetInputData(pdNormals(pd))
    cut.SetGenerateCutScalars(0)
    cut.Update()

    pd = cut.GetOutput()
    pd.GetPointData().DeepCopy(vtk.vtkPolyData().GetPointData())
    pd.GetCellData().DeepCopy(vtk.vtkPolyData().GetCellData())
    return pd


def pdAppend(pds) -> vtk.vtkPolyData:
    """拼接网格"""
    append = vtk.vtkAppendPolyData()
    for pd in pds:
        append.AddInputData(pd)
    append.Update()
    return append.GetOutput()


def pdClean(pd: vtk.vtkPolyData, point_merging=1) -> vtk.vtkPolyData:
    """清理网格"""
    clean = vtk.vtkCleanPolyData()
    clean.SetInputData(pd)
    clean.SetPointMerging(point_merging)
    clean.Update()
    return clean.GetOutput()


def pdBoolean_Union(pd0: vtk.vtkPolyData, pd1: vtk.vtkPolyData) -> vtk.vtkPolyData:
    """布尔并网格"""
    boolean = vtk.vtkLoopBooleanPolyDataFilter()
    boolean.SetOperationToUnion()
    boolean.SetInputData(0, pdNormals(pd0))
    boolean.SetInputData(1, pdNormals(pd1))
    boolean.Update()
    return boolean.GetOutput()


def pdBoolean_Intersection(pd0: vtk.vtkPolyData, pd1: vtk.vtkPolyData) -> vtk.vtkPolyData:
    """布尔交网格"""
    boolean = vtk.vtkLoopBooleanPolyDataFilter()
    boolean.SetOperationToIntersection()
    boolean.SetInputData(0, pdNormals(pd0))
    boolean.SetInputData(1, pdNormals(pd1))
    boolean.Update()
    return boolean.GetOutput()


def pdBoolean_Difference(pd0: vtk.vtkPolyData, pd1: vtk.vtkPolyData) -> vtk.vtkPolyData:
    """布尔减网格"""
    boolean = vtk.vtkLoopBooleanPolyDataFilter()
    boolean.SetOperationToDifference()
    boolean.SetInputData(0, pdNormals(pd0))
    boolean.SetInputData(1, pdNormals(pd1))
    boolean.Update()
    return boolean.GetOutput()


def pdRayDistance_Pt(pt: Union[np.ndarray, List[float]], vt: Union[np.ndarray, List[float]], target: vtk.vtkPolyData,
                     base_kd=None, base_obb=None) -> Optional[float]:
    """
    点pt沿方向vt投射到网格base的距离

    :param pt: 输入点
    :param vt: 投射方向
    :param target: 目标网格
    :param base_kd: 目标网格的vtkKdTreePointLocator
    :param base_obb: 目标网格的vtkOBBTree
    :return: 投射距离，无交点则返回None
    """
    pt = np.array([pt[i] for i in range(3)])
    vt = np.array([vt[i] for i in range(3)])
    vt /= np.linalg.norm(vt)

    bnd = target.GetBounds()
    d1 = np.array([bnd[1] - bnd[0], bnd[3] - bnd[2], bnd[5] - bnd[4]])
    d1 = np.linalg.norm(d1)

    if base_kd is None:
        base_kd = vtk.vtkKdTreePointLocator()
        base_kd.SetDataSet(target)
        base_kd.BuildLocator()

    cid = base_kd.FindClosestPoint(pt)

    cpt = np.array(target.GetPoint(cid))
    d2 = np.linalg.norm(pt - cpt)

    pt_last = pt + (d1 + d2) * vt

    if base_obb is None:
        base_obb = vtk.vtkOBBTree()
        base_obb.SetDataSet(target)
        base_obb.BuildLocator()

    pts = vtk.vtkPoints()
    base_obb.IntersectWithLine(pt, pt_last, pts, None)

    if pts.GetNumberOfPoints() > 0:
        return np.linalg.norm(pt - np.array(pts.GetPoint(0)))
    else:
        return None


def pdRayCast_Pd(pd: vtk.vtkPolyData, vt: Union[np.ndarray, List[float]], target: vtk.vtkPolyData,
                 max_dist: float) -> vtk.vtkPolyData:
    """
    网格pd中包含的所有点沿方向vt投射到网格base，保持pd单元关系不变

    :param pd: 输入网格
    :param vt: 投射方向
    :param target: 目标网格
    :param max_dist: 最大投射距离限制
    :return: 投射网格
    """
    vt = np.array([vt[i] for i in range(3)])
    vt /= np.linalg.norm(vt)

    base_kd = vtk.vtkKdTreePointLocator()
    base_kd.SetDataSet(target)
    base_kd.BuildLocator()

    base_obb = vtk.vtkOBBTree()
    base_obb.SetDataSet(target)
    base_obb.BuildLocator()

    out = vtk.vtkPolyData()
    out.DeepCopy(pd)

    for i in range(pd.GetNumberOfPoints()):
        pt = pd.GetPoint(i)
        d = pdRayDistance_Pt(pt, vt, target, base_kd, base_obb)

        if d is None or d > max_dist:
            d = max_dist

        pt = pt + d * vt
        out.GetPoints().SetPoint(i, pt)

    return out


def pdApproximate_Pd(pd: vtk.vtkPolyData, match_vt: Union[np.ndarray, List[float]],
                     target_poly: vtk.vtkPolyData, safe_radius: float = 1) -> vtk.vtkPolyData:
    """
    网格pd中包含的所有点沿方向vt一次近似到网格target，保持pd单元关系不变

    :param pd: 输入网格
    :param match_vt: 逼近方向
    :param target_poly: 目标网格
    :param safe_radius: 安全距离
    :return: 逼近网格
    """
    out = vtk.vtkPolyData()
    out.DeepCopy(pd)

    target_kd = vtk.vtkKdTreePointLocator()
    target_kd.SetDataSet(target_poly)
    target_kd.BuildLocator()

    target_obb = vtk.vtkOBBTree()
    target_obb.SetDataSet(target_poly)
    target_obb.BuildLocator()

    center = vmi.pdCenter(pd)

    for i in range(pd.GetNumberOfPoints()):
        pt = np.array(pd.GetPoint(i))
        vt_center = vmi.vtOnPlane(center - pt, match_vt)

        cs = vmi.CS4x4(axis0=vt_center, axis2=match_vt, origin=pt)
        cs.orthogonalize([1])
        cs.normalize()

        d = [pdRayDistance_Pt(p, match_vt, target_poly, target_kd, target_obb) for p in [
            cs.mpt([0, 0, 0]),
            cs.mpt([0, -safe_radius, 0]),
            cs.mpt([0, safe_radius, 0]),
            # cs.mpt([-safe_radius, 0, 0]),
            # cs.mpt([-safe_radius, -safe_radius, 0]),
            # cs.mpt([-safe_radius, safe_radius, 0]),
            cs.mpt([safe_radius, 0, 0]),
            cs.mpt([safe_radius, -safe_radius, 0]),
            cs.mpt([safe_radius, safe_radius, 0])]]
        d = [_ for _ in d if _ is not None]
        d = [_ for _ in d if _ < np.min(d) + 2 * safe_radius]
        d = np.mean(d) if len(d) else 0
        pt = pt + d * match_vt
        out.GetPoints().SetPoint(i, pt)
    return out


def pdOBB_Pts(pts: Union[List, vtk.vtkPolyData, vtk.vtkPoints]) -> Dict[str, Any]:
    """
    返回点列pts的OBB包围盒参数，点列分布的三个主轴方向和尺寸，以及分布中心

    :param pts: 输入点列
    :return: {'axis': 轴向量列表, 'size': 轴向尺寸, 'center': 中心, 'origin': 原点}
    """
    if isinstance(pts, vtk.vtkPolyData):
        pts = pts.GetPoints()
    elif not isinstance(pts, vtk.vtkPoints):
        points = vtk.vtkPoints()
        for pt in pts:
            points.InsertNextPoint([pt[0], pt[1], pt[2]])
        pts = points

    if pts.GetNumberOfPoints() > 0:
        args = {'origin': [0, 0, 0], 'axis': [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'size': [0, 0, 0]}
        vtk.vtkOBBTree().ComputeOBB(pts, args['origin'], args['axis'][0], args['axis'][1], args['axis'][2],
                                    args['size'])

        args['center'] = args['origin']
        for i in args:
            args[i] = np.array(args[i])

        for j in range(3):
            args['axis'][j] = args['axis'][j] / np.linalg.norm(args['axis'][j])
            args['center'] = [args['center'][i] + 0.5 * args['size'][j] * args['axis'][j][i] for i in range(3)]
        return args


def pdOffset_Normals(pd: vtk.vtkPolyData, d) -> vtk.vtkPolyData:
    """沿网格法向平移距离d"""
    pd = pdNormals(pd)
    pd_out = vtk.vtkPolyData()
    pd_out.DeepCopy(pd)

    normals = pd.GetPointData().GetNormals()
    for i in range(pd.GetNumberOfPoints()):
        n = [0, 0, 0]
        normals.GetTypedTuple(i, n)
        n = np.array(n)
        n /= np.linalg.norm(n)

        pt = np.array(pd.GetPoint(i)) + d * n
        pd_out.GetPoints().SetPoint(i, pt)
    return pd_out


def pdRuledSurface(pts0: Union[np.ndarray, List[float]], pts1: Union[np.ndarray, List[float]]) -> vtk.vtkPolyData:
    """由两个点列构造直纹面"""
    cells = vtk.vtkCellArray()
    points = vtk.vtkPoints()

    for i in range(len(pts0)):
        points.InsertNextPoint(pts0[i])
        points.InsertNextPoint(pts1[i])

        ids = vtk.vtkIdList()
        ids.InsertNextId(2 * i)
        ids.InsertNextId(2 * i + 1)
        ids.InsertNextId(2 * i + 2)
        cells.InsertNextCell(ids)

        ids = vtk.vtkIdList()
        ids.InsertNextId(2 * i + 3)
        ids.InsertNextId(2 * i + 2)
        ids.InsertNextId(2 * i + 1)
        cells.InsertNextCell(ids)

    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    pd.SetPolys(cells)
    return pd


def pdMatrix(pd: vtk.vtkPolyData, matrix: vtk.vtkMatrix4x4) -> vtk.vtkPolyData:
    """变换网格，变换矩阵matrix"""
    t = vtk.vtkTransform()
    t.SetMatrix(matrix)
    return pdTransform(pd, t)


def pdTransform(pd: vtk.vtkPolyData, transform: vtk.vtkTransform) -> vtk.vtkPolyData:
    """变换网格，变换transform"""
    tf = vtk.vtkTransformPolyDataFilter()
    tf.SetTransform(transform)
    tf.SetInputData(pd)
    tf.Update()
    return tf.GetOutput()
