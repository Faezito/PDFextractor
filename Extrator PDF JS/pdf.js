// carregar o PDF

async function loadPDF(pdfUrl) {
    const loadingTask = pdfjsLib.getDocument(pdfUrl)
    return loadingTask.promise
}


//extrair texto do PDF
async function extrairTexto(pdfUrl) {
    const pdf = await loadPDF(pdfUrl)
    let fullText = ""

    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++){
        const page = await pdf.getPage(pageNum)
        const txtContent = await page.getTextContent()
        const pageTxt = txtContent.items.map((item) => item.str).join(" ")
        fullText += pageTxt + "\n"       
    }
    return fullText
}

//filtrar email
function getEmail(texto) {
    const regexEmail = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g
    return texto.match(regexEmail) || [] 
}

function getTel(texto) {
    const regexTel = /\(?\d{2}\)?\s?\d{4,5}-?\d{4}/g
    return texto.match(regexTel) || []
}

let texto = ""

//processar o arquivo
document.getElementById("pdfInput").addEventListener("change", async (event) => {
    const arquivo = event.target.files[0]
    const tipo = [...document.getElementsByName("type")].find((el)=> el.checked)?.value
    texto = ""
    
    if (arquivo) {
        const urlPdf = URL.createObjectURL(arquivo)
        try {
            const texto = await extrairTexto(urlPdf)
            const emails = getEmail(texto)
            const tels = getTel(texto)

            if (tipo === 'Email') {
                document.getElementById("output").innerHTML = emails.length
                ? `<h2>Emails encontrados:</h2> <br> ${emails.join(", <br> ")}`
                : "Nenhum email encontrado."
            } else if (tipo === 'Tel') {
                document.getElementById("output").innerHTML = tels.length
                ? `<h2>Emails encontrados:</h2> <br> ${tels.join(", <br> ")}`
                : "Nenhum email encontrado."                
            } else {
                document.getElementById("output").textContent = "Selecione uma opção válida."
            }
            
        } catch (erro) {
            console.error("Erro ao processar o PDF", erro)
            document.getElementById("output").textContent =  "Erro ao processar o PDF"
        }       
    }
})