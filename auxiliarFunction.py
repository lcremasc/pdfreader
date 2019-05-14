import re

def checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso):
    status = "Leitura Realizada"
    if semestre < 0:
        semestre = 0
    if aprovacao + reprovacao <= 2:
        status = "Erro na Leitura: Análive Manual"
    if cr == 0:
        if status == "Leitura Realizada":
            status = "Erro na Leitura: Análise CR"
        else:
            status = status + ", Análise CR"
    return status

def getUniversityUnknown_port(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao = len(re.findall(r'Aprovado', text))
    reprovacao = len(re.findall(r'Reprovado', text))
    semestre = len(re.findall(r'Semestre', text))
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUniversityUnknown_eng(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao = len(re.findall(r'Passed', text))
    reprovacao = len(re.findall(r'Reprov', text))
    semestre = len(re.findall(r'Semester', text))
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status
