# -*- coding: utf-8 -*-

import ply.yacc as yacc

import lex as lex

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

tokens =  lex.tokens

num_id = 0

def p_programa(p):
    '''
        programa : lista_declaracoes
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Program", children = [p[1]])
    num_id += 1

def p_lista_declaracoes(p):
    '''
        lista_declaracoes : lista_declaracoes declaracao
                            | declaracao
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". Lista Declarações", children = [p[1], p[2]])
    else:
        p[0] = Node(str(num_id) + ". Lista Declarações", children = [p[1]])

    num_id += 1

def p_declaracao(p):
    '''
        declaracao : declaracao_variaveis
                    | inicializacao_variaveis
                    | declaracao_funcao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Declaração", children = [p[1]])

    num_id += 1

def p_declaracao_variaveis(p):
    '''
        declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + str(p[2]), children = [p[1], p[3]])

    num_id += 1

def p_inicializacao_variaveis(p):
    '''
        inicializacao_variaveis : atribuicao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Inicialização Variáveis", children = [p[1]])

    num_id += 1

def p_lista_variaveis(p):
    '''
        lista_variaveis : lista_variaveis VIRGULA var 
                        | var
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Lista Variáveis", children = [p[1], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Variável", children = [p[1]])
    num_id += 1

def p_var(p):
    '''
        var : ID
            | ID indice
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". Índice ID", children = [p[2]])
    else:
        p[0] = Node(str(num_id) + ". " + p[1])

    num_id += 1

def p_indice(p):
    '''
        indice : indice ABRE_CONCHETES expressao FECHA_CONCHETES
                | ABRE_CONCHETES expressao FECHA_CONCHETES
    '''

    global num_id

    if(len(p) == 5):
        p[0] = Node(str(num_id) + ". Índice " + str(p[2]) + " Expressão " + str(p[4]), children = [p[1], p[3]])
    else:
        p[0] = Node(str(num_id) + ". " + str(p[1]) + " Expressão " + str(p[3]), children = [p[2]])

    num_id += 1

def p_tipo(p):
    '''
        tipo : INTEIRO
            | FLUTUANTE
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + p[1])

    num_id += 1

def p_declaracao_funcao(p):
    '''
        declaracao_funcao : tipo cabecalho 
                        | cabecalho
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". Declaracão Função", children = [p[1], p[2]])
    else:
        p[0] = Node(str(num_id) + ". Declaracão Função", children = [p[1]])

    num_id += 1

def p_cabecalho(p):
    '''
        cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Cabeçalho", children = [p[3], p[5]])

    num_id += 1

def p_lista_parametros(p):
    '''
        lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Lista Parâmetros " + p[2] + " Parâmetro", children = [p[1], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Lista Parâmetros", children = [p[1]])

    num_id += 1

def p_parametro(p):
    '''
        parametro : tipo DOIS_PONTOS ID
                |  parametro ABRE_CONCHETES FECHA_CONCHETES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Tipo " + str(p[2]) + " " + str(p[3]), children = [1])

    num_id += 1

def p_corpo(p):
    '''
        corpo : corpo acao 
            | vazio
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". Corpo", children = [p[1], p[2]])
    else: 
        p[0] = Node(str(num_id) + ". Vazio", children = [p[1]])

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
            | error
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Ação", children = [p[1]])

    num_id += 1

def p_se(p):
    '''
        se : SE expressao ENTAO corpo FIM
            | SE expressao ENTAO corpo SENAO corpo FIM
    '''

    global num_id

    if(len(p) == 6):
        p[0] = Node(str(num_id) + ". Se", children = [p[2], p[4]])
    else:
        p[0] = Node(str(num_id) + ". Se", children = [p[2], p[4], p[6]])

    num_id += 1

def p_repita(p):
    '''
        repita : REPITA corpo ATE expressao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Repita", children = [p[2], p[4]])

    num_id += 1

def p_atribuicao(p):
    '''
        atribuicao : var ATRIBUICAO expressao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". :=", children = [p[1], p[3]])

    num_id += 1

def p_leia(p):
    '''
        leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Leia", children = [p[3]])

    num_id += 1

def p_escreva(p):
    '''
        escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + " escreva", children = [p[3]])

    num_id += 1

def p_retorna(p):
    '''
        retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Retorna", children = [p[3]])

    num_id += 1

def p_expressao(p):
    '''
        expressao : expressao_logica
                | atribuicao
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Expressão", children = [p[1]])

    num_id += 1

def p_expressao_logica(p):
    '''
        expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Expressão Lógica", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Expressão Lógica", children = [p[1]])

    num_id += 1

def p_expressao_simples(p):
    '''
        expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Expressão Simples", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Expressão Simples", children = [p[1]])

    num_id += 1

def p_expressao_aditiva(p):
    '''
        expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Expressão Aditiva", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Expressão Aditiva", children = [p[1]])

    num_id += 1

def p_expressao_multiplicativa(p):
    '''
        expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Expressão Multiplicativa", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Expressão Multiplicativa", children = [p[1]])

    num_id += 1

def p_expressao_unaria(p):
    '''
        expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator
    '''

    global num_id

    if(len(p) == 3):
        p[0] = Node(str(num_id) + ". Expressão Unária", children = [p[1], p[2]])
    else:
        p[0] = Node(str(num_id) + ". Expressão Unária", children = [p[1]])

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

    p[0] = Node(str(num_id) + ". " + str(p[1]))

    num_id += 1

def p_operador_soma(p):
    '''
        operador_soma : ADICAO
                    | SUBTRACAO
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + str(p[1]))

    num_id += 1

def p_operador_logico(p):
    '''
        operador_logico : E
                        | OU
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + str(p[1]))

    num_id += 1

def p_operador_negacao(p):
    '''
        operador_negacao : NEGACAO
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + str(p[1]))

    num_id += 1

def p_operador_multiplicacao(p):
    '''
        operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + str(p[1]))

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
        p[0] = Node(str(num_id) + ". Fator", children = [p[2]])
    else:
        p[0] = Node(str(num_id) + ". Fator", children = [p[1]])

    num_id += 1
    
def p_numero(p):
    '''
        numero : NUM_INTEIRO
            | NUM_FLUTUANTE
            | NUM_NOTACAO_CIENTIFICA
    '''

    global num_id

    p[0] = Node(str(num_id) + ". " + str(p[1]))

    num_id += 1

def p_chamada_funcao(p):
    '''
        chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Chamada Função", children = [p[3]])

    num_id += 1

def p_lista_argumentos(p):
    '''
        lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio
    '''

    global num_id

    if(len(p) == 4):
        p[0] = Node(str(num_id) + ". Lista Argumentos", children = [p[1], p[3]])
    else:
        p[0] = Node(str(num_id) + ". Lista Argumentos", children = [p[1]])

    num_id += 1

def p_vazio(p):
    '''
        vazio : 
    '''

    global num_id

    p[0] = Node(str(num_id) + ". Vazio")

    num_id += 1

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
    else:
        print("Syntax error at EOF")

yacc.yacc()

def parser(data, name):
    result = yacc.parse(data)
    DotExporter(result).to_dotfile("output/" + name + ".dot")