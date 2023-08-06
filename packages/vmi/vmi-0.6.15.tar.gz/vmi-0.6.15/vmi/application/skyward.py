import base64
import csv
import hashlib
import os
import pathlib
import tempfile
import time
from typing import Optional, Union

import gridfs
import pydicom
import pymongo
import requests
from PySide2.QtWidgets import *

import vmi

client = pymongo.MongoClient('mongodb://skyward:Yw#309309@skyw.ltd:18027/skyward')
database = client.skyward
case_db = database.get_collection('case')
order_db = database.get_collection('order')
user_db = database.get_collection('user')
role_customer_db = database.get_collection('role_customer')
role_sales_worker_db = database.get_collection('role_sales_worker')
role_product_designer_db = database.get_collection('role_product_designer')
role_order_reviewer_db = database.get_collection('role_order_reviewer')
role_machine_operator_db = database.get_collection('role_machine_operator')
role_admin_db = database.get_collection('role_admin')
dicom_fs = gridfs.GridFS(database, collection='dicom')
vti_fs = gridfs.GridFS(database, collection='vti')
vtp_fs = gridfs.GridFS(database, collection='vtp')
stl_fs = gridfs.GridFS(database, collection='stl')


def ask_user() -> Optional[dict]:
    ok, find_user = True, {}
    while ok:
        text, ok = QInputDialog.getText(None, '请输入', '手机号：', QLineEdit.Normal)
        if not ok:
            return None

        find_user = user_db.find_one({'telephone': text})
        if not find_user:
            vmi.askInfo('手机号未注册')
            ok = True
            continue

        ok = False

    ok = True
    while ok:
        text, ok = QInputDialog.getText(None, '请输入', '密码：', QLineEdit.Password)
        if not ok:
            return None

        if find_user['password'] != hashlib.md5(text.encode()).hexdigest():
            vmi.askInfo('密码错误')
            ok = True
            continue

        ok = False
    return find_user


def ask_customer_id() -> Optional[dict]:
    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('选择顾客')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)

    customer_combo = QComboBox()
    dialog.layout().addWidget(customer_combo)

    for i in role_customer_db.find():
        customer_combo.addItem('{} {} {}'.format(i['_id'], i['name'], i['organization']), i['_id'])

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() == QDialog.Accepted:
        return customer_combo.currentData()
    else:
        return None


def ask_sales_worker_id() -> Optional[dict]:
    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('选择销售')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)

    sales_worker_combo = QComboBox()
    dialog.layout().addWidget(sales_worker_combo)

    for i in role_sales_worker_db.find():
        sales_worker_combo.addItem('{} {} {}'.format(i['_id'], i['name'], i['organization']), i['_id'])

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() == QDialog.Accepted:
        return sales_worker_combo.currentData()
    else:
        return None


def dicom_kw_value(f: str) -> dict:
    kw_value = {}
    with pydicom.dcmread(f) as ds:
        for e in ds.iterall():
            if e.value.__class__ in [None, bool, int, float, str]:
                kw_value[e.keyword] = e.value
            elif e.value.__class__ in [bytes]:
                kw_value[e.keyword] = '{} bytes'.format(len(e.value))
            else:
                kw_value[e.keyword] = str(e.value)
    return {kw: kw_value[kw] for kw in sorted(kw_value)}


