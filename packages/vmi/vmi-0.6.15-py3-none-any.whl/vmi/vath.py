from typing import Optional, List, Union

import numpy as np
import vtk
import math
import cadquery as cq

import vmi

vmi.CS4x4 = None


class CS4x4:
    """
    坐标系，以4x4矩阵表示的局部坐标系或坐标变换
    """

    def __init__(self, ary=None, axis0: Union[np.ndarray, List[float]] = None,
                 axis1: Union[np.ndarray, List[float]] = None, axis2: Union[np.ndarray, List[float]] = None,
                 origin: Union[np.ndarray, List[float]] = None):
        """
        局部坐标系

        :param axis0: 3x1第一坐标轴，转为齐次坐标构成矩阵的第一行
        :param axis1: 3x1第二坐标轴，转为齐次坐标构成矩阵的第二行
        :param axis2: 3x1第三坐标轴，转为齐次坐标构成矩阵的第三行
        :param origin: 3x1坐标原点，转为齐次坐标构成矩阵的第四行
        """
        self._ary = np.identity(4)
        if ary is not None:
            self.setArray4x4(ary)
        if axis0 is not None:
            self.setAxis(0, axis0)
        if axis1 is not None:
            self.setAxis(1, axis1)
        if axis2 is not None:
            self.setAxis(2, axis2)
        if origin is not None:
            self.setOrigin(origin)

    def __repr__(self):
        return self.array4x4().__repr__()

    def copy(self) -> vmi.CS4x4:
        """
        复制实例

        :return: vmi.CS4x4 - 具有相同矩阵的实例
        """
        cs = CS4x4()
        cs._ary = self._ary.copy()
        return cs

    def workplane(self, local_origin: Union[np.ndarray, List[float]] = (0, 0, 0)) -> cq.Workplane:
        return cq.Workplane(cq.Plane(self.mpt(local_origin).tolist(), self.axis(0).tolist(), self.axis(2).tolist()))

    def array4x4(self) -> np.ndarray:
        """返回矩阵"""
        return self._ary

    def setArray4x4(self, ary: Union[np.ndarray, List[float]] = None):
        """设置矩阵"""
        self._ary = ary.copy()

    def ary4x4inv(self) -> np.ndarray:
        """返回当前矩阵的逆矩阵"""
        return np.linalg.inv(self.array4x4())

    def matrix4x4(self) -> vtk.vtkMatrix4x4:
        """返回当前矩阵的vtk矩阵"""
        ary = self.array4x4()
        matrix = vtk.vtkMatrix4x4()
        for j in range(4):
            for i in range(4):
                matrix.SetElement(j, i, ary[i, j])
        return matrix

    def setMatrix4x4(self, mat: vtk.vtkMatrix4x4 = None):
        """设置vtkMatrix4x4矩阵"""
        ary = np.zeros((4, 4))
        for j in range(4):
            for i in range(4):
                ary[i, j] = mat.GetElement(j, i)

    def mat4x4inv(self) -> vtk.vtkMatrix4x4:
        """返回当前矩阵的vtkMatrix4x4逆矩阵"""
        ary = self.ary4x4inv()
        matrix = vtk.vtkMatrix4x4()
        for j in range(4):
            for i in range(4):
                matrix.SetElement(j, i, ary[i, j])
        return matrix

    def inv(self) -> vmi.CS4x4:
        """返回逆变换"""
        cs = CS4x4()
        cs.setArray4x4(self.ary4x4inv())
        return cs

    def axis(self, i: int) -> np.ndarray:
        """返回第i坐标轴"""
        return self._ary[i][:3]

    def setAxis(self, i: int, arg: Union[np.ndarray, List[float]] = None):
        """设置第i坐标轴"""
        for j in range(3):
            self._ary[i][j] = arg[j]

    def origin(self) -> np.ndarray:
        """返回坐标原点"""
        return self._ary[3][:3]

    def setOrigin(self, arg: Union[np.ndarray, List[float]] = None):
        """设置坐标原点"""
        for j in range(3):
            self._ary[3][j] = arg[j]

    def orthogonalize(self, i_list: List[int]) -> None:
        """
        按照次序列表正交化坐标轴，例如i_list=[0, 2]表示先用z轴y轴正交化x轴，再用x轴y轴正交化z轴

        :param i_list: 坐标轴次序列表
        :return: None
        """
        for i in i_list:
            self.setAxis(i, np.cross(self.axis((i + 1) % 3), self.axis((i + 2) % 3)))

    def normalize(self, i_list: List[int] = None) -> None:
        """
        按照次序列表单位化坐标轴，例如i_list=[0, 2]表示将x轴z轴单位化

        :param i_list: 坐标轴次序列表
        :return: None
        """
        if i_list is None:
            i_list = [0, 1, 2]
        for i in i_list:
            self.setAxis(i, self.axis(i) / np.linalg.norm(self.axis(i)))

    def mpt(self, pt: Union[np.ndarray, List[float]], origin: Union[np.ndarray, List[float]] = None,
            other: Optional[vmi.CS4x4] = None) -> np.ndarray:
        """
        坐标系变换：点pt由当前坐标系变换到世界坐标系，如果设置了other则变换到other坐标系
        坐标变换：世界坐标系中的点pt经过当前变换得到新点，如果设置了origin则在此次计算中原点暂时设为origin

        :param pt: 3x1点坐标
        :param origin: 3x1坐标原点
        :param other: 坐标系
        :return: 变换后坐标
        """
        origin_ = self.origin()
        if origin is not None:
            self.setOrigin(origin)

        pt = np.append(np.array(pt[:3]), 1)
        pt = pt @ self.array4x4()
        if other is not None:
            pt = pt @ other.ary4x4inv()

        if origin is not None:
            self.setOrigin(origin_)
        return pt[:3]

    def mvt(self, vt: Union[np.ndarray, List[float]], other: Optional[vmi.CS4x4] = None) -> np.ndarray:
        """
        坐标系变换：向量vt由当前坐标系变换到世界坐标系，如果设置了other则变换到other坐标系
        坐标变换：世界坐标系中的向量vt经过当前变换，获得新向量

        :param vt: 3x1向量
        :param other: 坐标系
        :return: 变换后坐标
        """
        vt = np.append(np.array(vt[:3]), 0)
        vt = vt @ self.array4x4()
        if other is not None:
            vt = vt @ other.ary4x4inv()
        return vt[:3]

    def mcs(self, cs: vmi.CS4x4):
        """
        坐标系变换：坐标系cs由当前坐标系变换到世界坐标系，如果设置了other则变换到other坐标系
        坐标变换：世界坐标系中的局部坐标系cs经过当前变换得到新坐标系
        """
        cs_ = vmi.CS4x4()
        cs_.setArray4x4(cs.array4x4() @ self.array4x4())
        return cs_

    def translate(self, vt: Union[np.ndarray, List[float]]) -> vmi.CS4x4:
        """
        串接平移变换
        :param vt: 3x1平移变换
        :return: 新坐标系
        """
        mat = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [vt[0], vt[1], vt[2], 1]])
        self.setArray4x4(self.array4x4() @ mat)
        return self

    def rotate(self, angle: float, axis: Union[np.ndarray, List[float]],
               origin: Union[np.ndarray, List[float]] = None) -> vmi.CS4x4:
        """
        串接旋转变换
        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions

        :param angle: 旋转角度（deg）
        :param axis: 3x1旋转轴向量
        :param origin: 3x1旋转轴经过的一点
        :return: 新坐标系
        """
        axis = np.array(axis[:3])
        if np.linalg.norm(axis) == 0:
            raise np.linalg.LinAlgError('旋转轴向错误')

        if origin is None:
            origin = self.origin()

        t = vtk.vtkTransform()
        t.Translate(origin[0], origin[1], origin[2])
        t.RotateWXYZ(angle, axis[0], axis[1], axis[2])
        t.Translate(-origin[0], -origin[1], -origin[2])

        m = vtk.vtkMatrix4x4()
        t.GetMatrix(m)

        ary = np.zeros((4, 4))
        for j in range(4):
            for i in range(4):
                ary[i, j] = m.GetElement(j, i)
        return CS4x4(self.array4x4() @ ary)

    def reflect(self, normal: np.ndarray, origin: Union[np.ndarray, List[float]] = None) -> vmi.CS4x4:
        """
        串接反射变换
        https://en.wikipedia.org/wiki/Reflection_(mathematics)#Reflection_through_a_hyperplane_in_n_dimensions

        :param normal: 反射面法向量
        :param origin: 反射面经过的一点
        :return: 新坐标系
        """
        normal = np.array(normal[:3])
        if np.linalg.norm(normal) == 0:
            raise np.linalg.LinAlgError('反射法向错误')

        mat = np.identity(3) - 2 / np.linalg.norm(normal) ** 2 * np.outer(normal, normal)
        mat = np.hstack((np.vstack((mat, [0, 0, 0])), ([0], [0], [0], [1])))

        cs = self.copy()
        if origin is None:
            cs.setArray4x4(cs.array4x4() @ mat)
        else:
            origin = np.array(origin[:3])
            cs.translate(-origin)
            cs.setArray4x4(cs.array4x4() @ mat)
            cs.translate(origin)
        return cs

    def scale(self, factor: float, origin: Union[np.ndarray, List[float]] = None) -> vmi.CS4x4:
        """
        串接缩放变换

        :param factor: 缩放比例
        :param origin: 缩放投影中心
        :return: 新坐标系
        """
        mat = np.identity(3) * np.array(factor[:3])
        mat = np.hstack((np.vstack((mat, [0, 0, 0])), ([0], [0], [0], [1])))

        cs = self.copy()
        if origin is None:
            cs.setArray4x4(cs.array4x4() @ mat)
        else:
            origin = np.array(origin[:3])
            cs.translate(-origin)
            cs.setArray4x4(cs.array4x4() @ mat)
            cs.translate(origin)
        return cs


