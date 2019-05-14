import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getUFRJ_port(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao = len(re.findall(r'AP\n', text))
    reprovacao = len(re.findall(r'RF\n', text)) + len(re.findall(r'RM\n', text)) + len(re.findall(r'RFM\n', text))

    semestre_inicial = re.findall(r'\d\d\d\d/\d\n', text)[0]
    semestre_inicial = semestre_inicial[:4] + "-0" + semestre_inicial[-2]

    try:
        curso = text.split("HISTÓRICO NÃO OFICIAL")[1].split("Portaria")[0].split("\n")[2]
    except:
        curso = text.split("BOLETIM NÃO OFICIAL")[1].split("Portaria")[0].split("\n")[2]

    semestre = len(re.findall(r'\d\d\d\d/\d\n', text))

    semestre_final = re.findall(r'\d\d\d\d/\d\n', text)[len(re.findall(r'\d\d\d\d/\d\n', text)) - 1]

    try:
        aux = text.split("Totais: no período")[len(text.split("Totais: no período")) - 2].split(semestre_final)[1]

        if(len(re.findall(r'\d\d\.\d\n', aux)) >0 ):
            cr = re.findall(r'\d\d\.\d\n', aux)[1]
        else:
            cr = re.findall(r'\d\.\d\n', aux)[1]

    except:
        cr = re.findall(r'\d\.\d\n', text)
        cr = cr[len(cr) - 1]

    cr = float(cr)


    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUFRJ_eng(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status = getUniversityUnknown_eng(text)

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status
