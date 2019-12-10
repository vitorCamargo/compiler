# -*- coding: utf-8 -*-
from symbol_table import SymbolTable

TYPES = ['inteiro', 'flutuante']
OPERATIONS = ['=', '<>', '>', '<', '>=', '<=', '&&', '||']

success = True

class Analyzer():
  def __init__(self):
    self.symboltable = SymbolTable()
    success = True

  def scan_tree(self, node):
    currentStatus = self.verify_node(node)

    if(not currentStatus['goNextNode']):
      return

    for child in node.children:
      self.scan_tree(child)

    if(currentStatus['isNewContext']):
      self.symboltable.removeCurrentContext()

    if(currentStatus['isFunction']):
      line = self.symboltable.getGlobal()
      if(line['type'] != '' and not self.symboltable.hasReturn()):
        success = False
        print('[ERRO] Função ' + line['name'] + ' deveria retornar ' + line['type'] + ' em ' + str(line['line']) + ':' + str(line['column']))

  def verify_node(self, node):
    if(node.value == 'declaracao_variaveis'):
      for var in node.children[1:]:
        dimension = self.verify_variable(var)

        status = self.symboltable.insert({
          'name': var.children[0].value,
          'type': node.children[0].value,
          'used': False,
          'symbol_type': 'var',
          'initialized': False,
          'dimension': dimension,
          'line': var.children[0].line,
          'column': var.children[0].column,
          'value': None
        })

        var.children[0].table_pointer = self.symboltable.searchFor(var.children[0].value)
        if(not status):
          success = False

      return {
        'goNextNode': False,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'lista_parametros'):
      for param in node.children:
        self.symboltable.insert({
          'name': param.children[1].value,
          'type': param.children[0].value,
          'used': False,
          'symbol_type': 'params',
          'initialized': True,
          'dimension': int(len(param.children[2:]) / 2),
          'line': param.children[0].line,
          'column': param.children[0].column
        })

        line = self.symboltable.searchFor(param.children[1].value)
        param.children[1].table_pointer = line

      return {
        'goNextNode': False,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'atribuicao'):
      var = node.children[0]
      expression = node.children[1]

      self.verify_variable(var)
      line = self.verify_tableline(var, initialized = True, used = False)
      var_type = 'inteiro'
      if(line):
        var_type = line['type']

      expression_type = self.verify_expression(expression)
      if(expression_type == 'wrong_type'):
        print('[AVISO] Atribuição de tipos distintos \'' + var.table_pointer['name'] + '\' ' + var_type + ' em ' + str(var.table_pointer['line']) + ':' + str(var.table_pointer['column']))
        success = False
      elif(var_type != expression_type and expression_type != None):
        print('[AVISO] Atribuição de tipos distintos \'' + var.table_pointer['name'] + '\' ' + var_type + ' e ' + expression_type + ' em ' + str(var.table_pointer['line']) + ':' + str(var.table_pointer['column']))
        success = False

      return {
        'goNextNode': True,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'corpo'):
      for child in node.children:
        if(child.value == 'expressao'):
          self.verify_expression(child)

      return {
        'goNextNode': True,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'retorna'):
      self.symboltable.setReturn()

      expression_type = self.verify_expression(node.children[0])
      line = self.symboltable.getGlobal()

      if(line['type'] not in TYPES or expression_type not in TYPES):
        success = False
        print('[ERRO] Tipo de Retorno inválido em ' + str(node.line) + ':' + str(node.column))
      elif(line['type'] != expression_type):
        print('[AVISO] Conversão Implícita de tipos em ' + str(node.line) + ':' + str(node.column))

      return {
        'goNextNode': False,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'declaracao_funcao'):
      params = []
      function_type = None

      if(len(node.children) == 4):
        function_type = node.children[0].value
        function_name = node.children[1].value
        params_list = node.children[2]
      else:
        function_name = node.children[0].value
        params_list = node.children[1]

      for param in params_list.children:
        params.append({
          'type': param.children[0].value,
          'vet': 0 if len(param.children) == 2 else int((len(param.children) - 2)/2)
        })

      status = self.symboltable.insert({
        'name': function_name,
        'type': function_type if function_type else '',
        'used': False,
        'symbol_type': 'function',
        'initialized': True,
        'dimension': 0,
        'params': params,
        'line': node.children[0].line,
        'column': node.children[0].column
      })

      line = self.symboltable.searchFor(function_name, used = False)
      if(len(node.children) == 4):
        node.children[1].table_pointer = line
      else:
        node.children[0].table_pointer = line
      if(not status):
        success = False

      self.symboltable.insertContex(function_name)

      return {
        'goNextNode': True,
        'isNewContext': True,
        'isFunction': True,
      }
    elif(node.value == 'repita' or node.value == 'se' or node.value == 'senão'):
      self.symboltable.insertContex(node.value)

      if(node.value == 'repita'):
        for child in node.children:
          if(child.value == 'expression'):
            self.verify_expression(child)

      return {
        'goNextNode': True,
        'isNewContext': True,
        'isFunction': False,
      }
    elif(node.value == 'condicional'):
      for child in node.children:
        if(child.value == 'expression'):
          self.verify_expression(child)

      return {
        'goNextNode': True,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'leia'):
      var = node.children[0]
      var.children[0].table_pointer = self.verify_tableline(var, initialized = True)

      return {
        'goNextNode': True,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'chamada_funcao'):
      self.verify_function(node)

      return {
        'goNextNode': True,
        'isNewContext': False,
        'isFunction': False,
      }
    elif(node.value == 'escreva'):
      self.verify_expression(node.children[0])

      return {
        'goNextNode': False,
        'isNewContext': False,
        'isFunction': False,
      }
    else:
      return {
        'goNextNode': True,
        'isNewContext': False,
        'isFunction': False,
      }

  def verify_variable(self, node):
    dimension = 0

    if(len(node.children) > 1):
      for child in node.children[1].children:
        if(child.value != '[' and child.value != ']'):
          var_type = self.verify_expression(child)
          var = self.verify_tableline(node, False)

          if(var_type and var_type != 'inteiro'):
            success = False
            print('[ERRO] Índice de array \'' + node.children[0].value + '\' não é inteiro, em ' + str(node.children[0].line) + ':' + str(node.children[0].column))
          dimension += 1
    return dimension

  def verify_function(self, node):
    function = self.verify_tableline(node, False)
    node.table_pointer = function

    if(function):
      params = function['params']
      args = []

      for expression in node.children[-1].children:
        arg = {}
        expression_type = self.verify_expression(expression).split(' ')

        arg['type'] = expression_type[0]
        arg['vet'] = int(expression_type[1]) if len(expression_type) == 2 else 0
        args.append(arg)

      if(function['name'] == 'principal'):
        if(self.symboltable.getCurrentContex().scope == 'principal'):
          print('[AVISO] Chamada recursiva para principal.')
        else:
          success = False
          print('[ERRO] Chamada para a função principal não permitida.')
      if(len(params) != len(args)):
        success = False
        print('[ERRO] Chamada à função \'' + function['name'] + '\' com número de parâmetros diferente que o declarado. Esperado ' + str(len(params)) + ', mas recebido ' + str(len(args)) + ', em ' + str(function['line']) + ':' + str(function['column']))
      elif(params != args):
        success = False
        print('[ERRO] Conversão Implícita em função \'' + function['name'] + '\' em ' + str(function['line']) + ':' + str(function['column']))

  def verify_tableline(self, node_type, isError = True, used = True, initialized = False):
    aux = node_type.children[0].value
    line = self.symboltable.searchFor(aux, used = used, initialized = initialized)
    node_type.table_pointer = line

    if(not line):
      success = False
      if(isError):
        success = False
        print('[ERRO] Chamada à ' + ('variável ' if(node_type.value == 'var') else 'função ') + aux + ' que não foi declarada em ' + str(node_type.children[0].line) + ':' + str(node_type.children[0].column))
    return line if line else None

  def verify_expression(self, node):
    if(node.value == 'expressao'):
      return self.verify_expression(node.children[0])

    if(node.value == 'expressao_unaria'):
      children = node.children
      if(len(children) == 1):
        expression_type = children[0].children[0]
      else:
        operation = children[0].value
        expression_type = children[1].children[0]

        if(operation == '!'):
          if(expression_type.value == 'expressao'):
            self.verify_expression(expression_type)
          return 'wrong_type'

      if(expression_type.value == 'numero'):
        number = expression_type.children[0].value
        return 'inteiro' if(type(number) is int) else 'flutuante'
      elif(expression_type.value == 'expressao'):
        return self.verify_expression(expression_type)
      else:
        line = self.verify_tableline(expression_type)
        if(line and (line['symbol_type'] == 'var' or line['symbol_type'] == 'params')):
          dimension = line['dimension']
          if(dimension != 0):
            real_dimension = len(expression_type.children) - 1
            if(dimension - real_dimension != 0):
              return line['type']

        if(expression_type.value == 'chamada_funcao'):
          self.verify_function(expression_type)
        return line['type'] if line else None
    elif(len(node.children) >= 2):
      type1 = self.verify_expression(node.children[0])
      type2 = self.verify_expression(node.children[1])

      if(node.value in OPERATIONS):
        if(not type1 or not type2 or (len(type1.split(' ')) == 2 or len(type2.split(' ')) == 2)):
          print('[AVISO] Tipo Inválido em ' + str(node.line) + ':' + str(node.column))

        return 'wrong_type'

      if(type1 == type2):
        return type1
      elif(type1 in TYPES and type2 in TYPES):
        return 'flutuante'
    else:
      return self.verify_expression(node.children[0])

    return None

  def verify_principal(self):
    line = self.symboltable.hasPrincipal()

    if(line and line['used']):
      print('[ERRO] Chamada para a função principal não permitida.')
      success = False
    elif(not line):
      print('[ERRO] Função principal não declarada.')
      success = False

  def verify_other_points(self):
    for line in self.symboltable.getUninitializedLines():
      print('[AVISO] Variável \'' + line['name'] + '\' declarada, e não utilizada em ' + str(line['line']) + ':' + str(line['column']))

    for line in self.symboltable.getUnusedLines():
      if(line['name'] == 'principal'):
        continue
      print('[AVISO] Função \'' + line['name'] + '\' declarada, mas não utilizada em ' + str(line['line']) + ':' + str(line['column']))


def analyzer(tree):
  analyzer = Analyzer()
  analyzer.scan_tree(tree)
  analyzer.verify_principal()
  analyzer.verify_other_points()

  return success