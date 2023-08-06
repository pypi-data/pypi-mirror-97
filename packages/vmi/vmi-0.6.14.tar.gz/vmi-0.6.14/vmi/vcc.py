# from OCC.Core.AIS import *
# from OCC.Core.Adaptor2d import *
# from OCC.Core.Adaptor3d import *
import time

from OCC.Core.Addons import *
# from OCC.Core.AdvApp2Var import *
# from OCC.Core.AdvApprox import *
# from OCC.Core.AppBlend import *
# from OCC.Core.AppCont import *
# from OCC.Core.AppDef import *
# from OCC.Core.AppParCurves import *
# from OCC.Core.AppStd import *
# from OCC.Core.AppStdL import *
# from OCC.Core.Approx import *
# from OCC.Core.ApproxInt import *
# from OCC.Core.Aspect import *
# from OCC.Core.BOPAlgo import *
# from OCC.Core.BOPCol import *
# from OCC.Core.BOPDS import *
# from OCC.Core.BOPInt import *
# from OCC.Core.BOPTools import *
import pathlib
import tempfile
from typing import List, Optional, Union, Callable

import numpy as np
import vtk
from OCC.Core.BRep import *
from OCC.Core.BRepAdaptor import *
# from OCC.Core.BRepAlgo import *
from OCC.Core.BRepAlgoAPI import *
# from OCC.Core.BRepApprox import *
# from OCC.Core.BRepBlend import *
from OCC.Core.BRepBndLib import *
from OCC.Core.BRepBuilderAPI import *
# from OCC.Core.BRepCheck import *
# from OCC.Core.BRepClass import *
from OCC.Core.BRepClass3d import *
# from OCC.Core.BRepExtrema import *
# from OCC.Core.BRepFeat import *
# from OCC.Core.BRepFill import *
# from OCC.Core.BRepFilletAPI import *
from OCC.Core.BRepGProp import *
# from OCC.Core.BRepIntCurveSurface import *
# from OCC.Core.BRepLProp import *
# from OCC.Core.BRepLib import *
# from OCC.Core.BRepMAT2d import *
from OCC.Core.BRepMesh import *
# from OCC.Core.BRepOffset import *
from OCC.Core.BRepOffsetAPI import *
# from OCC.Core.BRepPrim import *
from OCC.Core.BRepPrimAPI import *
# from OCC.Core.BRepProj import *
from OCC.Core.BRepSweep import *
from OCC.Core.BRepTools import *
# from OCC.Core.BRepTopAdaptor import *
# from OCC.Core.BSplCLib import *
# from OCC.Core.BSplSLib import *
# from OCC.Core.BiTgte import *
# from OCC.Core.Bisector import *
# from OCC.Core.Blend import *
# from OCC.Core.BlendFunc import *
from OCC.Core.Bnd import *
# from OCC.Core.BndLib import *
# from OCC.Core.CDF import *
# from OCC.Core.CDM import *
# from OCC.Core.CPnts import *
# from OCC.Core.CSLib import *
# from OCC.Core.ChFi2d import *
# from OCC.Core.ChFi3d import *
# from OCC.Core.ChFiDS import *
# from OCC.Core.ChFiKPart import *
# from OCC.Core.Contap import *
# from OCC.Core.Convert import *
# from OCC.Core.Dico import *
# from OCC.Core.Draft import *
# from OCC.Core.DsgPrs import *
# from OCC.Core.Dynamic import *
# from OCC.Core.ElCLib import *
# from OCC.Core.ElSLib import *
# from OCC.Core.Expr import *
# from OCC.Core.ExprIntrp import *
# from OCC.Core.Extrema import *
# from OCC.Core.FEmTool import *
# from OCC.Core.FSD import *
# from OCC.Core.FairCurve import *
# from OCC.Core.FilletSurf import *
from OCC.Core.GC import *
# from OCC.Core.GCE2d import *
from OCC.Core.GCPnts import *
# from OCC.Core.GEOMAlgo import *
from OCC.Core.GProp import *
# from OCC.Core.GccAna import *
# from OCC.Core.GccEnt import *
# from OCC.Core.GccGeo import *
# from OCC.Core.GccInt import *
# from OCC.Core.GccIter import *
from OCC.Core.Geom import *
# from OCC.Core.Geom2d import *
# from OCC.Core.Geom2dAPI import *
# from OCC.Core.Geom2dAdaptor import *
# from OCC.Core.Geom2dConvert import *
# from OCC.Core.Geom2dGcc import *
# from OCC.Core.Geom2dHatch import *
# from OCC.Core.Geom2dInt import *
# from OCC.Core.Geom2dLProp import *
from OCC.Core.GeomAPI import *
# from OCC.Core.GeomAbs import *
# from OCC.Core.GeomAdaptor import *
# from OCC.Core.GeomConvert import *
# from OCC.Core.GeomFill import *
# from OCC.Core.GeomInt import *
# from OCC.Core.GeomLProp import *
# from OCC.Core.GeomLib import *
# from OCC.Core.GeomPlate import *
from OCC.Core.GeomProjLib import *
# from OCC.Core.GeomToStep import *
# from OCC.Core.GeomTools import *
# from OCC.Core.GraphDS import *
# from OCC.Core.GraphTools import *
# from OCC.Core.Graphic3d import *
# from OCC.Core.HLRAlgo import *
# from OCC.Core.HLRAppli import *
# from OCC.Core.HLRBRep import *
# from OCC.Core.HLRTopoBRep import *
# from OCC.Core.Hatch import *
# from OCC.Core.HatchGen import *
# from OCC.Core.Hermit import *
from OCC.Core.IFSelect import *
# from OCC.Core.IGESCAFControl import *
from OCC.Core.IGESControl import *
# from OCC.Core.Image import *
# from OCC.Core.IncludeLibrary import *
# from OCC.Core.IntAna import *
# from OCC.Core.IntAna2d import *
# from OCC.Core.IntCurve import *
# from OCC.Core.IntCurveSurface import *
# from OCC.Core.IntCurvesFace import *
# from OCC.Core.IntImp import *
# from OCC.Core.IntImpParGen import *
# from OCC.Core.IntPatch import *
# from OCC.Core.IntPoly import *
# from OCC.Core.IntPolyh import *
# from OCC.Core.IntRes2d import *
# from OCC.Core.IntStart import *
# from OCC.Core.IntSurf import *
# from OCC.Core.IntTools import *
# from OCC.Core.IntWalk import *
# from OCC.Core.Interface import *
# from OCC.Core.InterfaceGraphic import *
# from OCC.Core.Intf import *
# from OCC.Core.Intrv import *
# from OCC.Core.LProp import *
# from OCC.Core.LProp3d import *
# from OCC.Core.Law import *
# from OCC.Core.LocOpe import *
# from OCC.Core.LocalAnalysis import *
# from OCC.Core.MAT import *
# from OCC.Core.MAT2d import *
# from OCC.Core.MMgt import *
# from OCC.Core.Materials import *
# from OCC.Core.MeshVS import *
# from OCC.Core.Message import *
# from OCC.Core.NCollection import *
# from OCC.Core.NIS import *
# from OCC.Core.NLPlate import *
# from OCC.Core.OSD import *
# from OCC.Core.PCDM import *
# from OCC.Core.PLib import *
# from OCC.Core.Plate import *
# from OCC.Core.Plugin import *
from OCC.Core.Poly import *
from OCC.Core.Precision import *
# from OCC.Core.Primitives import *
# from OCC.Core.ProjLib import *
# from OCC.Core.Prs3d import *
# from OCC.Core.PrsMgr import *
# from OCC.Core.Quantity import *
# from OCC.Core.RWStepAP203 import *
# from OCC.Core.RWStepAP214 import *
# from OCC.Core.RWStepBasic import *
# from OCC.Core.RWStepDimTol import *
# from OCC.Core.RWStepElement import *
# from OCC.Core.RWStepFEA import *
# from OCC.Core.RWStepGeom import *
# from OCC.Core.RWStepRepr import *
# from OCC.Core.RWStepShape import *
# from OCC.Core.RWStepVisual import *
# from OCC.Core.RWStl import *
# from OCC.Core.Resource import *
# from OCC.Core.STEPCAFControl import *
# from OCC.Core.STEPConstruct import *
from OCC.Core.STEPControl import *
# from OCC.Core.STEPEdit import *
# from OCC.Core.STEPSelections import *
# from OCC.Core.Select3D import *
# from OCC.Core.SelectBasics import *
# from OCC.Core.SelectMgr import *
# from OCC.Core.ShapeAlgo import *
# from OCC.Core.ShapeAnalysis import *
# from OCC.Core.ShapeBuild import *
# from OCC.Core.ShapeConstruct import *
# from OCC.Core.ShapeCustom import *
# from OCC.Core.ShapeExtend import *
# from OCC.Core.ShapeFix import *
# from OCC.Core.ShapeProcess import *
# from OCC.Core.ShapeProcessAPI import *
# from OCC.Core.ShapeUpgrade import *
# from OCC.Core.SortTools import *
# from OCC.Core.Standard import *
# from OCC.Core.StdFail import *
# from OCC.Core.StdPrs import *
# from OCC.Core.StdSelect import *
# from OCC.Core.StepAP203 import *
# from OCC.Core.StepAP209 import *
# from OCC.Core.StepAP214 import *
# from OCC.Core.StepBasic import *
# from OCC.Core.StepDimTol import *
# from OCC.Core.StepElement import *
# from OCC.Core.StepFEA import *
# from OCC.Core.StepGeom import *
# from OCC.Core.StepRepr import *
# from OCC.Core.StepShape import *
# from OCC.Core.StepToGeom import *
# from OCC.Core.StepToTopoDS import *
# from OCC.Core.StepVisual import *
from OCC.Core.StlAPI import *
# from OCC.Core.StlTransfer import *
# from OCC.Core.Storage import *
# from OCC.Core.Sweep import *
# from OCC.Core.TColGeom import *
# from OCC.Core.TColGeom2d import *
# from OCC.Core.TColQuantity import *
from OCC.Core.TColStd import *
from OCC.Core.TColgp import *
# from OCC.Core.TCollection import *
# from OCC.Core.TDF import *
# from OCC.Core.TDataStd import *
# from OCC.Core.TDataXtd import *
# from OCC.Core.TDocStd import *
# from OCC.Core.TFunction import *
# from OCC.Core.TNaming import *
# from OCC.Core.TPrsStd import *
# from OCC.Core.TShort import *
from OCC.Core.TopAbs import *
# from OCC.Core.TopBas import *
# from OCC.Core.TopClass import *
# from OCC.Core.TopCnx import *
from OCC.Core.TopExp import *
from OCC.Core.TopLoc import *
# from OCC.Core.TopOpeBRep import *
# from OCC.Core.TopOpeBRepBuild import *
# from OCC.Core.TopOpeBRepDS import *
# from OCC.Core.TopOpeBRepTool import *
from OCC.Core.TopTools import *
# from OCC.Core.TopTrans import *
from OCC.Core.TopoDS import *
# from OCC.Core.TopoDSToStep import *
# from OCC.Core.Transfer import *
# from OCC.Core.TransferBRep import *
# from OCC.Core.UTL import *
# from OCC.Core.Units import *
# from OCC.Core.UnitsAPI import *
# from OCC.Core.V3d import *
# from OCC.Core.Visual3d import *
# from OCC.Core.Visualization import *
# from OCC.Core.Voxel import *
# from OCC.Core.XBRepMesh import *
# from OCC.Core.XCAFApp import *
# from OCC.Core.XCAFDoc import *
# from OCC.Core.XCAFPrs import *
# from OCC.Core.XSControl import *
# from OCC.Core.gce import *
from OCC.Core.gp import *
from PySide2.QtCore import *

