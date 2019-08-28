# -*- coding: utf-8 -*-
import sys
import os

import lex.lex as lex

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
  print('\n\nT++ Compiler developed by Vitor Bueno (RA: 1921959) for \'Compilers\' Subject at the Federal Technological University of Paraná (UTFPR) - Câmpus Campo Mourão')
  print('§§§§§§§§§§§ Running Lexer Parser §§§§§§§§§§§\n\n')

  tokens = lex.tokenizator(test_file)
  # print(tokens)

main()