def case(product_name: str, product_model: str, product_specification: str,
         order_uid: str, order_files: list,
         patient_name: str, patient_sex: str, patient_age: str,
         dicom_files: dict, vti_files: dict, vtp_files: dict, stl_files: dict,
         snapshot_list: list, **kwargs) -> Optional[dict]:
    """
    构造本地案例
    :param product_name: 产品名称
    :param product_model: 产品型号
    :param product_specification: 产品规格
    :param order_uid: 产品序列号
    :param order_files: 产品文件列表
    :param patient_name: 患者姓名
    :param patient_sex: 患者性别
    :param patient_age: 患者年龄
    :param dicom_files: 原始DICOM文件，每个关键词索引一个文件列表
    :param vti_files: vtkXMLImageData格式文件，每个关键词索引一个文件
    :param vtp_files: vtkXMLPolyData格式文件，每个关键词索引一个文件
    :param stl_files: STL格式文件，每个关键词索引一个文件
    :param snapshot_list: 快照列表
    :param kwargs: 其它相关信息，每个关键词索引一个支持数据库直接录入的对象
    :return: 案例信息
    """
    case_data = {}

    # 上传原始DICOM文件
    for kw in dicom_files:
        sop_uids = []
        for f in dicom_files[kw]:
            sop_uid = pydicom.dcmread(f).SOPInstanceUID
            sop_uids.append(sop_uid)

            if not dicom_fs.exists({'SOPInstanceUID': sop_uid}):
                dicom_fs.put(open(f, 'rb').read(), **dicom_kw_value(f))
        case_data[kw] = sop_uids

    # 上传其它格式文件
    files = [vti_files, vtp_files, stl_files]
    fs = [vti_fs, vtp_fs, stl_fs]
    for i in range(len(files)):
        for kw in files[i]:
            f_bytes = open(files[i][kw], 'rb').read()
            md5 = hashlib.md5(f_bytes).hexdigest()

            if fs[i].exists({'md5': md5}):
                case_data[kw] = fs[i].find_one({'md5': md5})._id
            else:
                case_data[kw] = fs[i].put(f_bytes)

    # 上传其它信息
    case_data['product_name'] = product_name
    case_data['product_model'] = product_model
    case_data['product_specification'] = product_specification
    case_data['order_uid'] = order_uid
    case_data['order_files'] = order_files
    case_data['patient_name'] = patient_name
    case_data['patient_sex'] = patient_sex
    case_data['patient_age'] = patient_age
    case_data['snapshot'] = snapshot_list

    for kw in kwargs:
        case_data[kw] = kwargs[kw]
    return case_data


def case_sync(case: dict, ukw: list) -> Union[dict, bool]:
    """
    同步案例
    :param case: 本地案例信息
    :param ukw: 特征键列表，用于判断相同案例
    :return: 同步后的案例信息
    """
    ukw_value = {kw: case[kw] for kw in ukw}

    # 清理相同无效案例
    for c in case_db.find(ukw_value):
        if 'case_uid' not in c:
            case_db.delete_one({'_id': c['_id']})

    # 查找相同有效案例
    find = case_db.find_one(ukw_value)

    if find and 'case_uid' in find:
        if find['customer_confirmed']:
            vmi.askInfo('顾客已确认')
        r = vmi.askButtons(['上传案例'])
    else:
        r = vmi.askButtons(['创建案例'])

    if r == '创建案例':
        user = ask_user()
        if not user:
            return False

        role_product_designer_id = user['role_product_designer_id']
        if not role_product_designer_db.find_one({'_id': role_product_designer_id}):
            vmi.askInfo('错误：只有产品设计师可以创建案例')
            return False

        customer_uid = ask_customer_id()
        if not customer_uid:
            return False

        sales_worker_uid = ask_sales_worker_id()
        if not sales_worker_uid:
            return False

        case['role_product_designer_id'] = role_product_designer_id
        case['role_customer_id'] = customer_uid
        case['role_sales_worker_id'] = sales_worker_uid
        case['role_order_reviewer_id'] = ''
        case['order_reviewed'] = False

        _id = case_db.insert_one({kw: case[kw] for kw in sorted(case)}).inserted_id
        try:
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='https://skyw.ltd/skyward/sys/caseCreate',
                                     headers={'_id': str(_id), 'case_uid': case_uid})
            if response.text == 'true':
                find = case_db.find_one({'_id': _id})
                if 'case_uid' in find:
                    return True
                else:
                    case_db.delete_one({'_id': _id})
                    vmi.askInfo('错误：云端未分配编号')
            else:
                case_db.delete_one({'_id': _id})
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            case_db.delete_one({'_id': _id})
            vmi.askInfo('错误：' + str(e))
    elif r == '上传案例':
        user = ask_user()
        if not user:
            return False

        role_product_designer_id = user['role_product_designer_id']
        if not role_product_designer_db.find_one({'_id': role_product_designer_id}):
            vmi.askInfo('错误：只有产品设计师可以上传案例')
            return False

        case['role_product_designer_id'] = role_product_designer_id
        case['order_reviewed'] = False

        try:
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='https://skyw.ltd/skyward/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case})
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))
    elif r == '下载案例':
        return case_db.find_one({'_id': find['_id']})


