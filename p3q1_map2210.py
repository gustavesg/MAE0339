# -*- coding: utf-8 -*-
"""P3Q1- MAP2210.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b7KRyEY73B9zosgRD4MJqZsfprPSPjKf
"""

#IMPORTA AS BIBLIOTECAS NECESSÁRIAS

import numpy as np
from numpy import linalg 
!pip install prettymatrix
import prettymatrix
import numpy as np
import sys
import time
import math
!pip install magic_square
import magic_square as ms
!pip install memory_profiler
!pip install -U memory_profiler
from memory_profiler import profile

"""##QR POR GRAM-SMITH CLÁSSICO (VERSÃO ORIGINAL)"""

def gs(A):
  
  #INICIA CONTAGEM DE TEMPO
  inicio = time.time()

  #CAPTA O NUMERO DE LINHAS E DE COLUNAS DE A
  num_linhas = np.shape(A)[0]
  num_colunas = np.shape(A)[1]

  #CRIA Q,R 
  Q = np.array([[0 for a in range(num_colunas)] for b in range(num_linhas)], dtype = 'float')
  R = np.array([[0 for a in range(num_colunas)] for b in range(num_colunas)], dtype = 'float')

  #PERCORRE AS COLUNAS
  for k in range(num_colunas):

    #IGUALA AS COLUNAS DE Q AS DE A
    Q[:,k] = A[:,k]

    #ORTOGONALIZA VIA GRAM SMITH
    if k != 0:
      R[0:k,k] = np.matmul(np.transpose(Q[:,k-1]),Q[:,k]) 
      Q[:,k] = Q[:,k] - np.matmul(Q[:,0:k],R[0:k,k]) 


    R[k,k] = np.linalg.norm(Q[:,k])
    Q[:,k] = Q[:,k]/R[k,k]
  
  #FINALIZE TEMPO
  fim = time.time()
  return Q,R,(fim-inicio)

"""##QR POR GRAM-SMITH MODIFICADO (ORIGINAL)




"""

#IMPLEMENTA QR POR GRAM-SMITH MODIFICADO

def modified_gram_smith(A):

  #INICIA A CONTAGEM DE TEMPO
  inicio = time.time()

  ## CAPTA O NÚMERO DE LINHAS E COLUNAS DE A
  num_linhas = np.shape(A)[0]
  num_colunas = np.shape(A)[1]

  #CRIA MATRIZES Q,R
  Q = np.array([[0 for j in range(num_colunas)] for w in range(num_linhas)], dtype = 'float')
  R = np.array([[0 for j in range(num_colunas)] for w in range(num_colunas)], dtype = 'float')

  #PERCORRE COLUNAS
  for k in range(num_colunas):

    #IGUALA COLUNA DE Q COM A DE A
    Q[:,k] = A[:,k]

    for i in range(k):

      R[i,k] = np.matmul(np.transpose(Q[:,i]),Q[:,k])
      Q[:,k] = Q[:,k] - R[i,k]*Q[:,i]
    
    R[k,k] = np.linalg.norm(Q[:,k])
    Q[:,k] = Q[:,k]/R[k,k]

  #FINALIZA TEMPO
  fim = time.time()
  return Q,R,(fim-inicio)

"""##QR POR HOUSEHOLDER (GITHUB ORIGINAL)"""

#IMPLEMENTA QR POR HOUSEHOLDER

# CONVERTE UM ARRAY 1D EM UM VETOR COLUNA

def column_convertor(x):
    
    x.shape = (1, x.shape[0])
    return x

# RETORNA A NORMA

def get_norm(x):
  
    return np.sqrt(np.sum(np.square(x)))

# RETORNA A MATRIZ DE HOUSEHOLDER DO VETOR X DADO

def householder_transformation(v):
  
    size_of_v = v.shape[1]
    e1 = np.zeros_like(v)
    e1[0, 0] = 1
    vector = get_norm(v) * e1
    if v[0, 0] < 0:
        vector = - vector
    u = (v + vector).astype(np.float64)
    H = np.identity(size_of_v) - ((2 * np.matmul(np.transpose(u), u)) / np.matmul(u, np.transpose(u)))

    return H

# RETORNA MATRIZES Q,R 
def qr_step_factorization(q, r, iter, n):
   
    v = column_convertor(r[iter:, iter])
    Hbar = householder_transformation(v)
    H = np.identity(n)
    H[iter:, iter:] = Hbar
    r = np.matmul(H, r)
    q = np.matmul(q, H)

    return q, r