def mpt_CS4x4(pt: Union[np.ndarray, List[float]], cs: vmi.CS4x4):
    """
    坐标变换：点pt由世界坐标系变换到新坐标系

    :param pt: 3x1点坐标
    :param cs: 坐标系
    :return: 变换后点坐标
    """
    p_cs = np.append(np.array(pt[:3]), 1)
    p_cs = p_cs @ cs.ary4x4inv()
    p_cs = p_cs[:3]

    return p_cs


def CS4x4_Sagittal() -> CS4x4:
    """返回矢状位观察坐标系"""
    cs = CS4x4(axis0=[0, -1, 0], axis1=[0, 0, -1])
    cs.orthogonalize([2])
    return cs


def CS4x4_Coronal() -> CS4x4:
    """返回冠状位观察坐标系"""
    cs = CS4x4(axis0=[1, 0, 0], axis1=[0, 0, -1])
    cs.orthogonalize([2])
    return cs


def CS4x4_Axial() -> CS4x4:
    """返回横断位观察坐标系"""
    cs = CS4x4(axis0=[1, 0, 0], axis1=[0, 1, 0])
    cs.orthogonalize([2])
    return cs


def CS4x4_Vt(i: int, vt: Union[np.ndarray, List[float]], theta: float = 0) -> CS4x4:
    """
    返回与向量vt与其正交向量组成的坐标系

    :param i: 坐标轴次序
    :param vt: 向量
    :param theta: 绕向量vt的旋转角
    :return: 坐标系
    """
    axes = [np.zeros(3), np.zeros(3), np.zeros(3)]
    axes[i] = np.array(vt)
    r = np.linalg.norm(axes[i])

    if axes[i][0] ** 2 > axes[i][1] ** 2 and axes[i][0] ** 2 > axes[i][2] ** 2:
        x, y, z = 0, 1, 2
    elif axes[i][1] ** 2 > axes[i][2] ** 2:
        x, y, z = 1, 2, 0
    else:
        x, y, z = 2, 0, 1

    a, b, c = axes[i][x] / r, axes[i][y] / r, axes[i][z] / r
    tmp = (a ** 2 + c ** 2) ** 0.5

    if theta != 0:
        sint = np.sin(theta)
        cost = np.cos(theta)

        axes[(i + 1) % 3][x] = (c * cost - a * b * sint) / tmp
        axes[(i + 1) % 3][y] = sint * tmp
        axes[(i + 1) % 3][z] = (-a * cost - b * c * sint) / tmp

        axes[(i + 2) % 3][x] = (-c * sint - a * b * cost) / tmp
        axes[(i + 2) % 3][y] = cost * tmp
        axes[(i + 2) % 3][z] = (a * sint - b * c * cost) / tmp
    else:
        axes[(i + 1) % 3][x] = c / tmp
        axes[(i + 1) % 3][y] = 0
        axes[(i + 1) % 3][z] = -a / tmp

        axes[(i + 2) % 3][x] = -a * b / tmp
        axes[(i + 2) % 3][y] = tmp
        axes[(i + 2) % 3][z] = -b * c / tmp

    return CS4x4(axis0=axes[0], axis1=axes[1], axis2=axes[2])