def order_review_docx(reviewer_id: str, order_uid: str, file: str):
    case = case_db.find_one({'order_uid': order_uid})

    with tempfile.TemporaryDirectory() as p:
        doc = vmi.docx_document('工单')
        vmi.docx_section_landscape_A4(doc.sections[0])
        vmi.docx_section_margin_middle(doc.sections[0])
        vmi.docx_section_header(doc.sections[0])

        s_title = vmi.docx_style(doc, '影为标题', 'Normal', size=26, alignment='CENTER')
        s_header = vmi.docx_style(doc, '影为页眉', 'Header', size=10)
        s_body_left = vmi.docx_style(doc, '影为正文', 'Body Text')
        s_body_left_indent = vmi.docx_style(doc, '影为正文首行缩进', 'Body Text', first_line_indent=2)
        s_body_center = vmi.docx_style(doc, '影为正文居中', 'Body Text', alignment='CENTER')
        s_table = vmi.docx_style(doc, '影为表格', 'Table Grid', alignment='CENTER')

        doc.sections[0].header.paragraphs[0].text = '工单号：{}\t\t\t\t{}'.format(case['order_uid'], 'R1-TS-SOP-0101')
        doc.sections[0].header.paragraphs[0].style = s_header

        def add_row_text(table, texts, styles, merge=None):
            r = len(table.add_row().table.rows) - 1
            if merge is not None:
                table.cell(r, merge[0]).merge(table.cell(r, merge[1]))
            for c in range(min(len(table.columns), len(texts))):
                table.cell(r, c).paragraphs[0].text = texts[c]
                table.cell(r, c).paragraphs[0].style = styles[c]

        def add_row_picture(table, text, styles, pic_file):
            r = len(table.add_row().table.rows) - 1
            table.cell(r, 1).merge(table.cell(r, 3))
            table.cell(r, 0).paragraphs[0].text = text
            table.cell(r, 0).paragraphs[0].style = styles[0]
            table.cell(r, 1).paragraphs[0].style = styles[1]

            with open(pic_file, 'rb') as pic:
                table.cell(r, 1).paragraphs[0].add_run().add_picture(pic, width=table.cell(r, 1).width * 0.7)

        body_table = doc.add_table(1, 4, s_table)
        body_table.autofit = True
        body_table.alignment = vmi.docx.enum.table.WD_TABLE_ALIGNMENT.CENTER

        body_table.cell(0, 0).merge(body_table.cell(0, 3))
        body_table.cell(0, 0).paragraphs[0].text = '髋关节手术导板（TH）工单'
        body_table.cell(0, 0).paragraphs[0].style = s_title

        add_row_text(body_table, ['产品名称\nProduct name', case['product_name'],
                                  '型号\nModel', case['product_model']], [s_body_center] * 4)

        customer_name = role_customer_db.find_one({'_id': case['role_customer_id']})['name']
        add_row_text(body_table, ['顾客\nCustomer', '{}\n{}'.format(customer_name, case['role_customer_id']),
                                  '规格\nSpecification', case['product_specification']], [s_body_center] * 4)

        design_time = time.localtime(vmi.convert_base_inv(order_uid[-8:].lower()) / 100)
        design_time = time.strftime('%Y/%m/%d %H:%M:%S', design_time)
        designer_name = role_product_designer_db.find_one({'_id': case['role_product_designer_id']})['name']

        add_row_text(body_table, [
            '产品设计师\nProduct designer', '{}\n{}'.format(designer_name, case['role_product_designer_id']),
            '设计时间\nDesign time', design_time], [s_body_center] * 4)
        add_row_text(body_table, [
            '软件名称\nSoftware name', case['app_name'],
            '软件版本\nSoftware version', case['app_version']], [s_body_center] * 4)

        info = case['pelvis_dicom_info']
        text = '姓名：{}\t性别：{}\t年龄：{}'.format(case['patient_name'], case['patient_sex'], case['patient_age'])
        text += '\n模态：{}\t日期：{}\t描述：{}'.format(info['Modality'], info['StudyDate'], info['StudyDescription'])
        text += '\n分辨率：{}\t体素间距：{}'.format(info['Resolution'], info['Spacing'])
        add_row_text(body_table, ['影像输入\nRadiological input', text], [s_body_center, s_body_left], [1, 3])

        text = '手术侧：{}'.format(case['surgical_side'])
        text += '\n髋臼杯半径：{:.0f} mm\t影像学前倾角：{:.1f}°\t影像学外展角：{:.1f}°'.format(
            case['cup_radius'], case['cup_RA'], case['cup_RI'])
        add_row_text(body_table, ['临床输入\nClinical input', text], [s_body_center, s_body_left], [1, 3])

        text = '主体方位：{:.0f}°，主体长径：{:.0f} mm，主体短径：{:.0f} mm，旋臂长度：{:.0f} mm，匹配方式：{}'.format(
            case['body_angle'], case['body_xr'], case['body_yr'], case['arm_length'], case['match_style'])
        add_row_text(body_table, ['造型输入\nModeling input', text], [s_body_center, s_body_left], [1, 3])

        png = pathlib.Path(p) / '.png'
        for i in range(len(case['snapshot'])):
            png.write_bytes(case['snapshot'][i])
            add_row_picture(body_table, '快照（{}/{}）\nSnapshot'.format(i + 1, len(case['snapshot'])),
                            [s_body_center, s_body_center], png)

        doc.add_page_break()

        foot_table = doc.add_table(1, 4, s_table)
        foot_table.autofit = True
        foot_table.alignment = vmi.docx.enum.table.WD_TABLE_ALIGNMENT.CENTER

        foot_table.cell(0, 1).merge(foot_table.cell(0, 3))
        foot_table.cell(0, 0).paragraphs[0].text = '评审结果'
        foot_table.cell(0, 0).paragraphs[0].style = s_body_center
        foot_table.cell(0, 1).paragraphs[0].text = '（通过/不通过）' + '\n' * 18
        foot_table.cell(0, 1).paragraphs[0].style = s_body_left

        reviewer = role_order_reviewer_db.find_one({'_id': reviewer_id})['name']
        add_row_text(foot_table, ['评审员/日期', '（{}）'.format(reviewer) + '\n' * 2],
                     [s_body_center, s_body_left], [1, 3])

        try:
            doc.save(file)
        except PermissionError as e:
            vmi.askInfo(str(e))


