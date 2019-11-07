# -*- coding: utf-8 -*-
from anytree import Node, RenderTree

nodes = []

def verify_node(node):
  if(node.value == 'programa'):
    program = node
    children = list(program.children)

    while(len(children) > 0):
      if(children[0].value == 'declaracao'):
        node = children[0]
        children = children[1:]

        node.parent = None
        node.children[0].parent = program
      else:
        node = children[0]
        node.parent = None

        children = children[1:]
        children = list(node.children) + children

    return program
  elif(node.value == 'cabecalho'):
    for child in node.children:
      node.parent.children = list(node.parent.children) + [child]

    cabecalho = node.parent
    node.parent = None

    return cabecalho
  elif(node.value == 'corpo'):
    body = node
    children = list(body.children)
    
    while(len(children) > 0):
      if(children[0].value == 'acao'):
        node = children[0]
        children = children[1:]

        node.parent = None
        node.children[0].parent = body
      else:
        node = children[0]
        node.parent = None

        children = children[1:]
        if len(node.children) > 0:
          children = list(node.children) + children

    return body
  elif(node.value == 'tipo' or node.value == ',' or node.value == ':' or node.value == ':=' or node.value == '(' or node.value == ')' or node.value == 'fim'):
    for child in node.children:
      node.parent.children = [child] + list(node.parent.children)
    node.parent = None

    return None
  elif(node.value == 'lista_variaveis'):
    parent = node.parent
    children = list(node.children)

    while(len(children) > 0):
      if(children[0].value == 'var'):
        var = children[0]
        children = children[1:]
        var.parent = parent
      else:
        var = children[0]
        var.parent = None

        children = children[1:]
        children = list(var.children) + children

    node.parent = None

    return parent
  elif(node.value == 'inicializacao_variaveis'):
    new_var = node
    new_var.value = 'atribuicao'
    aux = new_var.children[0]
    aux.parent = None

    for child in aux.children:
      child.parent = new_var

    return new_var
  elif(node.value == 'lista_parametros'):
    first_params_list = node
    children = list(first_params_list.children)

    while(len(children) > 0):
      if(children[0].value == 'parametro'):
        node = children[0]
        children = children[1:]
        if(node.parent != first_params_list):
          node.parent = None
          first_params_list.children = [node] + list(first_params_list.children)
      else:
        node = children[0]
        node.parent = None
        children = children[1:]
        if(len(node.children) > 0):
          children = list(node.children) + children

    return first_params_list
  elif(node.value == 'lista_argumentos'):
    first_argument_list = node
    children = list(first_argument_list.children)

    while(len(children) > 0):
      if(children[0].value != 'expressao'):
        node = children[0]
        children = children[1:]
        if(node.parent != first_argument_list):
          node.parent = None
          first_argument_list.children = [node] + list(first_argument_list.children)
      else:
        node = children[0]
        node.parent = None
        children = children[1:]
        if(len(node.children) > 0):
          children = list(node.children) + children

    return first_argument_list
  elif(node.value == 'parametro'):
    first_param = node
    children = list(first_param.children)

    while(len(children) > 0):
      if(children[0].value == 'parametro'):
        node = children[0]
        node.parent = None
        children = children[1:]
        if len(node.children) > 0:
          children = list(node.children) + children
      else:
        node = children[0]
        children = children[1:]
        if(node.parent != first_param):
          first_param.children = [node] + list(first_param.children)

    return first_param
  elif(node.value == 'indice'):
    index = node
    children = list(index.children)

    while(len(children) > 0):
      if(children[0].value == 'indice'):
        node = children[0]
        children = children[1:]
        node.parent = None
        new_children = []

        for child in node.children:
          child.parent = None
          new_children.append(child)

        children = new_children + children
        index.children = new_children + list(index.children)
      else:
        children = children[1:]

    return index
  elif(node.value == 'retorna' or node.value == 'leia' or  node.value == 'escreva' or node.value == 'então' or node.value == 'repita' or node.value == 'até'):
    action = node
    children = list(action.children)

    while(len(children) > 0):
      if(children[0].value == 'então' or children[0].value == 'até' or children[0].value == 'leia' or children[0].value == 'repita' or children[0].value == 'escreva' or children[0].value == 'retorna'):
        children[0].parent = None
        action.line = children[0].line
        action.column = children[0].column
      children = children[1:]

    return action
  elif(node.value == 'condicional'):
    conditional = node
    children = conditional.children
    se = children[0]
    exp = children[1]
    body = children[3]

    se.parent = None
    exp.parent = None
    children[2].parent = None
    body.parent = None

    exp.parent = conditional
    se.parent = conditional
    body.parent = se

    if(len(children) > 5):
      senao = children[4]
      body_senao = children[5]

      senao.parent = None

      children[6].parent = None

      senao.parent = conditional
      body_senao.parent = senao
    else:
      children[4].parent = None
    
    return conditional
  elif(node.value == 'expressao_logica' or node.value == 'expressao_simples' or node.value == 'expressao_multiplicativa' or node.value == 'expressao_adtiva'):
    expression = node
    children = list(expression.children)

    if(len(children) == 1):
      expression.value = children[0].value
      children[0].parent = None

      for child in children[0].children:
        child.parent = expression

      expression = expression.parent
    elif(len(children) == 3):
      expression.value = children[1].children[0].value
      expression.line = children[1].children[0].line
      expression.column = children[1].children[0].column

      new_children = list(expression.children)
      new_children.pop(1)
      expression.children = new_children

    return expression
  elif(node.value == 'operador_logico' or node.value == 'operador_soma' or node.value == 'operador_multiplicacao' or node.value == 'operador_relacional'):
    root = node
    child = root.children[0]

    child.parent = None
    root.value = child.value

    return root
  elif(node.value == 'expressao'):
    expression = node
    child = list(expression.children)[0]

    if(child.value == 'atribuicao'):
      child.parent = None
      expression.value = child.value
      expression.children = child.children
    return expression

  return node

def prune(original_tree):
  global nodes
  nodes.append(original_tree)

  tree = verify_node(original_tree)

  if(not tree and tree not in nodes):
    return
  for child in tree.children:
    prune(child)