import vmi
from numba import jit

# from OCC.Core.math import *


register_font('C:/Windows/Fonts/msyh.ttc')
register_font('C:/Windows/Fonts/simfang.ttf')
register_font('C:/Windows/Fonts/Deng.ttf')
register_font('C:/Windows/Fonts/Dengb.ttf')
register_font('C:/Windows/Fonts/Dengl.ttf')

ccType = [TopAbs_COMPOUND,
          TopAbs_COMPSOLID,
          TopAbs_SOLID,
          TopAbs_SHELL,
          TopAbs_FACE,
          TopAbs_WIRE,
          TopAbs_EDGE,
          TopAbs_VERTEX,
          TopAbs_SHAPE]

ccTypeCast = {TopAbs_COMPOUND: topods.Compound,
              TopAbs_COMPSOLID: topods.CompSolid,
              TopAbs_SOLID: topods.Solid,
              TopAbs_SHELL: topods.Shell,
              TopAbs_FACE: topods.Face,
              TopAbs_WIRE: topods.Wire,
              TopAbs_EDGE: topods.Edge,
              TopAbs_VERTEX: topods.Vertex}


def ccExplore_Recursive(sh: TopoDS_Shape, target_type: int = ccType[-1]) -> List[TopoDS_Shape]:
    """返回sh的所有下级形状，筛选目标类型target_type =

    TopAbs_COMPOUND /
    TopAbs_COMPSOLID /
    TopAbs_SOLID /
    TopAbs_SHELL /
    TopAbs_FACE /
    TopAbs_WIRE /
    TopAbs_EDGE /
    TopAbs_VERTEX /
    TopAbs_SHAPE"""
    shs, exp = [], TopExp_Explorer(sh, target_type)
    while exp.More():
        shs.append(exp.Current())
        exp.Next()
    return shs


def ccExplore_Once(sh: TopoDS_Shape) -> List[TopoDS_Shape]:
    """返回sh的直接下级形状"""
    shs, it = [], TopoDS_Iterator(sh)
    while it.More():
        shs.append(it.Value())
        it.Next()
    return shs


def ccOpenFile_IGES(file: str = None) -> Optional[TopoDS_Shape]:
    """打开IGES文件，返回形状"""
    if file is None:
        file = vmi.askOpenFile('*.igs', '导入 (Import) IGES')
        if file is None:
            return
    r = IGESControl_Reader()
    if r.ReadFile(file):
        r.TransferRoots()
        sh: TopoDS_Shape = r.OneShape()
        sh_sub = ccExplore_Once(sh)
        if sh.ShapeType() is TopAbs_COMPOUND and len(sh_sub) == 1:
            sh = sh_sub[0]
        return sh


def ccOpenFile_STEP(file: str = None) -> Optional[TopoDS_Shape]:
    """打开STEP文件，返回形状"""
    if file is None:
        file = vmi.askOpenFile('*.stp', '导入 (Import) STEP')
        if file is None:
            return
    r = STEPControl_Reader()
    if IFSelect_RetDone == r.ReadFile(file):
        r.TransferRoots()
        sh: TopoDS_Shape = r.OneShape()
        sh_sub = ccExplore_Once(sh)
        if sh.ShapeType() is TopAbs_COMPOUND and len(sh_sub) == 1:
            sh = sh_sub[0]
        return sh


