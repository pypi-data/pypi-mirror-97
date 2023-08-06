import pathlib
import time
from typing import List

import numpy as np
import pydicom
import vtk
from PySide2.QtGui import *
from numba import jit

import vmi


def LeftButtonPress(**kwargs):
    if kwargs['picked'] is view:
        if local_roi_box.text() == '请框选目标区域':
            pt = view.pickPt_FocalPlane()
            global local_roi_pts
            local_roi_pts = [pt.copy(), pt.copy()]
            update_local_roi()


def LeftButtonPressMove(**kwargs):
    global spcut_center, pelvis_cs
    if kwargs['picked'] is view:
        if local_roi_box.text() == '请框选目标区域':
            pt = view.pickPt_Cell()
            global local_roi_pts
            local_roi_pts[-1] = pt.copy()
            update_local_roi()
        else:
            view.mouseRotateFocal(**kwargs)


def LeftButtonPressMoveRelease(**kwargs):
    if kwargs['picked'] is view:
        if local_roi_box.text() == '请框选目标区域':
            local_roi_box.draw_text('请耐心等待')
            update_local_solid()
            global local_roi_pts
            local_roi_pts.clear()
            update_local_roi()
            local_roi_box.draw_text('捧一下')


def LeftButtonPressRelease(**kwargs):
    if kwargs['picked'] is local_roi_box:
        if local_roi_box.text() in ['捧一下', '请耐心等待']:
            local_roi_box.draw_text('请框选目标区域')
        elif local_roi_box.text() == '请框选目标区域':
            local_roi_box.draw_text('捧一下')
    elif kwargs['picked'] is view:
        if local_roi_box.text() == '请框选目标区域':
            local_roi_box.draw_text('请耐心等待')
            update_local_solid()
            global local_roi_pts
            local_roi_pts.clear()
            update_local_roi()
            local_roi_box.draw_text('捧一下')


def init_view():
    global target
    target = vmi.pdOpenFile_STL()
    if target is None:
        vmi.appexit()

    global view
    view = vmi.View()
    view.setCamera_Coronal()
    view.mouse['LeftButton']['Press'] = [LeftButtonPress]
    view.mouse['LeftButton']['PressMove'] = [LeftButtonPressMove]
    view.mouse['LeftButton']['PressMoveRelease'] = [LeftButtonPressMoveRelease]

    global target_prop
    target_prop = vmi.PolyActor(view, color=[0.8, 0.8, 0.8], repres='wireframe')
    target_prop.setData(target)
    view.setCamera_FitAll()

    global local_roi_box
    local_roi_box = vmi.TextBox(view, text='捧一下', size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0], pickable=True)
    local_roi_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    global local_roi_prop
    local_roi_prop = vmi.PolyActor(view, color=[1, 0.6, 0.6], line_width=3, always_on_top=True)

    global local_solid_target_prop, local_solid_match_prop
    local_solid_target_prop = vmi.PolyActor(view, color=[1, 1, 0.6])
    local_solid_match_prop = vmi.PolyActor(view, color=[0.6, 0.8, 1], opacity=0.5)

    global output_solid_target, output_solid_match
    output_solid_target, output_solid_match = None, None

    global output_solid_target_prop, output_solid_match_prop
    output_solid_target_prop = vmi.PolyActor(view, color=[1, 1, 0.4])
    output_solid_match_prop = vmi.PolyActor(view, color=[0.4, 0.6, 1])


def update_local_roi():
    global local_roi_pts
    if len(local_roi_pts) and np.linalg.norm(local_roi_pts[0] - local_roi_pts[1]):
        global target, output_solid_target_prop, local_cs, local_max_z
        local_cs = view.cameraCS_FPlane()
        if output_solid_target is None:
            local_max_z = np.linalg.norm(vmi.pdSize(target))
            local_center = vmi.pdCenter(target) - 0.5 * local_max_z * local_cs.axis(2)
        else:
            local_max_z = np.linalg.norm(vmi.pdSize(output_solid_target_prop.data()))
            local_center = vmi.pdCenter(output_solid_target_prop.data()) - 0.5 * local_max_z * local_cs.axis(2)

        local_center = vmi.ptOnPlane(local_roi_pts[0], local_center, local_cs.axis(2))
        local_cs.setOrigin(local_roi_pts[0])

        global local_rect_xr, local_rect_yr
        vt = local_roi_pts[0] - local_roi_pts[1]
        vt = local_cs.inv().mvt(vt)
        local_rect_xr, local_rect_yr = np.linalg.norm(vt[0]), np.linalg.norm(vt[1])
        local_roi_wire = local_cs.workplane().rect(local_rect_xr * 2, local_rect_yr * 2).val().wrapped
        local_roi_prop.setData(local_roi_wire)

        local_cs.setOrigin(local_center)
    else:
        local_roi_prop.setData(None)


def update_local_solid():
    global target, local_cs, local_max_z
    res = vmi.askFloat(0.1, 1, 5, 1, 0.1, '精度', 'mm', '精度')
    if res is None:
        vmi.askInfo('已取消')
        return
    smooth = vmi.askInt(0, 0, 10, 1, '光顺指数', None, '光顺指数')
    if smooth is None:
        vmi.askInfo('已取消')
        return
    smooth = res / smooth if smooth else 0
    ok = vmi.askYesNo('确定执行？')
    if not ok:
        vmi.askInfo('已取消')
        return

    xn, yn = int(np.ceil(local_rect_xr / res)) + 1, int(np.ceil(local_rect_yr / res)) + 1
    local_solid_target = []
    local_solid_match = vmi.ccMatchSolid_Rect(
        target, local_cs, xn, yn, res, res, local_max_z, smooth, local_solid_target)
    local_solid_target = local_solid_target[0]

    global output_solid_target, output_solid_match
    if output_solid_target is None:
        output_solid_target = local_solid_target
        output_solid_target_prop.setData(output_solid_target)
        local_solid_match_prop.setData(local_solid_match)
    else:
        output_solid_target = vmi.ccBoolean_Difference([output_solid_target, local_solid_match])
        output_solid_target_prop.setData(output_solid_target)
        # local_solid_target_prop.setData(local_solid_target)
        local_solid_match_prop.setData(local_solid_match)


if __name__ == '__main__':
    vmi.app.setApplicationName('StraightMan')
    init_view()

    global view
    vmi.appexec(view)
    vmi.appexit()
