import re
from auxiliarFunction import checkKPI, getUniversityUnknown_eng

def getPUCRIO_port(text):

    # O documento de histórico da PUCRIO não traz as informações de cr_curso e nem classificação
    cr_curso = ""
    classificacao = ""
    curso = ""

    # Resultado da extração do texto do arquivo de pdf em análise
    # A partir dos padrões de divulgação de informação nessa string podemos usar
    # a rotina de re.findall(pattern,string) e obter os valores e quantidades de dados desejados

    # Obtenção do número de aprovações dos alunos
    # Padrão: Utilização da sigla 'AP' entre espaços
    aprovacao = len(re.findall(r'\nAP', text))

    # Obtenção do número de aprovações dos alunos
    # Padrão: Utilização da sigla 'RM' entre espaços
    reprovacao = len(re.findall(r'\nRM', text)) + len(re.findall(r'\nRF', text))

    # Para a obtenção do semestre atual devemos fazer uma contagem do numero de semestres distintos
    # Na PUCRIO a informação do semestre vem sempre antes da informação da matéria cursada
    # Buscamos então o padrão de: 5 numeros + espaço + 3 letras + 4 numeros
    semestres = re.findall(r'\n\d\d\d\d\d\n\w\w\w\d\d\d\d', text)
    if(len(semestres) > 1):
        lista_semestres = []

        # Retirmos apenas os chars nas posiões de 1 a 6 para termos a descrição do semestre
        for j in semestres:
            lista_semestres.append(j[1:6])

        # Selecionamos apenas os valores distintos
        output = []
        for x in lista_semestres:
            if x not in output:
                output.append(x)

        # Armazenamos a contagem do vetor final na variavel desejada
        semestre = len(output)

        if semestre == 0:
            semestre_inicial = 0
        else:
            # Guardamos a informação do semestre inicial
            semestre_inicial = output[0]
            semestre_inicial = output[0][0:4] + "-0" + output[0][-1:]
    else:
        semestres = re.findall(r'\n\d\n\d\n\d\n\d\n\d\n\d\n\w\w\w', text)
        semestres = [float(x.replace('\n', '')[1:6]) for x in semestres]
        semestre = len(set(semestres))
        semestre_inicial = str(min(semestres))
        semestre_inicial = semestre_inicial[:4] + "-0" + semestre_inicial[4]

    # Para obtenção do CR pegamos a sequencia padrão do cabeçalho do histórico
    cr_pattern = re.findall(r'\n...\n...\n\d\d\d\d\n\d\n\d,\d', text)
    if cr_pattern == []:
        cr_pattern = re.findall(r'\n\d\d\d\d\n\d\n\d,\d', text)
        # Retiramos as informações respectivas nos locais conhecidos da string
        if cr_pattern != []:
            # Obtenção do CR. Descontruimos e reconstruimos o numero com ponto pois no documento ele possui vírgulas
            cr = cr_pattern[0][-3] + "." + cr_pattern[0][-1]
            cr = float(cr)
        else:
            cr_pattern = re.findall(r'\n\d\n\d\n\d\n\d\n\d\n\d\n\d\n', text)
            if(len(cr_pattern) > 0):
                cr = float(cr_pattern[0].replace('\n','')[-2:])/10
            else:
                cr = 0
    else:
        # Retiramos as informações respectivas nos locais conhecidos da string

        # Obtenção do CR. Descontruimos e reconstruimos o numero com ponto pois no documento ele possui vírgulas
        cr = cr_pattern[0][-3] + "." + cr_pattern[0][-1]
        cr = float(cr)

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status

def getPUCRIO_eng(text):
    aprovacao = 0
    reprovacao = 0
    semestre = 0
    cr = 0
    cr_curso = 0
    classificacao = ""
    semestre_inicial = ""
    curso = ""

    aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status = getUniversityUnknown_eng(
        text)

    status = checkKPI(aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso)

    return aprovacao, reprovacao, semestre, cr, cr_curso, classificacao, semestre_inicial, curso, status