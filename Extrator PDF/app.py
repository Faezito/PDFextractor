from flask import Flask, render_template, request
import os
import re
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar_pdf():
    if 'pdf' not in request.files:
        return "Nenhum arquivo PDF enviado", 400
    file = request.files['pdf']

    if file.filename == '':
        return "Nenhum arquivo selecionado", 400
    
    filename = file.filename

    reader = PdfReader(file)
    txtPdf = ""
    for page in reader.pages:
        txtPdf += page.extract_text()
    
    tipo = request.form['tipo']

    if tipo == "Email":
        resultado = "\n".join(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}", txtPdf))
    elif tipo == "Telefone":
        resultado = "\n".join(re.findall(r"\(?\d{2}\)?\s?\d{4,5}-\d{4}", txtPdf))
    else:
        resultado = "Tipo de informação desconhecida."

    return render_template('resultado.html', filename=filename, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)