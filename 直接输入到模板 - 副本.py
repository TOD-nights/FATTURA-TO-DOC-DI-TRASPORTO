import fitz  # PyMuPDF
import json
import re
from datetime import datetime

# 自定义数据输入
custom_num = input("请输入发票编号 (num): ")
custom_date = input("请输入日期 (date，格式如 DD/MM/YYYY): ")
custom_pag = input("请输入页码 (pag): ")
colli = input("请输入colli : ")


def parse_line(line):
    pattern = r'^(.*?)\s+(\d+)\s+€\s*([\d,]+)\s+€\s*([\d,]+)\s+(\d+)$'
    match = re.match(pattern, line)

    if match:
        descrizione, quantita, prezzo, importo, iva = match.groups()

        descrizione = descrizione.strip()
        quantita = int(quantita)
        prezzo = float(prezzo.replace(',', '.'))
        importo = float(importo.replace(',', '.'))
        iva = int(iva)

        return {
            "descrizione": descrizione,
            "quantita": quantita,
            "prezzo": prezzo,
            "importo": importo,
            "iva": iva
        }
    return None


# 读取文本内容
text = """GIMI STENDIBIANCHERIA JOLLY 18M 180 € 5,800 € 1.044,00 22
GIMI STENDIBIANCHERIA VIP3 DA PAVIMENTO 60 € 14,500 € 870,00 22
CONTENITORE PORTAOGGETTI PLAST 40*40*30CM 60 € 3,700 € 222,00 22
CONTENITORE PORTAOGGETTI PLAST 70*50*40CM 50 € 5,500 € 275,00 22
CONTENITORE PORTAOGGETTI PLAST 100*60*40CM 60 € 7,800 € 468,00 22
VILEDA BASTONE PER SCOPA IN ALLUMINIO 120CM 200 € 1,100 € 220,00 22
VILEDA SCIOA 2IN1 CLASSICO 14.5*34*5.5 CM 100 € 3,950 € 395,00 22
VILEDA TURBO MOP EASY WRING COMPLETO 30 € 26,500 € 795,00 22
VILEDA TURBO 2IN 1 FIOCCO RICAMBIO 30 € 8,800 € 264,00 22
VILEDA SUPER MOCIO 3 ACTION 50 € 1,650 € 82,50 22
VILEDA SUPER MOCIO SOFT FIOCCO 50 € 1,700 € 85,00 22
BIB SCOPA TESTA ROSSA PER PAV,ì. 200 € 0,750 € 150,00 22
BIB BASTONE SCOPA IN ALLUMINIO 110CM 200 € 0,900 € 180,00 22
INTEX SPUGNA ANTIGRASSO MULTI POWER 6PZ 100 € 1,500 € 150,00 22
SET 10PZ SPUGNETTE DA CUCINA A 2 LATI 75*50*28mm 100 € 2,200 € 220,00 22
SPUGNA ABRASIVA RESISTENTE 10PZ 100 € 1,800 € 180,00 22
PANNO PREMIUM IN MICROFIBRA 60 € 1,500 € 90,00 22
VILEDA GLITZI CRYSTAL SPUGNA DA CUCINA 3PZ 60 € 0,680 € 40,80 22
PATTUMIERA A PEDALE CON SECCHIO INTERNO 10L 50 € 4,200 € 210,00 22
BELLI E FORTI PATTUMIERA PER RICLO IDIFFERENZIATA NERO/GRIOGIO 50L 50 € 6,500 € 325,00 22
POKER BAMA PATTUMIERA DIFFERENZIATA 4PZ COLORI ASS 30 € 19,000 € 570,00 22
PATTUMIERA ROTONDO A PEDALE IN ACCIAIO 30L 10 € 23,000 € 230,00 22
PATTUMIERA ROTONDO A PEDALE IN ACCIAIO 5L 20 € 3,500 € 70,00 22
SACCHI SPAZZATURA ALTA RESISTENZA BLU 50*60CM 20PZ 90 € 0,330 € 29,70 22
SACCHI SPAZZATURA ALTA RESISTENZA GIALLO 50*60CM 20PZ 90 € 0,330 € 29,70 22
SACCHI SPAZZATURA ALTA RESISTENZA LILLA 50*60CM 20PZ 90 € 0,330 € 29,70 22
SACCHI SPAZZATURA ALTA RESISTENZA TRASPARENTE 50*60CM 20PZ 90 € 0,330 € 29,70 22
SACCHI SPAZZATURA ALTA RESISTENZA BLU 70*110CM 20PZ 60 € 0,590 € 35,40 22
SACCHI SPAZZATURA ALTA RESISTENZA LILLA 70*110CM 20PZ 60 € 0,590 € 35,40 22
SACCHI SPAZZATURA ALTA RESISTENZA GIALLO 70*110CM 20PZ 60 € 0,590 € 35,40 22
SACCHI SPAZZATURA ALTA RESISTENZA TRASPARENTE70*110CM 20PZ 60 € 0,590 € 35,40 22
SACCHI SPAZZATURA NERO 90*120CM 10PZ 60 € 3,900 € 234,00 22
SACCHI SPAZZATURA GRANDI NERO SUPER RESISTENTE 120L 60 € 3,960 € 237,60 22
"""