def ccSaveFile_IGES(sh: TopoDS_Shape, file=None) -> bool:
    """保存形状sh为IGES文件，返回写入是否成功"""
    if file is None:
        file = vmi.askSaveFile('*.igs', '导出 (Export) IGES')
        if file is None:
            return False
    w = IGESControl_Writer()
    w.AddShape(sh)
    return w.Write(file)


def ccSaveFile_STEP(sh: TopoDS_Shape, file=None) -> bool:
    """保存形状sh为STEP文件，返回写入是否成功"""
    if file is None:
        file = vmi.askSaveFile('*.stp', '导出 (Export) STEP')
        if file is None:
            return False
    w = STEPControl_Writer()

    w.Transfer(sh, STEPControl_AsIs)
    status = w.Write(file)
    if status == IFSelect_RetDone:
        # f = pathlib.Path(file).read_bytes()
        # i = f.find((str(time.localtime().tm_mday) + 'T' + str(time.localtime().tm_hour)).encode())
        # f = f.replace(f[i - 8: i + 11], b'')
        # pathlib.Path(file).write_bytes(f)
        return True
    return False


def ccPd_Sh(sh: TopoDS_Shape) -> vtk.vtkPolyData:
    """转换形状sh为网格，离散化不可逆"""
    if sh.IsNull():
        return vtk.vtkPolyData()

    pts = vtk.vtkPoints()
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(pts)
    polydata.Allocate()

    # 1. 离散化
    breptools.Clean(sh)

    discrete = BRepMesh_IncrementalMesh(sh, 1e-3, True, 0.5, True)
    discrete.Perform()

    # 2. 转换Vertex
    exp = TopExp_Explorer(sh, TopAbs_VERTEX)
    while exp.More():
        vertex = topods.Vertex(exp.Current())
        exp.Next()

        pnt = BRep_Tool.Pnt(vertex)
        id = polydata.GetPoints().InsertNextPoint(pnt.X(), pnt.Y(), pnt.Z())
        polydata.InsertNextCell(vtk.VTK_VERTEX, 1, [id])

    # 3. 转换Edge
    exp = TopExp_Explorer(sh, TopAbs_EDGE)
    while exp.More():
        edge = topods.Edge(exp.Current())
        exp.Next()

        if edge.IsNull() or BRep_Tool.Degenerated(edge):
            continue

        p_on_tri = Handle_Poly_PolygonOnTriangulation()
        triangulation = Handle_Poly_Triangulation()
        loc = TopLoc_Location()
        BRep_Tool.PolygonOnTriangulation(edge, p_on_tri, triangulation, loc, 1)
        p_3d = Handle_Poly_Polygon3D()

        if p_on_tri.IsNull():
            p_3d = BRep_Tool.Polygon3D(BRep_Tool(), edge, loc)
            p_3d = Handle_Poly_Polygon3D() if p_3d is None else p_3d

        if p_3d.IsNull() and p_on_tri.IsNull():
            continue

        trsf = loc.Transformation()

        if not p_3d.IsNull():
            n = p_3d.NbNodes()
            pnts = p_3d.Nodes()
            ids = list(range(1, n + 1))
        else:
            n = p_on_tri.NbNodes()
            pnts = triangulation.Nodes()
            ids = p_on_tri.Nodes()
            ids = [ids.Value(i) for i in range(ids.Lower(), ids.Upper() + 1)]

        if n > 1:
            idList = vtk.vtkIdList()
            for i in ids:
                pnt = pnts.Value(i)
                pnt.Transform(trsf)
                id = polydata.GetPoints().InsertNextPoint(pnt.X(), pnt.Y(), pnt.Z())
                idList.InsertNextId(id)
            polydata.InsertNextCell(vtk.VTK_POLY_LINE, idList)

    # 4. 转换Face并合并
    exp = TopExp_Explorer(sh, TopAbs_FACE)
    if exp.More():
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.stl'
            stlapi.Write(sh, str(p), False)

            r = vtk.vtkSTLReader()
            r.SetFileName(str(p))
            r.Update()

            a = vtk.vtkAppendPolyData()
            a.AddInputData(r.GetOutput())
            a.AddInputData(polydata)
            a.Update()

            c = vtk.vtkCleanPolyData()
            c.SetInputData(a.GetOutput())
            c.Update()

            polydata.DeepCopy(a.GetOutput())

    return polydata


def ccSh_Pd(pd: vtk.vtkPolyData) -> TopoDS_Shape:
    """转换网格pd为形状，点单元转换为TopoDS_Vertex，线单元转换为TopoDS_Line，多边形单元转换为TopoDS_Face"""
    builder, compound = BRep_Builder(), TopoDS_Compound()
    builder.MakeCompound(compound)

    triangles = vtk.vtkTriangleFilter()
    triangles.SetInputData(pd)
    triangles.Update()
    triangles = triangles.GetOutput()

    for i in range(triangles.GetNumberOfCells()):
        cell: vtk.vtkCell = triangles.GetCell(i)
        if cell.GetCellType() == vtk.VTK_TRIANGLE:
            ids: vtk.vtkIdList = cell.GetPointIds()
            pts = [triangles.GetPoint(ids.GetId(0)),
                   triangles.GetPoint(ids.GetId(1)),
                   triangles.GetPoint(ids.GetId(2))]
            face = ccFace(ccWire(ccSegments(pts, True)))
            builder.Add(compound, face)

    sewing = BRepBuilderAPI_Sewing()
    sewing.Load(compound)
    sewing.Perform()

    sh = sewing.SewedShape()

    if sh.ShapeType() is TopAbs_SHELL and sh.Closed():
        return ccSolid(sh)
    else:
        return sh


def ccPnt(arg: Union[np.ndarray, List[float]]) -> gp_Pnt:
    """构造几何点"""
    return gp_Pnt(arg[0], arg[1], arg[2])


def ccVec(arg: Union[np.ndarray, List[float]]) -> gp_Vec:
    """构造几何向量"""
    return gp_Vec(arg[0], arg[1], arg[2])


def ccDir(arg: Union[np.ndarray, List[float]]) -> gp_Dir:
    """构造几何方向"""
    return gp_Dir(arg[0], arg[1], arg[2])


def ccAx2(origin: Union[np.ndarray, List[float]], z: Union[np.ndarray, List[float]],
          x: Union[np.ndarray, List[float]] = None) -> gp_Ax2:
    """
    构造几何坐标系

    :param origin: 原点
    :param z: Z轴向量
    :param x: X轴向量
    :return: 几何坐标系
    """
    args = [ccPnt(origin), ccDir(z)]
    if x is not None:
        args.append(ccDir(x))
    return gp_Ax2(*args)


def ccSegment(pt0: Union[np.ndarray, List[float]], pt1: Union[np.ndarray, List[float]]) -> Geom_TrimmedCurve:
    """
    构造线段

    :param pt0: 起点
    :param pt1: 终点
    :return: 线段
    """
    pt0 = pt0 if isinstance(pt0, gp_Pnt) else ccPnt(pt0)
    pt1 = pt1 if isinstance(pt1, gp_Pnt) else ccPnt(pt1)
    return GC_MakeSegment(pt0, pt1).Value()


def ccSegments(pts: List[Union[np.ndarray, List[float]]], closed: bool = False) -> List[Geom_TrimmedCurve]:
    """
    构造线段列表

    :param pts: 点列
    :param closed: 是否闭合
    :return: 线段列表
    """
    pnts_ = [pnt for pnt in pts]
    if closed:
        pnts_.append(pts[0])
    return [ccSegment(pnts_[i], pnts_[i + 1]) for i in range(len(pnts_) - 1)]


