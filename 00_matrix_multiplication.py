# -*- coding: utf-8 -*-
"""00_Matrix_Multiplication.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lVScnGvhfA7rlqkR4cpe3DXA_ItQPhj_

# Multiplicación de Matrices

En este laboratorio, utilizarás funciones de `NumPy` para realizar la multiplicación de matrices y verás cómo puede aplicarse en las aplicaciones de Aprendizaje Automático.

# Tabla de Contenidos

- [ 1 - Definición de la Multiplicación de Matrices](#1)
- [ 2 - Multiplicación de Matrices con Python](#2)
- [ 3 - Convención de Matrices y Difusión (Broadcasting)](#3)

## Paquetes

Carga el paquete `NumPy` para acceder a sus funciones.
"""

import numpy as np

"""<a name='1'></a>
## 1 - Definición de la Multiplicación de Matrices

Si $A$ es una matriz de dimensiones $m \times n$ y $B$ es una matriz de dimensiones $n \times p$, el producto matricial $C = AB$ (denotado sin signos de multiplicación ni puntos) se define como la matriz de dimensiones $m \times p$ tal que
$c_{ij}=a_{i1}b_{1j}+a_{i2}b_{2j}+ ... +a_{in}b_{nj}=\sum_{k=1}^{n} a_{ik}b_{kj}, \tag{4}$

donde $a_{ik}$ son los elementos de la matriz $A$, $b_{kj}$ son los elementos de la matriz $B$, e $i = 1, ..., m$, $k=1, ... , n$, $j = 1, ..., p$. En otras palabras, $c_{ij}$ es el producto punto de la $i$-ésima fila de $A$ y la $j$-ésima columna de $B$.

<a name='2'></a>
## 2 - Multiplicación de Matrices con Python

Al igual que con el producto punto, hay varias formas de realizar la multiplicación de matrices en Python. Como se discutió en el laboratorio anterior, los cálculos son más eficientes en la forma vectorizada. Analicemos las funciones más comúnmente utilizadas en la forma vectorizada. Primero, definamos dos matrices:
"""

A = np.array([[4, 9, 9], [9, 1, 6], [9, 2, 3]])
print("Matrix A (3 by 3):\n", A)

B = np.array([[2, 2], [5, 7], [4, 4]])
print("Matrix B (3 by 2):\n", B)

"""Puedes multiplicar las matrices $A$ y $B$ utilizando la función `np.matmul()` del paquete `NumPy`:

"""

np.matmul(A, B)

"""Esto producirá una matriz de $3 \times 2$ como un `np.array`. El operador `@` de Python también funcionará aquí, dando el mismo resultado:

"""

A @ B

"""<a name='3'></a>
## 3 - Convención de Matrices y Difusión (Broadcasting)

Matemáticamente, la multiplicación de matrices está definida solo si el número de columnas de la matriz $A$ es igual al número de filas de la matriz $B$ (puedes revisar nuevamente la definición en la sección [1](#1) y ver que, de lo contrario, los productos punto entre filas y columnas no estarán definidos).

Por lo tanto, en el ejemplo anterior ([2](#2)), cambiar el orden de las matrices al realizar la multiplicación $BA$ no funcionará, ya que la regla mencionada anteriormente ya no se cumple. Puedes comprobarlo ejecutando las celdas a continuación; ambas darán errores.

"""

try:
    np.matmul(B, A)
except ValueError as err:
    print(err)

try:
    B @ A
except ValueError as err:
    print(err)

"""Por lo tanto, al utilizar la multiplicación de matrices, debes tener mucho cuidado con las dimensiones: el número de columnas en la primera matriz debe coincidir con el número de filas en la segunda matriz. Esto es muy importante para tu comprensión futura de las Redes Neuronales y cómo funcionan.

Sin embargo, para multiplicar vectores, `NumPy` tiene un atajo. Puedes definir dos vectores $x$ e $y$ del mismo tamaño (que se pueden entender como dos matrices $3 \times 1$). Si verificas la forma del vector $x$, puedes ver que:

"""

x = np.array([1, -2, -5])
y = np.array([4, 3, -1])

print("Shape of vector x:", x.shape)
print("Number of dimensions of vector x:", x.ndim)
print("Shape of vector x, reshaped to a matrix:", x.reshape((3, 1)).shape)
print("Number of dimensions of vector x, reshaped to a matrix:", x.reshape((3, 1)).ndim)

"""Siguiendo la convención de matrices, la multiplicación de matrices $3 \times 1$ y $3 \times 1$ no está definida. Para la multiplicación de matrices, esperarías un error en la siguiente celda, pero comprobemos la salida:

"""

np.matmul(x,y)

"""Puedes ver que no hay error y que el resultado es, de hecho, un producto punto $x \cdot y\,$. Así que, el vector $x$ se transpuso automáticamente al vector $1 \times 3$ y se calculó la multiplicación de matrices $x^Ty$. Aunque esto es muy conveniente, debes tener en cuenta esta funcionalidad en Python y prestar atención para no usarla de manera incorrecta. La siguiente celda devolverá un error:

"""

try:
    np.matmul(x.reshape((3, 1)), y.reshape((3, 1)))
except ValueError as err:
    print(err)

"""Puede que te estés preguntando: ¿la función `np.dot()` también funciona para la multiplicación de matrices? Probémoslo:

"""

np.dot(A, B)

"""¡Sí, funciona! Lo que realmente sucede es lo que se llama **difusión** en Python: `NumPy` difunde esta operación de producto punto a todas las filas y columnas, obteniendo la matriz de producto resultante. La difusión también funciona en otros casos, por ejemplo:

"""

A-2

"""Matemáticamente, la resta de la matriz $3 \times 3$ $A$ y un escalar no está definida, pero Python difunde el escalar, creando un `np.array` de $3 \times 3$ y realizando la resta elemento por elemento. Un ejemplo práctico de multiplicación de matrices se puede ver en un modelo de regresión lineal. ¡Lo implementarás en la tarea de esta semana!

"""