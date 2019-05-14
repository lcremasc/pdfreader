import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getCEFET_port(text):

    # Resultado da extração do texto do arquivo de pdf em análise
    # A partir dos padrões de divulgação de informação nessa string podemos usar
    # a rotina de re.findall(pattern,string) e obter os valores e quantidades de dados desejados

    # O documento de histórico da PUCRIO não traz as informações de cr_curso e nem classificação
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    # Obtenção do número de aprovações dos alunos
    # Padrão: Utilização da sigla 'AP' entre espaços
    aprovacao = len(re.findall(r',\d\d Aprovado\n', text))

    trancamento = len(re.findall(r',\d\d Trancamento de Disciplinas\n', text))

    # Obtenção do número de aprovações dos alunos
    # Padrão: Utilização da sigla 'RM' entre espaços
    reprovacao = len(re.findall(r',\d\d Reprovado\n', text)) + trancamento

    # Para a obtenção do semestre atual devemos fazer uma contagem do numero de semestres distintos
    # Na PUCRIO a informação do semestre vem sempre antes da informação da matéria cursada
    # Buscamos então o padrão de: 5 numeros + espaço + 3 letras + 4 numeros
    semestres = re.findall(r'\nPeríodo Atual: \dº Semestre', text)
    if semestres == []:
        semestres = re.findall(r'\nPeríodo Atual:\n\d\dº Semestre\n', text)
        semestre = int(semestres[0][-13] + semestres[0][-12]) -1
    else:
        semestre = int(semestres[0][-11]) - 1

    semestre_inicial_list = re.findall(r'\n\dº Semestre de \d\d\d\d\n', text)
    if len(semestre_inicial_list) > 1:
        semestre_inicial = semestre_inicial_list[0][-5:-1] + "-0" + semestre_inicial_list[0][-20]
    else:
        semestre_inicial_list = re.findall(r'\n\dº Semes tre de \d\d\d\d\n', text)
        semestre_inicial = semestre_inicial_list[0][-5:-1] + "-0" + semestre_inicial_list[0][-21]

    # Para obtenção do CR pegamos a sequencia padrão do cabeçalho do histórico

    cr_pattern = re.findall(r'\n\d,\d\d\d\d\n', text)
    len_cr = len(cr_pattern)
    if cr_pattern == []:
        cr = 0
    else:
        cr = float(cr_pattern[len_cr - 1].replace(",", "."))
    curso = text.split("CENTRO FED. DE EDUC.")
    curso = curso[1].split("\n")[1].split(" - ")
    len_curso = len(curso)
    curso = curso[len_curso - 1]

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getCEFET_eng(text):
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
