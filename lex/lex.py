# -*- coding: utf-8 -*-
import ply.lex as lex

reserved = { # Reserved Words in T++
  'principal': 'PRINCIPAL',
  'retorna': 'RETORNA',
  'leia': 'LEIA',
  'escreva': 'ESCREVA',
  'se': 'SE',
  'então': 'ENTAO',
  'senão': 'SENAO',
  'repita': 'REPITA',
  'até': 'ATE',
  'fim': 'FIM',
  'inteiro': 'INTEIRO',
  'flutuante': 'FLUTUANTE'
}

tokens = [
  'ID',
  'ATRIBUICAO',
  'COMENTARIO',

  # Language Symbols
  'DOIS_PONTOS',
  'VIRGULA',
  'ABRE_PARENTESES',
  'FECHA_PARENTESES',
  'ABRE_CONCHETES',
  'FECHA_CONCHETES',

  # Operators
  'ADICAO',
  'SUBTRACAO',
  'MULTIPLICACAO',
  'DIVISAO',
  'IGUAL',
  'DIFERENTE',
  'MENOR_IGUAL',
  'MAIOR_IGUAL',
  'MENOR',
  'MAIOR',

  # Logical
  'E',
  'OU',
  'NEGACAO',

  # Numbers (Type of)
  'NUM_FLUTUANTE',
  'NUM_INTEIRO'
] + list(reserved.values())

# Regular Expressions
t_ATRIBUICAO = r'\:\='

t_DOIS_PONTOS = r'\:'
t_VIRGULA = r'\,'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_ABRE_CONCHETES = r'\['
t_FECHA_CONCHETES = r'\]'

t_ADICAO = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'\/'
t_IGUAL = r'\='
t_DIFERENTE = r'\<\>'
t_MENOR_IGUAL = r'\<\='
t_MAIOR_IGUAL = r'\>\='
t_MENOR = r'\<'
t_MAIOR = r'\>'

t_E = r'\&\&'
t_OU = r'\|\|'
t_NEGACAO = r'\!'

t_ignore = ' \t\r\f\v'

# Other (More Specific) Regular Expressions
def t_ID(t):
  r'[a-zA-Z_áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ][a-zA-Z_0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_COMENTARIO(t):
  r'(\{(.|\n)*?\})|(\{(.|\n)*?)$'
  return t

def t_NUM_FLUTUANTE(t):
  r'(\d+(\.\d*)?[eE][-+]?\d+)|(\d+\.\d*)'
  t.value = float(t.value)
  return t

def t_NUM_INTEIRO(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	pass

def t_error(t):
	print('Invalid Caracter was found:', t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

def tokenizator(data):
  lexer.input(data)

  tokens = []

  while True:
    generated_token = lexer.token()
    if not generated_token: break
    print(generated_token)

    tokens.append(generated_token)

  return tokens