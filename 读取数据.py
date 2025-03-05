import PyPDF2
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class InvoiceItem:
    descrizione: str
    quantita: int
    prezzo: float
    importo: float
    iva: int

@dataclass
class Invoice:
    number: str
    date: str
    sender: str
    sender_address: str
    sender_vat: str
    recipient: str
    recipient_address: str
    recipient_vat: str
    items: List[InvoiceItem]
    total: float
    payment_method: str
    payment_due: str

def safe_search(pattern: str, text: str) -> Optional[re.Match]:
    return re.search(pattern, text, re.DOTALL)

def parse_invoice(text):
    # 提取发票号码和日期
    number_date = safe_search(r'nr\.\s*(\d+)\s*del\s*(\d{2}/\d{2}/\d{4})', text)
    number = number_date.group(1) if number_date else ""
    date = number_date.group(2) if number_date else ""

    # 提取发送方信息
    sender_match = safe_search(r'VITTORIA S\.R\.L\.S\.', text)
    sender = sender_match.group() if sender_match else "未找到发送方"
    sender_address_match = safe_search(r'STRADA PROVINCIALE 40.*?LACCHIARELLA.*?MI', text)
    sender_address = sender_address_match.group() if sender_address_match else "未找到发送方地址"
    sender_vat_match = safe_search(r'C\.F\./P\.Iva\s*(\d+)', text)
    sender_vat = sender_vat_match.group(1) if sender_vat_match else "未找到发送方VAT"

    # 提取接收方信息
    recipient_match = safe_search(r'F SETTE S\.R\.L\.S\.', text)
    recipient = recipient_match.group() if recipient_match else "未找到接收方"
    recipient_address_match = safe_search(r'VIA REGGGIO EMILIA.*?ASSAGO.*?MI', text)
    recipient_address = recipient_address_match.group() if recipient_address_match else "未找到接收方地址"
    recipient_vat_match = safe_search(r'C\.F\./P\.Iva\s*(\d+)', text)
    recipient_vat = recipient_vat_match.group(1) if recipient_vat_match else "未找到接收方VAT"

    # 提取商品项目
    items = []
    item_pattern = r'(\d+)\s+(.*?)\s+(\d+)\s+€\s*([\d,]+)\s+€\s*([\d,]+)\s+22'
    for match in re.finditer(item_pattern, text, re.DOTALL):
        quantita = int(match.group(3))
        descrizione = match.group(2).strip()
        prezzo = float(match.group(4).replace(',', '.'))
        importo = float(match.group(5).replace(',', '.'))
        items.append(InvoiceItem(descrizione, quantita, prezzo, importo, 22))

    # 提取总金额
    total_match = safe_search(r'Tot\.\s*documento\s*€\s*([\d.,]+)', text)
    total = float(total_match.group(1).replace('.', '').replace(',', '.')) if total_match else 0

    # 提取付款方式和到期日
    payment_info = safe_search(r'(\d{2}/\d{2}/\d{4})\s+(.*?)\s+€([\d.,]+)', text)
    payment_due = payment_info.group(1) if payment_info else ""
    payment_method = payment_info.group(2) if payment_info else ""

    return Invoice(number, date, sender, sender_address, sender_vat,
                   recipient, recipient_address, recipient_vat,
                   items, total, payment_method, payment_due)

# 读取PDF文件
pdf_path = 'Fattura.pdf'  # 请确保这是正确的PDF文件路径
pdf_text = ""

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        pdf_text += page.extract_text()

# 打印PDF内容（用于调试）
print("PDF 内容:")
print(pdf_text[:1000])  # 只打印前1000个字符
print("=" * 50)

# 解析发票
invoice = parse_invoice(pdf_text)

# 打印发票信息
print(f"发票号码: {invoice.number}")
print(f"发票日期: {invoice.date}")
print(f"发送方: {invoice.sender}")
print(f"发送方地址: {invoice.sender_address}")
print(f"发送方VAT: {invoice.sender_vat}")
print(f"接收方: {invoice.recipient}")
print(f"接收方地址: {invoice.recipient_address}")
print(f"接收方VAT: {invoice.recipient_vat}")
print(f"总金额: €{invoice.total}")
print(f"付款方式: {invoice.payment_method}")
print(f"付款到期日: {invoice.payment_due}")
print("\n商品列表:")
for item in invoice.items:
    print(f"- {item.descrizione}: 数量 {item.quantita}, 单价 €{item.prezzo}, 总价 €{item.importo}")