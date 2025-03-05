import pdfplumber
import pandas as pd
import os


def extract_text_from_pdf(pdf_path):
    # 打开 PDF 文件
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        # 遍历每一页
        for page in pdf.pages:
            # 提取每页文本
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
        return "\n".join(all_text)


def parse_text_to_table(text):
    # 将文本按行分割并创建列表
    rows = []
    for line in text.split('\n'):
        # 按空格分割列
        columns = line.split()
        # 如果检测到列则添加到行
        if len(columns) > 1:
            rows.append(columns)
    return rows


def save_to_csv(data, output_csv_path):
    # 将列表转换为 DataFrame 并保存为 CSV
    df = pd.DataFrame(data[1:], columns=data[0])  # 假设第一行为表头
    df.to_csv(output_csv_path, index=False)


def convert_pdf_to_csv(pdf_path):
    # 提取 PDF 文本
    text = extract_text_from_pdf(pdf_path)

    # 将文本解析为表格格式
    table_data = parse_text_to_table(text)

    # 构建输出 CSV 文件路径
    output_csv_path = pdf_path.replace(".pdf", ".csv")

    # 保存解析数据为 CSV
    save_to_csv(table_data, output_csv_path)


def main():
    # PDF 文件所在目录
    input_dir = r"E:\studio\info\Python\progetti\模板\da_1736505393416.pdf"

    # 遍历输入目录中的 PDF 文件
    for filename in os.listdir(input_dir):
        pdf_path = os.path.join(input_dir, filename)
        if os.path.isfile(pdf_path) and filename.endswith(".pdf"):
            print(f"正在转换 {pdf_path} 为 CSV...")
            convert_pdf_to_csv(pdf_path)

    print("转换完成。")


if __name__ == "__main__":
    main()
