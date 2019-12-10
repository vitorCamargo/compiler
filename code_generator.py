# -*- coding: utf-8 -*-
from llvmlite import ir
from llvmlite import binding as llvm
from ctypes import CFUNCTYPE, c_int

t_int = ir.IntType(32)
t_float = ir.DoubleType()
t_void = ir.VoidType()

operations_types = {
  'retorna': 'retorna',
  'conditional': 'conditional',
  'loop': 'loop'
}

class CodeGenerator():
  def __init__(self, filename):
    self.module = ir.Module(filename)

    self.id_loop = 0

    self.builder = None
    self.current_function = None

    self.functions = {}
    self.variables_global = {}
    self.variables_locals = {}

    self.seen_nodes = []

  def scan_tree(self, node):
    returnedValue = None
    insideFunction = False
    hasSpecialType = False

    if(node.value == 'declaracao_variaveis'):
      children = node.children

      llvm_type = self.getType(children[0].value)

      for variable in children[1:]:
        table = variable.children[0].table_pointer

        if(not self.current_function):
          if(table['dimension'] == 0):
            self.variables_global[table['name']] = ir.GlobalVariable(self.module, llvm_type, table['name'])
            self.variables_global[table['name']].linkage = 'internal'

          elif(table['dimension'] == 1):
            index = variable.children[1]
            val = self.verify_expression(index.children[1])
            array_type = ir.ArrayType(llvm_type, val.constant)
            self.variables_global[table['name']] = ir.GlobalVariable(self.module, array_type, table['name'])
            self.variables_global[table['name']].linkage = 'internal'

          else:
            index = variable.children[1]
            val_1 = self.verify_expression(index.children[1])
            val_2 = self.verify_expression(index.children[4])
            array_type_inner = ir.ArrayType(llvm_type, val_2.constant)
            array_type = ir.ArrayType(array_type_inner, val_1.constant)
            self.variables_global[table['name']] = ir.GlobalVariable(self.module, array_type, table['name'])
            self.variables_global[table['name']].linkage = 'internal'

        else:
          if(table['dimension'] == 0):
            self.variables_locals[table['name']] = self.builder.alloca(llvm_type, name = table['name'])

          elif(table['dimension'] == 1):
            index = variable.children[1]
            val = self.verify_expression(index.children[1])
            array_type = ir.ArrayType(llvm_type, val.constant)

            self.variables_locals[table['name']] = self.builder.alloca(array_type, name = table['name'])

          else:
            index = variable.children[1]
            val_1 = self.verify_expression(index.children[1])
            val_2 = self.verify_expression(index.children[4])

            array_type_inner = ir.ArrayType(llvm_type, val_2.constant)
            array_type = ir.ArrayType(array_type_inner, val_1.constant)

            self.variables_locals[table['name']] = self.builder.alloca(array_type, name = table['name'])
    elif(node.value == 'atribuicao'):
      self.verify_assignment(node)
    elif(node.value == 'declaracao_funcao'):
      children = node.children
      params_names = []
      params_types = []

      if(len(children) != 3):
        return_type = children[0].value
        function_names = children[1].value

        for par in children[2].children:
          params_types.append(par.children[0].value)
          params_names.append(par.children[1].value)
      else:
        return_type = 'void'
        function_names = children[0].value

        for par in children[1].children:
          params_types.append(par.children[0].value)
          params_names.append(par.children[1].value)        

      function_names = function_names if function_names != 'principal' else 'main'

      llvm_return_type = self.getType(return_type)
      llvm_args_type = []
      for _type in params_types:
        llvm_args_type.append(self.getType(_type))

      function_type = ir.FunctionType(llvm_return_type, llvm_args_type)

      self.current_function = ir.Function(self.module, function_type, function_names)
      bb = self.current_function.append_basic_block('entry')
      self.builder = ir.IRBuilder(bb)

      self.functions[function_names] = self.current_function

      i = 0
      for name in params_names:
        val = self.current_function.args[i]
        type_ = params_types[i]
        self.variables_locals[name] = self.builder.alloca(self.getType(type_), name = name)
        self.builder.store(val, self.variables_locals[name])
        i += 1

      if(function_names == 'main'):
        for global_init in self.seen_nodes:
          self.verify_assignment(global_init)

      insideFunction = True
    elif(node.value == 'retorna'):
      self.builder.ret(self.loadValue(self.verify_expression(node.children[0])))

      return operations_types['retorna']
    elif(node.value == 'condicional'):
      node_before = self.verify_expression(node.children[0])

      if(len(node.children) == 3):
        se = node.children[1]
        senao = node.children[2]

        with self.builder.if_else(node_before) as (if_block, else_block):
          with if_block:
            self.scan_tree(se)
          with else_block:
            self.scan_tree(senao)
      else:
        se = node.children[1]

        with self.builder.if_then(node_before):
          self.scan_tree(se)

      return operations_types['conditional']
    elif(node.value == 'repita'):
      body = node.children[0]
      expression = node.children[1]

      loop_block = self.builder.append_basic_block('loop_' + str(self.id_loop))
      loop_end = self.builder.append_basic_block('end_loop_' + str(self.id_loop))
      self.id_loop += 1

      self.builder.cbranch(self.verify_stop_pred(expression), loop_block, loop_end)
      self.builder.position_at_end(loop_block)

      self.scan_tree(body)

      self.builder.cbranch(self.verify_stop_pred(expression), loop_block, loop_end)
      self.builder.position_at_end(loop_end)

      return operations_types['loop']
    elif(node.value == 'escreva'):
      value = self.verify_expression(node.children[0])

      if(str(value.type) == 'i32'):
        fmt = self.global_int
      else:
        fmt = self.global_float

      voidptr_ty = ir.IntType(8).as_pointer()
      fmt_arg = self.builder.bitcast(fmt, voidptr_ty)

      self.builder.call(self.printf, [fmt_arg, value])
    elif(node.value == 'leia'):
      node_variable = node.children[0]
      name = node_variable.children[0].value
      value = self.verify_variable(name)

      line = node_variable.children[0].table_pointer
      if(line['type'] == 'inteiro'):
        fmt = self.global_int_read
      else:
        fmt = self.global_float_read

      voidptr_ty = ir.IntType(8).as_pointer()
      fmt_arg = self.builder.bitcast(fmt, voidptr_ty)

      read_value = self.builder.call(self.scanf, [fmt_arg, value])
    elif(node.value == 'expressao'):
      if(node.parent.value == 'corpo'):
        self.verify_expression(node)

    for child in node.children:
      next_node = self.scan_tree(child)

      if(insideFunction and next_node == operations_types['conditional'] or next_node == operations_types['loop']):
        hasSpecialType = False
      elif(insideFunction and next_node == operations_types['retorna']):
        hasSpecialType = True
      elif(not insideFunction):
        returnedValue = next_node if next_node else returnedValue

    if(insideFunction):
      if not hasSpecialType:
        return_type = self.current_function.return_value.type
        integer_type = self.getType('inteiro')
        float_type = self.getType('flutuante')

        if(return_type is integer_type):
          self.builder.ret(ir.Constant(integer_type, 0))
        elif(return_type is float_type):
          self.builder.ret(ir.Constant(float_type, 0))
        else:
          self.builder.ret_void()

      self.variables_locals = {}
      self.current_function = None

    return returnedValue

  def start_printf(self):
    voidptr_ty = ir.IntType(8).as_pointer()
    printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg = True)
    printf = ir.Function(self.module, printf_ty, name = 'printf')
    self.printf = printf

    fmt = '%f \n\0'
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode('utf8')))
    global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name = 'fstr_float')
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    self.global_float = global_fmt

    fmt = '%d \n\0'
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode('utf8')))
    global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name = 'fstr_int')
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    self.global_int = global_fmt

  def start_scanf(self):
    voidptr_ty = ir.IntType(8).as_pointer()
    scanf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg = True)
    scanf = ir.Function(self.module, scanf_ty, name = 'scanf')
    self.scanf = scanf

    fmt = '%lf\00'
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode('utf8')))
    global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name = 'fstr_float_r')
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    self.global_float_read = global_fmt

    fmt = '%i\00'
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode('utf8')))
    global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name = 'fstr_int_r')
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    self.global_int_read = global_fmt

  def verify_variable(self, name):
    return self.variables_locals[name] if name in self.variables_locals.keys() else self.variables_global[name]

  def verify_call_function(self, node):
    params = node.table_pointer['params']
    pos = 0
    args = []

    for arg in node.children[1].children:
      exp = self.verify_expression(arg)
      if(params[pos]['type'] == 'inteiro'):
        try:
          exp = self.builder.fptosi(exp, self.getType('inteiro'))
        except expression as identifier:
          pass
      else:
        try:
          exp = self.builder.sitofp(exp, self.getType('flutuante'))
        except expression as identifier:
          pass
      args.append(exp)
      pos += 1

    function_name = self.functions[node.children[0].value]
    return self.builder.call(function_name, args)

  def verify_expression(self, node):
    child = node.children[0] if node.value == 'expressao' else node

    if(child.value == 'lista_argumentos' and child.children[0].value == 'expressao_unaria'):
      child = child.children[0]

    if(child.value == 'expressao_unaria'):
      if(len(child.children) == 1):
        number_type = child.children[0].children[0]

        if(number_type.value == 'numero'):
          num = number_type.children[0].value
          t_num = 'inteiro' if type(num) is int else 'flutuante'

          return ir.Constant(self.getType(t_num), num)
        elif(number_type.value == 'var'):
          name = number_type.children[0].value
          var = self.loadValue(self.verify_variable(name))

          if(len(number_type.children) == 2):
            index = number_type.children[1]
            for child in index.children:
              if(child.value == 'expression'):
                exp = self.verify_expression(child)
                var = self.builder.gep(self.verify_variable(name), [ir.Constant(self.getType('inteiro')), exp], 0)
                var = self.loadValue(var)

          return var
        elif(number_type.value == 'chamada_funcao'):
          return self.verify_call_function(number_type)
        else:
          return self.verify_expression(number_type)
      else:
        number_type = child.children[1].children[0]

        if(number_type.value == 'numero'):
          num = number_type.children[0].value
          t_num = 'inteiro' if type(num) is int else 'flutuante'
          return self.builder.not_(ir.Constant(self.getType(t_num)), num)
        elif(number_type.value == 'var'):
          name = number_type.children[0].value
          var = self.loadValue(self.verify_variable(name))

          if(len(number_type.children) == 2):
            i = number_type.children[1]
            for child in i.children:
              if(child.value == 'expression'):
                exp = self.verify_expression(child)
                var = self.builder.gep(self.verify_variable(name), [ir.Constant(self.getType('inteiro')), exp], 0)
                var = self.loadValue(var)

          return self.builder.not_(var)
        elif(number_type.value == 'chamada_funcao'):
          return self.builder.not_(self.verify_call_function(number_type))
        else:
          return self.builder.not_(self.verify_expression(number_type))
    else:
      val_1 = self.verify_expression(child.children[0])
      val_2 = self.verify_expression(child.children[1])
      value = child.value

      if(val_1.type is self.getType('inteiro') and val_2.type is self.getType('inteiro')):
        if(value == '+'):
          return self.builder.add(val_1, val_2)
        elif(value == '-'):
          return self.builder.sub(val_1, val_2)
        elif(value == '*'):
          return self.builder.mul(val_1, val_2)
        elif(value == '/'):
          return self.builder.sdiv(val_1, val_2)
        elif(value == '='):
          return self.builder.icmp_signed('==', val_1, val_2)
        elif(value == '<'):
          return self.builder.icmp_signed('<', val_1, val_2)
        elif(value == '>'):
          return self.builder.icmp_signed('>', val_1, val_2)
        elif(value == '<='):
          return self.builder.icmp_signed('<=', val_1, val_2)
        elif(value == '>='):
          return self.builder.icmp_signed('>=', val_1, val_2)
        elif(value == '<>'):
          return self.builder.icmp_signed('!=', val_1, val_2)
        elif(value == '&&'):
          return self.builder.and_(val_1, val_2)
        elif(value == '||'):
          return self.builder.or_(val_1, val_2)
      else:
        if(val_1.type is t_int):
          val_1 = self.builder.sitofp(val_1, t_float)
        if(val_2.type is t_int):
          val_2 = self.builder.sitofp(val_2, t_float)

        if(value == '+'):
          return self.builder.fadd(val_1, val_2)
        elif(value == '-'):
          return self.builder.fsub(val_1, val_2)
        elif(value == '*'):
          return self.builder.fmul(val_1, val_2)
        elif(value == '/'):
          return self.builder.fdiv(val_1, val_2)
        elif(value == '='):
          return self.builder.icmp_signed('==', val_1, val_2)
        elif(value == '<'):
          return self.builder.icmp_signed('<', val_1, val_2)
        elif(value == '>'):
          return self.builder.icmp_signed('>', val_1, val_2)
        elif(value == '<='):
          return self.builder.icmp_signed('<=', val_1, val_2)
        elif(value == '>='):
          return self.builder.icmp_signed('>=', val_1, val_2)
        elif(value == '<>'):
          return self.builder.icmp_signed('!=', val_1, val_2)
        elif(value == '&&'):
          return self.builder.and_(val_1, val_2)
        elif(value == '||'):
          return self.builder.or_(val_1, val_2)

  def verify_assignment(self, node):
    children = node.children
    node_variable = children[0]
    name = node_variable.children[0].value

    if(not self.current_function):
      self.seen_nodes.append(node)
    else:
      variable = self.verify_variable(name)
      res = self.verify_expression(children[1])
      res = self.loadValue(res)

      if(len(node_variable.children) == 2):
        index = node_variable.children[1]
        for child in index.children:
          if(child.value == 'expressao'):
            variable = self.builder.gep(variable, [ir.Constant(self.getType('inteiro'), 0), self.verify_expression(child)])

      try:
        self.builder.store(res, variable)
      except TypeError:
        if(node_variable.table_pointer['type'] == 'inteiro'):
          response = self.builder.fptosi(res, self.getType('inteiro'))
          self.builder.store(response, variable)
        else:
          response = self.builder.sitofp(res, self.getType('flutuante'))
          self.builder.store(response, variable)

  def verify_stop_pred(self, exp):
    return self.builder.not_(self.verify_expression(exp))

  def compile_code(self):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()

    backing_mod = llvm.parse_assembly('')
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    mod = llvm.parse_assembly(str(self.module))
    mod.verify()

    engine.add_module(mod)
    engine.finalize_object()

    func_ptr = engine.get_function_address('main')

    c_fn = CFUNCTYPE(c_int)(func_ptr)
    c_fn()

  def getType(self, value):
    if(value.lower() == 'inteiro'):
      return t_int
    elif(value.lower() == 'flutuante'):
      return t_float
    elif(value.lower() == 'void'):
      return t_void

  def loadValue(self, val):
    if(type(val) is not ir.values.GlobalVariable and type(val) is not ir.instructions.AllocaInstr and type(val) is not ir.instructions.GEPInstr):
      return val
    else:
      return self.builder.load(val, align = 4)

def main(tree, filename):
  generator = CodeGenerator(filename)
  generator.start_printf()
  generator.start_scanf()

  generator.scan_tree(tree)

  print(generator.module)
  generator.compile_code()