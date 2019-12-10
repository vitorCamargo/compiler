# -*- coding: utf-8 -*-
import sys
import os

from anytree.exporter import UniqueDotExporter

import lex
import syn
import pruning_tree
import sem
import code_generator

def print_tokens(tokens):
  for token in tokens:
    print("<" + token["token"] + "> --> \"" + str(token["value"]) + "\" at " + str(token["line"]) + ":" + str(token["column"]))

def main():
  if(len(sys.argv) != 2):
    print('\n\n---------------> ERRO: -1 <---------------')
    print('Rode o progama com: ')
    print('# python .\\main.py .\\test_file.tpp \n\n')
    return -1

  if(os.path.isfile(str(sys.argv[1])) == False):
    print('\n\n---------------> ERRO: -2 <---------------')
    print('Arquivo Teste Inválido!\n\n')
    return -2

  test_file = open(sys.argv[1], 'r', encoding = 'utf-8').read()
  filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
  file_num_lines = sum(1 for line in open(sys.argv[1], 'r', encoding = 'utf-8'))

  print('\n\nCompilador T++ desenvolvido por Vitor Bueno (RA: 1921959) para a matéria de  \'Compiladores\' na Universidade Tecnológica Federal do Paraná (UTFPR) - Câmpus Campo Mourão')
  print('§§§§§§§§§§§ Rodando Léxico §§§§§§§§§§§\n\n')

  tokens, success = lex.tokenizator(test_file)
  if(not success):
    return

  print_tokens(tokens)

  print('\n\n§§§§§§§§§§§ Rodando Analisador Sintático §§§§§§§§§§§\n\n')

  tree, success = syn.parser(test_file, file_num_lines)
  if(not success):
    return

  UniqueDotExporter(tree).to_picture("output/" + filename + ".png")
  print("Árvore .dot gerada em: \'./output/" + filename + ".png\'")

  print('\n\n§§§§§§§§§§§ Rodando Analisador Semântico §§§§§§§§§§§\n\n')

  pruning_tree.prune(tree)
  UniqueDotExporter(tree).to_picture("output/pruned_" + filename + ".png")

  semantic_success = sem.analyzer(tree)

  if(not semantic_success):
    return

  print('\n\n§§§§§§§§§§§ Gerando Código §§§§§§§§§§§\n\n')

  code_generator.main(tree, filename)

main()