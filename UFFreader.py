import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getUFF_port(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    if len(re.findall(r'\dº/\d\d\d\d', text)) >= 1:
        semestre_inicial = re.findall(r'\dº/\d\d\d\d', text)[1][-4:] + "-0" + \
                           re.findall(r'\dº/\d\d\d\d', text)[1][0]

    semestre = len(set(re.findall(r'\dº/\d\d\d\d', text)))
    try:
        cr = re.findall(r'COEFICIENTE DE RENDIMENTO:\n\d\.\d\n',text)
        len_cr = len(cr)
        cr = cr[len_cr -1][-4:-1]
    except:
        cr = text.split("COEFICIENTE DE RENDIMENTO:")
        cr = cr[len(cr) - 1]
        cr = re.findall(r'\d\.\d',cr)
        cr = cr[len(cr)-1]

    qtd_cr = len(re.findall(r'COEFICIENTE DE RENDIMENTO:',text))

    notas = re.findall(r'\d\d\.\d\n', text)
    len_notas_10 = len(notas)
    notas.extend(re.findall(r'\d\.\d\n', text))
    len_notas_dup = len(notas)
    try:
        notas.remove('0.0\n')
    except:
        pass

    if(len(notas) != len_notas_dup - len_notas_10):
        list_aux = ['0.0\n']*(len_notas_dup - len(notas) - len_notas_10)
        notas.extend(list_aux)

    notas = [1 if float(x)>=6 else 0 for x in notas]
    aprovacao = sum(notas)
    reprovacao = len(notas) - aprovacao

    if(float(cr) >=6):
        aprovacao -= qtd_cr
    else:
        reprovacao -= qtd_cr


    curso_aux = text.split("PORTARIA")
    if len(curso_aux) > 1:
        curso_aux2 = curso_aux[1].split("\n")
        if len(curso_aux2) > 1:
            curso = curso_aux2[2]

    cr = float(cr)

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getUFF_eng(text):
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
