# -*- coding: utf-8 -*-

import ply.yacc as yacc

import lex as lex

from anytree import Node

tokens = lex.tokens

num_id = 0
success = True

def p_programa(p):
    '''
        programa : lista_declaracoes
    '''

    global num_id

    p[0] = Node(str(num_id) + ". programa", children = [p[1]])

    num_id += 1

def p_lista_declaracoes(p):
    '''
        lista_declaracoes : lista_declaracoes declaracao
                            | declaracao
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". lista_declaracoes", children = [p[1], p[2]])
    else:
        p[0] = Node(str(num_id) + ". lista_declaracoes", children = [p[1]])

    num_id += 1

def p_declaracao(p):
    '''
        declaracao : declaracao_variaveis
                    | inicializacao_variaveis
                    | declaracao_funcao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". declaracao", children = [p[1]])

    num_id += 1

def p_declaracao_variaveis(p):
    '''
        declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis
    '''

    global num_id

    p[0] = Node(str(num_id) + ". declaracao_variaveis", children = [
        p[1], Node(str(num_id) + ". " +  str(p[2])), p[3]
    ])

    num_id += 1

def p_inicializacao_variaveis(p):
    '''
        inicializacao_variaveis : atribuicao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". inicializacao_variaveis", children = [p[1]])

    num_id += 1

def p_lista_variaveis(p):
    '''
        lista_variaveis : lista_variaveis VIRGULA var 
                        | var
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". lista_variaveis", children = [
            p[1], Node(str(num_id) + ". " +  str(p[2])), p[3]
        ])
    else:
        p[0] = Node(str(num_id) + ". lista_variaveis", children = [p[1]])

    num_id += 1

def p_var(p):
    '''
        var : ID
            | ID indice
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". var", children = [
            Node(str(num_id) + ". " +  str(p[1])), p[2]
        ])
    else:
        p[0] = Node(str(num_id) + ". var", children = [
            Node(str(num_id) + ". " +  str(p[1]))
        ])

    num_id += 1

def p_indice(p):
    '''
        indice : indice ABRE_CONCHETES expressao FECHA_CONCHETES
                | ABRE_CONCHETES expressao FECHA_CONCHETES
    '''

    global num_id

    if(len(p) == 5):
        p[0] = Node(str(num_id) + ". indice", children = [
            p[1], Node(str(num_id) + ". " +  str(p[2])), p[3], Node(str(num_id) + ". " +  str(p[4]))
        ])
    else:
        p[0] = Node(str(num_id) + ". indice", children = [
            Node(str(num_id) + ". " +  str(p[1])), p[2], Node(str(num_id) + ". " +  str(p[3]))
        ])

    num_id += 1

def p_tipo(p):
    '''
        tipo : INTEIRO
            | FLUTUANTE
    '''

    global num_id

    p[0] = Node(str(num_id) + ". tipo", children = [
        Node(str(num_id) + ". " +  str(p[1]))
    ])

    num_id += 1

def p_declaracao_funcao(p):
    '''
        declaracao_funcao : tipo cabecalho 
                        | cabecalho
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". declaracao_funcao", children = [p[1], p[2]])
    else:
        p[0] = Node(str(num_id) + ". declaracao_funcao", children = [p[1]])

    num_id += 1

def p_cabecalho(p):
    '''
        cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM
    '''

    global num_id

    p[0] = Node(str(num_id) + ". cabecalho", children = [
        Node(str(num_id) + ". " +  str(p[1])), Node(str(num_id) + ". " +  str(p[2])), p[3], Node(str(num_id) + ". " +  str(p[4])), p[5]
    ])

    num_id += 1

def p_lista_parametros(p):
    '''
        lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". lista_parametros", children = [
            p[1], Node(str(num_id) + ". " +  str(p[2])), p[3]
        ])
    else:
        p[0] = Node(str(num_id) + ". lista_parametros", children = [p[1]])

    num_id += 1

def p_parametro(p):
    '''
        parametro : tipo DOIS_PONTOS ID
                |  parametro ABRE_CONCHETES FECHA_CONCHETES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". parametro", children = [
        p[1], Node(str(num_id) + ". " +  str(p[2])), Node(str(num_id) + ". " +  str(p[3]))
    ])

    num_id += 1

