from fpdf import FPDF
from datetime import datetime


def create_pdf(bloco):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Informações do Bloco", ln=True, align='C')
    
    pdf.cell(200, 10, txt=f"ID Bloco: {bloco.id_bloco}", ln=True)
    pdf.cell(200, 10, txt=f"ID Dono: {bloco.id_dono}", ln=True)
    pdf.cell(200, 10, txt=f"Material: {bloco.material}", ln=True)
    pdf.cell(200, 10, txt=f"Ativo: {bloco.is_active}", ln=True)
    pdf.cell(200, 10, txt=f"Registrado: {bloco.registrado}", ln=True)
    pdf.cell(200, 10, txt=f"Atualizado: {bloco.atualizado}", ln=True)
    pdf.cell(200, 10, txt=f"Valor: {bloco.valor}", ln=True)
    pdf.cell(200, 10, txt=f"Título: {bloco.titulo}", ln=True)
    pdf.cell(200, 10, txt=f"Classificação: {bloco.classificao}", ln=True)
    pdf.cell(200, 10, txt=f"Coloração: {bloco.coloracao}", ln=True)
    pdf.cell(200, 10, txt=f"Medida Bruta: {bloco.medida_bruta}", ln=True)
    pdf.cell(200, 10, txt=f"Volume Bruto: {bloco.volume_bruto}", ln=True)
    pdf.cell(200, 10, txt=f"Medida Líquida: {bloco.medida_liquida}", ln=True)
    pdf.cell(200, 10, txt=f"Volume Líquido: {bloco.volume_liquido}", ln=True)
    pdf.cell(200, 10, txt=f"Pedreira: {bloco.pedreira}", ln=True)
    pdf.cell(200, 10, txt=f"Frente Pedreira: {bloco.frente_pedreira}", ln=True)
    pdf.cell(200, 10, txt=f"Informações: {bloco.info}", ln=True)
    pdf.cell(200, 10, txt=f"CEP: {bloco.cep}", ln=True)
    pdf.cell(200, 10, txt=f"Frete: {bloco.frete}", ln=True)
    pdf.cell(200, 10, txt=f"Localização: {bloco.localizacao}", ln=True)
    
    pdf.output("bloco_info.pdf")