def order_review():
    combo = QComboBox()
    for case in case_db.find():
        customer = role_customer_db.find_one({'_id': case['role_customer_id']})
        sales_worker = role_sales_worker_db.find_one({'_id': case['role_sales_worker_id']})
        product_designer = role_product_designer_db.find_one({'_id': case['role_product_designer_id']})
        order_reviewer = role_order_reviewer_db.find_one({'_id': case['role_order_reviewer_id']})

        text = ' 已确认' if case['customer_confirmed'] else ' 未确认'
        text += ' 已评审' if case['order_reviewed'] else ' 未评审'
        text += ' 工单 ' + case['order_uid']
        text += ' 患者 ' + case['patient_name']
        text += ' 顾客 ' + (customer['name'] if customer else '无')
        text += ' 销售 ' + (sales_worker['name'] if sales_worker else '无')
        text += ' 设计 ' + (product_designer['name'] if product_designer else '无')
        text += ' 评审 ' + (order_reviewer['name'] if order_reviewer else '无')

        combo.addItem(text, case['order_uid'])

    if not combo.count():
        vmi.askInfo('无工单')
        return

    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('评审工单')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)
    dialog.layout().addWidget(combo)

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() != QDialog.Accepted:
        return

    order_uid = combo.currentData()

    r = vmi.askButtons(['下载工单', '完成评审'])
    if r == '下载工单':
        user = ask_user()
        if not user:
            return False

        role_order_reviewer_id = user['role_order_reviewer_id']
        if not role_order_reviewer_db.find_one({'_id': role_order_reviewer_id}):
            vmi.askInfo('错误：只有评审人员可以下载工单')
            return False

        p = vmi.askDirectory('设计文件夹')
        if not p:
            return

        f = '{} {}.docx'.format(order_uid, time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
        f = pathlib.Path(p) / f
        order_review_docx(role_order_reviewer_id, order_uid, str(f))
        vmi.askInfo('下载完成')
    elif r == '完成评审':
        user = ask_user()
        if not user:
            return False

        role_order_reviewer_id = user['role_order_reviewer_id']
        if not role_order_reviewer_db.find_one({'_id': role_order_reviewer_id}):
            vmi.askInfo('错误：只有评审人员可以完成评审')
            return False

        case_set = {'role_order_reviewer_id': role_order_reviewer_id,
                    'order_reviewed': True}

        try:
            find = case_db.find_one({'order_uid': combo.currentData()})
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='https://skyw.ltd/skyward/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case_set})
                vmi.askInfo('同步完成')
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))


