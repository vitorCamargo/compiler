# -*- coding: utf-8 -*-
from anytree import PreOrderIter, Node

class SymbolTable():
  def __init__(self):
    self.id = 1
    self.root = Node(0, scope = 'global', table = [])
    self.contex = self.root

  def insert(self, item):
    item['contex'] = self.contex.scope
    line = self.searchFor(item['name'], False)

    if(item['name'] == 'principal' and item['contex'] != 'global' and item['symbol_type'] != 'function'):
      print('[ERRO] Função \'principal\' deve ser uma função.')
      return False

    if(line and line['contex'] == self.contex.scope):
      print('[ERRO] ' + ('Variável ' if(item['symbol_type'] == 'var') else 'Função ') + '\'' + item['name'] + '\' já declarada anteriormente em ' + str(item['line']) + ':' + str(item['column']))
      return False

    self.contex.table.append(item)

    return True

  def insertContex(self, contex):
    self.contex = Node(self.id, self.contex, scope = contex, table = [], hasReturn = False)
    self.id += 1

  def removeCurrentContext(self):
    self.contex = self.contex.parent

  def search(self, node, name):
    for line in node.table:
      if(line['name'] == name):
        return line

    if(node.parent):
      return self.search(node.parent, name)
    else:
      return False

  def searchReturn(self, contex):
    flag_return = False
    has_return = False

    for inner in contex.children:
      response_return = inner.hasReturn

      if(not inner.hasReturn):
        response_return = self.searchReturn(inner)

      if(inner.scope == 'se'):
        flag_return = response_return
      elif(flag_return and inner.scope == 'senão' and response_return):
        has_return = True
    return has_return

  def searchFor(self, name, used = True, initialized = False):
    line = self.search(self.contex, name)

    if(line and used):
      line['used'] = True

    if(line and initialized):
      line['initialized'] = True
    return line

  def getUnusedLines(self):
    response = []

    for contex in PreOrderIter(self.root):
      for line in contex.table:
        if(not line['used']):
          response.append(line)

    return response

  def getUninitializedLines(self):
    response = []

    for contex in PreOrderIter(self.root):
      for line in contex.table:
        if(not line['initialized']):
          response.append(line)

    return response

  def getCurrentContex(self):
    return self.contex
    
  def getGlobal(self):
    return self.root.table[-1]

  def setReturn(self):
    self.contex.hasReturn = True

  def hasPrincipal(self):
    for line in self.root.table:
      if(line['name'] == 'principal'):
        return line

    return False

  def hasReturn(self):
    function_return = self.root.children[-1].hasReturn

    if(function_return):
      return function_return

    return self.searchReturn(self.root.children[-1])

  def __repr__(self):
    return str(self.root.table[-1])