def ccBSpline(pts: List[Union[np.ndarray, List[float]]], tgs: List[Union[np.ndarray, List[float]]] = None,
              tgflags: List[bool] = None, closed: bool = False, scale: bool = True,
              tol: float = precision.Confusion()) -> Optional[Geom_BSplineCurve]:
    """
    构造B样条

    :param pts: 插值点列
    :param tgs: 切向量列表
    :param tgflags: 切向量有效状态列表
    :param closed: 是否闭合
    :param scale: 是否自动调节尺度
    :param tol: 误差限
    :return: B样条
    """
    if len(pts) < 2:
        return None

    if pts is not None and not isinstance(pts, TColgp_HArray1OfPnt):
        _ = TColgp_HArray1OfPnt(1, len(pts))
        for i in range(len(pts)):
            if isinstance(pts[i], gp_Pnt):
                _.SetValue(i + 1, pts[i])
            else:
                _.SetValue(i + 1, ccPnt(pts[i]))
        pts = _

    if tgs is not None and not isinstance(tgs, TColgp_Array1OfVec):
        _ = TColgp_Array1OfVec(1, len(tgs))
        for i in range(len(tgs)):
            if isinstance(pts[i], gp_Vec):
                _.SetValue(i + 1, tgs[i])
            else:
                _.SetValue(i + 1, ccVec(tgs[i]))
        tgs = _

    if tgs is not None and tgflags is None:
        tgflags = [True for _ in tgs]

    if tgflags is not None and not isinstance(tgflags, TColStd_HArray1OfBoolean):
        _ = TColStd_HArray1OfBoolean(1, len(tgflags))
        for i in range(len(tgflags)):
            _.SetValue(i + 1, tgflags[i])
        tgflags = _

    lower, upper = pts.Lower(), pts.Upper() + (1 if closed else 0)
    knots = TColStd_HArray1OfReal(lower, upper)
    knots.SetValue(lower, 0)

    for i in range(lower, upper):
        if closed and i == upper - 1:
            var = pts.Value(i).Distance(pts.Value(lower)) ** 0.5
        else:
            var = pts.Value(i).Distance(pts.Value(i + 1)) ** 0.5
        knots.SetValue(i + 1, knots.Value(i) + var)

    curve = GeomAPI_Interpolate(pts, knots, closed, tol)
    if tgs is not None:
        curve.Load(tgs, tgflags, scale)
    curve.Perform()
    return curve.Curve() if curve.IsDone() else None


def ccBSpline_Kochanek(pts: List[Union[np.ndarray, List[float]]], closed: bool = False,
                       tol: float = precision.Confusion()) -> Optional[Geom_BSplineCurve]:
    """
    构造K样条，转换为B样条返回

    :param pts: 插值点列
    :param closed: 闭合
    :param tol: 容差
    :return:
    """
    if len(pts) < 2:
        return None

    points = vtk.vtkPoints()
    for pt in pts:
        points.InsertNextPoint(pt)

    ks = [vtk.vtkKochanekSpline(), vtk.vtkKochanekSpline(), vtk.vtkKochanekSpline()]

    ps = vtk.vtkParametricSpline()
    ps.SetXSpline(ks[0])
    ps.SetYSpline(ks[1])
    ps.SetZSpline(ks[2])
    ps.SetPoints(points)
    ps.SetClosed(1 if closed else 0)
    ps.SetParameterizeByLength(1)
    ps.SetLeftConstraint(1)
    ps.SetRightConstraint(1)

    n = 100 * len(pts)

    pf = vtk.vtkParametricFunctionSource()
    pf.SetParametricFunction(ps)
    pf.SetUResolution(n)
    pf.SetVResolution(n)
    pf.SetWResolution(n)
    pf.Update()

    pts_, points = [], pf.GetOutput().GetPoints()

    for i in range(points.GetNumberOfPoints() - (1 if closed else 0)):
        pts_.append(points.GetPoint(i))
    pts_[0] = pts[0].copy()
    if not closed:
        pts_[-1] = pts[-1].copy()

    curve = ccBSpline(pts_, closed=closed, tol=tol)

    obb = vmi.pdOBB_Pts(points)
    if 0 < obb['size'][2] < tol:
        curve = ccCurveOnPlane(curve, obb['center'], obb['axis'][2])
    return curve


def ccCurveOnPlane(curve: Handle_Geom_Curve,
                   origin: Union[np.ndarray, List[float]], normal: Union[np.ndarray, List[float]],
                   vt: Union[np.ndarray, List[float]] = None) -> Handle_Geom_Curve:
    """
    曲线沿vt方向投影到过一点origin法向为normal的平面

    :param curve: 输入曲线
    :param origin: 投影面过一点
    :param normal: 投影面法向
    :param vt: 投影方向，默认为投影面法向
    :return: 投影曲线
    """
    if vt is None:
        vt = normal
    return geomprojlib.ProjectOnPlane(curve, ccPlane(origin, normal), ccDir(vt), True)


def ccCircle(radius: float,
             origin: Union[np.ndarray, List[float]],
             z: Union[np.ndarray, List[float]],
             x: Union[np.ndarray, List[float]] = None) -> Optional[Handle_Geom_Curve]:
    """
    构造圆形，指定半径和圆心坐标系

    :param radius: 圆半径
    :param origin: 圆心
    :param z: 圆法向
    :param x: 圆面内主方向
    :return: 圆形
    """
    origin = [origin[0], origin[1], origin[2]]
    z = [z[0], z[1], z[2]]
    if x is not None:
        x = [x[0], x[1], x[2]]
    mk = GC_MakeCircle(ccAx2(origin, z, x), radius)
    return mk.Value() if mk.IsDone() else None


def ccRect_Origin(origin: Union[np.ndarray, List[float]],
                  x: Union[np.ndarray, List[float]],
                  y: Union[np.ndarray, List[float]],
                  xl: float, yl: float) -> List[Geom_Curve]:
    """
    构造平行四边形，指定原点和两边方向和长度

    :param origin: 原点
    :param x: x边方向
    :param y: y边方向
    :param xl: x边长度
    :param yl: y边长度
    :return: 平行四边形
    """
    origin, x, y = np.array(origin), np.array(x), np.array(y)
    pts = [origin,
           origin + xl * x,
           origin + xl * x, + yl * y,
           origin + yl * y]
    return ccWire(ccSegments(pts, True))


def ccRect_Center(center: Union[np.ndarray, List[float]],
                  x: Union[np.ndarray, List[float]],
                  y: Union[np.ndarray, List[float]],
                  xl: float, yl: float) -> List[Geom_Curve]:
    """
    构造平行四边形，指定中心和两边方向和长度

    :param center: 中心
    :param x: x边方向
    :param y: y边方向
    :param xl: x边长度
    :param yl: y边长度
    :return: 平行四边形
    """
    center, x, y = np.array(center), np.array(x), np.array(y)
    pts = [center - 0.5 * xl * x - 0.5 * yl * y,
           center + 0.5 * xl * x - 0.5 * yl * y,
           center + 0.5 * xl * x + 0.5 * yl * y,
           center - 0.5 * xl * x + 0.5 * yl * y]
    return ccWire(ccSegments(pts, True))


