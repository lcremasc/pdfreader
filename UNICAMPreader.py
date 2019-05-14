import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getUNICAMP_port(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    if len(re.findall(r'\d\.\d\d\d\d', text)) >= 2:
        aux = re.findall(r'\d\.\d\d\d\d', text)[0]
        cr = float(aux[-6:])
        aux = re.findall(r'\d\.\d\d\d\d', text)[1]
        cr_curso = float(aux[-6:])
    if len(re.findall(r'\d\.\d\d\d\d', text)) == 1:
        cr = 0
        aux = re.findall(r'\d\.\d\d\d\d', text)[0]
        cr_curso = float(aux[-6:])

    aprovacao = len(re.findall(r'Aprovado ', text))
    reprovacao = len(re.findall(r'Reprovado ', text))
    semestre = len(re.findall(r'Semestre', text))


    if len(re.findall(r'\dº Semestre de \d\d\d\d', text)) >= 1:
        semestre_inicial = re.findall(r'\dº Semestre de \d\d\d\d', text)[0][-4:] + "-0" + \
                           re.findall(r'\dº Semestre de \d\d\d\d', text)[0][0]
    if len(re.findall(r'\n\d\dº de \d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\d\dº de \d\d alunos', text)[0]
    elif len(re.findall(r'\n\d\dº de \d\d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\d\dº de \d\d\d alunos', text)[0]
    elif len(re.findall(r'\n\d\d\dº de \d\d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\d\d\dº de \d\d\d alunos', text)[0]
    elif len(re.findall(r'\n\dº de \d\d alunos', text)) >= 1:
        classificacao = re.findall(r'\n\dº de \d\d alunos', text)[0]
    curso_aux = text.split("Reconhecido pel")
    if len(curso_aux) > 1:
        curso_aux2 = curso_aux[0].split("Curso: ")
        if len(curso_aux2) > 1:
            curso = curso_aux2[1].split(" - ")[1]
    else:
        curso_aux = text.split("Habilita")
        if len(curso_aux) > 1:
            curso_aux2 = curso_aux[0].split("Curso: ")
            if len(curso_aux2) > 1:
                curso = curso_aux2[1].split(" - ")[1]

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUNICAMP_eng(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    if len(re.findall(r'\d\.\d\d\d\d', text)) >= 1:
        aux = re.findall(r'\d\.\d\d\d\d', text)[1]
        cr = float(aux[-6:])
    if len(re.findall(r'\d\.\d\d\d\d', text)) >= 2:
        aux = re.findall(r'\d\.\d\d\d\d', text)[0]
        cr_curso = float(aux[-6:])


    aprovacao = len(re.findall(r'Passed ', text))
    reprovacao = len(re.findall(r'Reproved', text))
    semestre = len(re.findall(r'SEMESTER', text.upper()))

    if len(re.findall(r'\dº Semester of \d\d\d\d', text)) >= 1:
        semestre_inicial = re.findall(r'\dº Semester of \d\d\d\d', text)[0][-4:] + "-0" + \
                           re.findall(r'\dº Semester of \d\d\d\d', text)[0][0]
    if semestre_inicial == "":
        if len(re.findall(r' semester of \d\d\d\d', text)) >= 1:
            ano = re.findall(r' semester of \d\d\d\d', text)[0][-4:]
            if len(re.findall(r'First semester of '+ano, text)) >= 1:
                semestre_inicial = ano + "-01"
            else:
                semestre_inicial = ano + + "-02"

    course_aux = text.split("Course")
    if len(course_aux) > 1:
        course_aux1 = course_aux[1].split("Accredited by Ministerial Decree")
        if len(course_aux1[0].split("\n")) > 8:
            curso = course_aux1[0].split("\n")[8]
        else:
            curso = course_aux1[0].split(" – ")[1]

    if len(re.findall(r'\n\d\dº de \d\d alunos', text)) >= 1:
         classificacao = re.findall(r'\n\d\dº de \d\d alunos', text)[0]
    elif len(re.findall(r'\n\d\dº de \d\d\d alunos', text)) >= 1:
         classificacao = re.findall(r'\n\d\dº de \d\d\d alunos', text)[0]
    elif len(re.findall(r'\n\d\d\dº de \d\d\d alunos', text)) >= 1:
         classificacao = re.findall(r'\n\d\d\dº de \d\d\d alunos', text)[0]
    elif len(re.findall(r'\n\dº de \d\d alunos', text)) >= 1:
         classificacao = re.findall(r'\n\dº de \d\d alunos', text)[0]

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status