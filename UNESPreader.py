import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getUNESP_port(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    if len(re.findall(r'\dº semestre de \d\d\d\d', text)) >= 1:
        semestre_inicial = re.findall(r'\dº semestre de \d\d\d\d', text)[0][-4:] + "-0" + \
                           re.findall(r'\dº semestre de \d\d\d\d', text)[0][0]
    semestre = len(re.findall(r'semestre', text))
    aprovacao = len(re.findall(r'Aprovado', text))
    reprovacao = len(re.findall(r'Reprovado', text))


    if len(re.findall(r'\n\d\dº de \d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\d\dº de \d\d alunos', text)[0]
    elif len(re.findall(r'\n\d\dº de \d\d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\d\dº de \d\d\d alunos', text)[0]
    elif len(re.findall(r'\n\d\d\dº de \d\d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\d\d\dº de \d\d\d alunos', text)[0]
    elif len(re.findall(r'\n\dº de \d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\dº de \d\d alunos', text)[0]


    if len(re.findall(r'\d,\d\d\d', text)) > 1:
        len_cr = len(re.findall(r'\d,\d\d\d', text))
        cr = float(re.findall(r'\d,\d\d\d', text)[len_cr - 2].replace(',', '.'))
        cr_curso = float(re.findall(r'\d,\d\d\d', text)[len_cr - 1].replace(',', '.'))


    curso_aux = text.split("Curso:")
    if len(curso_aux) > 1:
        curso_aux2 = curso_aux[1].split("\n")
        if len(curso_aux2) > 1:
            curso = curso_aux2[0]

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUNESP_eng(text):
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
