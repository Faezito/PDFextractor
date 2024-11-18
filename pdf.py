import tkinter as tk
from tkinter import filedialog  #Diálogos Tkinter
import fitz   # PyMuPDF
import re #biblioteca para expressões regulares

#aqui selecionamos o arquivo PDF
def selecionar():
    caminho = filedialog.askopenfilename(  #abre uma caixa para seleção de arquivo, onde title é o título da janela e filetypes é o tipo de arquivo aceito
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*pdf")]
    )
    if caminho:   # verifica se algum arquivo foi selecionado
        label_arquivo["text"] = f"Arquivo selecionado: {caminho}"    #atualiza o texto label para mostrar o caminho do arquivo selecionado
            #tenta abrir e extrair o texto
        try:
            with fitz.open(caminho) as pdf:  #abre o PDF com o PyMuPDF
                texto = ""                     #string para armazenar o texto

                for pagina in pdf:
                    texto += pagina.get_text("text")

            email(texto)

        except Exception as e:
            caixa_texto.delete(1.0, tk.END)
            caixa_texto.insert(tk.END, f"Erro ao ler o PDF: {e}")

def email(texto):
    tipo = tipo_info.get()
    resultado = ""

    if tipo == "Email":
        resultado = "\n".join(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", texto))
    if tipo == "Telefone":
        resultado = "\n".join(re.findall(r"\(?\d{2}\)?\s?\d{4,5}-\d{4}", texto))

    caixa_texto.delete(1.0, tk.END)
    caixa_texto.insert(tk.END, resultado if resultado else f"Nenhum {tipo} encontrado.")

root = tk.Tk()
root.title("Extrator de PDF")
root.geometry("800x600")

#menu dropdown para selecionar o tipo de arquivo
tipo_info = tk.StringVar(value="Email")
options = ["Email", "Telefone"]
menu_info = tk.OptionMenu(root, tipo_info, *options)
menu_info.pack(pady=10)

#criação do botão para selecionar o PDF

btn_select = tk.Button (
    root,                       #indica que o botão ficará na janela principal
    text="SELECIONAR PDF",      #texto que aparecerá no botão
    command=selecionar          #define que ao clicar no botão, será acionada a função para selecionar o PDF
)
btn_select.pack(pady=10) #exibe o botão na janela com espaçamento vertical

#label para mostrar o caminho do arquivo selecionado
label_arquivo = tk.Label (
    root,
    text="Nenhum arquivo selecionado"
)
label_arquivo.pack(pady=5)

#caixa onde o texto ficará
frame_texto = tk.Frame(root)
frame_texto.pack(pady=10, fill="both", expand=True)

#caixa do texto para exibir o conteúdo do PDF
caixa_texto = tk.Text(frame_texto, wrap="word")
caixa_texto.pack(side="left", fill="both", expand=True)

#barra de rolagem, caso o texto seja muito grande
scrollbar = tk.Scrollbar(frame_texto, command=caixa_texto.yview)
scrollbar.pack(side="right", fill="y")
caixa_texto.config(yscrollcommand=scrollbar.set)


root.mainloop()