def ccPolyline_Regular(radius: float,
                       center: Union[np.ndarray, List[float]],
                       z: Union[np.ndarray, List[float]],
                       x: Union[np.ndarray, List[float]],
                       side_num=120) -> List[Geom_Curve]:
    """
    构造正多边形，指定半径和中心坐标系

    :param radius: 半径，中心到边缘节点的距离
    :param center: 中心
    :param z: 法向
    :param x: 面内主方向
    :param side_num: 边数
    :return: 正多边形
    """
    pts, cs = [], vmi.CS4x4(axis0=x, axis2=z, origin=center)
    cs.orthogonalize([1, 0])
    cs.normalize()

    for i in range(side_num):
        cs = cs.rotate(360 / side_num, cs.axis(2))
        pt = cs.mpt([radius, 0, 0])
        pts.append(pt)
    return ccSegments(pts, True)


def ccPlane(origin: Union[np.ndarray, List[float]],
            normal: Union[np.ndarray, List[float]]) -> Optional[Handle_Geom_Plane]:
    """
    构造平面

    :param origin: 过一点
    :param normal: 法向
    :return: 平面
    """
    mk = GC_MakePlane(ccPnt(origin), ccDir(normal))
    return mk.Value() if mk.IsDone() else None


def ccVertex(pt: Union[np.ndarray, List[float]]) -> Optional[TopoDS_Vertex]:
    """
    构造顶点拓扑

    :param pt: 点坐标
    :return: 顶点
    """
    pt = pt if isinstance(pt, gp_Pnt) else ccPnt(pt)
    mk = BRepBuilderAPI_MakeVertex(pt)
    mk.Build()
    return mk.Vertex() if mk.IsDone() else None


def ccEdge(curve: Handle_Geom_Curve) -> Optional[TopoDS_Edge]:
    """
    构造边拓扑

    :param curve: 曲线
    :return: 边
    """
    mk = BRepBuilderAPI_MakeEdge(curve)
    mk.Build()
    return mk.Edge() if mk.IsDone() else None


def ccEdges(curves: List[Handle_Geom_Curve]) -> List[TopoDS_Edge]:
    """
    构造边拓扑列表

    :param curves: 曲线列表
    :return: 边列表
    """
    return [ccEdge(curve) for curve in curves]


def ccWire(edges: Union[TopoDS_Edge, Handle_Geom_Curve,
                        List[Union[TopoDS_Edge, Handle_Geom_Curve]]]) -> Optional[TopoDS_Wire]:
    """
    构造线

    :param edges: 边列表
    :return: 线
    """
    edges_ = edges
    if not hasattr(edges_, '__iter__'):
        edges_ = [edges_]
    edges_ = [edge if isinstance(edge, TopoDS_Edge) else ccEdge(edge) for edge in edges_]
    mk = BRepBuilderAPI_MakeWire()
    for edge in edges_:
        mk.Add(edge)
    mk.Build()
    return mk.Wire() if mk.IsDone() else None


def ccWires(edges: List[TopoDS_Edge]) -> List[TopoDS_Wire]:
    """
    构造线列表

    :param edges: 边列表
    :return: 线列表
    """
    return [ccWire(edge) for edge in edges]


def ccFace(wire: TopoDS_Wire) -> Optional[TopoDS_Face]:
    """
    构造面

    :param wire: 线，应是闭合的
    :return: 面
    """
    mk = BRepBuilderAPI_MakeFace(wire)
    mk.Build()
    return mk.Face() if mk.IsDone() else None


def ccFace_OnPlane(wire: TopoDS_Wire,
                   origin: Union[np.ndarray, List[float]],
                   normal: Union[np.ndarray, List[float]]) -> Optional[TopoDS_Face]:
    """
    构造面，约束投影到平面

    :param wire: 线
    :param origin: 平面过一点
    :param normal: 平面法向
    :return: 面
    """
    mk = BRepBuilderAPI_MakeFace(gp_Pln(ccPnt(origin), ccDir(normal)), wire)
    mk.Build()
    return mk.Face() if mk.IsDone() else None


def ccLoft(sections: List[TopoDS_Wire],
           ruled=False, redirect=False, solid=False) -> Union[TopoDS_Shell, TopoDS_Solid, None]:
    """
    构造放样面，指定截面轮廓

    :param sections: 截面轮廓列表
    :param ruled: 直纹面，相邻界面轮廓之间是否以直线段连接
    :param redirect: 重定向，相邻界面轮廓之间的连接是否需要根据位置姿态重新计算对应关系
    :param solid: 实体化，是否将首末截面轮廓视为封闭面构造实体
    :return: 壳或实体
    """
    mk = BRepOffsetAPI_ThruSections(solid, ruled)
    mk.CheckCompatibility(redirect)
    for section in sections:
        if isinstance(section, TopoDS_Edge):
            section = ccWire(section)
        if isinstance(section, TopoDS_Wire):
            mk.AddWire(section)
        if isinstance(section, TopoDS_Vertex):
            mk.AddVertex(section)
    mk.Build()
    return mk.Shape() if mk.IsDone() else None


def ccSew(shs: List[TopoDS_Shape]) -> TopoDS_Shell:
    """
    构造缝合体，指定相互连接的面或壳

    :param shs: 缝合形状列表
    :return: 缝合体
    """
    mk = BRepBuilderAPI_Sewing()
    for sh in shs:
        mk.Add(sh)
    mk.Perform()
    return mk.SewedShape()


def ccSolid(shells: Union[TopoDS_Shell, List[TopoDS_Shell]]) -> Optional[TopoDS_Solid]:
    """
    构造实体，指定相互连接的壳表示封闭空间

    :param shells: 壳列表
    :return: 实体
    """
    if isinstance(shells, TopoDS_Shell):
        shells = [shells]
    mk = BRepBuilderAPI_MakeSolid()
    for shell in shells:
        if shell.ShapeType() is TopAbs_SHELL:
            mk.Add(topods.Shell(shell))
    if mk.IsDone():
        s = mk.Solid()

        if ccInside_Pt(s):
            s.Reverse()
        return s


def ccBoolean_Union(sh: List[TopoDS_Shape]) -> Optional[TopoDS_Shape]:
    """布尔并，列表中所有形状并集，至少2个形状"""
    if len(sh) == 0:
        return None
    elif len(sh) == 1:
        return sh[0]
    elif len(sh) > 1:
        sh = [sh[:1], sh[1:]]
        shape_list = [TopTools_ListOfShape(), TopTools_ListOfShape()]

        for j in range(2):
            for i in sh[j]:
                shape_list[j].Append(i)

        mk = BRepAlgoAPI_Fuse()
        mk.SetArguments(shape_list[0])
        mk.SetTools(shape_list[1])
        mk.SetRunParallel(True)
        mk.Build()

        if not mk.IsDone() or mk.ErrorStatus() or mk.WarningStatus():
            raise Exception('ccBoolean_Union', mk.ErrorStatus(), mk.WarningStatus())
        return mk.Shape()


def ccBoolean_Difference(sh: List[TopoDS_Shape]) -> Optional[TopoDS_Shape]:
    """布尔差，列表中第一个形状减掉其它所有形状"""
    if len(sh) == 0:
        return None
    elif len(sh) == 1:
        return sh[0]
    elif len(sh) > 1:
        sh = [sh[:1], sh[1:]]
        shape_list = [TopTools_ListOfShape(), TopTools_ListOfShape()]

        for j in range(2):
            for i in sh[j]:
                shape_list[j].Append(i)

        mk = BRepAlgoAPI_Cut()
        mk.SetArguments(shape_list[0])
        mk.SetTools(shape_list[1])
        mk.SetRunParallel(True)
        mk.Build()

        if not mk.IsDone() or mk.ErrorStatus() or mk.WarningStatus():
            raise Exception('ccBoolean_Difference', mk.ErrorStatus(), mk.WarningStatus())
        return mk.Shape()


