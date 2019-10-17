# -*- coding: utf-8 -*-
import sys
import os

from anytree.exporter import DotExporter

import lex
import syn

def print_tokens(tokens):
  for token in tokens:
    print("<" + token["token"] + "> --> \"" + str(token["value"]) + "\" at " + str(token["line"]) + ":" + str(token["column"]))

def main():
  if(len(sys.argv) != 2):
    print('\n\n---------------> ERROR: -1 <---------------')
    print('Run programm with: ')
    print('# python .\\main.py .\\test_file.tpp \n\n')
    return -1

  if(os.path.isfile(str(sys.argv[1])) == False):
    print('\n\n---------------> ERROR: -2 <---------------')
    print('Invalid Test File!\n\n')
    return -2

  test_file = open(sys.argv[1], 'r', encoding = 'utf-8').read()
  filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
  print('\n\nT++ Compiler developed by Vitor Bueno (RA: 1921959) for \'Compilers\' Subject at the Federal Technological University of Paraná (UTFPR) - Câmpus Campo Mourão')
  print('§§§§§§§§§§§ Running Lexer §§§§§§§§§§§\n\n')

  tokens, success = lex.tokenizator(test_file)
  if(not success):
    return

  print_tokens(tokens)

  print('\n\n§§§§§§§§§§§ Running Syntatic Parser §§§§§§§§§§§\n\n')

  tree, success = syn.parser(test_file)
  if(not success):
    return
  
  DotExporter(tree).to_picture("output/" + filename + ".png")
  print("Generated .dot tree at: \'./output/" + filename + ".png\'")

main()