def fatHouseholder(A):

    #INICIA TEMPO
    inicio = time.time()

    n = np.shape(A)[0]
    m = np.shape(A)[1]

    Q = np.identity(n)
    R = A.astype(np.float64)

    for i in range(min(n, m)):
        # For each iteration, H matrix is calculated for (i+1)th row
        Q, R = qr_step_factorization(Q, R, i, n)

    min_dim = min(m, n)
    
    #R = np.around(R, decimals=6)
    R = R[:min_dim, :min_dim]
    #Q = np.around(Q, decimals=6)
    
    #FINALIZA TEMPO
    fim = time.time()
    return Q,R,(fim-inicio)

"""##TESTE GRAM-SMITH CLÁSSICO"""

#TESTE ÚNICO PARA QR POR GRAM-SMITH

#MATRIZ ALEATÓRIA
A = np.random.rand(10,10)

#MATRIZ DIFERENÇA ENTRE A E QR
diferenca =  A - np.matmul(gs(A)[0],gs(A)[1])
print('-'*60)

#NORMA DO MÁXIMO
norma = np.linalg.norm(diferenca, np.inf)
print(f'NORMA DO MÁXIMO DE D = A-QR = {norma}')
print('-'*60)

#NORMA DE FROBENIUS
norma = np.linalg.norm(diferenca, ord = 'fro')
print(f'NORMA DE FROBENIUS DE D = A-QR = {norma}')
print('-'*60)

#NORMA 1
norma = np.linalg.norm(diferenca, ord = 1)
print(f'NORMA 1 DE D = A-QR = {norma}')
print('-'*60)

"""##TESTE GRAM-SMITH MODIFICADO"""

#TESTE ÚNICO PARA QR DE GRAM-SMITH MODIFICADO

#MATRIZ ALEATÓRIA
A = np.random.rand(10,10)

#DIFERENÇA ENTRE A E QR
diferenca =  A - np.matmul(modified_gram_smith(A)[0], modified_gram_smith(A)[1])
print('-'*60)
#NORMA DO MÁXIMO
norma = np.linalg.norm(diferenca, np.inf)
print(f'NORMA DO MÁXIMO DE D = A-QR = {norma}')
print('-'*60)

#NORMA DE FROBENIUS
norma = np.linalg.norm(diferenca, ord = 'fro')
print(f'NORMA DE FROBENIUS DE D = A-QR = {norma}')
print('-'*60)

#NORMA 1
norma = np.linalg.norm(diferenca, ord = 1)
print(f'NORMA 1 DE D = A-QR = {norma}')
print('-'*60)

"""##TESTE HOUSEHOLDER"""

#TESTE ÚNICO PARA QR POR HOUSEHOLDER

#MATRIZ ALEATÓRIA
A = np.random.rand(10,10)

#DIFERENÇA ENTRE A E QR
diferenca =  A - np.matmul(fatHouseholder(A)[0],fatHouseholder(A)[1])

#NORMA DO MÁXIMO
norma = np.linalg.norm(diferenca, np.inf)
print(f'NORMA DO MÁXIMO DE D = A-QR = {norma}')
print('-'*50)

#NORMA DE FROBENIUS
norma = np.linalg.norm(diferenca, ord = 'fro')
print(f'NORMA DE FROBENIUS DE D = A-QR = {norma}')
print('-'*50)

#NORMA 1
norma = np.linalg.norm(diferenca, ord = 1)
print(f'NORMA 1 DE D = A-QR = {norma}')
print('-'*50)

#FUNÇÃO PARA DEVOLVER MATRIZ DE HILBERT

def hilbert_matrix(order):

  h_matrix = np.zeros((order,order))

  for i in range(order):
    for j in range(order):
      h_matrix[i][j] = 1/((i+1)+(j+1)-1)
  
  return h_matrix

# Commented out IPython magic to ensure Python compatibility.
#CARREGA PACOTE DA BIBLIOTECA
# %load_ext memory_profiler

#LISTA PARA ARMAZENAS ERROS DE A E QR

lista_condicionamento_magic = []

#lista dos n 

lista_n =  []