def ccBoolean_Intersection(sh: List[TopoDS_Shape]) -> Optional[TopoDS_Shape]:
    """布尔交，列表中所有形状交集，至少2个形状"""
    if len(sh) == 0:
        return None
    elif len(sh) == 1:
        return sh[0]
    elif len(sh) > 1:
        sh = [sh[:1], sh[1:]]
        shape_list = [TopTools_ListOfShape(), TopTools_ListOfShape()]

        for j in range(2):
            for i in sh[j]:
                shape_list[j].Append(i)

        mk = BRepAlgoAPI_Common()
        mk.SetArguments(shape_list[0])
        mk.SetTools(shape_list[1])
        mk.SetRunParallel(True)
        mk.Build()

        if not mk.IsDone() or mk.ErrorStatus() or mk.WarningStatus():
            raise Exception('ccBoolean_Intersection', mk.ErrorStatus(), mk.WarningStatus())
        return mk.Shape()


def ccSection(sh: List[TopoDS_Shape]) -> Optional[TopoDS_Shape]:
    """布尔割，高维度形状与低维度形状的交集"""
    if len(sh) == 0:
        return None
    elif len(sh) == 1:
        return sh[0]
    elif len(sh) > 1:
        sh = [sh[:1], sh[1:]]
        shape_list = [TopTools_ListOfShape(), TopTools_ListOfShape()]

        for j in range(2):
            for i in sh[j]:
                shape_list[j].Append(i)

        mk = BRepAlgoAPI_Section()
        mk.SetArguments(shape_list[0])
        mk.SetTools(shape_list[1])
        mk.SetRunParallel(True)
        mk.Build()

        if not mk.IsDone() or mk.ErrorStatus() or mk.WarningStatus():
            raise Exception('ccSection', mk.ErrorStatus(), mk.WarningStatus())
        return mk.Shape()


def ccCylinder(radius: float,
               height: float,
               center: Union[np.ndarray, List[float]],
               z: Union[np.ndarray, List[float]],
               x: Union[np.ndarray, List[float]] = None) -> Optional[TopoDS_Shape]:
    """
    构造圆柱，指定半径、高度和底面中心坐标系

    :param radius: 半径
    :param height: 高度
    :param center: 底面中心
    :param z: 底面法向
    :param x: 底面主方向
    :return: 圆柱
    """
    center = [center[0], center[1], center[2]]
    z = [z[0], z[1], z[2]]
    if x is not None:
        x = [x[0], x[1], x[2]]
    mk = BRepPrimAPI_MakeCylinder(ccAx2(center, z, x), radius, height)
    mk.Build()
    return mk.Shape() if mk.IsDone() else None


def ccSphere(radius: float,
             center: Union[np.ndarray, List[float]],
             z: Union[np.ndarray, List[float]],
             x: Union[np.ndarray, List[float]] = None) -> Optional[TopoDS_Shape]:
    """
    构造球，指定半径和球心坐标系

    :param radius: 半径
    :param center: 球心
    :param z: 球主方向
    :param x: 球次方向
    :return: 球
    """
    center = [center[0], center[1], center[2]]
    z = [z[0], z[1], z[2]]
    if x is not None:
        x = [x[0], x[1], x[2]]
    mk = BRepPrimAPI_MakeSphere(ccAx2(center, z, x), radius)
    mk.Build()
    return mk.Shape() if mk.IsDone() else None


def ccSphere_Half(radius: float,
                  center: Union[np.ndarray, List[float]],
                  z: Union[np.ndarray, List[float]],
                  x: Union[np.ndarray, List[float]] = None) -> Optional[TopoDS_Shape]:
    """
    构造半球，指定半径和球心坐标系

    :param radius: 半径
    :param center: 球心
    :param z: 球主方向
    :param x: 球次方向
    :return: 球
    """
    center = [center[0], center[1], center[2]]
    z = [z[0], z[1], z[2]]
    if x is not None:
        x = [x[0], x[1], x[2]]
    mk = BRepPrimAPI_MakeSphere(ccAx2(center, z, x), radius, np.pi)
    mk.Build()
    return mk.Shape() if mk.IsDone() else None


def ccPrism(sh: TopoDS_Shape, vt: Union[np.ndarray, List[float]], length: float) -> Optional[TopoDS_Shape]:
    """
    构造拉伸体，指定基础形状和拉伸方向、长度

    :param sh: 基础形状
    :param vt: 拉伸方向
    :param length: 拉伸长度
    :return: 拉伸体
    """
    vt = np.array(vt)
    vec = length * vt / np.linalg.norm(vt)
    vec = gp_Vec(vec[0], vec[1], vec[2])
    mk = BRepPrimAPI_MakePrism(sh, vec)
    mk.Build()
    return mk.Shape() if mk.IsDone() else None


def ccRevolve(sh: TopoDS_Shape, pt: Union[np.ndarray, List[float]], vt: Union[np.ndarray, List[float]],
              angle: float = 360) -> Optional[TopoDS_Shape]:
    """
    构造回转体，指定基础形状和回转轴、回转角度

    :param sh: 基础形状
    :param pt: 回转轴过一点
    :param vt: 回转轴方向
    :param angle: 回转角度
    :return:
    """
    pt = np.array(pt)
    vt = np.array(vt)
    mk = BRepPrimAPI_MakeRevol(sh, gp_Ax1(ccPnt(pt), ccDir(vt)), np.deg2rad(angle), True)
    return mk.Shape() if mk.IsDone() else None


def ccOffset(sh: TopoDS_Shape, offset: float) -> Optional[TopoDS_Shape]:
    """
    构造等距体，指定基础形状和距离

    :param sh: 基础形状
    :param offset: 等距距离
    :return: 等距体
    """
    mk = BRepOffsetAPI_MakeOffsetShape(sh, offset, precision.Confusion())
    mk.Build()
    return mk.Shape() if mk.IsDone() else None


def ccBounds(shs: Union[TopoDS_Shape, List[TopoDS_Shape]]) -> np.ndarray:
    """返回列表中所有形状的总包围盒"""
    if isinstance(shs, TopoDS_Shape):
        shs = [shs]
    b = Bnd_Box()
    for sh in shs:
        brepbndlib.Add(sh, b)
    return np.array(b.Get())


def ccCenter(shs: Union[TopoDS_Shape, List[TopoDS_Shape]]) -> np.ndarray:
    """返回列表中所有形状的总中心"""
    if isinstance(shs, TopoDS_Shape):
        shs = [shs]
    b = ccBounds(shs)
    return 0.5 * np.array([b[0] + b[1], b[2] + b[3], b[4] + b[5]])


def ccDiagonal(shs: Union[TopoDS_Shape, List[TopoDS_Shape]]) -> float:
    """返回列表中所有形状的总体对角线长度"""
    if isinstance(shs, TopoDS_Shape):
        shs = [shs]
    b = ccBounds(shs)
    return np.linalg.norm(np.array([b[1] - b[0], b[3] - b[2], b[5] - b[4]]))