# 分割文本为行
lines = text.split('\n')

# 解析每一行并存储结果
invoice_data = []
current_item = {}

for line in lines:
    parsed = parse_line(line)
    if parsed:
        if current_item:
            invoice_data.append(current_item)
        current_item = parsed
    elif current_item:
        current_item['descrizione'] += ' ' + line.strip()

# 添加最后一个项目
if current_item:
    invoice_data.append(current_item)

# Load the confezione PDF
confezione_path = r"路单模板.pdf"
output_path = r"3.pdf"
confezione_pdf = fitz.open(confezione_path)


def add_page_content(page, items, start_index, page_num):
    # 添加公司信息和自定义数据
    add_company_info(page)
    add_custom_data(page, page_num)

    # 添加发票项目
    x_start_nr = 50
    x_start_descrizione = 90
    x_start_quantita = 400
    x_start_prezzo = 450
    x_start_importo = 480
    x_start_iva = 530
    y_start = 290
    line_height = 15

    y_position = y_start
    for i, item in enumerate(items, start=start_index):
        page.insert_text((x_start_nr, y_position), str(i), fontsize=8, fontname="helv")
        page.insert_text((x_start_descrizione, y_position), item['descrizione'], fontsize=8, fontname="helv")
        page.insert_text((x_start_quantita, y_position), str(item['quantita']), fontsize=8, fontname="helv")
        page.insert_text((x_start_prezzo, y_position), f" {item['prezzo']:.2f} E", fontsize=8, fontname="helv")
        page.insert_text((x_start_importo, y_position), f" {item['importo']:.2f} E", fontsize=8, fontname="helv")
        page.insert_text((x_start_iva, y_position), str(item['iva']), fontsize=8, fontname="helv")
        y_position += line_height


def add_company_info(page):
    right_company_info = """UNIQUE SRL
VIA DANTE ALIGHIERI, 163
33013 GEMONA DEL FRIULI (UD)
C.F./P.Iva 03067400303"""

    left_company_info = """LEMON SRLS
VIA BRAMANTINO, 9 - 20155 MILANO (MI)
C.F./P.Iva 13188040961 
"""

    page.insert_text((50, 50), left_company_info, fontsize=10, fontname="helv")

    right_margin = 50
    page_width = page.rect.width
    right_align_x = page_width - right_margin

    for i, line in enumerate(right_company_info.split('\n')):
        text_width = fitz.get_text_length(line, fontname="helv", fontsize=10)
        x = right_align_x - text_width
        y = 50 + i * 15
        page.insert_text((x, y), line, fontsize=10, fontname="helv")


def add_custom_data(page, page_num):
    page.insert_text((210, 143), f" {custom_num}", fontsize=10, fontname="helv")
    page.insert_text((265, 143), f" {custom_date}", fontsize=10, fontname="helv")
    page.insert_text((350, 163), f" {colli}", fontsize=10, fontname="helv")


    # 将页码放在右下角
    page_width = page.rect.width
    page_height = page.rect.height
    pag_text = f"Pag. {page_num}/{total_pages}"
    x = page_width - 50  # 距离右边 50 点
    y = page_height - 30  # 距离底部 30 点
    page.insert_text((x, y), pag_text, fontsize=10, fontname="helv")


# 计算总页数
total_pages = (len(invoice_data) + 23) // 24

# 创建一个新的PDF文档
output_pdf = fitz.open()

# 复制模板页面到新文档
output_pdf.insert_pdf(confezione_pdf, from_page=0, to_page=0)

# 添加第一页内容
page1 = output_pdf[0]
add_page_content(page1, invoice_data[:24], 1, 1)

# 如果有超过24个项目，添加额外的页面
for i in range(1, total_pages):
    start_index = i * 24
    end_index = min((i + 1) * 24, len(invoice_data))

    # 复制第一页作为新页面的模板
    output_pdf.insert_pdf(confezione_pdf, from_page=0, to_page=0)
    new_page = output_pdf[-1]  # 获取刚刚添加的页面

    # 在新页面上添加内容
    add_page_content(new_page, invoice_data[start_index:end_index], start_index + 1, i + 1)

# Save the modified PDF
output_pdf.save(output_path)
output_pdf.close()
confezione_pdf.close()

print(f"Modified PDF saved to {output_path}")