def CS4x4_InterLandmarks(pts0: List[np.ndarray], pts1: List[np.ndarray]) -> vmi.CS4x4:
    """
    返回对应点列变换，计算点列pts0到点列pts1的最小二乘变换

    :param pts0: 点列
    :param pts1: 点列
    :return: 变换
    """
    if len(pts0) > 2 and len(pts1) > 2:
        pts = [vtk.vtkPoints(), vtk.vtkPoints()]
        for pt in pts0:
            pts[0].InsertNextPoint([pt[0], pt[1], pt[2]])
        for pt in pts1:
            pts[1].InsertNextPoint([pt[0], pt[1], pt[2]])

        lt = vtk.vtkLandmarkTransform()
        lt.SetSourceLandmarks(pts[0])
        lt.SetTargetLandmarks(pts[1])
        lt.SetModeToRigidBody()
        lt.Update()

        mat = vtk.vtkMatrix4x4()
        lt.GetMatrix(mat)

        cs = CS4x4()
        cs.setMatrix4x4(mat)
        return cs


def ptOnPlane(pt: np.ndarray, origin: np.ndarray, normal: np.ndarray) -> np.ndarray:
    """
    计算点到平面投影

    :param pt: 初始点
    :param origin: 相关平面经过一点
    :param normal: 相关平面法向量
    :return: 投影后的点
    """
    pt, origin, normal = np.array(pt), np.array(origin), np.array(normal)
    return pt - normal * np.dot(pt - origin, normal)