def ccRayCast(pt: Union[np.ndarray, List[float]], vt: Union[np.ndarray, List[float]],
              sh: Union[TopoDS_Shape]) -> List[Union[np.ndarray, List[float]]]:
    """返回经过点pt方向vt的射线与形状sh的交点列表"""
    pt, vt = np.array(pt), np.array(vt)

    def dmax(s0, s1):
        b = [Bnd_Box(), Bnd_Box()]
        brepbndlib.Add(s0, b[0])
        brepbndlib.Add(s1, b[1])

        min = [[b[0].Get()[i] for i in range(3)],
               [b[1].Get()[i] for i in range(3)]]
        max = [[b[0].Get()[i] for i in range(3, 6)],
               [b[1].Get()[i] for i in range(3, 6)]]
        xyz = [[gp_XYZ(min[0][0], min[0][1], min[0][2]),
                gp_XYZ(max[0][0], max[0][1], max[0][2])],
               [gp_XYZ(min[1][0], min[1][1], min[1][2]),
                gp_XYZ(max[1][0], max[1][1], max[1][2])]]
        delta = [xyz[0][1].Subtracted(xyz[0][0]),
                 xyz[1][1].Subtracted(xyz[1][0])]

        def dmin(s0, s1):
            b = [Bnd_Box(), Bnd_Box()]
            brepbndlib.Add(s0, b[0])
            brepbndlib.Add(s1, b[1])
            return b[0].Distance(b[1])

        return delta[0].Modulus() + delta[1].Modulus() + dmin(s0, s1)

    d = dmax(ccVertex(pt), sh)
    vtmax = d * vt / np.linalg.norm(vt)

    sweep = BRepSweep_Prism(ccVertex(pt), vtmax)
    section = ccSection([sh, sweep.Shape()])

    origin = ccPnt(pt)

    pts = {}
    for s in ccExplore_Recursive(section, TopAbs_VERTEX):
        pnt = BRep_Tool.Pnt(s)
        pts[pnt.Distance(origin)] = [pnt.X(), pnt.Y(), pnt.Z()]
    return [pts[i] for i in sorted(pts)]


def ccUniformPts_Edge(edge: TopoDS_Shape, n: int) -> List[np.ndarray]:
    """按照曲线长度等分边为n个点，n应不小于2"""
    n = int(n)
    if n < 2:
        return []
    curve = BRepAdaptor_Curve(edge)
    mk = GCPnts_QuasiUniformAbscissa(curve, n)
    if mk.IsDone():
        pts = [curve.Value(mk.Parameter(i)) for i in range(1, n + 1)]
        return [np.array([pt.X(), pt.Y(), pt.Z()]) for pt in pts]


def ccEdge_FirstLastVertex(edge) -> List[TopoDS_Vertex]:
    """返回边的首末顶点坐标"""
    pts = [TopoDS_Vertex(), TopoDS_Vertex()]
    topexp.Vertices(edge, pts[0], pts[1])
    return pts


def ccEdge_FirstLastPoint(edge) -> List[np.ndarray]:
    """返回边的首末顶点坐标"""
    pts = ccEdge_FirstLastVertex(edge)
    pts = [BRep_Tool.Pnt(pt) for pt in pts]
    pts = [np.array([pt.X(), pt.Y(), pt.Z()]) for pt in pts]
    return pts


def ccLength(sh: TopoDS_Shape) -> float:
    """返回形状sh的一维密度属性，即长度"""
    p = GProp_GProps()
    brepgprop.LinearProperties(sh, p)
    return p.Mass()


def ccArea(sh: TopoDS_Shape) -> float:
    """返回形状sh的二维密度属性，即表面积"""
    p = GProp_GProps()
    brepgprop.SurfaceProperties(sh, p)
    return p.Mass()


def ccInside_Pt(sh: TopoDS_Shape, pt=None) -> float:
    """返回点pt是否在形状的内部"""
    c = BRepClass3d_SolidClassifier(sh)
    if pt is None:
        c.PerformInfinitePoint(precision.Confusion())
    else:
        c.Perform(ccPnt(pt), precision.Confusion())

    if c.State() == TopAbs_IN or c.State() == TopAbs_ON:
        return True
    return False


def ccMatchSolid_Thick(closed_pts: List[Union[np.ndarray, List[float]]], match_vt: Union[np.ndarray, List[float]],
                       target_poly: vtk.vtkPolyData, thick: Optional[float] = None, safe_dist: float = 2,
                       return_bottom_pd: Optional[List] = None) -> TopoDS_Shape:
    """
    匹配closed_pts包围的区域到面网格模型，沿match_vt方向拉伸thick距离创建匹配实体

    :param closed_pts: 首尾相连包围区域的点列
    :param match_vt: 匹配的投射方向
    :param target_poly: 匹配的模型
    :param thick: 匹配实体的厚度，thick=None时上表面为平面
    :param safe_dist: 匹配时忽略的最大孔洞半径
    :param return_bottom_pd: 返回匹配面vtkPolyData
    :return: 与模型相匹配的实体
    """
    cs = vmi.CS4x4_Vt(2, match_vt)
    z_pt = {cs.inv().mpt(pt)[2]: pt for pt in closed_pts}
    zmin = min(z_pt)

    top_pts = [vmi.ptOnPlane(pt, z_pt[zmin], match_vt) for pt in closed_pts]
    top_pd = vmi.pdTriangulate_Polyline(top_pts)
    top_pd = vmi.pdRemesh(top_pd)

    bottom_pd = vmi.pdApproximate_Pd(top_pd, match_vt, target_poly, safe_dist)
    # bottom_pd = vmi.pdSmooth_Laplacian(bottom_pd)

    if thick is not None:
        t = vtk.vtkTransform()
        t.Translate(-thick * match_vt)
        top_pd = vmi.pdTransform(bottom_pd, t)

    top_pts = vmi.pdBorder_Pts(top_pd)
    top_wire = ccWire(ccSegments(top_pts, True))
    top_face = ccSh_Pd(top_pd)

    bottom_pts = vmi.pdBorder_Pts(bottom_pd)
    bottom_wire = ccWire(ccSegments(bottom_pts, True))
    bottom_face = ccSh_Pd(bottom_pd)

    profile = ccLoft([top_wire, bottom_wire], True, True)
    sh = ccSolid(ccSew([top_face, profile, bottom_face]))

    if return_bottom_pd is not None:
        return_bottom_pd.clear()
        return_bottom_pd.append(bottom_pd)
    return sh


def ccMatchSolid_Blocks(closed_pts: List[Union[np.ndarray, List[float]]], match_vt: Union[np.ndarray, List[float]],
                        target_poly: vtk.vtkPolyData, block_size: float, safe_dist: float = 1,
                        return_bottom_pd: Optional[List] = None) -> TopoDS_Shape:
    """
    匹配closed_pts包围的区域到面网格模型，沿match_vt方向投射一群三棱柱状小块组合创建匹配实体

    :param closed_pts: 首尾相连包围区域的点列
    :param match_vt: 匹配的投射方向
    :param target_poly: 匹配的模型
    :param block_size: 柱状小块的尺寸
    :param safe_dist: 匹配时忽略的最大孔洞半径
    :param return_bottom_pd: 返回匹配面vtkPolyData
    :return: 与模型相匹配的实体
    """
    cs = vmi.CS4x4_Vt(2, match_vt)
    z_pt = {cs.inv().mpt(pt)[2]: pt for pt in closed_pts}
    zmin = min(z_pt)

    top_pts = [vmi.ptOnPlane(pt, z_pt[zmin], match_vt) for pt in closed_pts]
    top_pd = vmi.pdTriangulate_Polyline(top_pts)
    top_pd = vmi.pdRemesh(top_pd, block_size)

    bottom_pd = vmi.pdApproximate_Pd(top_pd, match_vt, target_poly, safe_dist)
    bottom_pd = vmi.pdTriangle(bottom_pd, 0, 0)
    if return_bottom_pd is not None:
        return_bottom_pd.clear()
        return_bottom_pd.append(bottom_pd)

    cs = vmi.CS4x4_Vt(0, match_vt)

    histogram = []
    for i in range(bottom_pd.GetNumberOfCells()):
        if bottom_pd.GetCell(i).GetCellType() != vtk.VTK_TRIANGLE:
            continue

        ids = [bottom_pd.GetCell(i).GetPointId(_) for _ in range(3)]
        bottom_pts = [np.array(bottom_pd.GetPoint(_)) for _ in ids]
        bottom_wire = ccWire(ccSegments(bottom_pts, True))
        bottom_face = ccFace(bottom_wire)

        top_origin = bottom_pts[0]
        for pt in bottom_pts[1:]:
            if np.dot(match_vt, top_origin - pt) > 0:
                top_origin = pt
        top_origin -= block_size * match_vt
        top_origin = cs.inv().mpt(top_origin)
        top_origin[0] = np.floor(top_origin[0] / block_size) * block_size
        top_origin = cs.mpt(top_origin)

        top_pts = [vmi.ptOnPlane(pt, top_origin, match_vt) for pt in bottom_pts]
        top_wire = ccWire(ccSegments(top_pts, True))
        top_face = ccFace(top_wire)

        profile = ccLoft([top_wire, bottom_wire], True)
        sh = ccSolid(ccSew([top_face, profile, bottom_face]))
        histogram.append(sh)

    return ccBoolean_Union(histogram)