for n in [i for i in range(51,351,50)]:
  
  #APPENDA N NA LISTA
  lista_n.append(n)

  print('-'*35,f'N = {n}', '-------------------------------------'.ljust(10))
  print('='*80)

  #PARTE PARA O GRAM-SMITH CLASSICO
  print('-'*30,'GRAM-SMITH CLÁSSICO','-----------------------------'.ljust(10))
  print('='*80)
  print()
  print('='*30,'MATRIZ DE HILBERT','==============================='.ljust(10))

  #GERA MATRIZ DE HIILBERT 
  matrix_1 = hilbert_matrix(n)

  #CALCULA CONDICIONAMENTO
  condicionamento = np.linalg.cond(matrix_1, p = np.inf)


  #NORMA DA DIFERENÇA ENTRE A E QR
  diferenca_1 =  matrix_1 - np.matmul(gs(matrix_1)[0],gs(matrix_1)[1])
  norma_1 = np.linalg.norm(diferenca_1, np.inf)

  #NORMA DA DIFERENÇA ENTRE I E QQT
  diferenca_2 = np.identity(n) - np.matmul(np.transpose(gs(matrix_1)[0]),gs(matrix_1)[0])
  norma_2 = np.linalg.norm(diferenca_2,np.inf)

  #TEMPO DE EXECUÇÃO
  tempo = gs(matrix_1)[2]

  print('-'*80)
  print(f'MATRIZ DE HILBERT GERADA TEM CONDICIONAMENTO {round(condicionamento,10)}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE A E QR = {norma_1}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE I E Q^T*Q = {norma_2}')
  print('-'*80)
  print(f'TEMPO DE EXECUÇÃO = {tempo}s')
  print('-'*80)
  print()
  print('='*30,'MATRIZ MÁGICA','==================================='.ljust(10))

  #GERA MATRIZ MÁGICA
  matrix_2 = ms.magic(n)

  #CALCULA CONDICIONAMENTO 
  condicionamento = np.linalg.cond(matrix_2, p = np.inf)

  #APPENDA NA LISTA
  lista_condicionamento_magic.append(condicionamento)

  #NORMA DA DIFERENÇA
  diferenca_1 = matrix_2 - np.matmul(gs(matrix_2)[0],gs(matrix_2)[1])
  norma_1 = np.linalg.norm(diferenca_1, np.inf)

  #NORMA DA DIFERENÇA ENTRE I E QQT
  diferenca_2 = np.identity(n) - np.matmul(np.transpose(gs(matrix_2)[0]),gs(matrix_2)[0])
  norma_2 = np.linalg.norm(diferenca_2,np.inf)

  #APPENDA NORMA NA LISTA DE ERROS

  #TEMPO DE EXECUÇÃO
  tempo = gs(matrix_2)[2]

  print('-'*80)
  print(f'MATRIZ MÁGICA GERADA TEM CONDICIONAMENTO {round(condicionamento,10)}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE A E QR = {norma_1}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE I E Q^T*Q = {norma_2}')
  print('-'*80)
  print(f'TEMPO DE EXECUÇÃO = {tempo}s')
  print('-'*80)
#---------------------------------------------------------------------------------------------------------------#
  #*PARTE PARA O GRAM-SMITH MODIFICADO
  print()
  print()
  print('='*80)
  print('-'*30,'GRAM-SMITH MODIFICADO','---------------------------'.ljust(10))
  
  print('='*80)
  print()
  print('='*30,'MATRIZ DE HILBERT','==============================='.ljust(10))

  #GERA MATRIZ DE HIILBERT 
  matrix_1 = hilbert_matrix(n)

  #CALCULA CONDICIONAMENTO
  condicionamento = np.linalg.cond(matrix_1, p = np.inf)


  #NORMA DA DIFERENÇA ENTRE A E QR
  diferenca_1 =  matrix_1 - np.matmul(modified_gram_smith(matrix_1)[0],modified_gram_smith(matrix_1)[1])
  norma_1 = np.linalg.norm(diferenca_1, np.inf)

  #NORMA DA DIFERENÇA ENTRE I E QQT
  diferenca_2 = np.identity(n) - np.matmul(np.transpose(modified_gram_smith(matrix_1)[0]),modified_gram_smith(matrix_1)[0])
  norma_2 = np.linalg.norm(diferenca_2,np.inf)

  #TEMPO DE EXECUÇÃO
  tempo = modified_gram_smith(matrix_1)[2]

  print('-'*80)
  print(f'MATRIZ DE HILBERT GERADA TEM CONDICIONAMENTO {round(condicionamento,10)}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE A E QR = {norma_1}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE I E Q^T*Q = {norma_2}')
  print('-'*80)
  print(f'TEMPO DE EXECUÇÃO = {tempo}s')
  print('-'*80)
  print()
  print('='*30,'MATRIZ MÁGICA','==================================='.ljust(10))

  #GERA MATRIZ MÁGICA
  matrix_2 = ms.magic(n)

  #CALCULA CONDICIONAMENTO 
  condicionamento = np.linalg.cond(matrix_2, p = np.inf)

  #APPENDA NA LISTA
  lista_condicionamento_magic.append(condicionamento)

  #NORMA DA DIFERENÇA ENTRE A E QR
  diferenca_1 = matrix_2 - np.matmul(modified_gram_smith(matrix_2)[0],modified_gram_smith(matrix_2)[1])
  norma_1 = np.linalg.norm(diferenca_1, np.inf)

  #NORMA DA DIFERENÇA ENTRE I E QQT
  diferenca_2 = np.identity(n) - np.matmul(np.transpose(modified_gram_smith(matrix_2)[0]),modified_gram_smith(matrix_2)[0])
  norma_2 = np.linalg.norm(diferenca_2,np.inf)

  #TEMPO DE EXECUÇÃO
  tempo = modified_gram_smith(matrix_2)[2]


  print('-'*80)
  print(f'MATRIZ MÁGICA GERADA TEM CONDICIONAMENTO {round(condicionamento,10)}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE A E QR = {norma_1}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE I E Q^T*Q = {norma_2}')
  print('-'*80)
  print(f'TEMPO DE EXECUÇÃO = {tempo}s')
  print('-'*80)

