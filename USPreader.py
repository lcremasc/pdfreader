import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getUSP_port(text):

    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao = len(re.findall(r'\d\.\dA\w', text))
    trancada = len(re.findall(r'\d\.\dT\w', text))
    reprovacao_nota = len(re.findall(r'\d\.\dRN\w', text))
    reprovacao_nota_freq = len(re.findall(r'\d\.\dRA\w', text))
    reprovaca_freq = len(re.findall(r'\d\.\dRF\w', text))
    reprovacao = reprovacao_nota_freq + reprovaca_freq + reprovacao_nota

    if len(re.findall(r'\d\d\d\d  \dº. Semestre', text)) >= 1:
        semestre_inicial = re.findall(r'\d\d\d\d  \dº. Semestre', text)[0][0:4] + "-0" + \
                               re.findall(r'\d\d\d\d  \dº. Semestre', text)[0][6]
    elif len(re.findall(r'\d\d\d\d  \d¼. Semestre', text)) >= 1:
        semestre_inicial = re.findall(r'\d\d\d\d  \d¼. Semestre', text)[0][0:4] + "-0" + \
                               re.findall(r'\d\d\d\d  \d¼. Semestre', text)[0][6]

    semestre = len(re.findall(r'Semestre', text)) - len(re.findall(r'no Semestre', text))

    if len(re.findall(r'Média Ponderada com reprovações:   \d\.\d', text)) >= 1:
        cr = float(re.findall(r'Média Ponderada com reprovações:   \d\.\d', text)[0][-3:])
        if len(re.findall(r'Média ponderada de seu curso : \d\.\d\d\d\d', text)) >= 1:
            cr_curso = float(re.findall(r'Média ponderada de seu curso : \d\.\d\d\d\d', text)[0][-6:])
        if len(re.findall(r'M”dia Ponderada com reprova“łes:   \d\.\d', text)) >= 1:
            cr = float(re.findall(r'M”dia Ponderada com reprova“łes:   \d\.\d', text)[0][-3:])
        if len(re.findall(r'M”dia ponderada de seu curso : \d\.\d\d\d\d', text)) >= 1:
            cr_curso = float(re.findall(r'M”dia ponderada de seu curso : \d\.\d\d\d\d', text)[0][-6:])

        curso_aux = text.split("Curso:")
        if len(curso_aux) > 1:
            curso_aux2 = curso_aux[1].split(" Quantidade de reingressos: ")
            if len(curso_aux2) > 1:
                curso = curso_aux2[0].split(" - ")[1]


    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUSP_eng(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao = len(re.findall(r'\d\.\dA\w', text))
    trancada = len(re.findall(r'\d\.\dT\w', text))
    reprovacao_nota = len(re.findall(r'\d\.\dRN\w', text))
    reprovacao_nota_freq = len(re.findall(r'\d\.\dRA\w', text))
    reprovaca_freq = len(re.findall(r'\d\.\dRF\w', text))
    reprovacao = reprovacao_nota_freq + reprovaca_freq + reprovacao_nota

    semestre_inicial_aux = text.split(" Semester")
    if len(semestre_inicial_aux) > 1:
        semestre_inicial_aux2 = semestre_inicial_aux[0].split("Period:      ")
        if len(semestre_inicial_aux2) > 1:
            semestre_inicial_aux3 = semestre_inicial_aux2[1].split("  ")
            if len(semestre_inicial_aux3) > 1:
                if semestre_inicial_aux3[1] == "First":
                    semestre_mes = "01"
                else:
                    semestre_mes = "02"
                semestre_inicial = semestre_inicial_aux3[0] + "-" + semestre_mes
    if len(re.findall(r'Pondered average including failures: \d\.\d', text)) >= 1:
        cr = float(re.findall(r'Pondered average including failures: \d\.\d', text)[0][-3:])
    if semestre == 0:
        semestre = len(re.findall(r'Semester', text))
        semestre = semestre - len(re.findall(r'Credits attained in the Semester', text))
        semestre = semestre - len(re.findall(r'Credits earned by the end of the Semester', text))

    curso_aux = text.split("Program Name:  ")
    if len(curso_aux) > 1:
        curso_aux2 = curso_aux[1].split("_")
        if len(curso_aux2) > 1:
            curso = curso_aux2[0].split("     ")[1]

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status
