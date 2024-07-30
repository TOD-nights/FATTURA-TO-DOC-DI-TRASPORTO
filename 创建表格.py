from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer

# 文件路径
output_path = r"invoice_data.pdf"

# 创建PDF文档
pdf = SimpleDocTemplate(output_path, pagesize=A4)

# 标题行
data = [["NR", "Descrizione", "Quantità", "Prezzo", "Importo", "Iva"]]

# 添加发票数据
invoice_data = invoice_data = [
  {
    "descrizione": "VASO PER FIORI IN VETRO 18CM",
    "quantita": 240,
    "prezzo": 2.80,
    "importo": 672.00,
    "iva": 22
  },
  {
    "descrizione": "CANOTTA CUCITE",
    "quantita": 1780,
    "prezzo": 2.15,
    "importo": 3827.00,
    "iva": 22
  },
  {
    "descrizione": "TOP CUCITE",
    "quantita": 2150,
    "prezzo": 2.20,
    "importo": 4730.00,
    "iva": 22
  },
  {
    "descrizione": "T-SHIRT M/C CUCITE",
    "quantita": 1526,
    "prezzo": 1.95,
    "importo": 2975.70,
    "iva": 22
  },
  {
    "descrizione": "T-SHIRT M/L CUCITE",
    "quantita": 2512,
    "prezzo": 1.75,
    "importo": 4396.00,
    "iva": 22
  },
  {
    "descrizione": "SOTTOCASCO CUCITE",
    "quantita": 3221,
    "prezzo": 0.75,
    "importo": 2415.75,
    "iva": 22
  }
]

for i, item in enumerate(invoice_data, start=1):
    data.append([str(i), item['descrizione'], str(item['quantita']), f"€ {item['prezzo']:.2f}", f"€ {item['importo']:.2f}", str(item['iva'])])

# 创建表格
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

# 生成PDF
elements = [Spacer(1, 130), table]  # 在表格前添加空白，以调整表格位置

pdf.build(elements)

print(f"PDF saved to {output_path}")