def vtOnPlane(vt: np.ndarray, normal: np.ndarray) -> np.ndarray:
    """
    计算向量到平面投影

    :param vt: 初始向量
    :param normal: 相关平面法向量
    :return: 投影后的向量
    """
    vt, normal = np.array(vt), np.array(normal)
    n2 = np.dot(normal, normal)
    n2 = n2 if n2 != 0 else 1
    t = np.dot(vt, normal)
    return vt - t * normal / n2


def vtOnVector(vt: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """
    计算向量到向量投影
    :param vt: 初始向量
    :param vector: 相关向量
    :return: 投影后的向量
    """
    vt, vector = np.array(vt[:3]), np.array(vector[:3])
    dot = np.dot(vector, vector)
    if dot == 0:
        return np.zeros(3)
    return np.dot(vt, vector) / dot * vector


def vtAngle(vt0: Union[np.ndarray, List[float]], vt1: Union[np.ndarray, List[float]]) -> np.ndarray:
    """
    计算两个向量夹角

    :param vt0: 向量0
    :param vt1: 向量1
    :return: 角度
    """
    vt0 = np.array(vt0)
    vt1 = np.array(vt1)
    angle = np.arccos(np.dot(vt0, vt1) / np.linalg.norm(vt0) / np.linalg.norm(vt1))
    angle = np.rad2deg(angle)
    return angle


def coMidPt(p0: Union[np.ndarray, List[float]], p1: Union[np.ndarray, List[float]]):
    """
    计算两个点中点

    :param p0: 坐标点0
    :param p1: 坐标点1
    :return: 中点坐标
    """
    pt = np.array([0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1]), 0.5 * (p0[2] + p1[2])])
    return pt


def coDisToPt(p0: Union[np.ndarray, List[float]], p1: Union[np.ndarray, List[float]]):
    """
    计算两个点距离

    :param p0: 坐标点0
    :param p1: 坐标点1
    :return: 距离
    """
    dis = math.sqrt(math.pow(p0[0] - p1[0], 2) +
                    math.pow(p0[1] - p1[1], 2) +
                    math.pow(p0[2] - p1[2], 2))
    return dis


def rayPlane(plane_origin: Union[np.ndarray, List[float]],
             plane_normal: Union[np.ndarray, List[float]],
             ray_origin: Union[np.ndarray, List[float]],
             ray_vt: Union[np.ndarray, List[float]]) -> Optional[np.ndarray]:
    """
    计算射线与平面交点

    :param plane_origin: 平面过一点
    :param plane_normal: 平面法向量
    :param ray_origin: 射线起点
    :param ray_vt: 射线方向
    :return: 交点坐标，无交点则返回None
    """
    plane_normal, plane_origin = np.array(plane_normal), np.array(plane_origin)
    ray_origin, ray_vt = np.array(ray_origin), np.array(ray_vt)

    if np.linalg.norm(plane_normal) == 0:
        raise Exception('plane_normal is {}'.format(plane_normal))
    if np.linalg.norm(ray_vt) == 0:
        raise Exception('ray_vt is {}'.format(ray_vt))

    ray_vt = ray_vt / np.linalg.norm(ray_vt)

    num = np.dot(plane_normal, plane_origin) - np.dot(plane_normal, ray_origin)
    den = np.dot(plane_normal, ray_vt)

    fabsden = -den if den < 0 else den
    fabstolerance = -num * 1e-6 if num < 0 else num * 1e-6

    if fabsden <= fabstolerance:
        return None

    x = ray_origin + num / den * ray_vt
    return x


def convert_base(number_dec: int, n: int = 36, codec: str = '0123456789abcdefghijklmnopqrstuvwxyz') -> str:
    rem_stack = []
    while number_dec > 0:
        rem = number_dec % n
        rem_stack.append(rem)
        number_dec //= n

    number_n = ""
    while len(rem_stack):
        number_n = number_n + codec[rem_stack.pop()]
    return number_n


def convert_base_inv(number_str: str, n: int = 36, codec: str = '0123456789abcdefghijklmnopqrstuvwxyz') -> int:
    number_dec = 0
    for i in range(len(number_str)):
        x = codec.find(number_str[i])
        if x >= 0:
            number_dec += x * n ** (len(number_str) - i - 1)
        else:
            raise Exception('codec not support')
    return number_dec
