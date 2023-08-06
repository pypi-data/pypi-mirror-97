import json
import pathlib
import shutil
import tempfile
from typing import Dict

import numpy as np
import vtk
from PySide2.QtGui import QKeySequence, QColor
from PySide2.QtWidgets import QShortcut, QColorDialog

import vmi


def snapshot(ok: bool):
    if ok:
        global snapshot_i
        f = snapshot_path / '{}.png'.format(snapshot_i)
        view.snapshot_PNG(str(f))
        main.statusBar().showMessage('快照 {}'.format(f))
        snapshot_i += 1


def on_shortcut(key: str):
    global rt_prop, camera_dv, camera_dt, rt_cs, cs_dv, cs_dt, snapshot_i, snapshot_path, snapshot_auto

    if key == 'F1':
        text = 'F1 帮助 F2 模型 F3 相机 F4 坐标系 F5捕获'
        text += 'Tab Shift+Tab 切换当前模型'
        text += '\nq 相机逆转 e 相机顺转'
        text += '\nw 相机上转 s 相机下转'
        text += '\na 相机左转 d 相机右转'
        text += '\nr 相机缩小 y 相机放大'
        text += '\nt 相机上移 g 相机下移'
        text += '\nf 相机左移 h 相机右移'
        text += '\nu 模型前移 o 模型后移'
        text += '\ni 模型上移 k 模型下移'
        text += '\nj 模型左移 l 模型右移'
        text += '\np 模型重置'
        text += '\n[ 模型逆转 ] 模型顺转'
        text += '\n; 模型左转 \' 模型右转'
        text += '\n, 模型上转 . 模型下转'
        text += '\nz 模型表达方式 x 模型纹理 c 模型主色 v 模型可见'
        text += '\nb 背景纹理'
        text += '\nn '
        text += '\nm '
        text += '\n` 快照 Ctrl+` 自动快照'
        text += '\n1 模型环境色 2 模型环境光减少 3 模型环境光增加'
        text += '\n4 模型扩散色 5 模型扩散光减少 6 模型扩散光增加'
        text += '\n7 模型反光系数减少 8 模型反光系数增加'
        text += '\n9 模型反光强度减少 0 模型反光强度增加'
        text += '\n- 模型不透明度减少 = 模型不透明度增加'
        text += '\nBackspace 模型透明校正'
        text += '\n/ '
        text += '\n\\ '
        text += '\n '
        text += '\n '
        vmi.askInfo(text, '帮助')
    elif key == 'F2':
        b = vmi.askButtons(['导入', '设置模型属性', '导出模型属性', '列表'], '模型')
        if b is None:
            return
        elif b == '导入':
            fs = vmi.askOpenFiles('*.stl', 'STL')
            if fs is None:
                return

            for f in fs:
                pd = vmi.pdOpenFile_STL(f)
                prop = vmi.PolyActor(view)
                prop.setData(pd)
                prop.prop().SetUserMatrix(vtk.vtkMatrix4x4())
                prop.prop_property().SetAmbient(0.2)
                prop.prop_property().SetDiffuse(0.8)
                prop.prop_property().SetSpecular(0.1)
                prop.prop_property().SetSpecularPower(10)
                props[prop] = {'path': f}
        elif b == '设置模型属性':
            if rt_prop:
                f = vmi.askOpenFile('*.json', '模型属性')
                if f is None:
                    return
                data = json.loads(pathlib.Path(f).read_text())
                vmi.vtkInstance_sets(rt_prop.prop(), data['prop'])
                vmi.vtkInstance_sets(rt_prop.prop_property(), data['property'])
                cs = vmi.CS4x4()
                cs.setArray4x4(np.array(data['user_matrix']))
                rt_prop.prop().SetUserMatrix(cs.matrix4x4())
                view.updateInTime()
                main.statusBar().showMessage('设置模型属性 {}'.format(f))
        elif b == '导出模型属性':
            if rt_prop:
                f = vmi.askSaveFile('*.json', '*.json', '模型属性')
                if f is None:
                    return
                cs = vmi.CS4x4()
                cs.setMatrix4x4(rt_prop.prop().GetUserMatrix())
                data = {'prop': vmi.vtkInstance_gets(rt_prop.prop()),
                        'property': vmi.vtkInstance_gets(rt_prop.prop_property()),
                        'user_matrix': cs.array4x4().tolist()}
                pathlib.Path(f).write_text(json.dumps(data))
                main.statusBar().showMessage('导出模型属性 {}'.format(f))
        elif b == '列表':
            prop = vmi.askCombo({props[prop]['path']: prop for prop in props})
            if prop is None:
                return

            button = vmi.askButtons(['设为当前模型'], '模型')
            if button is None:
                return
            elif button == '设为当前模型':
                rt_prop = prop
                print('设置当前模型 {}'.format(props[rt_prop]['path']))
                main.statusBar().showMessage('设置当前模型 {}'.format(props[rt_prop]['path']))
    elif key == 'F3':
        button = vmi.askButtons(['导入', '导入坐标系XZ', '导出', '最适', '设置单位距离', '设置单位角度'], '相机')
        if button is None:
            return
        elif button == '导入':
            f = vmi.askOpenFile('*.json', '相机')
            if f is None:
                return
            vmi.vtkInstance_sets(view.camera(), json.loads(pathlib.Path(f).read_text()))
            view.camera().OrthogonalizeViewUp()
            print('设置相机 {}'.format(vmi.vtkInstance_gets(view.camera())))
            main.statusBar().showMessage('设置相机')
        elif button == '导入坐标系XZ':
            vl = np.cross(rt_cs.axis(2), rt_cs.axis(0))
            fp = rt_cs.origin()
            d = view.camera().GetDistance()
            cp = fp - d * vl
            view.camera().SetPosition(*cp)
            view.camera().SetFocalPoint(*fp)
            view.camera().SetViewUp(*rt_cs.axis(2))
            print('设置相机\n{}'.format(vmi.vtkInstance_gets(view.camera())))
            main.statusBar().showMessage('设置相机')
        elif button == '导出':
            f = vmi.askSaveFile('*.json', '*.json', '相机')
            if f is None:
                return
            pathlib.Path(f).write_text(json.dumps(vmi.vtkInstance_gets(view.camera())))
            main.statusBar().showMessage('导出相机')
        elif button == '最适':
            view.setCamera_FitAll()
            print('设置相机\n{}'.format(vmi.vtkInstance_gets(view.camera())))
            main.statusBar().showMessage('设置相机')
        elif button == '设置单位距离':
            dv = vmi.askFloat(1e-3, camera_dv, 1e3, 3, 1, suffix='mm', title='设置单位距离')
            if dv is not None:
                camera_dv = dv
                print('设置单位距离\n{}'.format(camera_dv))
                main.statusBar().showMessage('设置单位距离 {} mm'.format(camera_dv))
        elif button == '设置单位角度':
            dt = vmi.askFloat(1e-3, camera_dt, 1e3, 3, 1, suffix='°', title='设置单位角度')
            if dt is not None:
                camera_dt = dt
                print('设置单位角度\n{}'.format(camera_dt))
                main.statusBar().showMessage('设置单位角度 {} °'.format(camera_dt))
    elif key == 'F4':
        button = vmi.askButtons(['导入', '导入相机', '导出', '重设', '设置单位距离', '设置单位角度'], '坐标系')
        if button is None:
            return
        elif button == '导入':
            f = vmi.askOpenFile('*.json', '坐标系')
            if f is None:
                return
            rt_cs.setArray4x4(np.array(json.loads(pathlib.Path(f).read_text())))
            rt_cs.normalize()
            print('导入坐标系\n{}'.format(repr(rt_cs)))
            main.statusBar().showMessage('设置坐标系')
        elif button == '导入相机':
            vu = np.array(view.camera().GetViewUp())
            fp = np.array(view.camera().GetFocalPoint())
            cp = np.array(view.camera().GetPosition())
            vl = fp - cp
            rt_cs.setOrigin(fp)
            rt_cs.setAxis(1, vl)
            rt_cs.setAxis(2, vu)
            rt_cs.orthogonalize([0])
            rt_cs.normalize()
            print('设置坐标系\n{}'.format(repr(rt_cs)))
            main.statusBar().showMessage('设置坐标系')
        elif button == '导出':
            f = vmi.askSaveFile('*.json', '*.json', '坐标系')
            if f is None:
                return
            pathlib.Path(f).write_text(json.dumps(rt_cs.array4x4().tolist()))
            main.statusBar().showMessage('导出坐标系')
        elif button == '重设':
            rt_cs = vmi.CS4x4()
            print('重设坐标系\n{}'.format(repr(rt_cs)))
            main.statusBar().showMessage('设置坐标系')
        elif button == '设置单位距离':
            dv = vmi.askFloat(1e-3, cs_dv, 1e3, 3, 1, suffix='mm', title='设置单位距离')
            if dv is not None:
                cs_dv = dv
                print('设置单位距离\n{}'.format(cs_dv))
                main.statusBar().showMessage('设置单位距离 {} mm'.format(cs_dv))
        elif button == '设置单位角度':
            dt = vmi.askFloat(1e-3, cs_dt, 1e3, 3, 1, suffix='°', title='设置单位角度')
            if dt is not None:
                cs_dt = dt
                print('设置单位角度\n{}'.format(cs_dt))
                main.statusBar().showMessage('设置单位角度 {} °'.format(cs_dt))
    elif key == 'F5':
        button = vmi.askButtons(['设置图片序号', '设置图片路径'], '坐标系')
        if button is None:
            return
        elif button == '设置图片序号':
            i = vmi.askInt(0, snapshot_i, int(1e9), 1, title='设置图片序号')
            if i is not None:
                snapshot_i = i
                main.statusBar().showMessage('设置图片序号 {}'.format(snapshot_i))
        elif button == '设置图片路径':
            f = vmi.askDirectory('设置图片路径')
            if f is not None:
                snapshot_path = pathlib.Path(f)
                main.statusBar().showMessage('设置图片路径 {}'.format(snapshot_path))
    elif key == 'Tab':
        keys = list(props.keys())
        if rt_prop in props:
            i = keys.index(rt_prop)
            rt_prop = keys[(i + 1) % len(keys)]
        else:
            rt_prop = keys[0]
        print('设置当前模型 {}'.format(props[rt_prop]['path']))
        main.statusBar().showMessage('设置当前模型 {}'.format(props[rt_prop]['path']))
    elif key == 'Shift+Tab':
        keys = list(props.keys())
        if rt_prop in props:
            i = keys.index(rt_prop)
            rt_prop = keys[(i - 1) % len(keys)]
        else:
            rt_prop = keys[0]
        print('设置当前模型 {}'.format(props[rt_prop]['path']))
        main.statusBar().showMessage('设置当前模型 {}'.format(props[rt_prop]['path']))
    elif key == 'q':
        view.camera().Roll(camera_dt)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机逆转 {} °'.format(camera_dt))
        snapshot(snapshot_auto)
    elif key == 'e':
        view.camera().Roll(-camera_dt)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机顺转 {} °'.format(camera_dt))
        snapshot(snapshot_auto)
    elif key == 'w':
        view.camera().Elevation(-camera_dt)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机上转 {} °'.format(camera_dt))
        snapshot(snapshot_auto)
    elif key == 's':
        view.camera().Elevation(camera_dt)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机下转 {} °'.format(camera_dt))
        snapshot(snapshot_auto)
    elif key == 'a':
        view.camera().Azimuth(camera_dt)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机左转 {} °'.format(camera_dt))
        snapshot(snapshot_auto)
    elif key == 'd':
        view.camera().Azimuth(-camera_dt)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机右转 {} °'.format(camera_dt))
        snapshot(snapshot_auto)
    elif key == 'r':
        value = view.camera().GetParallelScale()
        view.camera().SetParallelScale(value - camera_dv)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机放大 {} mm'.format(camera_dv))
        snapshot(snapshot_auto)
    elif key == 'y':
        value = view.camera().GetParallelScale()
        view.camera().SetParallelScale(value + camera_dv)
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机缩小 {} mm'.format(camera_dv))
        snapshot(snapshot_auto)
    elif key == 't':
        fp = np.array(view.camera().GetFocalPoint())
        cp = np.array(view.camera().GetPosition())
        vu = np.array(view.camera().GetViewUp())
        view.camera().SetFocalPoint(*(fp - camera_dv * vu))
        view.camera().SetPosition(*(cp - camera_dv * vu))
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机上移 {} mm'.format(camera_dv))
        snapshot(snapshot_auto)
    elif key == 'g':
        fp = np.array(view.camera().GetFocalPoint())
        cp = np.array(view.camera().GetPosition())
        vu = np.array(view.camera().GetViewUp())
        view.camera().SetFocalPoint(*(fp + camera_dv * vu))
        view.camera().SetPosition(*(cp + camera_dv * vu))
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机下移 {} mm'.format(camera_dv))
        snapshot(snapshot_auto)
    elif key == 'f':
        fp = np.array(view.camera().GetFocalPoint())
        cp = np.array(view.camera().GetPosition())
        vl = fp - cp
        vu = np.array(view.camera().GetViewUp())
        vr = np.cross(vl, vu)
        vr = vr / np.linalg.norm(vr)
        view.camera().SetFocalPoint(*(fp + camera_dv * vr))
        view.camera().SetPosition(*(cp + camera_dv * vr))
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机左移 {} mm'.format(camera_dv))
        snapshot(snapshot_auto)
    elif key == 'h':
        fp = np.array(view.camera().GetFocalPoint())
        cp = np.array(view.camera().GetPosition())
        vl = fp - cp
        vu = np.array(view.camera().GetViewUp())
        vr = np.cross(vl, vu)
        vr = vr / np.linalg.norm(vr)
        view.camera().SetFocalPoint(*(fp - camera_dv * vr))
        view.camera().SetPosition(*(cp - camera_dv * vr))
        view.camera().OrthogonalizeViewUp()
        view.updateInTime()
        main.statusBar().showMessage('相机右移 {} mm'.format(camera_dv))
        snapshot(snapshot_auto)
    elif key == 'u':
        if rt_prop:
            mat = vmi.CS4x4().translate(-cs_dv * rt_cs.axis(1)).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型前移 {} mm'.format(cs_dv))
            snapshot(snapshot_auto)
    elif key == 'o':
        if rt_prop:
            mat = vmi.CS4x4().translate(cs_dv * rt_cs.axis(1)).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型后移 {} mm'.format(cs_dv))
            snapshot(snapshot_auto)
    elif key == 'i':
        if rt_prop:
            mat = vmi.CS4x4().translate(cs_dv * rt_cs.axis(2)).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型上移 {} mm'.format(cs_dv))
            snapshot(snapshot_auto)
    elif key == 'k':
        if rt_prop:
            mat = vmi.CS4x4().translate(-cs_dv * rt_cs.axis(2)).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型下移 {} mm'.format(cs_dv))
            snapshot(snapshot_auto)
    elif key == 'j':
        if rt_prop:
            mat = vmi.CS4x4().translate(-cs_dv * rt_cs.axis(0)).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型左移 {} mm'.format(cs_dv))
            snapshot(snapshot_auto)
    elif key == 'l':
        if rt_prop:
            mat = vmi.CS4x4().translate(cs_dv * rt_cs.axis(0)).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型右移 {} mm'.format(cs_dv))
            snapshot(snapshot_auto)
    elif key == 'p':
        if rt_prop and vmi.askYesNo('重置模型位置姿态？'):
            rt_prop.prop().SetUserMatrix(vtk.vtkMatrix4x4())
            view.updateInTime()
            main.statusBar().showMessage('模型重置'.format())
    elif key == '[':
        if rt_prop:
            mat = vmi.CS4x4().rotate(-cs_dt, rt_cs.axis(1), rt_cs.origin()).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型逆转 {} °'.format(cs_dt))
            snapshot(snapshot_auto)
    elif key == ']':
        if rt_prop:
            mat = vmi.CS4x4().rotate(cs_dt, rt_cs.axis(1), rt_cs.origin()).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型顺转 {} °'.format(cs_dt))
            snapshot(snapshot_auto)
    elif key == ';':
        if rt_prop:
            mat = vmi.CS4x4().rotate(-cs_dt, rt_cs.axis(2), rt_cs.origin()).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型左转 {} °'.format(cs_dt))
            snapshot(snapshot_auto)
    elif key == '\'':
        if rt_prop:
            mat = vmi.CS4x4().rotate(cs_dt, rt_cs.axis(2), rt_cs.origin()).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型右转 {} °'.format(cs_dt))
            snapshot(snapshot_auto)
    elif key == ',':
        if rt_prop:
            mat = vmi.CS4x4().rotate(-cs_dt, rt_cs.axis(0), rt_cs.origin()).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型上转 {} °'.format(cs_dt))
            snapshot(snapshot_auto)
    elif key == '.':
        if rt_prop:
            mat = vmi.CS4x4().rotate(cs_dt, rt_cs.axis(0), rt_cs.origin()).matrix4x4()
            vtk.vtkMatrix4x4.Multiply4x4(mat, rt_prop.prop().GetUserMatrix(), mat)
            rt_prop.prop().SetUserMatrix(mat)
            view.updateInTime()
            main.statusBar().showMessage('模型下转 {} °'.format(cs_dt))
            snapshot(snapshot_auto)
    elif key == 'z':
        if rt_prop:
            r = rt_prop.repres()
            r = ['points', 'wireframe', 'surface'].index(r)
            r = ['points', 'wireframe', 'surface'][(r + 1) % 3]
            rt_prop.setRepres(r)
            main.statusBar().showMessage('设置模型表达 {}'.format(r))
    elif key == 'x':
        if rt_prop:
            f = vmi.askOpenFile('*.png', '模型纹理')
            if f is None:
                return

            with tempfile.TemporaryDirectory() as p:
                p = pathlib.Path(p) / '.png'
                shutil.copy2(f, p)
                reader = vtk.vtkImageReader2Factory().CreateImageReader2(str(p))
                reader.SetFileName(str(p))
                reader.Update()
                texture_data = reader.GetOutput()

            texture = vtk.vtkTexture()
            texture.SetInputData(texture_data)
            texture.SetInterpolate(1)
            rt_prop.prop_property().RemoveAllTextures()
            rt_prop.prop_property().SetTexture('texture', texture)

            map_to = vtk.vtkTextureMapToPlane()
            map_to.SetInputData(rt_prop.data())
            map_to.Update()
            rt_prop.setData(map_to.GetOutput())
            main.statusBar().showMessage('设置模型纹理')
    elif key == 'c':
        if rt_prop:
            c = QColorDialog.getColor(QColor.fromRgbF(*rt_prop.prop_property().GetColor()))
            if c.isValid():
                rt_prop.prop_property().SetColor(c.redF(), c.greenF(), c.blueF())
                view.updateInTime()
                main.statusBar().showMessage('设置模型主色 {} {} {}'.format(c.red(), c.green(), c.blue()))
    elif key == 'v':
        if rt_prop:
            rt_prop.visibleToggle()
            main.statusBar().showMessage('设置模型可见 {}'.format(rt_prop.visible()))
    elif key == 'b':
        f = vmi.askOpenFile('*.png', '背景纹理')
        if f is None:
            return

        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.png'
            shutil.copy2(f, p)
            reader = vtk.vtkImageReader2Factory().CreateImageReader2(str(p))
            reader.SetFileName(str(p))
            reader.Update()
            texture_data = reader.GetOutput()

        texture = vtk.vtkTexture()
        texture.SetInputData(texture_data)
        texture.SetInterpolate(1)
        view.renderer().SetTexturedBackground(True)
        view.renderer().SetBackgroundTexture(texture)
        main.statusBar().showMessage('设置背景纹理')
    # elif key == 'n':
    # elif key == 'm':
    elif key == '`':
        snapshot(True)
    elif key == 'Ctrl+`':
        snapshot_auto = not snapshot_auto
        main.statusBar().showMessage('自动快照 {}'.format(snapshot_auto))
    elif key == '1':
        if rt_prop:
            c = QColorDialog.getColor(QColor.fromRgbF(*rt_prop.prop_property().GetAmbientColor()))
            if c.isValid():
                rt_prop.prop_property().SetAmbientColor(c.redF(), c.greenF(), c.blueF())
                view.updateInTime()
                main.statusBar().showMessage('设置环境色 {} {} {}'.format(c.red(), c.green(), c.blue()))
    elif key == '2':
        if rt_prop:
            value = rt_prop.prop_property().GetAmbient()
            value = min(max(value - 0.01, rt_prop.prop_property().GetAmbientMinValue()),
                        rt_prop.prop_property().GetAmbientMaxValue())
            rt_prop.prop_property().SetAmbient(value)
            view.updateInTime()
            main.statusBar().showMessage('设置环境光 {:.2f}'.format(rt_prop.prop_property().GetAmbient()))
    elif key == '3':
        if rt_prop:
            value = rt_prop.prop_property().GetAmbient()
            value = min(max(value + 0.01, rt_prop.prop_property().GetAmbientMinValue()),
                        rt_prop.prop_property().GetAmbientMaxValue())
            rt_prop.prop_property().SetAmbient(value)
            view.updateInTime()
            main.statusBar().showMessage('设置环境光 {:.2f}'.format(rt_prop.prop_property().GetAmbient()))
    elif key == '4':
        if rt_prop:
            c = QColorDialog.getColor(QColor.fromRgbF(*rt_prop.prop_property().GetDiffuseColor()))
            if c.isValid():
                rt_prop.prop_property().SetDiffuseColor(c.redF(), c.greenF(), c.blueF())
                view.updateInTime()
                main.statusBar().showMessage('设置扩散色 {} {} {}'.format(c.red(), c.green(), c.blue()))
    elif key == '5':
        if rt_prop:
            value = rt_prop.prop_property().GetDiffuse()
            value = min(max(value - 0.01, rt_prop.prop_property().GetDiffuseMinValue()),
                        rt_prop.prop_property().GetDiffuseMaxValue())
            rt_prop.prop_property().SetDiffuse(value)
            view.updateInTime()
            main.statusBar().showMessage('设置扩散光 {:.2f}'.format(rt_prop.prop_property().GetDiffuse()))
    elif key == '6':
        if rt_prop:
            value = rt_prop.prop_property().GetDiffuse()
            value = min(max(value + 0.01, rt_prop.prop_property().GetDiffuseMinValue()),
                        rt_prop.prop_property().GetDiffuseMaxValue())
            rt_prop.prop_property().SetDiffuse(value)
            view.updateInTime()
            main.statusBar().showMessage('设置扩散光 {:.2f}'.format(rt_prop.prop_property().GetDiffuse()))
    elif key == '7':
        if rt_prop:
            value = rt_prop.prop_property().GetSpecular()
            value = min(max(value - 0.01, rt_prop.prop_property().GetSpecularMinValue()),
                        rt_prop.prop_property().GetSpecularMaxValue())
            rt_prop.prop_property().SetSpecular(value)
            view.updateInTime()
            main.statusBar().showMessage('设置反光系数 {:.2f}'.format(rt_prop.prop_property().GetSpecular()))
    elif key == '8':
        if rt_prop:
            value = rt_prop.prop_property().GetSpecular()
            value = min(max(value + 0.01, rt_prop.prop_property().GetSpecularMinValue()),
                        rt_prop.prop_property().GetSpecularMaxValue())
            rt_prop.prop_property().SetSpecular(value)
            view.updateInTime()
            main.statusBar().showMessage('设置反光系数 {:.2f}'.format(rt_prop.prop_property().GetSpecular()))
    elif key == '9':
        if rt_prop:
            value = rt_prop.prop_property().GetSpecularPower()
            value = min(max(value - 1, rt_prop.prop_property().GetSpecularPowerMinValue()),
                        rt_prop.prop_property().GetSpecularPowerMaxValue())
            rt_prop.prop_property().SetSpecularPower(value)
            view.updateInTime()
            main.statusBar().showMessage('设置反光强度 {:.0f}'.format(rt_prop.prop_property().GetSpecularPower()))
    elif key == '0':
        if rt_prop:
            value = rt_prop.prop_property().GetSpecularPower()
            value = min(max(value + 1, rt_prop.prop_property().GetSpecularPowerMinValue()),
                        rt_prop.prop_property().GetSpecularPowerMaxValue())
            rt_prop.prop_property().SetSpecularPower(value)
            view.updateInTime()
            main.statusBar().showMessage('设置反光强度 {:.0f}'.format(rt_prop.prop_property().GetSpecularPower()))
    elif key == '-':
        if rt_prop:
            value = rt_prop.prop_property().GetOpacity()
            value = min(max(value - 0.01, 0), 1)
            rt_prop.prop_property().SetOpacity(value)
            view.updateInTime()
            main.statusBar().showMessage('设置不透明度 {:.2f}'.format(rt_prop.prop_property().GetOpacity()))
    elif key == '=':
        if rt_prop:
            value = rt_prop.prop_property().GetOpacity()
            value = min(max(value + 0.01, 0), 1)
            rt_prop.prop_property().SetOpacity(value)
            view.updateInTime()
            main.statusBar().showMessage('设置不透明度 {:.2f}'.format(rt_prop.prop_property().GetOpacity()))
    elif key == 'Backspace':
        if rt_prop:
            ds = vtk.vtkDepthSortPolyData()
            ds.SetInputData(rt_prop.data())
            ds.SetDirectionToBackToFront()
            ds.SetCamera(view.camera())
            ds.Update()
            rt_prop.setData(ds.GetOutput())
            view.updateInTime()
            main.statusBar().showMessage('透明校正')
    # elif key == '/':
    # elif key == '\\':