#---------------------------------------------------------------------------------------------------------#
#PARTE PARA A HOUSEHOLDER

  print()
  print()
  print('='*80)
  print('-'*30,'FATORACAO HOUSEHOLDER','---------------------------'.ljust(10))
  print('='*80)
  print()
  print('='*30,'MATRIZ DE HILBERT','==============================='.ljust(10))

  #GERA MATRIZ DE HIILBERT 
  matrix_1 = hilbert_matrix(n)

  #CALCULA CONDICIONAMENTO
  condicionamento = np.linalg.cond(matrix_1, p = np.inf)


  #NORMA DA DIFERENÇA
  diferenca_1 =  matrix_1 - np.matmul(fatHouseholder(matrix_1)[0],fatHouseholder(matrix_1)[1])
  norma_1 = np.linalg.norm(diferenca_1, np.inf)

  #NORMA DA DIFERENÇA ENTRE I E QQT
  diferenca_2 = np.identity(n) - np.matmul(np.transpose(fatHouseholder(matrix_1)[0]),fatHouseholder(matrix_1)[0])
  norma_2 = np.linalg.norm(diferenca_2,np.inf)


  #TEMPO DE EXECUÇÃO
  tempo = fatHouseholder(matrix_1)[2]


  print('-'*80)
  print(f'MATRIZ DE HILBERT GERADA TEM CONDICIONAMENTO {round(condicionamento,10)}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE A E QR = {norma_1}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE I E Q^T*Q = {norma_2}')
  print('-'*80)
  print(f'TEMPO DE EXECUÇÃO = {tempo}s')
  print('-'*80)

  print('='*30,'MATRIZ MAGICA','================================='.ljust(10))

  #GERA MATRIZ MÁGICA
  matrix_2 = ms.magic(n)

  #CALCULA CONDICIONAMENTO 
  condicionamento = np.linalg.cond(matrix_2, p = np.inf)

  #APPENDA NA LISTA
  lista_condicionamento_magic.append(condicionamento)

  #NORMA DA DIFERENÇA ENTRE A E QR
  diferenca_1 = matrix_2 - np.matmul(fatHouseholder(matrix_2)[0], fatHouseholder(matrix_2)[1])
  norma_1 = np.linalg.norm(diferenca_1, np.inf)

  #NORMA DA DIFERENÇA ENTRE I E QQT
  diferenca_2 = np.identity(n) - np.matmul(np.transpose(gs(matrix_2)[0]),gs(matrix_2)[0])
  norma_2 = np.linalg.norm(diferenca_2,np.inf)

  #TEMPO DE EXECUÇÃO
  tempo = fatHouseholder(matrix_2)[2]

  print('-'*80)
  print(f'MATRIZ MÁGICA GERADA TEM CONDICIONAMENTO {round(condicionamento,10)}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE A E QR = {norma_1}')
  print('-'*80)
  print(f'NORMA DA DIFERENÇA ENTRE I E Q^T*Q = {norma_2}')
  print('-'*80)
  print(f'TEMPO DE EXECUÇÃO = {tempo}s')
  print('-'*80)
  print()
  print()

