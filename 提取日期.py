import fitz  # PyMuPDF库，用于处理PDF文件
import re
from datetime import datetime, timedelta


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

    # 正则表达式匹配日期（格式为DD/MM/YYYY）
    date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"
    date_match = re.search(date_pattern, full_text)
    extracted_date = date_match.group(1) if date_match else None

    # 正则表达式匹配发票编号（假设发票编号是一个数字）
    num_pattern = r"\bPrezzo\s*(\d+)\b"
    num_match = re.search(num_pattern, full_text)
    extracted_num = int(num_match.group(1)) if num_match else None

    return extracted_num, extracted_date


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
pdf_path = "Fattura 160 del 17-06-2024  SOLUZIONE 4 0 S R L S.pdf"  # 替换为你的PDF文件路径
num, date = extract_date_and_number_from_pdf(pdf_path)

if num and date:
    # 调整日期往前推3天
    adjusted_date = adjust_date(date, 3)
    # 发票编号减去4
    adjusted_num = num - 4

    print(f"调整后的发票编号是: {adjusted_num}")
    print(f"调整后的日期是: {adjusted_date}")
else:
    print("未能提取到发票编号和日期。")