def return_globals():
    return globals()


if __name__ == '__main__':
    global original_view, voi_view, spcut_y_views, spcut_z_views, pelvis_view, guide_view
    main = vmi.Main(return_globals)
    main.setAppName('skydio')
    main.setAppVersion('1.0.0')
    main.excludeKeys += ['main', 'shortcuts']

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
        view = vmi.View()
        view.setCamera_Coronal()
        view.setCornerVisible_LeftBottom(False)
        view.mouse['RightButton']['PressRelease'] = []

        props: Dict[vmi.PolyActor, dict] = {}
        rt_prop = None  # 当前模型
        rt_cs = vmi.CS4x4()  # 当前坐标系
        camera_dv, camera_dt = 1, 1
        cs_dv, cs_dt = 1, 1

    main.layout().addWidget(view, 0, 0, 1, 1)

    shortcuts = {'F1': QShortcut(QKeySequence('F1'), view, lambda: on_shortcut(key='F1')),
                 'F2': QShortcut(QKeySequence('F2'), view, lambda: on_shortcut(key='F2')),
                 'F3': QShortcut(QKeySequence('F3'), view, lambda: on_shortcut(key='F3')),
                 'F4': QShortcut(QKeySequence('F4'), view, lambda: on_shortcut(key='F4')),
                 'F5': QShortcut(QKeySequence('F5'), view, lambda: on_shortcut(key='F5')),
                 'Tab': QShortcut(QKeySequence('Tab'), view, lambda: on_shortcut(key='Tab')),
                 'Shift+Tab': QShortcut(QKeySequence('Shift+Tab'), view, lambda: on_shortcut(key='Shift+Tab')),
                 'q': QShortcut(QKeySequence('q'), view, lambda: on_shortcut(key='q')),
                 'w': QShortcut(QKeySequence('w'), view, lambda: on_shortcut(key='w')),
                 'e': QShortcut(QKeySequence('e'), view, lambda: on_shortcut(key='e')),
                 'a': QShortcut(QKeySequence('a'), view, lambda: on_shortcut(key='a')),
                 's': QShortcut(QKeySequence('s'), view, lambda: on_shortcut(key='s')),
                 'd': QShortcut(QKeySequence('d'), view, lambda: on_shortcut(key='d')),
                 'r': QShortcut(QKeySequence('r'), view, lambda: on_shortcut(key='r')),
                 't': QShortcut(QKeySequence('t'), view, lambda: on_shortcut(key='t')),
                 'y': QShortcut(QKeySequence('y'), view, lambda: on_shortcut(key='y')),
                 'f': QShortcut(QKeySequence('f'), view, lambda: on_shortcut(key='f')),
                 'g': QShortcut(QKeySequence('g'), view, lambda: on_shortcut(key='g')),
                 'h': QShortcut(QKeySequence('h'), view, lambda: on_shortcut(key='h')),
                 'u': QShortcut(QKeySequence('u'), view, lambda: on_shortcut(key='u')),
                 'o': QShortcut(QKeySequence('o'), view, lambda: on_shortcut(key='o')),
                 'i': QShortcut(QKeySequence('i'), view, lambda: on_shortcut(key='i')),
                 'k': QShortcut(QKeySequence('k'), view, lambda: on_shortcut(key='k')),
                 'j': QShortcut(QKeySequence('j'), view, lambda: on_shortcut(key='j')),
                 'l': QShortcut(QKeySequence('l'), view, lambda: on_shortcut(key='l')),
                 '[': QShortcut(QKeySequence('['), view, lambda: on_shortcut(key='[')),
                 ']': QShortcut(QKeySequence(']'), view, lambda: on_shortcut(key=']')),
                 ';': QShortcut(QKeySequence(';'), view, lambda: on_shortcut(key=';')),
                 '\'': QShortcut(QKeySequence('\''), view, lambda: on_shortcut(key='\'')),
                 ',': QShortcut(QKeySequence(','), view, lambda: on_shortcut(key=',')),
                 '.': QShortcut(QKeySequence('.'), view, lambda: on_shortcut(key='.')),
                 'z': QShortcut(QKeySequence('z'), view, lambda: on_shortcut(key='z')),
                 'x': QShortcut(QKeySequence('x'), view, lambda: on_shortcut(key='x')),
                 'c': QShortcut(QKeySequence('c'), view, lambda: on_shortcut(key='c')),
                 'v': QShortcut(QKeySequence('v'), view, lambda: on_shortcut(key='v')),
                 'b': QShortcut(QKeySequence('b'), view, lambda: on_shortcut(key='b')),
                 'n': QShortcut(QKeySequence('n'), view, lambda: on_shortcut(key='n')),
                 'm': QShortcut(QKeySequence('m'), view, lambda: on_shortcut(key='m')),
                 '`': QShortcut(QKeySequence('`'), view, lambda: on_shortcut(key='`')),
                 'Ctrl+`': QShortcut(QKeySequence('Ctrl+`'), view, lambda: on_shortcut(key='Ctrl+`')),
                 '1': QShortcut(QKeySequence('1'), view, lambda: on_shortcut(key='1')),
                 '2': QShortcut(QKeySequence('2'), view, lambda: on_shortcut(key='2')),
                 '3': QShortcut(QKeySequence('3'), view, lambda: on_shortcut(key='3')),
                 '4': QShortcut(QKeySequence('4'), view, lambda: on_shortcut(key='4')),
                 '5': QShortcut(QKeySequence('5'), view, lambda: on_shortcut(key='5')),
                 '6': QShortcut(QKeySequence('6'), view, lambda: on_shortcut(key='6')),
                 '7': QShortcut(QKeySequence('7'), view, lambda: on_shortcut(key='7')),
                 '8': QShortcut(QKeySequence('8'), view, lambda: on_shortcut(key='8')),
                 '9': QShortcut(QKeySequence('9'), view, lambda: on_shortcut(key='9')),
                 '0': QShortcut(QKeySequence('0'), view, lambda: on_shortcut(key='0')),
                 '-': QShortcut(QKeySequence('-'), view, lambda: on_shortcut(key='-')),
                 '=': QShortcut(QKeySequence('='), view, lambda: on_shortcut(key='=')),
                 'Backspace': QShortcut(QKeySequence('Backspace'), view, lambda: on_shortcut(key='Backspace')),
                 'p': QShortcut(QKeySequence('p'), view, lambda: on_shortcut(key='p')),
                 '/': QShortcut(QKeySequence('/'), view, lambda: on_shortcut(key='/')),
                 '\\': QShortcut(QKeySequence('\\'), view, lambda: on_shortcut(key='\\'))}

    snapshot_auto = False
    snapshot_i = 0
    snapshot_path = pathlib.Path('./')
    vmi.appexec(main)
    vmi.appexit()
