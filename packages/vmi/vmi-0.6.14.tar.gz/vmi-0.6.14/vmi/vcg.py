from typing import List

import numpy as np
import vtk
from CGAL.CGAL_AABB_tree import *
from CGAL.CGAL_Kernel import *
from CGAL.CGAL_Convex_hull_2 import *
from CGAL.CGAL_Mesh_3 import *
from CGAL.CGAL_Spatial_searching import *
from CGAL.CGAL_Triangulation_2 import *
from CGAL.CGAL_HalfedgeDS import *
from CGAL.CGAL_Triangulation_3 import *
from CGAL.CGAL_Alpha_shape_2 import *
from CGAL.CGAL_Polyhedron_3 import *
from CGAL.CGAL_Voronoi_diagram_2 import *
from CGAL.CGAL_Mesh_2 import *
from CGAL.CGAL_Interpolation import *
from CGAL.CGAL_Box_intersection_d import *
from CGAL.CGAL_Convex_hull_3 import *
from CGAL.CGAL_Point_set_processing_3 import *
from CGAL.CGAL_Polyline_simplification_2 import *
from CGAL.CGAL_Advancing_front_surface_reconstruction import *
from CGAL.CGAL_Polygon_mesh_processing import *
from CGAL import *

import vmi


def cgPh_Pd(pd: vtk.vtkPolyData) -> Polyhedron_3:
    """转换vtkPolyData为Polyhedron_3"""
    num_vertex = pd.GetNumberOfPoints()
    num_facet = 0
    for i in range(pd.GetNumberOfCells()):
        cell: vtk.vtkCell = pd.GetCell(i)
        if cell.GetCellType() in [vtk.VTK_TRIANGLE, vtk.VTK_QUAD, vtk.VTK_POLYGON]:
            num_facet += 1

    m = Polyhedron_modifier()
    m.begin_surface(num_vertex, num_facet)

    for i in range(pd.GetNumberOfPoints()):
        pt = pd.GetPoint(i)
        m.add_vertex(Point_3(pt[0], pt[1], pt[2]))

    for cell_id in range(pd.GetNumberOfCells()):
        cell: vtk.vtkCell = pd.GetCell(cell_id)
        if cell.GetCellType() in [vtk.VTK_TRIANGLE, vtk.VTK_QUAD, vtk.VTK_POLYGON]:
            m.begin_facet()
            for ii in range(cell.GetPointIds().GetNumberOfIds()):
                pid = cell.GetPointId(ii)
                m.add_vertex_to_facet(pid)
            m.end_facet()

    m.end_surface()

    ph = Polyhedron_3()
    ph.delegate(m)
    return ph


def cgPd_Ph(ph: Polyhedron_3) -> vtk.vtkPolyData:
    """转换Polyhedron_3为vtkPolyData"""
    pd = vtk.vtkPolyData()
    pd.SetPoints(vtk.vtkPoints())
    pd.SetPolys(vtk.vtkCellArray())

    points, i = {}, 0
    for vertex in ph.vertices():
        p = vertex.point()
        pd.GetPoints().InsertNextPoint([p.x(), p.y(), p.z()])
        points[str(p)] = i
        i += 1

    for facet in ph.facets():
        halfedge = facet.halfedge()
        cell_ids = []

        while len(cell_ids) == 0 or halfedge != facet.halfedge():
            cell_ids.append(points[str(halfedge.vertex().point())])
            halfedge = halfedge.next()

        n = len(cell_ids)

        if n == 3:
            cell = vtk.vtkTriangle()
            for i in range(n):
                cell.GetPointIds().SetId(i, cell_ids[i])
            pd.GetPolys().InsertNextCell(cell)
        elif n == 4:
            cell = vtk.vtkQuad()
            for i in range(n):
                cell.GetPointIds().SetId(i, cell_ids[i])
            pd.GetPolys().InsertNextCell(cell)
        elif n > 4:
            cell = vtk.vtkPolygon()
            cell.GetPointIds().SetNumberOfIds(n)
            for i in range(n):
                cell.GetPointIds().SetId(i, cell_ids[i])
            pd.GetPolys().InsertNextCell(cell)

    return pd


def pdRemesh(pd: vtk.vtkPolyData, target_edge_length: float = 1, number_of_iterations: int = 10)->vtk.vtkPolyData:
    """
    网格重划分

    :param pd: 输入网格
    :param target_edge_length: 目标边长
    :param number_of_iterations: 迭代次数
    :return: 重划分网格
    """
    ph = vmi.cgPh_Pd(pd)
    isotropic_remeshing([_ for _ in ph.facets()], target_edge_length, ph, number_of_iterations)
    pd = vmi.cgPd_Ph(ph)
    return pd


def pdTriangulate_Polyline(pts) -> vtk.vtkPolyData:
    """三角网格化闭合多边形，多边形节点按照pts首尾相连"""
    points = pts.copy()
    for i in range(len(points)):
        if not isinstance(points[i], Point_3):
            points[i] = Point_3(points[i][0], points[i][1], points[i][2])

    cell_ids = []
    triangulate_hole_polyline(points, cell_ids)

    pd = vtk.vtkPolyData()
    pd.SetPoints(vtk.vtkPoints())
    pd.SetPolys(vtk.vtkCellArray())

    for pt in points:
        pd.GetPoints().InsertNextPoint(pt.x(), pt.y(), pt.z())

    for cell_id in cell_ids:
        cell = vtk.vtkTriangle()
        cell.GetPointIds().SetId(0, cell_id.first)
        cell.GetPointIds().SetId(1, cell_id.second)
        cell.GetPointIds().SetId(2, cell_id.third)
        pd.GetPolys().InsertNextCell(cell)

    return pd


def cgBorder_Halfedges(ph: Polyhedron_3):
    """提取多面体ph的边界半边，仅支持单个连通多面体"""
    hs = []
    for facet in ph.facets():
        n, h = 0, facet.halfedge()

        while n == 0 or h != facet.halfedge():
            n, h = n + 1, h.next()

            if h in hs:
                hs.remove(h)
            elif h.opposite() in hs:
                hs.remove(h.opposite())
            else:
                hs.append(h)

    if len(hs) > 0:
        hs_border = [hs[0]]
        hv = {h.opposite().vertex(): h for h in hs}

        while hs_border[-1].vertex() in hv:
            h_next = hv[hs_border[-1].vertex()]
            if h_next not in hs_border:
                hs_border.append(h_next)
            else:
                break

        hs = hs_border

    return hs


def cgBorder_Pts(ph: Polyhedron_3):
    hs, pts = cgBorder_Halfedges(ph), []
    for h in hs:
        pt = h.vertex().point()
        pts.append(np.array([pt.x(), pt.y(), pt.z()]))
    return pts


def pdBorder_Pts(pd: vtk.vtkPolyData) -> List[np.ndarray]:
    """
    返回顺次排列的网格边界点，网格必须是单连通的简单形状

    :param pd: 输入网格
    :return: [[x, y, z]]
    """
    ph = vmi.cgPh_Pd(pd)
    return vmi.cgBorder_Pts(ph)
