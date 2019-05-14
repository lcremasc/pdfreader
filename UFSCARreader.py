import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getUFSCAR_port(text):

    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    if len(re.findall(r'\d\d\d\d/\d\n', text)) > 1:
        semestre_inicial = re.findall(r'\d\d\d\d/\d\n', text)[1][0:4] + "-0" + re.findall(r'\d\d\d\d/\d\n', text)[0][5]


    aprovacao = len(re.findall(r'APROVADO', text))
    reprovacao = len(re.findall(r'REPROVADO', text))
    semestre = max(len(re.findall(r'\d\d\d\d/\d\n', text)) - 3,0)

    if len(re.findall(r'Média Geral\nTotal:\d\.\d\d', text)) >= 1:
        cr = float(re.findall(r'Média Geral\nTotal:\d\.\d\d', text)[0].split(':')[1])
    curso_aux = text.split("\n")
    if len(re.findall(r'\d\d\d\d\d\d - \w', curso_aux[0])) >= 1 and curso_aux[1] != "\n" and not(curso_aux[1].isupper()) and curso_aux[1] != '':
        curso = curso_aux[1].replace("Curso: ", "")
    else:
        curso_aux = text.split("Ingresso:")
        if len(curso_aux) > 2:
            curso = curso_aux[1].split("\n")[2].replace("Curso: ", "")

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUFSCAR_eng(text):
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