def p_corpo(p):
    '''
        corpo : corpo acao
            | vazio
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". corpo", children = [p[1], p[2]])
    else: 
        p[0] = Node(str(num_id) + ". corpo", children = [p[1]])

    num_id += 1

def p_acao(p):
    '''
        acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
    '''

    global num_id

    p[0] = Node(str(num_id) + ". acao", children = [p[1]])

    num_id += 1

def p_se(p):
    '''
        se : SE expressao ENTAO corpo FIM
            | SE expressao ENTAO corpo SENAO corpo FIM
    '''

    global num_id

    if(len(p) == 6):
        p[0] = Node(str(num_id) + ". se", children = [
            Node(str(num_id) + ". " +  str(p[1])), p[2], Node(str(num_id) + ". " +  str(p[3])), p[4], Node(str(num_id) + ". " +  str(p[5]))
        ])
    else:
        p[0] = Node(str(num_id) + ". se", children = [
            Node(str(num_id) + ". " +  str(p[1])), p[2], Node(str(num_id) + ". " +  str(p[3])), p[4], Node(str(num_id) + ". " +  str(p[5])), p[6]
        ])

    num_id += 1

def p_repita(p):
    '''
        repita : REPITA corpo ATE expressao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". repita", children = [
        Node(str(num_id) + ". " +  str(p[1])), p[2], Node(str(num_id) + ". " +  str(p[3])), p[4]
    ])

    num_id += 1

def p_atribuicao(p):
    '''
        atribuicao : var ATRIBUICAO expressao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". atribuicao", children = [
        p[1], Node(str(num_id) + ". " +  str(p[2])), p[3]
    ])

    num_id += 1

def p_leia(p):
    '''
        leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". leia", children = [
        Node(str(num_id) + ". " +  str(p[1])), Node(str(num_id) + ". " +  str(p[2])), p[3], Node(str(num_id) + ". " +  str(p[4]))
    ])

    num_id += 1

def p_escreva(p):
    '''
        escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". escreva", children = [
        Node(str(num_id) + ". " +  str(p[1])), Node(str(num_id) + ". " +  str(p[2])), p[3], Node(str(num_id) + ". " +  str(p[4]))
    ])

    num_id += 1

def p_retorna(p):
    '''
        retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". retorna", children = [
        Node(str(num_id) + ". " +  str(p[1])), Node(str(num_id) + ". " +  str(p[2])), p[3], Node(str(num_id) + ". " +  str(p[4]))
    ])

    num_id += 1

def p_expressao(p):
    '''
        expressao : expressao_logica
                | atribuicao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". expressao", children = [p[1]])

    num_id += 1

def p_expressao_logica(p):
    '''
        expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". expressao_logica", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". expressao_logica", children = [p[1]])

    num_id += 1

def p_expressao_simples(p):
    '''
        expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". expressao_simples", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". expressao_simples", children = [p[1]])

    num_id += 1

def p_expressao_aditiva(p):
    '''
        expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". expressao_adtiva", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". expressao_adtiva", children = [p[1]])

    num_id += 1

def p_expressao_multiplicativa(p):
    '''
        expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". expressao_multiplicativa", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". expressao_multiplicativa", children = [p[1]])

    num_id += 1

def p_expressao_unaria(p):
    '''
        expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". expressao_unaria", children = [p[1], p[2]])
    else:
        p[0] = Node(str(num_id) + ". expressao_unaria", children = [p[1]])

    num_id += 1

def p_operador_relacional(p):
    '''
        operador_relacional : MENOR
                            | MAIOR 
                            | IGUAL 
                            | DIFERENTE 
                            | MENOR_IGUAL 
                            | MAIOR_IGUAL
    '''

    global num_id

    p[0] = Node(str(num_id) + ". operador_relacional", children = [Node(str(num_id) + ". " +  str(p[1]))])

    num_id += 1

def p_operador_soma(p):
    '''
        operador_soma : ADICAO
                    | SUBTRACAO
    '''

    global num_id

    p[0] = Node(str(num_id) + ". operador_soma", children = [Node(str(num_id) + ". " +  str(p[1]))])

    num_id += 1

def p_operador_logico(p):
    '''
        operador_logico : E
                        | OU
    '''

    global num_id

    p[0] = Node(str(num_id) + ". operador_logico", children = [Node(str(num_id) + ". " +  str(p[1]))])

    num_id += 1

def p_operador_negacao(p):
    '''
        operador_negacao : NEGACAO
    '''

    global num_id

    p[0] = Node(str(num_id) + ". operador_negacao", children = [Node(str(num_id) + ". " +  str(p[1]))])

    num_id += 1

def p_operador_multiplicacao(p):
    '''
        operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO
    '''

    global num_id

    p[0] = Node(str(num_id) + ". operador_multiplicacao", children = [Node(str(num_id) + ". " +  str(p[1]))])

    num_id += 1

