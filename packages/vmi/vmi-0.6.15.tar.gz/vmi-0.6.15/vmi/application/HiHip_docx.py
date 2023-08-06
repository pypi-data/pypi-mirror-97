import vmi


def save_docx():
    doc = vmi.docx_document('二维规划报告')
    vmi.docx_section_landscape_A4(doc.sections[0])
    vmi.docx_section_margin_middle(doc.sections[0])
    vmi.docx_section_header(doc.sections[0])

    s_title = vmi.docx_style(doc, '影为标题', 'Normal', size=26, alignment='CENTER')
    s_header = vmi.docx_style(doc, '影为页眉', 'Header', size=10)
    s_body_left = vmi.docx_style(doc, '影为正文', 'Body Text')
    s_body_left_indent = vmi.docx_style(doc, '影为正文首行缩进', 'Body Text', first_line_indent=2)
    s_body_center = vmi.docx_style(doc, '影为正文居中', 'Body Text', alignment='CENTER')
    s_table = vmi.docx_style(doc, '影为表格', 'Table Grid', alignment='CENTER')

    doc.sections[0].header.paragraphs[0].text = '影为医疗科技（上海）有限公司\t\t\t\t{}'.format('[表单号]')
    doc.sections[0].header.paragraphs[0].style = s_header

    def add_row_text(table, texts, styles, merge=None):
        r = len(table.add_row().table.rows) - 1
        if merge is not None:
            table.cell(r, merge[0]).merge(table.cell(r, merge[1]))
        for c in range(min(len(table.columns), len(texts))):
            table.cell(r, c).paragraphs[0].text = texts[c]
            table.cell(r, c).paragraphs[0].style = styles[c]

    doc_table = doc.add_table(1, 4, s_table)
    doc_table.autofit = True
    doc_table.alignment = vmi.docx.enum.table.WD_TABLE_ALIGNMENT.CENTER

    doc_table.cell(0, 0).merge(doc_table.cell(0, 3))
    doc_table.cell(0, 0).paragraphs[0].text = '二维规划报告\n2D Planning Report'
    doc_table.cell(0, 0).paragraphs[0].style = s_title

    add_row_text(doc_table, ['顾客名称\nCustomer name', '',
                             '顾客编号\nCustomer number', ''], [s_body_center] * 4)
    add_row_text(doc_table, ['医师\nPhysician', '',
                             '电邮\nEmail', ''], [s_body_center] * 4)
    add_row_text(doc_table, ['联系人\nContact', '',
                             '电话\nPhone number', ''], [s_body_center] * 4)

    doc.save('C:/Users/YW/Desktop/test_docx.docx')


if __name__ == '__main__':
    save_docx()
