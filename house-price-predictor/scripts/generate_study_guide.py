import json
import re
from fpdf import FPDF

class NotebookPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'House Price Predictor - Linear Regression Study Guide', 0, 1, 'L')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(ipynb_path, pdf_path):
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    pdf = NotebookPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    def clean_text(text):
        replacements = {
            '🏠': '[House]',
            '🚀': '[Launch]',
            '📈': '[Chart]',
            '📊': '[Data]',
            '📋': '[List]',
            '🎓': '[Summary]',
            '💡': '[Insight]',
            '🔑': '[Key]',
            '📐': '[Math]',
            '✅': '[OK]',
            '⚠️': '[Warning]',
            'ŷ': 'y_pred',
            'ŷ_i': 'y_pred_i',
            'w₁': 'w1',
            'w₂': 'w2',
            'w_1': 'w1',
            'w_2': 'w2',
            'w_3': 'w3',
            'w_4': 'w4',
            'w_5': 'w5',
            'x_1': 'x1',
            'x_2': 'x2',
            'x_3': 'x3',
            'x_4': 'x4',
            'x_5': 'x5',
            'w_i': 'wi',
            'x_i': 'xi',
            'ŷ_i': 'y_pred_i',
            '$$': '',
            '\\hat{y}': 'y_pred',
            '\\text{size}': 'size',
            '\\text{bedrooms}': 'bedrooms',
            '\\text{bathrooms}': 'bathrooms',
            '\\text{age}': 'age',
            '\\text{location}': 'location',
            '\\sum': 'sum',
            '\\frac{1}{n}': '1/n',
            '\\sum_{i=1}^{n}': 'sum_{i=1..n}',
            '\\Delta': 'delta',
            '²': '^2',
            '₁': '1',
            '₂': '2',
            '₃': '3',
            '₄': '4',
            '₅': '5',
            '⁻¹': '^-1',
            '⁻': '-',
            '₹': 'Rs. ',
            'Lakhs': ' Lakhs',
            '—': '--',
            '–': '-',
            '…': '...',
            '•': '-',
            '➜': '->',
            '├──': '|--',
            '└──': '|__',
            '½': '1/2',
            '⅓': '1/3',
            '¼': '1/4',
            '•': '*'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        return text

    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type')
        source = cell.get('source', [])
        
        if not source:
            continue
            
        full_text = clean_text(''.join(source))
        
        if cell_type == 'markdown':
            lines = full_text.split('\n')
            for line in lines:
                if not line.strip():
                    pdf.ln(3)
                    continue
                if line.startswith('#'):
                    level = len(line) - len(line.lstrip('#'))
                    title = line.lstrip('#').strip()
                    pdf.set_font('helvetica', 'B', 16 - level)
                    pdf.set_text_color(17, 24, 39)
                    pdf.multi_cell(0, 8, title)
                    pdf.ln(4)
                elif line.startswith('>'):
                    quote = line.lstrip('>').strip()
                    pdf.set_font('helvetica', 'I', 10)
                    pdf.set_text_color(75, 85, 99)
                    pdf.multi_cell(0, 5, quote)
                    pdf.ln(2)
                else:
                    pdf.set_font('helvetica', '', 10)
                    pdf.set_text_color(31, 41, 55)
                    pdf.multi_cell(0, 5, line)
                    pdf.ln(1)
            pdf.ln(4)
            
        elif cell_type == 'code':
            pdf.set_font('courier', '', 9)
            pdf.set_text_color(5, 150, 105)
            pdf.set_fill_color(243, 244, 246)
            
            lines = full_text.split('\n')
            code_str = '\n'.join(lines)
            pdf.multi_cell(0, 4, code_str, border=1, fill=True)
            pdf.ln(4)
            
    pdf.output(pdf_path)
    print("PDF generated successfully:", pdf_path)

if __name__ == '__main__':
    create_pdf(
        r'c:\Projects\Software Projects\ML Demo(HomePrizePredictor)\house-price-predictor\model\train.ipynb',
        r'c:\Projects\Software Projects\ML Demo(HomePrizePredictor)\house-price-predictor\model\train_study_guide.pdf'
    )
