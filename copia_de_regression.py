# -*- coding: utf-8 -*-
"""Copia de Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sunjpdhnmYoKxy-ij_Q2yBoVy9pcRuLJ

##### Copyright 2018 The TensorFlow Authors.
"""

#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#@title MIT License
#
# Copyright (c) 2017 François Chollet
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""# Regresión básica: predicción de la eficiencia del combustible

<table class="tfo-notebook-buttons" align="left">
  <td><a target="_blank" href="https://www.tensorflow.org/tutorials/keras/regression"><img src="https://www.tensorflow.org/images/tf_logo_32px.png">Ver en TensorFlow.org</a></td>
  <td><a target="_blank" href="https://colab.research.google.com/github/tensorflow/docs-l10n/blob/master/site/es-419/tutorials/keras/regression.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png">Ejecutar en Google Colab</a></td>
  <td>     <a target="_blank" href="https://github.com/tensorflow/docs-l10n/blob/master/site/es-419/tutorials/keras/regression.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png">Ver fuente en GitHub</a> </td>
  <td>     <a href="https://storage.googleapis.com/tensorflow_docs/docs-l10n/site/es-419/tutorials/keras/regression.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png">Descargar notebook</a> </td>
</table>

En un problema de *regresión*, la meta es predecir la salida de un valor continuo, como un precio o una probabilidad. Comparemos esto con un problema de *clasificación*, donde la meta es seleccionar una clase de una lista de clases (por ejemplo, donde una imagen contiene una manzana o una naranja, reconocer qué fruta se muestra en la imagen).

