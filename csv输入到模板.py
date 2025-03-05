import fitz  # PyMuPDF
import csv
from datetime import datetime
import fitz  # PyMuPDF库，用于处理PDF文件
import re
from datetime import datetime, timedelta


pdf_path = "da_1736505411071..pdf"
csv_file_path = r"E:\studio\info\Python\progetti\模板\da_1736505411071.csv"
# custom_num = input("请输入发票编号 (num): ")
# custom_date = input("请输入日期 (date，格式如 DD/MM/YYYY): ")
#custom_pag = input("请输入页码 (pag): ")

right_company_info = """PLENA SRL
 VIA COMO 10
 20063  CERNUSCO SUL NAVIGLIO  (MI)
  C.F./P.Iva 11427570962
    """

# 定义一个函数，从PDF中提取日期和发票编号
def extract_date_and_number_from_pdf(pdf_path):
    # 打开PDF文件
    doc = fitz.open(pdf_path)

    # 用于存储提取的文本
    extracted_text = []

    # 遍历每一页并提取文本
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        extracted_text.append(text)

    # 关闭PDF文件
    doc.close()

    # 合并所有页的文本内容
    full_text = "\n".join(extracted_text)

    content_length = len(full_text)



    # 正则表达式匹配日期（格式为DD/MM/YYYY）
    date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"
    date_match = re.search(date_pattern, full_text)
    extracted_date = date_match.group(1) if date_match else None

    # 正则表达式匹配发票编号（假设发票编号是一个数字）
    num_pattern = r"\bPrezzo\s*(\d+)\b"
    num_match = re.search(num_pattern, full_text)
    extracted_num = int(num_match.group(1)) if num_match else None

    return extracted_num, extracted_date, content_length


# 函数将日期往前推几天，排除周末
def adjust_date(date_str, days_to_subtract):
    # 将字符串日期转换为datetime对象
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")

    # 往前推指定的天数，排除周末
    while days_to_subtract > 0:
        date_obj -= timedelta(days=1)  # 每次往前推一天
        # 如果当前日期不是周六或周日，减少待推的天数
        if date_obj.weekday() < 5:  # 0-4是周一到周五
            days_to_subtract -= 1

    # 返回调整后的日期字符串
    return date_obj.strftime("%d/%m/%Y")


# 使用示例
num, date, content_length = extract_date_and_number_from_pdf(pdf_path)

if num and date:
    # 调整日期往前推3天
    adjusted_date = adjust_date(date, 3)
    # 发票编号减去4
    adjusted_num = num - 4

    #    print(f"调整后的发票编号是: {adjusted_num}")
    print(f"调整后的发票编号是: {num}")
    print(f"调整后的日期是: {adjusted_date}")
else:
    print("未能提取到发票编号和日期。")

# 根据PDF内容的长度动态计算colli的值，范围从50到300
colli = int(50 + (content_length / 10000) * (345 - 50))  # 假设内容长度不会超过10000字符
colli = min(max(colli, 50), 345)  # 限制在50到300之间

print(f"自动选择的colli值为: {colli}")



# 读取CSV文
invoice_data = []
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        invoice_data.append({
            "descrizione": row['descrizione'],
            "quantita": int(row['quantita']),
            "prezzo": float(row['prezzo']),
            "importo": float(row['importo']),
            "iva": int(row['iva'])
        })

# Load the confezione PDF
confezione_path = r"路单模板.pdf"
output_path = r"路单out_"+ pdf_path

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
    #left_company_info = """VITTORIA S.R.L.S.
    #STRADA PROVINCIALE 40 - 20084
    #LACCHIARELLA (MI)
    #C.F./P.Iva 13255720966
    #"""

    left_company_info = """CERI S.R.L.S.
    VIA BREMBO 11 - 20139 MILANO(MI) - ITALY
    C.F. / P.Iva 13774080967
    """



    page.insert_text((50, 50), left_company_info, fontsize=10, fontname="helv")

    right_margin = 50
    page_width = page.rect.width
    right_align_x = page_width - right_margin

    for i, line in enumerate(right_company_info.split('\n')):

        x=350
        y = 50 + i * 15
        page.insert_text((x, y), line, fontsize=10, fontname="helv")

def add_custom_data(page, page_num):


    num=19
    date='30.12.2024'
    page.insert_text((210, 145), f" {num}", fontsize=10, fontname="helv")
    #    page.insert_text((265, 143), f" {adjusted_date}", fontsize=10, fontname="helv")
    page.insert_text((265, 145), f" {date}", fontsize=10, fontname="helv")
    page.insert_text((350, 170), f" {colli}", fontsize=10, fontname="helv")

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