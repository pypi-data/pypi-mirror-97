import vmi

# 创建视图，设置冠状位相机
view = vmi.View()
view.setCamera_Coronal()

# 创建局部坐标系
cs = vmi.CS4x4(axis0=[1, 0, 0], axis1=[0, 0, 1], axis2=[0, -1, 0])

# 创建文字形状
shape = cs.workplane().text('Hello World', 10, 1).val().wrapped

# 创建场景对象
prop = vmi.PolyActor(view, color=[1, 0.6, 0.6])
prop.setData(shape)

# 重置相机适应场景大小
view.setCamera_FitAll()

# 启动主程序
vmi.appexec(view)

# 退出主程序
vmi.appexit()