def ccMatchSolid_Prism(closed_pts: List[Union[np.ndarray, List[float]]], match_vt: Union[np.ndarray, List[float]],
                       match_dmax: float, target_poly: vtk.vtkPolyData,
                       return_bottom_pd: Optional[List] = None) -> TopoDS_Shape:
    """
    匹配closed_pts包围的区域到面网格模型，返回匹配实体

    :param closed_pts: 首尾相连包围区域的点列
    :param match_vt: 匹配的投射方向
    :param target_poly: 匹配的模型
    :param match_dmax: vt方向最后方点的最大投射距离
    :param return_bottom_pd: 返回匹配面vtkPolyData
    :return: 与模型相匹配的实体
    """

    cs = vmi.CS4x4_Vt(2, match_vt)
    z_pt = {cs.inv().mpt(pt)[2]: pt for pt in closed_pts}
    zmin = min(z_pt)

    top_pts = [vmi.ptOnPlane(pt, z_pt[zmin], match_vt) for pt in closed_pts]
    top_pd = vmi.pdTriangulate_Polyline(top_pts)
    top_pd = vmi.pdRemesh(top_pd)

    bottom_pd = vmi.pdRayCast_Pd(top_pd, match_vt, target_poly, match_dmax)
    bottom_pd = vmi.pdRemesh(bottom_pd)

    bottom_pts = vmi.pdBorder_Pts(bottom_pd)
    bottom_wire = ccWire(ccSegments(bottom_pts, True))
    bottom_face = ccSh_Pd(bottom_pd)

    top_pts = [vmi.ptOnPlane(pt, z_pt[zmin], match_vt) for pt in bottom_pts]
    top_wire = ccWire(ccSegments(top_pts, True))
    top_face = ccFace_OnPlane(top_wire, z_pt[zmin], match_vt)
    top_wire = ccExplore_Once(top_face)[0]

    profile = ccLoft([top_wire, bottom_wire], True, True)
    shape = ccSolid(ccSew([top_face, profile, bottom_face]))

    if return_bottom_pd is not None:
        return_bottom_pd.clear()
        return_bottom_pd.append(bottom_pd)
    return shape


def ccMatchSolid_Rect(target_poly: vtk.vtkPolyData, cs: vmi.CS4x4, nx: int, ny: int, res: float,
                      z_min: float, z_max: float, z_filter: Callable = None,
                      return_mold: Optional[List] = None):
    """
    匹配矩形区域到面网格模型，返回匹配实体

    :param target_poly: 匹配的模型
    :param cs: 匹配方位坐标系
    :param nx: x半方向网格节点数
    :param ny: y半方向网格节点数
    :param res: 网格精度
    :param z_min: 网格节点最小z坐标
    :param z_max: 网格节点最大z坐标
    :param z_filter: 网格节点z坐标滤波器，z_filter(x_array, y_array, z_array) -> z_array
    :param return_mold: 返回匹配实体的反向实体
    :return: 与模型相匹配的实体
    """
    if not nx >= 1:
        raise Exception('nx={}'.format(nx))
    if not ny >= 1:
        raise Exception('ny={}'.format(ny))
    if not res > 0:
        raise Exception('res={}'.format(res))
    if not z_min > 0:
        raise Exception('thick_min={}'.format(z_min))
    if not z_max > 0:
        raise Exception('ray_max={}'.format(z_max))

    target_kd = vtk.vtkKdTreePointLocator()
    target_kd.SetDataSet(target_poly)
    target_kd.BuildLocator()

    target_obb = vtk.vtkOBBTree()
    target_obb.SetDataSet(target_poly)
    target_obb.BuildLocator()

    match_pts_list, mold_pts_list = [], []
    xs, ys = np.zeros((2 * ny + 1, 2 * nx + 1)), np.zeros((2 * ny + 1, 2 * nx + 1))
    zs = np.zeros((2 * ny + 1, 2 * nx + 1))
    for j in range(2 * ny + 1):
        match_pts, mold_pts = [], []
        for i in range(2 * nx + 1):
            xs[j][i] = res * (i - nx)
            ys[j][i] = res * (j - ny)

            pt = cs.mpt([xs[j][i], ys[j][i], 0])
            match_pts.append(pt.copy())
            mold_pts.append(pt.copy())

            d = vmi.pdRayDistance_Pt(pt, cs.axis(2), target_poly, target_kd, target_obb)
            zs[j][i] = z_max if d is None else d
            zs[j][i] = min(max(zs[j][i], z_min), z_max)

        match_pts.append(cs.mpt([res * nx, res * (j - ny), z_min]))
        match_pts.append(cs.mpt([res * -nx, res * (j - ny), z_min]))
        match_pts_list.append(match_pts)

        mold_pts.append(cs.mpt([res * nx, res * (j - ny), z_max + z_min]))
        mold_pts.append(cs.mpt([res * -nx, res * (j - ny), z_max + z_min]))
        mold_pts_list.append(mold_pts)

    if z_filter is not None:
        zs = z_filter(xs, ys, zs)

    # mold
    if return_mold is not None:
        for j in range(0, 2 * ny + 1):
            for i in range(0, 2 * nx + 1):
                mold_pts_list[j][i] += zs[j][i] * cs.axis(2)

        wires = [ccWire(ccSegments(x_pts, True)) for x_pts in mold_pts_list]
        mold = ccLoft(wires, ruled=True, solid=True)
        return_mold.clear()
        return_mold.append(mold)

    # match
    for j in range(0, 2 * ny + 1):
        for i in range(0, 2 * nx + 1):
            match_pts_list[j][i] += zs[j][i] * cs.axis(2)

    wires = [ccWire(ccSegments(x_pts, True)) for x_pts in match_pts_list]
    match = ccLoft(wires, ruled=True, solid=True)
    return match


def ccTransform_Translation(sh: TopoDS_Shape, translation: Union[np.ndarray, List[float]]) -> TopoDS_Shape:
    """
    平移变换TopoDS_Shape

    :param sh: 输入形状
    :param translation: 平移参数x,y,z
    :return: 变换后的形状
    """
    trsf = gp_Trsf()
    trsf.SetTranslation(ccVec(translation))
    return BRepBuilderAPI_Transform(sh, trsf, True).Shape()