Este tutorial usa el clásico conjunto de datos [Auto MPG](https://archive.ics.uci.edu/ml/datasets/auto+mpg) y demuestra cómo generar modelos para predecir la eficiencia del combustible de los automóviles de fines de 1970 y principios de 1980. Para ello, deberá brindarles a los modelos una descripción de muchos automóviles de ese período. Esta descripción incluye atributos como cilindros, desplazamiento, potencia y peso.

En este ejemplo se usa la API de Keras. (Visite los [tutoriales](https://www.tensorflow.org/tutorials/keras) y las [guías](https://www.tensorflow.org/guide/keras) de Keras para obtener más información).
"""

# Se instala seaborn para visualización de datos
!pip install -q seaborn

# Se importan las librerías necesarias
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configuración para imprimir números con formato
np.set_printoptions(precision=3, suppress=True)

# Se importa TensorFlow y Keras
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

# Se muestra la versión de TensorFlow
print(tf.__version__)

"""## El conjunto de datos Auto MPG

El conjunto de datos está disponible desde el [repositorio UCI Machine Learning](https://archive.ics.uci.edu/ml/).

### Obtener los datos

Para empezar, use pandas para descargar e importar el conjunto de datos:
"""

# URL del conjunto de datos
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'

# Nombres de las columnas del conjunto de datos
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
                'Acceleration', 'Model Year', 'Origin']

# Se lee el conjunto de datos en un DataFrame de Pandas
raw_dataset = pd.read_csv(url, names=column_names,
                          na_values='?', comment='\t',
                          sep=' ', skipinitialspace=True)

# Se crea una copia del conjunto de datos
dataset = raw_dataset.copy()

# Se muestran las últimas filas del conjunto de datos
dataset.tail()

"""### Limpiar los datos

El conjunto de datos contiene algunos valores desconocidos:
"""

# Se verifica si hay valores faltantes en el conjunto de datos
dataset.isna().sum()

"""Descarte esas filas para simplificar este tutorial inicial:"""

# Se eliminan las filas con valores faltantes
dataset = dataset.dropna()

"""La columna `"Origin"` corresponde a una categoría, no es numérica. Entonces, el siguiente paso es aplicar la codificación en un solo paso de los valores en la columna con [pd.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html).

Nota: Puede configurar `tf.keras.Model` para que realice este tipo de transformación por usted, pero eso está fuera del alcance de este tutorial. Consulte los tutoriales [Clasificar datos estructurados con las capas de preprocesamiento de Keras](../structured_data/preprocessing_layers.ipynb) o [Cargar datos CSV](../load_data/csv.ipynb) para ver ejemplos.
"""

# Se mapean los valores numéricos de la columna 'Origin' a nombres
dataset['Origin'] = dataset['Origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})

# Se convierte la columna 'Origin' en columnas dummy
dataset = pd.get_dummies(dataset, columns=['Origin'], prefix='', prefix_sep='')

# Se muestran las últimas filas del conjunto de datos
dataset.tail()

"""### Dividir los datos en conjuntos de entrenamiento y prueba

Ahora, divida los conjuntos de datos en un conjunto de entrenamiento y un conjunto de prueba. Usará el conjunto de prueba para la evaluación final de sus modelos.
"""

# Se divide el conjunto de datos en conjuntos de entrenamiento y prueba
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

"""### Inspeccionar los datos

Revise la distribución conjunta de algunos pares de columnas del conjunto de entrenamiento.

La fila superior sugiere que la eficiencia del combustible (MPG) es una función conjunta de todos los demás parámetros. Las otras filas indican que son funciones entre sí.
"""

# Se muestra un gráfico de pares de características para el conjunto de entrenamiento
sns.pairplot(train_dataset[['MPG', 'Cylinders', 'Displacement', 'Weight']], diag_kind='kde')

"""Comprobemos también las estadísticas generales. Observe cómo cada característica cubre un rango muy distinto:"""

# Se muestran estadísticas descriptivas del conjunto de entrenamiento
train_dataset.describe().transpose()

"""### Separar las características de las etiquetas

Separe el valor de destino, la "etiqueta", de las características. Esta etiqueta es el valor que deberá predecir el modelo entrenado.
"""

# Se copian los conjuntos de características de entrenamiento y prueba
train_features = train_dataset.copy()
test_features = test_dataset.copy()

# Se extraen las etiquetas (MPG) de los conjuntos de características
train_labels = train_features.pop('MPG')
test_labels = test_features.pop('MPG')

"""## Normalización

En la tabla de estadísticas se puede ver con claridad lo distintos que son los rangos de cada característica:
"""

# Se muestran estadísticas descriptivas de las características de entrenamiento
train_dataset.describe().transpose()[['mean', 'std']]

"""Resulta muy práctico normalizar características que usan diferentes escalas y rangos.

Uno de los motivos por los que esto resulta importante es que las características se multiplican por los pesos del modelo. Por lo tanto, la escala de las salidas y la escala de los gradientes se ve afectada por la escala de las entradas.

Si bien un modelo *podría* converger sin implementar la normalización de las características, dicha normalización le aporta más estabilidad al entrenamiento.

Nota: Normalizar las características de codificación en un solo paso no presenta ninguna ventaja, solo se hace aquí para simplificar. Si desea obtener más información sobre cómo se usan las capas de preprocesamiento, consulte la guía [Trabajar con capas de preprocesamiento](https://www.tensorflow.org/guide/keras/preprocessing_layers) y el tutorial [Clasificar datos estructurados con las capas de preprocesamiento de Keras](../structured_data/preprocessing_layers.ipynb).

### La capa de normalización

`tf.keras.layers.Normalization` presenta un método simple y directo de agregar normalización de características a su modelo.

El primer paso consiste en crear la capa:
"""

# Se crea una capa de normalización para normalizar las características
normalizer = tf.keras.layers.Normalization(axis=-1)

# Se convierten las características de entrenamiento a tipo float
train_features = train_features.astype(float)

# Se adapta el normalizador a las características de entrenamiento
normalizer.adapt(train_features)

"""Luego, debe llamar `Normalization.adapt` para ajustar el estado de la capa de preprocesamiento a los datos:"""

# Se adapta el normalizador a un array de características de entrenamiento
normalizer.adapt(np.array(train_features))

"""Calcule la media y la desviación, y almacénelas en la capa:"""

# Se imprimen las medias de las características normalizadas
print(normalizer.mean.numpy())

"""Cuando se llama a la capa, esta devuelve los datos de entrada, con cada característica normalizada de forma independiente:"""

# Se selecciona el primer ejemplo de características de entrenamiento
first = np.array(train_features[:1])

# Se imprimen el primer ejemplo y sus valores normalizados
with np.printoptions(precision=2, suppress=True):
  print('First example:', first)
  print()
  print('Normalized:', normalizer(first).numpy())

"""## Regresión lineal

Antes de generar un modelo de red neuronal profunda, comience con la regresión lineal y use una y varias variables.

### Regresión lineal con una variable

Comience por aplicar una regresión lineal de una sola variable para predecir `'MPG'` a partir de `'Horsepower'`.

Al entrenar un modelo con `tf.keras` generalmente se comienza por definir la arquitectura del modelo. Use un modelo `tf.keras.Sequential`, que [representa una secuencia de pasos](https://www.tensorflow.org/guide/keras/sequential_model).

Un modelo de regresión lineal de una variable consta de dos pasos:

- Normalice las características de la entrada `'Horsepower'` mediante el uso de la capa de preprocesamiento `tf.keras.layers.Normalization`.
- Aplique una transformación lineal ($y = mx+b$) para producir 1 salida mediante el uso de una capa lineal (`tf.keras.layers.Dense`).

La cantidad de *entradas* se pueden establecer tanto mediante el argumento `input_shape` como de forma automática cuando el modelo se ejecute por primera vez.

En primer lugar, cree un arreglo NumPy compuesto por las características de `'Horsepower'`. Luego, cree instancias de `tf.keras.layers.Normalization` y ajuste su estado a los datos de `horsepower`:
"""

# Se extraen las características 'Horsepower' para el modelo de predicción
horsepower = np.array(train_features['Horsepower'])

# Se crea un normalizador para las características 'Horsepower'
horsepower_normalizer = layers.Normalization(input_shape=[1,], axis=None)
horsepower_normalizer.adapt(horsepower)

"""Generar el modelo secuencial de Keras:"""

# Se crea un modelo secuencial para predecir 'MPG' basado en 'Horsepower'
horsepower_model = tf.keras.Sequential([
    horsepower_normalizer,
    layers.Dense(units=1)
])

# Se muestra la arquitectura del modelo
horsepower_model.summary()

"""Este modelo puede predecir `'MPG'` a partir de `'Horsepower'`.

Ejecute el modelo sin entrenar en los primeros 10 valores de 'Horsepower'. La salida no será buena, pero observe que tiene la forma esperada de `(10, 1)`:
"""

# Se realizan predicciones con el modelo para las características 'Horsepower'
horsepower_model.predict(horsepower[:10])

"""Una vez que se haya generado el modelo, configure el procedimiento de entrenamiento a través del método `Model.compile` de Keras. Los argumentos más importantes para compilar son `loss` y `optimizer`, ya que estos definen qué se optimizará (`mean_absolute_error`) y cómo (mediante el uso de `tf.keras.optimizers.Adam`)."""

# Se compila el modelo especificando el optimizador y la función de pérdida
horsepower_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

"""Use `Model.fit` de Keras para ejecutar el entrenamiento durante 100 épocas:"""

# Commented out IPython magic to ensure Python compatibility.
# # Se entrena el modelo durante 100 épocas
# %%time
# history = horsepower_model.fit(
#     train_features['Horsepower'],
#     train_labels,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.2)

"""Visualice el progreso del entrenamiento del modelo con ayuda de las estadísticas almacenadas en el objeto `history`:"""

# Se crea un DataFrame con la historia de entrenamiento
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

# Función para graficar la pérdida durante el entrenamiento
def plot_loss(history):
  plt.plot(history.history['loss'], label='loss')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Error [MPG]')
  plt.legend()
  plt.grid(True)

# Se grafica la pérdida durante el entrenamiento
plot_loss(history)

"""Recopile los resultados del conjunto de prueba para después:"""

# Se inicializa un diccionario para almacenar los resultados de prueba
test_results = {}

# Se evalúa el modelo en el conjunto de prueba y se almacena el error absoluto medio
test_results['horsepower_model'] = horsepower_model.evaluate(
    test_features['Horsepower'],
    test_labels, verbose=0)

"""Como se trata de una regresión lineal con una sola variable, es fácil ver las predicciones del modelo como una función de la entrada:"""

# Se generan valores de 'Horsepower' para hacer predicciones
x = tf.linspace(0.0, 250, 251)
y = horsepower_model.predict(x)

# Función para graficar las características 'Horsepower' y las predicciones de 'MPG'
def plot_horsepower(x, y):
  plt.scatter(train_features['Horsepower'], train_labels, label='Data')
  plt.plot(x, y, color='k', label='Predictions')
  plt.xlabel('Horsepower')
  plt.ylabel('MPG')
  plt.legend()

# Se grafica 'Horsepower' vs 'MPG' con las predicciones del modelo
plot_horsepower(x, y)

"""### Regresión lineal con múltiples entradas

Puede usar una configuración prácticamente idéntica para hacer predicciones basadas en múltiples entradas. Este modelo hace lo mismo que $y = mx+b$ con la diferencia de que $m$ es una matriz y $x$ es un vector.

Cree un modelo secuencial de Keras nuevamente donde la primera capa sea `normalizer` (`tf.keras.layers.Normalization(axis=-1)`) que anteriormente ya definió y adaptó a todo el conjunto de datos:
"""

# Se crea un modelo lineal que utiliza las características normalizadas como entrada
linear_model = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1)
])

"""Cuando llama `Model.predict` en un lote de entradas, produce salidas `units=1` para cada ejemplo:"""

# Se realizan predicciones con el modelo lineal
linear_model.predict(train_features[:10])

"""Cuando llama el modelo, sus matrices de peso se generarán; compruebe que los pesos `kernel` (the $m$ in $y=mx+b$) tengan la misma forma que `(9, 1)`:"""

# Se muestra el kernel del modelo lineal
linear_model.layers[1].kernel

"""Configure el modelo con Keras `Model.compile` y entrénelo con `Model.fit` durante 100 épocas:"""

# Se compila el modelo lineal especificando el optimizador y la función de pérdida
linear_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

# Commented out IPython magic to ensure Python compatibility.
# # Se entrena el modelo lineal durante 100 épocas
# %%time
# history = linear_model.fit(
#     train_features,
#     train_labels,
#     epochs=100,
#     verbose=0,
#     validation_split = 0.2)

"""Usar todas las entradas en este modelo de regresión consigue un error de entrenamiento y validación mucho más bajo que `horsepower_model`, que tenía una sola entrada:"""

# Se grafica la pérdida durante el entrenamiento del modelo lineal
plot_loss(history)

"""Recopile los resultados del conjunto de prueba para después:"""

# Se convierten las características y etiquetas de prueba a tipo float
test_features = test_features.astype(float)
test_labels = test_labels.astype(float)

# Se evalúa el modelo lineal en el conjunto de prueba y se almacena el error absoluto medio
test_results['linear_model'] = linear_model.evaluate(test_features, test_labels, verbose=0)

"""## Regresión con una red neuronal profunda (DNN)

En la sección anterior, implementó dos modelos lineales tanto con una entrada como con múltiples entradas.

Aquí, implementará modelos de DNN de una sola entrada y de múltiples entradas.

El código es básicamente el mismo, con la diferencia de que el modelo se amplió para incluir algunas capas no lineales "ocultas". Con el término "ocultas" nos referimos a que no están directamente conectadas con las entradas y las salidas.

Estos modelos contendrán algunas capas más que el modelo lineal:

- La capa de normalización, de la misma forma que sucedió anteriormente (con `horsepower_normalizer` para un modelo de una sola entrada y `normalizer` para un modelo con múltiples entradas).
- Dos capas `Dense` ocultas, no lineales con la función de activación no lineal ReLU (`relu`).
- Una capa `Dense` lineal de una sola salida.

Ambos modelos usarán el mismo procedimiento de entrenamiento, por lo que el método `compile` se incluye en la función `build_and_compile_model` a continuación.
"""

# Función para construir y compilar un modelo DNN con capas de normalización
def build_and_compile_model(norm):
  model = keras.Sequential([
      norm,
      layers.Dense(64, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(1)
  ])

  model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(0.001))
  return model

"""### Regresión usando una DNN y una sola entrada

Cree un modelo de DNN con solo `'Horsepower'` como entrada y `horsepower_normalizer` (definido anteriormente) como capa de normalización:
"""

# Se construye y compila un modelo DNN utilizando el normalizador de 'Horsepower'
dnn_horsepower_model = build_and_compile_model(horsepower_normalizer)

"""Este modelo tiene bastantes parámetros entrenables más que el modelo lineal:"""

# Se muestra la arquitectura del modelo DNN
dnn_horsepower_model.summary()

"""Entrene el modelo con `Model.fit` de Keras:"""

# Commented out IPython magic to ensure Python compatibility.
# # Se entrena el modelo DNN durante 100 épocas
# %%time
# history = dnn_horsepower_model.fit(
#     train_features['Horsepower'],
#     train_labels,
#     validation_split=0.2,
#     verbose=0, epochs=100)

"""Este modelo tiene un rendimiento ligeramente superior al modelo lineal `horsepower_model` de una sola entrada:"""

# Se grafica la pérdida durante el entrenamiento del modelo DNN
plot_loss(history)

"""Si traza estas predicciones como una función de `'Horsepower'`, notará que este modelo aprovecha la falta de linealidad que le aportan las capas ocultas:"""

# Se generan valores de 'Horsepower' para hacer predicciones con el modelo DNN
x = tf.linspace(0.0, 250, 251)
y = dnn_horsepower_model.predict(x)

# Se grafica 'Horsepower' vs 'MPG' con las predicciones del modelo DNN
plot_horsepower(x, y)

"""Recopile los resultados del conjunto de prueba para después:"""

# Se evalúa el modelo DNN en el conjunto de prueba y se almacena el error absoluto medio
test_results['dnn_horsepower_model'] = dnn_horsepower_model.evaluate(
    test_features['Horsepower'], test_labels,
    verbose=0)

"""### Regresión usando una DNN y múltiples entradas

Repita el proceso anterior usando todas las entradas. El rendimiento del modelo mejora levemente con el conjunto de datos de validación.
"""

# Se construye y compila un modelo DNN utilizando el normalizador de características
dnn_model = build_and_compile_model(normalizer)

# Se muestra la arquitectura del modelo DNN
dnn_model.summary()

# Commented out IPython magic to ensure Python compatibility.
# # Se entrena el modelo DNN durante 100 épocas
# %%time
# history = dnn_model.fit(
#     train_features,
#     train_labels,
#     validation_split=0.2,
#     verbose=0, epochs=100)

# Se grafica la pérdida durante el entrenamiento del modelo DNN
plot_loss(history)

"""Recopile los resultados del conjunto de prueba:"""

# Se evalúa el modelo DNN en el conjunto de prueba y se almacena el error absoluto medio
test_results['dnn_model'] = dnn_model.evaluate(test_features, test_labels, verbose=0)

"""## Rendimiento

Dado que ya ha entrenado todos los modelos, puede consultar el rendimiento del conjunto de prueba:
"""

# Se crea un DataFrame con los resultados de prueba
pd.DataFrame(test_results, index=['Mean absolute error [MPG]']).T

"""Estos resultados coinciden con el error de validación que se observó durante el entrenamiento.

### Hacer predicciones

Ahora puede hacer predicciones con `dnn_model` en el conjunto de prueba usando Keras `Model.predict` y revisar la pérdida:
"""

# Se realizan predicciones con el modelo DNN en el conjunto de prueba
test_predictions = dnn_model.predict(test_features).flatten()

# Se grafica 'MPG' predicho vs 'MPG' real en el conjunto de prueba
a = plt.axes(aspect='equal')
plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
lims = [0, 50]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)

"""Al parecer, el modelo predice bastante bien.

Ahora, compruebe la distribución de los errores:
"""

# Se calcula el error de predicción en el conjunto de prueba
error = test_predictions - test_labels
plt.hist(error, bins=25)
plt.xlabel('Prediction Error [MPG]')
_ = plt.ylabel('Count')

"""Si está satisfecho con el modelo, guárdelo para usarlo más tarde con `Model.save`:"""

# Se guarda el modelo DNN entrenado
dnn_model.save('dnn_model.keras')

"""Si vuelve a cargar el modelo, le da una salida idéntica:"""

# Se carga el modelo DNN guardado con especificación de input_shape
NUM_FEATURES = len(train_features.columns)

reloaded = tf.keras.models.load_model('dnn_model.keras', custom_objects={'Normalization': tf.keras.layers.Normalization(input_shape=(NUM_FEATURES,))})

# Se evalúa el modelo DNN recargado en el conjunto de prueba y se almacena el error absoluto medio
test_results['reloaded'] = reloaded.evaluate(test_features, test_labels, verbose=0)

# Se muestra un DataFrame con los resultados de prueba
pd.DataFrame(test_results, index=['Mean absolute error [MPG]']).T

"""## Conclusión

Este bloc de notas introdujo algunas técnicas para hacer frente a un problema de regresión. Aquí encontrará algunos consejos más que pueden ayudarle:

- El error cuadrático medio (MSE) (`tf.keras.losses.MeanSquaredError`) y el error absoluto medio (MAE) (`tf.keras.losses.MeanAbsoluteError`) son funciones de pérdida comunes que se usan para problemas de regresión. MAE es menos susceptible a los valores atípicos. Para los problemas de clasificación se usan otras funciones de pérdida.
- Asimismo, las métricas de evaluación que se usan para la regresión son distintas de las que se usan para la clasificación.
- Cuando las características de los datos de entradas numéricas tienen valores con diferentes rangos, se debe escalar por separado cada característica al mismo rango.
- El sobreajuste es un problema común para los modelos de DNN, aunque no fue un problema para este tutorial. Visite el tutorial [Sobreajuste y subajuste](overfit_and_underfit.ipynb) para obtener más ayuda al respecto.
"""