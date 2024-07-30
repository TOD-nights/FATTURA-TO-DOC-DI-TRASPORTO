import fitz  # PyMuPDF
import re

# Load the two PDFs
fattura_path = r"Fattura.pdf"
confezione_path = r"路单模板.pdf"
output_path = r"路单1.pdf"

fattura_pdf = fitz.open(fattura_path)
confezione_pdf = fitz.open(confezione_path)

# Extract text from the fattura PDF to gather data
fattura_text = fattura_pdf[0].get_text("text")

# Parse the extracted text to create a list of dictionaries containing the invoice items
invoice_data = []
pattern = re.compile(r"^([\w\s\/\.,*]+)\s+(\d+)\s+€ ([\d,\.]+)\s+€ ([\d,\.]+)\s+(\d+)$", re.MULTILINE)
for match in pattern.finditer(fattura_text):
    descrizione, quantita, prezzo, importo, iva = match.groups()
    invoice_data.append({
        "descrizione": descrizione.strip(),
        "quantita": int(quantita),
        "prezzo": float(prezzo.replace(',', '.')),
        "importo": float(importo.replace(',', '.')),
        "iva": int(iva)
    })

# Get the page where we need to insert the data in the confezione PDF
page = confezione_pdf[0]

# Coordinates and formatting information for the new data
x_start_nr = 50  # X coordinate for NR column
x_start_descrizione = 100  # X coordinate for Descrizione column
x_start_quantita = 300  # X coordinate for Quantità column
x_start_prezzo = 420  # X coordinate for Prezzo column
x_start_importo = 550  # X coordinate for Importo column
x_start_iva = 580  # X coordinate for Iva column
y_start = 320  # Adjusted y coordinate to move the text further down
line_height = 15

# Insert the parsed data into the confezione PDF
y_position = y_start
for i, item in enumerate(invoice_data, start=1):
    page.insert_text((x_start_nr, y_position), str(i), fontsize=8, fontname="helv")
    page.insert_text((x_start_descrizione, y_position), item['descrizione'], fontsize=8, fontname="helv")
    page.insert_text((x_start_quantita, y_position), str(item['quantita']), fontsize=8, fontname="helv")
    page.insert_text((x_start_prezzo, y_position), f"€ {item['prezzo']:.2f}", fontsize=8, fontname="helv")
    page.insert_text((x_start_importo, y_position), f"€ {item['importo']:.2f}", fontsize=8, fontname="helv")
    page.insert_text((x_start_iva, y_position), str(item['iva']), fontsize=8, fontname="helv")
    y_position += line_height

# Save the modified PDF
confezione_pdf.save(output_path)

# Close the PDFs
fattura_pdf.close()
confezione_pdf.close()

print(f"Modified PDF saved to {output_path}")
