import re
import PyPDF2
import pandas as pd
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import os
import glob
from auxiliarFunction import checkKPI

from UFFreader import getUFF_eng,getUFF_port
from UFRJreader import getUFRJ_eng, getUFRJ_port
from UFSCARreader import getUFSCAR_eng, getUFSCAR_port
from UNESPreader import getUNESP_eng, getUNESP_port
from UNICAMPreader import getUNICAMP_eng, getUNICAMP_port
from USPreader import getUSP_eng, getUSP_port
from CEFETreader import getCEFET_eng, getCEFET_port
from PUCRIOreader import getPUCRIO_eng, getPUCRIO_port
from auxiliarFunction import getUniversityUnknown_eng, getUniversityUnknown_port

def idtUniversidade(text):
    if(len(re.findall(r'Júpiter Web', text)) > 0) or len(re.findall(r'SCHOOL RESULTS SUMMARY', text)) > 0:
        tipo = "USP"
    elif(len(re.findall(r'UNICAMP', text.upper())) > 0):
        tipo = "UNICAMP"
    elif(len(re.findall(r'UFSCAR', text)) > 0 or len(re.findall(r'UNIVERSIDADE FEDERAL DE SÃO CARLOS', text)) > 0):
        tipo = "UFSCAR"
    elif(len(re.findall(r'UNESP', text)) > 0):
        tipo = "UNESP"
    elif(len(re.findall(r'UNIVERSIDADE FEDERAL DO RIO DE JANEIRO', text)) > 0):
        tipo = "UFRJ"
    elif(len(re.findall(r'UNIVERSIDADE FEDERAL FLUMINENSE', text)) > 0):
        tipo = "UFF"
    elif(len(re.findall(r'puc-rio', text.replace("\n","").replace(" ", ""))) > 0):
        tipo = "PUCRIO"
    elif(len(re.findall(r'CENTRO FED\. DE EDUC\.',text)) > 0):
        tipo = "CEFET"
    else:
        tipo = "UniversityUnknown"
    if len(re.findall(r'COURSE',text.upper())) >= 1:
        ling = 'eng'
    else:
        ling = 'port'
    return(tipo, ling)

def getKPI(text):
    universidade, ling = idtUniversidade(text)
    str_command = "get" + universidade
    str_command += "_" + ling + "(text)"
    return eval(str_command)

def getInfoPyPDF2(filename):
    text = ""
    file = os.path.basename(filename).split(' - ')
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    try:
        for pageNumber in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNumber)
            text = text + pageObj.extractText()
    except:
        print("Erro no PyPDF2")
    pdfFileObj.close()
    return(text)

def getInfoPDFMiner(filename):
    file = os.path.basename(filename).split(' - ')
    text = ""

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    try:
        fp = open(filename, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = text + lt_obj.get_text()
    except:
        print("Erro no PDFMiner")
    fp.close()

    return(text)

def getHistorico(filename):
    col_names = ['Nome', 'Universidade', 'Aprovacao', 'Reprovacao', 'Semestre', 'CR', 'CR Curso', 'Classificacao',
                 'Semestre Inicial', 'Curso', 'Status', 'Arquivo']
    df = pd.DataFrame(columns=col_names)
    file = os.path.basename(filename).split(' - ')
    nome = file[0]
    universidade = file[1]
    if filename.find(" - ") > 0:
        try:
            text = getInfoPDFMiner(filename)
            aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status = getKPI(text)
            df2 = pd.DataFrame([[nome, universidade, aprovacao, reprovacao, semestre, cr, cr_curso, classificacao,
                                semestre_inicial, curso, status,
                                os.path.basename(filename)]], columns=col_names)

            if (float(df2['Aprovacao']) + float(df2['Reprovacao'])) <= 2:
                try:
                    text = getInfoPyPDF2(filename)
                    aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status = getKPI(
                        text)
                    df3 = pd.DataFrame(
                        [[nome, universidade, aprovacao, reprovacao, semestre, cr, cr_curso, classificacao,
                          semestre_inicial, curso, status,
                          os.path.basename(filename)]], columns=col_names)
                    if (float(df3['Aprovacao']) + float(df3['Reprovacao'])) > (
                            float(df2['Aprovacao']) + float(df2['Reprovacao'])):
                        df2 = df3
                except:
                    pass
            df = df.append(df2)

        except:
            try:
                text = getInfoPyPDF2(filename)
                aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status = getKPI(
                    text)
                df3 = pd.DataFrame(
                    [[nome, universidade, aprovacao, reprovacao, semestre, cr, cr_curso, classificacao,
                      semestre_inicial, curso, status,
                      os.path.basename(filename)]], columns=col_names)
                df = df.append(df3)
            except:
                aprovacao = 0
                reprovacao = 0
                semestre = 0
                cr = 0
                cr_curso = 0
                classificacao = ""
                semestre_inicial = ""
                curso = ""

                status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)
                df3 = pd.DataFrame([[nome, universidade, aprovacao, reprovacao, semestre, cr, cr_curso, classificacao,
                  semestre_inicial, curso, status,
                  os.path.basename(filename)]], columns=col_names)
                df = df.append(df3)
    return(df)


path = 'C:\\Users\\Suporte\Documents\\02_Visagio\\PS\\01_Consultoria_RJ\\01_Histórico'
col_names = ['Nome', 'Universidade', 'Aprovacao', 'Reprovacao', 'Semestre', 'CR', 'CR Curso', 'Classificacao', 'Semestre Inicial', 'Curso','Status', 'Arquivo']
df = pd.DataFrame(columns = col_names)

for filename in glob.glob(os.path.join(path, '*.pdf')):
   print(filename)
   if filename.find(" - ") > 0:
       try:
           df2 = getHistorico(filename)
           df = df.append(df2)
       except:
           pass

writer = pd.ExcelWriter(path +'Historicos.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