def order_download():
    combo = QComboBox()
    for case in case_db.find():
        customer = role_customer_db.find_one({'_id': case['role_customer_id']})
        sales_worker = role_sales_worker_db.find_one({'_id': case['role_sales_worker_id']})
        product_designer = role_product_designer_db.find_one({'_id': case['role_product_designer_id']})
        order_reviewer = role_order_reviewer_db.find_one({'_id': case['role_order_reviewer_id']})

        text = ' 已确认' if case['customer_confirmed'] else ' 未确认'
        text += ' 已评审' if case['order_reviewed'] else ' 未评审'
        text += ' 工单 ' + case['order_uid']
        text += ' 患者 ' + case['patient_name']
        text += ' 顾客 ' + (customer['name'] if customer else '无')
        text += ' 销售 ' + (sales_worker['name'] if sales_worker else '无')
        text += ' 设计 ' + (product_designer['name'] if product_designer else '无')
        text += ' 评审 ' + (order_reviewer['name'] if order_reviewer else '无')

        combo.addItem(text, case['order_uid'])

    if not combo.count():
        vmi.askInfo('无工单')
        return

    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('下载设计文件')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)
    dialog.layout().addWidget(combo)

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() != QDialog.Accepted:
        return

    order_uid = combo.currentData()

    r = vmi.askButtons(['下载设计文件'])
    if r == '下载设计文件':
        user = ask_user()
        if not user:
            return False

        role_machine_operator_id = user['role_machine_operator_id']
        if not role_machine_operator_db.find_one({'_id': role_machine_operator_id}):
            vmi.askInfo('错误：只有设备操作员可以下载设计文件')
            return False

        p = vmi.askDirectory('设计文件夹')
        if not p:
            return

        case = case_db.find_one({'order_uid': order_uid})

        for f in case['order_files']:
            if f.endswith('stl'):
                if not stl_fs.find_one({'_id': case[f]}):
                    vmi.askInfo('错误：设计文件不存在 {}'.format(f))
                    return

        p = pathlib.Path(p) / (order_uid + ' ' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
        os.mkdir(p)

        for f in case['order_files']:
            if f.endswith('stl'):
                b = stl_fs.find_one({'_id': case[f]}).read()
                (pathlib.Path(p) / (f + '.stl')).write_bytes(b)

        vmi.askInfo('下载完成')


def csv_update(db: str):
    user = ask_user()
    if not user:
        return False

    role_admin_id = user['role_admin_id']
    if not role_admin_db.find_one({'_id': role_admin_id}):
        vmi.askInfo('错误：只有管理员可以更新角色信息')
        return False

    f = vmi.askOpenFile('*.csv', db)
    if f is None:
        return

    db = database.get_collection(db)

    with open(f, newline='') as f:
        kw = []
        for row in csv.reader(f):
            if len(kw):
                kw[0] = '_id'
                i = dict(zip(kw, row))
                db.find_one_and_update({'_id': i['_id']}, {'$set': i}, upsert=True)
            else:
                kw = row.copy()


if __name__ == '__main__':
    vmi.app.setApplicationName('Skyward')
    vmi.app.setApplicationVersion('1.1.1')
    vmi.app.setQuitOnLastWindowClosed(False)


    def csv_update_role_customer():
        csv_update('role_customer')


    def csv_update_role_sales_worker():
        csv_update('role_sales_worker')


    def csv_update_role_product_designer():
        csv_update('role_product_designer')


    def csv_update_role_order_reviewer():
        csv_update('role_order_reviewer')


    def csv_update_role_machine_operator():
        csv_update('role_machine_operator')


    tray_icon_menu = QMenu()
    tray_icon_menu.addSection('工单评审员')
    tray_icon_menu.addAction('评审工单').triggered.connect(order_review)
    tray_icon_menu.addSection('设备操作员')
    tray_icon_menu.addAction('下载设计文件').triggered.connect(order_download)
    tray_icon_menu.addSection('系统')
    admin_menu = QMenu('管理')
    admin_menu.addAction('更新顾客').triggered.connect(csv_update_role_customer)
    admin_menu.addAction('更新销售人员').triggered.connect(csv_update_role_sales_worker)
    admin_menu.addAction('更新产品设计师').triggered.connect(csv_update_role_product_designer)
    admin_menu.addAction('更新工单评审员').triggered.connect(csv_update_role_order_reviewer)
    admin_menu.addAction('更新设备操作员').triggered.connect(csv_update_role_machine_operator)
    tray_icon_menu.addMenu(admin_menu)
    tray_icon_menu.addAction('关于').triggered.connect(vmi.app_about)
    tray_icon_menu.addAction('退出').triggered.connect(vmi.app.quit)

    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QWidget().style().standardIcon(QStyle.SP_ComputerIcon))
    tray_icon.setToolTip('{} {}'.format(vmi.app.applicationName(), vmi.app.applicationVersion()))
    tray_icon.setContextMenu(tray_icon_menu)
    tray_icon.show()

    vmi.app.exec_()
    vmi.appexit()
