inteiro:vet[10]
inteiro: tam

tam := 10

preencheVetor() { preenche o vetor no pior caso }
  inteiro: i
  inteiro: j

  i := 0
  j := tam

  repita
    vet[i] = j
    i := i + 1
    j := j - 1
  até i < tam
fim

insertion_sort() { implementação do insertion sort }
  inteiro: i
  inteiro: j
  inteiro: key

  i := 1

  repita
    key := vet[i]
    j := i - 1

    inteiro: aux
    aux := 1

    repita
      se j >= 0 && vet[j] > key então
        vet[j + 1] := vet[j]
        j := j - 1
      senão
        aux := 0
      fim
    até aux = 0

    i := i + 1
  até i < tam
fim

inteiro principal() { programa principal }
  preencheVetor()
  insertion_sort()
  retorna(0)
fim