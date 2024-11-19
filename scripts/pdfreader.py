import pdfplumber
import re

with pdfplumber.open(r"data\manuals\2020-Cessna_150_1977_MM_D2011-1-13.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()

pdf.pages[65].extract_text()
cleaned_text = re.sub(r'\s+', ' ', text).strip().lower()
print(cleaned_text)
breakpoint()