def p_fator(p):
    '''
        fator : ABRE_PARENTESES expressao FECHA_PARENTESES
            | var
            | chamada_funcao
            | numero
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". fator", children = [
            Node(str(num_id) + ". " +  str(p[1])), p[2], Node(str(num_id) + ". " +  str(p[3]))
        ])
    else:
        p[0] = Node(str(num_id) + ". fator", children = [p[1]])

    num_id += 1
    
def p_numero(p):
    '''
        numero : NUM_INTEIRO
            | NUM_FLUTUANTE
            | NUM_NOTACAO_CIENTIFICA
    '''

    global num_id

    p[0] = Node(str(num_id) + ". numero", children = [
        Node(str(num_id) + ". " +  str(p[1]))
    ])

    num_id += 1

def p_chamada_funcao(p):
    '''
        chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". chamada_funcao", children = [
        Node(str(num_id) + ". " +  str(p[1])), Node(str(num_id) + ". " +  str(p[2])), p[3], Node(str(num_id) + ". " +  str(p[4]))
    ])

    num_id += 1

def p_lista_argumentos(p):
    '''
        lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". lista_argumentos", children = [
            p[1], Node(str(num_id) + ". " +  str(p[2])), p[3]
        ])
    else:
        p[0] = Node(str(num_id) + ". lista_argumentos", children = [p[1]])

    num_id += 1

def p_vazio(p):
    '''
        vazio : 
    '''

    global num_id

    p[0] = Node(str(num_id) + ". vazio")

    num_id += 1

def p_error(p):
    global success
    success = False
    print('99999', p)

    if p:
        print('Invalid syntax at token \'' + str(p.value) + '\' at ' + str(int((p.lineno - 1)/2)) + ':' + str(lex.f_column(p)))
    else:
        print("Syntax error at EOF")

def p_leia_error(p):
    '''
        leia : LEIA ABRE_PARENTESES error FECHA_PARENTESES
    '''

    print("Invalid Argument in Function 'LEIA'")
    exit(1)

def p_escreva_error(p):
    '''
        escreva : ESCREVA ABRE_PARENTESES error FECHA_PARENTESES
    '''

    print("Invalid Argument in Function 'LEIA'")
    exit(1)

def p_retorna_error(p):
    '''
        retorna : RETORNA ABRE_PARENTESES error FECHA_PARENTESES
    '''

    print("Invalid Argument in Function 'RETORNA'")
    exit(1)

def p_declaracao_variaveis_error(p):
    '''
        declaracao_variaveis : error DOIS_PONTOS lista_variaveis
    '''

    print("Variable Declaration Error")
    exit(1)
    
def p_atribuicao_error(p):
    '''
        atribuicao : var ATRIBUICAO error
                | error ATRIBUICAO expressao
    '''

    print("Atribution Error")
    exit(1)

def p_lista_declaracoes_error(p):
    '''
        lista_declaracoes : error error
                        | error
    '''

    print("Declaration List Error")
    exit(1)

def p_indice_error(p):
    '''
        indice : indice ABRE_CONCHETES error FECHA_CONCHETES
            | ABRE_CONCHETES error FECHA_CONCHETES
    '''

    print("Index Error")
    exit(1)

def p_acao_error(p):
    '''
        acao : error
    '''

    print("Action Error")
    exit(1)

def p_cabecalho_error(p):
    '''
        cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES error FIM
    '''

    print("Function Header Error")
    exit(1)

def p_repita_error(p):
    '''
        repita : REPITA error ATE error
    '''

    print("'REPITA' Looping Error")
    exit(1)

def p_declaracao_error(p):
    '''
        declaracao : error
    '''

    print("Declaration Error")
    exit(1)

def p_inicializacao_variaveis_error(p):
    '''
        inicializacao_variaveis : error
    '''

    print("Variable Initialization Error")
    exit(1)

def p_lista_variaveis_error(p):
    '''
        lista_variaveis : error VIRGULA error
                        | error
    '''

    print("Variable List Error")
    exit(1)

def p_declaracao_funcao_error(p):
    '''
        declaracao_funcao : error error
                        | error
    '''

    print("Function Declaration Error")
    exit(1)

def p_lista_parametros_error(p):
    '''
        lista_parametros : error VIRGULA error
                        | error
    '''

    print("Parameters List Error")
    exit(1)

def p_corpo_error(p):
    '''
        corpo : error error
            | error
    '''

    print("Body Function Error")
    exit(1)

def p_se_error(p):
    '''
        se : SE error ENTAO error FIM
            | SE error ENTAO error SENAO error FIM
    '''

    print("Conditional Error")
    exit(1)

def p_expressao_error(p):
    '''
        expressao : error
    '''

    print("Expression Error")
    exit(1)

def p_expressao_simples_error(p):
    '''
        expressao_simples : error
                        | error error error
    '''

    print("Expression Error")
    exit(1)

yacc.yacc()

def parser(data):
    tree = yacc.parse(data, tracking = True)

    return tree, success