# -*- coding: utf-8 -*-
"""Aprendizagem de Máquina.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d5Oq17BoVUtqWAtyPFX1ZSS0YezGI5dO

<hr style="height:10px"> 
 
<div class='container2'>
	<h1> Trabalho Aprendizado de Máquina - CSI704</h1>
    <h2>UFOP - DECSI</h2>
    <h4>Alunos: Aline Martins Dias, Daniele Cristina Almeida, Gustavo Estevam Sena</h4>
</div>

<hr style="height:5px"> 

Modificado do original desenvolvido por: <a href="http://lattes.cnpq.br/2532893661927339">Renato Moraes Silva</a> para [2].

<hr style="height:2px">

## 1- Introdução
Aprendizado de Máquina é caracterizado pelo desenvolvimento de técnicas que  buscam equipar os softwares para melhorar o seu desempenho adquirindo conhecimento através da experiência, ou seja através do aprendizado indutivo.  [2]

Diante disso,  o aprendizado indutivo é adquirido através da implementação de algoritmos que fazem o processamento da base de dados e  conseguem representar os dados em um modelo sob algum aspecto observado. 

Para conseguir realizar a  visualização dos dados e a sua  interpretação  de como os mesmos estão estão distribuídos, será utilizado recursos da tecnologia  Python, que possui algumas bibliotecas que facilitam o processo de visualização, tais como: `Pandas`, `Matplotlib` e `Seaborn`. Para aprender a usar essas ferramentas, será usada a base de dados Wine [1]. É importante destacar que a base de dados Wine usada neste trabalho foi modificada pelos autores por motivos didáticos. A versão original dela pode ser encontrada no seguinte link: <https://archive.ics.uci.edu/ml/datasets/wine>. 

Diante deste contexto, o presente trabalho  tem como objetivo aplicar a teoria de aprendizagem de máquina usando a versão modificada da  base Wine. Também será apresentado como foi realizado para fazer a eliminação de atributos irrelevantes e o tratamento de valores faltantes. Além disso, será mostrado como tratar valores redundantes ou inconsistentes e como fazer a normalização dos dados. Depois, será feita a detecção e remoção de *outliers* da base dados. Por fim, será mostrado como fazer a análise da distribuição das classes e da correlação entre os atributos.

---
## 2- Recursos Necessários

Para executar este *notebook*, deve ser utilizado o `Python 3.5` ou superior com as seguintes bibliotecas externas, que deverão ser instaladas:

* [`matplotlib`](https://matplotlib.org/) (versão 3.1.3 ou superior): construção e exibição de gráficos variados
* [`seaborn`](https://seaborn.pydata.org/) (versão 0.10.0 ou superior): construção e exibição de gráficos variados
* [`numpy`](https://numpy.org) (versão 1.16.2 ou superior): manipulação de dados em formato de vetores e matrizes
* [`pandas`](https://pandas.pydata.org/pandas-docs/stable/index.html) (versão 0.24.1 ou superior): manipulação de dados em formato de tabelas

Será utilizado também o conjuntos de dados disponibilizado junto com este *notebook*, que se encontra no diretório `datasets`, em formato de arquivo `.csv`.

---
## 3- Carregando os dados

O primeiro passo para executar este notebook, deve-se importar todas as bibliotecas necessárias. Abaixo é possível realizar este procedimento.
"""

# -*- coding: utf-8 -*-

import numpy as np # importa a biblioteca usada para trabalhar com vetores e matrizes
import pandas as pd # importa a biblioteca usada para trabalhar com dataframes (dados em formato de tabela) e análise de dados
import sklearn

# bibliotecas usadas para geracao de graficos
import seaborn as sns
import matplotlib.pyplot as plt

#Normalização
from sklearn.preprocessing import StandardScaler

#Split (divisão da base de teste e de treino)
from sklearn.model_selection import train_test_split

#Algoritmo KNN e algoritmo para calculo de vizinhança
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors

#Customização e Métricas
from matplotlib.colors import ListedColormap
from sklearn.metrics import classification_report, confusion_matrix

print('Bibliotecas carregadas com sucesso')

"""Em seguida, os dados serão carregados do arquivo."""

from google.colab import drive
drive.mount('/content/drive')

"""Após realizar o carregamento do arquivo, é necessário importar a base de dados Wine. Se este procedimento não for realizado o código abaixo não será executado."""

# importa o arquivo e guarda em um dataframe do Pandas
df_dataset = pd.read_csv( 'wine.csv', sep=',', index_col=None, header=None) 

print('Dados importados com sucesso!')

"""O próximo passo é setar o nome das Colunas dos Atributos conforme os detalhes disponibilizados no repositório original: https://archive.ics.uci.edu/ml/datasets/wine"""

df_dataset.set_axis(['Álcool', 
                     'Ácido Málico', 
                     'Cinzas', 'Alcalinidade das Cinzas', 'Magnésio', 
                     'Fenóis Totais', 'Flavonoides', 
                     'Fenóis não Flavonóides',
                     'Proantocianidinas',
                     'Intensidade da cor',
                     'Matiz',
                     'Vinhos Diluídos',
                     'Prolina',
                     'Classe de Vinhos'], 1, inplace=True)

"""Agora, vamos dar uma olhada nos metadados do dataset e nas 100 primeiras amostras da base de dados."""

# exibe o dataframe
df_dataset.info()
df_dataset.head(n=100)

"""A base de dados contém amostras de vinhos (linhas) representadas pelos seguintes atributos (colunas): 'Álcool', 'Ácido Málico', 'Cinzas', 'Alcalinidade das Cinzas', 'Magnésio', 'Fenóis Totais', 'Flavonoides', 'Fenóis não Flavonóides', 'Proantocianidinas', 'Intensidade da cor', 'Matiz', 'Vinhos Diluídos', 'Prolina', 'Classe de Vinhos' 	

Obs: Vinhos Diluídos: DO280/OD315


## 4- Pré-processamento: eliminação de atributos irrelevantes

Em uma tarefa de aprendizado de máquina devemos remover atributos irrelevantes para a classificação. Em cenários reais, muitas vezes é necessário consultar especialistas para ajudar a identificar quais atributos são irrelevantes. Nesse caso não identificamos atributos irrelevantes, então deixamos todos os 13.

"""

# remove a coluna que tenha algum atributo irrelevante
# não tem nenhum atributo irrelevante
#df_dataset = df_dataset.drop(columns=['']) 

# imprime o dataframe
display(df_dataset.head(n=100))

"""## 5- Pré-processamento: tratamento de atributos com valores ausentes

Outro passo importante, é verificar se existem atributos com valores ausentes (*NaN*) na base de dados:

Para o dataset wine.csv não foram encontrados valores Not a Number, portanto não apresenta atributos com valores ausentes.

"""

# índices das linhas que contém valores NaN
idxRowNan = pd.isnull(df_dataset).any(1).to_numpy().nonzero()

# imprime apenas as linhas com valoes ausentes
display(df_dataset.iloc[idxRowNan])

"""
Caso existisse atributos com valores faltantes seria necessário corrigir esses valores fazendo o cáculo da média dos valores conhecidos da respectiva classe. Abaixo é apresentado uma forma para corrigir esta situação."""

# def trataFaltantes( df_dataset ):

#    Substitui os valores faltantes pela média dos outros valores do mesmo atributo
#    de amostras que sejam da mesma classe    
    
    # seleciona apenas as linhas da base de dados onde a coluna largura_sepala não contém valores nulos
    # notNull_ls = df_dataset.loc[ ~pd.isnull(df_dataset['']), :]
    # notNull_cp = df_dataset.loc[ ~pd.isnull(df_dataset['']), :]

    # calcula a media dos valores do atributo largura_sepala que não são nulos e que são da classe Iris-setosa 
    # media_ls = notNull_ls[ notNull_ls['classe']=='' ][''].mean()
    # media_cp = notNull_cp[ notNull_cp['classe']=='' ][''].mean()

    # substitui os valores nulos pela média 
    # df_dataset.loc[ pd.isnull(df_dataset['']), ''] = media_ls
    # df_dataset.loc[ pd.isnull(df_dataset['']), ''] = media_cp
    
    # return df_dataset

# trataFaltantes( df_dataset )
    
# imprime apenas as linhas que antes possuiam valores NaN
# print('\nAmostras que possuiam valores faltantes:')
# display(df_dataset.iloc[idxRowNan])

"""## 6- Pré-processamento: tratamento de dados inconsistentes ou redundantes

Outro passo importante, é verificar se existem dados inconsistentes ou redundantes. A forma mais comum de inconsistência é quando há amostras representadas por atributos com todos os valores iguais, mas com classes diferentes. A redundância é dada pela repetição de linhas na base de dados.

A seguir, vamos verificar se existem amostras duplicadas (redundantes) e inconsistentes.
"""

df_duplicates = df_dataset[ df_dataset.duplicated(subset=['Álcool', 'Ácido Málico', 'Cinzas', 'Alcalinidade das Cinzas', 'Magnésio', 'Fenóis Totais', 'Flavonoides', 'Fenóis não Flavonóides', 'Proantocianidinas', 'Intensidade da cor', 'Matiz', 'Vinhos Diluídos', 'Prolina'],keep=False)] 

# se houver valores redundantes ou inconsistentes, imprima 
if len(df_duplicates)>0:
    print('\nAmostras redundantes ou inconsistentes:')
    display(df_duplicates)
else:
    print('Não existem valores duplicados')

"""No caso da wine dataset não existem amostras duplicadas.

Caso existesse amostra duplicadas, o procedimento que seria executado era:

1) Remover as amostras redundantes, mantendo na base apenas uma delas.
"""

# def delDuplicatas( df_dataset ):
    # Para cada grupo de amostras duplicadas, mantém uma e apaga as demais
    
    
    # remove as amostras duplicadas, mantendo apenas a primeira ocorrencia
    # df_dataset = df_dataset.drop_duplicates(keep = 'first')    

    # return df_dataset

# df_dataset = delDuplicatas( df_dataset )

"""Após remover as amostras redundantes, é preciso checar se há amostras inconsistentes.  Na base de dados em estudo não houve amostras redudantes, por isso o código abaixo não precisa ser executado."""

# para detectar inconsistências, a rotina abaixo obtém as amostras onde os valores 
# dos atributos continuam duplicados. Neste caso, os atributos serão iguais, mas as classes serão distintas
# df_duplicates = df_dataset[ df_dataset.duplicated(subset=['Álcool', 'Ácido Málico', 'Cinzas', 'Alcalinidade das Cinzas', 'Magnésio', 'Fenóis Totais', 'Flavonoides', 'Fenóis não Flavonóides', 'Proantocianidinas', 'Intensidade da cor', 'Matiz', 'Vinhos Diluídos', 'Prolina'],keep=False)] 

# se tiver valores inconsistentes, imprime 
# if len(df_duplicates)>0:
   # print('\nAmostras inconsistentes:')
   # display(df_duplicates)
# else:
   # print('Não existem mostras inconsistentes')

"""Caso existe amostras incosistentes seria necessário fazer a exclusão das mesmas, por isso o código abaixo está comentado."""

# def delInconsistencias( df_dataset ):
    # Remove todas as amostras inconsistentes da base de dados
    
    # df_dataset = df_dataset.drop_duplicates(subset=['Álcool', 'Ácido Málico', 'Cinzas', 'Alcalinidade das Cinzas', 'Magnésio', 'Fenóis Totais', 'Flavonoides', 'Fenóis não Flavonóides', 'Proantocianidinas', 'Intensidade da cor', 'Matiz', 'Vinhos Diluídos', 'Prolina'], keep = False)    
  
    # return df_dataset

# df_dataset = delInconsistencias( df_dataset )

# obtém apenas as amostras onde os valores dos atributos estão duplicados
# df_duplicates = df_dataset[ df_dataset.duplicated(subset=['Álcool', 'Ácido Málico', 'Cinzas', 'Alcalinidade das Cinzas', 'Magnésio', 'Fenóis Totais', 'Flavonoides', 'Fenóis não Flavonóides', 'Proantocianidinas', 'Intensidade da cor', 'Matiz', 'Vinhos Diluídos', 'Prolina'],keep=False)] 

# se tiver valores redundantes ou inconsistentes, imprime 
# if len(df_duplicates)>0:
    # display(df_duplicates)
# else:
    # print('Não existem amostras redundantes ou inconsistentes')

"""# 7- Algumas estatísticas sobre a base de dados. 

A função `describe()` da `Pandas` sumariza as principais estatísticas sobre os dados de um *data frame*, como:

1) Count (Contagem de Valores): 178 Amostras por Variável
2) Mean: Média da Variável
3) std: Devio padrão da Variável
4) min: O valor mínimo presente na Variável
5) 25%, 50%, 75%: Os quartis da distribuição da Variável
6) max: O valor máximo presente na Variável
"""

# apresenta as principais estatísticas da base de dados
df_detalhes = df_dataset.describe()

display(df_detalhes)

"""## 8- Pré-processamento: normalização dos atributos 

Podemos notar que a média dos atributos Alcool, Alcalinidade das Cinzas, Magnésio e Prolina são muito maiores que a dos outros atributos, assim sendo
precisamos realizar a normalização para essas variávels com escala maior, do contrário haveria um grande impacto para o cálculo da distância nas váriaveis de escala pequena, compromentendo a qualidade de execução do KNN, uma vez que este estima a classe baseando nas distâncias entre as observações mais próximas,

**Normalização com criação da Função de Normalizar - Vide - Trabalho Orignalt**
"""

def normalizar(X):
    """
    Normaliza os atributos em X
    
    Esta função retorna uma versao normalizada de X onde o valor da
    média de cada atributo é igual a 0 e desvio padrao é igual a 1. Trata-se de
    um importante passo de pré-processamento quando trabalha-se com 
    métodos de aprendizado de máquina.
    """
    
    m, n = X.shape # m = qtde de objetos e n = qtde de atributos por objeto
    
    # Incializa as variaves de saída
    X_norm = np.random.rand(m,n) # inicializa X_norm com valores aleatórios
    mu = 0 # inicializa a média
    sigma = 1 # inicializa o desvio padrão
     
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0, ddof=1)
    
    for i in range(m):
        X_norm[i,:] = (X[i,:]-mu) / sigma
        
    
    return X_norm, mu, sigma


# coloca os valores dos atributos na variável X
X = df_dataset.iloc[:,0:-1].values

# chama a função para normalizar X
X_norm, mu, sigma = normalizar(X)

df_dataset.iloc[:,0:-1] = X_norm


print('\nPrimeira amostra da base antes da normalização: [%2.4f %2.4f].' %(X[0,0],X[0,1]))
print('\nApós a normalização, espera-se que a primeira amostra seja igual a: [-0.5747 0.1804].')
print('\nPrimeira amostra da base apos normalização: [%2.4f %2.4f].' %(X_norm[0,0],X_norm[0,1]))

"""Agora que os dados estão normalizados, analisa-se as informações estatísticas novamente."""

# apresenta as principais estatísticas da base de dados
df_detalhes = df_dataset.describe()
display(df_detalhes.round(8))

"""**Compararamos o método de normalização def_normalizar(x) com o método padrão de normalização em python: sklearn.preprocessing.StandardScaler para garantir que a normalização foi feita de forma correta**

Invoca o método padrão para normalização da Biblioteca scikit-learn
"""

scaler = StandardScaler()

"""Configura o escalador para considerar apenas as colunas desejadas. Retirar da escala a  classe do dataframe ('Classificacacao')"""

scaler.fit(df_dataset.drop(['Classe de Vinhos'], axis=1))

# apresenta as principais estatísticas da base de dados
df_detalhes = df_dataset.describe()
display(df_detalhes.round(8))

"""Pode-se ver acima que a média (*mean*) ficou igual a 0 e o desvio padrão (*std*) igual a 1. 

## 9- Pré-processamento: detecção de *outliers* 

Outro passo importante na análise e tratamento dos dados é a detecção de *outliers* (*i.e.*, dados gerados por leituras incorretas, erros de digitação, etc). 

Uma das maneiras mais simples de verificar se os dados contém *outliers* é criar um gráfico box plot de cada atributo. Para isso, podemos usar a função `boxplot` da biblioteca `Pandas`.
"""

# gera um bloxplot para cada atributo
df_dataset.boxplot(figsize=(30,15))
plt.show()

"""Verificar que os atributos Ácido Málico, Cinzas, Alcalinidade das Cinzas, Magnésio, Proantocianidinas, Intensidade da Cor, Matiz possuem outliers e podem prejudicar o desempenho de vários métodos de aprendizado de máquina, pois tratam-se de amostras com valores de atributos incorretos. Verificar

Outra forma de analisar se a base de dados contém *outliers* é usar gráficos de dispersão. Pode-se plotar gráficos de dispersão de todas as combinações de atributos da base de dados usando a função `scatter_matrix` da `Pandas`.
"""

pd.plotting.scatter_matrix(df_dataset, figsize=(30,30))

plt.show()

"""Outra forma de plotar gráficos de dispersão a partir dos _dataframes_ é usando a biblioteca `Seaborn`. Juntamente com essa biblioteca, também é recomendável importar a biblioteca `Matplotlib` para personalizar os gráficos. """

# matriz de gráficos scatter 
sns.pairplot(df_dataset,  height=3.6);

# mostra o gráfico usando a função show() da matplotlib
plt.show()

"""A bilioteca `Seaborn` permite criar gráficos boxplot agrupados por um determinado atributo, o que facilita a análise dos dados. No exemplo abaixo, criaremos boxplots para cada atributo agrupados pela classe."""

for atributo in df_dataset.columns[:-1]:
    # define a dimensão do gráfico
    plt.figure(figsize=(8,8))

    # cria o boxplot
    sns.boxplot(x="Classe de Vinhos", y=atributo, data=df_dataset, whis=1.5)

    # mostra o gráfico
    plt.show()

"""Os box plots dos atributos mostraram outros *outliers* que não haviam aparecido no primeiro box plot. Portanto, esses novos valores são considerados *outliers* se analisarmos as classes individualmente, mas não são considerados *outliers* se analisarmos a base de dados de forma geral. 

Outro tipo de gráfico que ajuda a detectar *outliers* é o histograma. Portanto, será usado para analisar cada atributo.
"""

for atributo in df_dataset.columns[:-1]:
    
    # cria o histograma
    n, bins, patches = plt.hist(df_dataset[atributo].values,bins=10, color='red', edgecolor='black', linewidth=0.9)

    # cria um título para o gráfico
    plt.title(atributo)

    # mostra o gráfico
    plt.show()

"""Agora, pode-se usar um gráfico de densidade para fazer o mesmo tipo de análise."""

for atributo in df_dataset.columns[:-1]:

    # criando o gráfico de densidade para cada atributo
    densityplot = df_dataset[atributo].plot(kind='density')
    
    # cria um título para o gráfico
    plt.title(atributo)

    # mostra o gráfico
    plt.show()

"""Uma das maneiras mais simples de tratar *outliers* é remover aqueles valores que são menores que $Q1 - 1.5 * IQR$ ou maiores que $Q3 + 1.5 * IQR$, onde $Q1$ é o primeiro quartil, $Q3$ é o terceiro quartil e $IQR$ é o intervalo interquartil. O IQR pode ser calculado pela seguinte equação: $IQR = Q3-Q1$. 

Com base nessas informações, vamos usar a função abaixo para remover os *outliers* da base de dados. Usaremos como base o IQR de cada atributo em relação a todos os valores na base de dados, em vez do IQR individual de cada classe.

**OBSERVAÇÃO: Para remoção de todos os outliers dessa base de dados foi necessário executar o método 03 VEZES (x03).**
"""

def removeOutliers(df_dataset):
    """
    Remove os outliers da base de dados 
    """
    
    for atributo in df_dataset.columns[:-1]:

        # obtem o terceiro e o primeiro quartil. 
        q75, q25 = np.percentile(df_dataset[atributo].values, [75 ,25])
        
        # calcula o IQR
        IQR = q75 - q25

        # remove os outliers com base no valor do IQR
        df_dataset = df_dataset[ (df_dataset[atributo]<=(q75+1.5*IQR)) & (df_dataset[atributo]>=(q25-1.5*IQR)) ]
    
    return df_dataset

# remove os outliers
df_dataset = removeOutliers( df_dataset )

# apresenta as principais estatísticas sobre a base de dados
df_dataset.boxplot(figsize=(28,7))
plt.show()

# matriz de gráficos scatter 
sns.pairplot(df_dataset, hue='Classe de Vinhos', height=3.5);

# mostra o gráfico usando a função show() da matplotlib
plt.show()

"""Depois da remoção, o box plot e os gráficos de dispersão indicam que não há mais nenhum *outlier* na base de dados. 


**IMPORTANTE:** antes de realizar a remoção de *outliers*, é mandatório analisar cuidadosamente as características das amostras antes de removê-las. Em alguns casos, remover os *outliers* pode ser prejudicial. Além disso, algumas tarefas de aprendizado de máquina são voltadas para a detecção de *outliers* e, portanto, esses dados não podem ser removidos. Adicionalmente, se a base de dados for desbalanceada, a remoção dos *outliers* com base nas estatísticas de toda a base, pode acabar removendo amostras da classe minoritária (aquela que possui menos amostras).

## 10- Pré-processamento: distribuição das classes

Outro passo importante na análise de dados é verificar a distribuição das classes. Para isso, é possível criar um gráfico de barra indicando quantas amostras de cada classe há na base de dados.
"""

display( df_dataset['Classe de Vinhos'].value_counts() )

# cria um gráfico de barras com a frequência de cada classe
sns.countplot(x="Classe de Vinhos", data=df_dataset)

# mostra o gráfico
plt.show()

"""Pode-se ver que as classes são balanceadas. Se o número de exemplos em alguma das classes fosse muito superior às demais, seria necessário usar alguma técnica de balanceamento de classes, pois o modelo gerado pela maioria dos métodos de aprendizado supervisionado costuma ser tendencioso para as classes com maior número de amostras.

##11- Pré-processamento: correlação entre os atributos

Quando dois atributos possuem valores idênticos ou muito semelhantes para todas as amostras, um deles deve ser eliminado ou eles devem ser combinados. Isso ajuda a diminuir o custo computacional das tarefas de aprendizado e evita que o aprendizado de alguns método seja prejudicado, principalmente os métodos baseados em otimização.

Uma das maneiras mais comuns de analisar a correlação dos dados é através das matrizes de correlação e covariância. Pode-se fazer isso usando a biblioteca `Numpy` ou a `Pandas`.

Primeiro, será utilizada a `Numpy`.
"""

# criando uma matriz X com os valores do data frame
X = df_dataset.iloc[:,:-1].values

# matriz de covariancia
covariance = np.cov(X, rowvar=False)

# matriz de correlação
correlation = np.corrcoef(X, rowvar=False)

print('Matriz de covariância: ')
display(covariance)

print('\n\nMatriz de correlação: ')
display(correlation)

"""Agora, serão calculadas as matrizes de correlação e covariância usando a `Pandas`."""

# matriz de covariancia
df_covariance = df_dataset.cov()

# matriz de correlação
df_correlation = df_dataset.corr()

print('Matriz de covariância: ')
display(df_covariance)

print('\n\nMatriz de correlação: ')
display(df_correlation)

"""Para facilitar a visualização, será plotada a matriz de covariância e a de correlação usando mapas de cores."""

# cria um mapa de cores dos valores da covariancia
sns.heatmap(df_covariance, 
        xticklabels=df_correlation.columns,
        yticklabels=df_correlation.columns)

plt.title('Covariancia')
plt.show()

# cria um mapa de cores dos valores da correlação
sns.heatmap(df_correlation, 
        xticklabels=df_correlation.columns,
        yticklabels=df_correlation.columns)

plt.title('Correlacao')
plt.show()

"""# 12-Implementação do KNN

**Implementação do KNN considerando os dois primeiros atributos: 'Alcool' e  'Ácido Málico' + matriz de confusao + relatório do algoritmo para saber se está aumentando ou não a precisão a medida que se varia o valor de K - Vide Exemplo KNN com Social dataset - Aula de IA no Moodle**
"""

# Trabalho Original: Algoritmo Vizinhos Mais Próximos (KNN) no Moodle - IA-UFOP

# Algoritmo de Aprendizagem dos Vizinhos Mais Próximos (K-NN)

# Definindo as colunas 1 'Alcool', 2 'Ácido Málico' como atributos descritivos
X = df_dataset.iloc[:, [0, 1]].values
# Definindo a coluna 13 'Classe de Vinhos' como atributo Classe (Preditivo)
y = df_dataset.iloc[:, 13].values

# Separando o conjunto de dados em conjunto de treinamento (70%) e de teste (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, 
random_state = 0)

# Normalizando os dados
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Gerando o Classificador com os dados de treinamento

classifier = KNeighborsClassifier(n_neighbors = 7)
classifier.fit(X_train, y_train)

# Realizando a Predição das Classes dos dados do conjunto de teste 
y_pred = classifier.predict(X_test)

# Gerando a Matriz de Confusão com os dados de teste
confmatriz = confusion_matrix(y_test, y_pred)

# Gerando o relatório de Predição de Classe
classreport = classification_report(y_test, y_pred)

# Vizualização dos Resultados sobre o Conjunto de Treinamento
# Uso da biblioteca Matplotlib
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('cyan', 'gray')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green', 'yellow'))(i), label = j)
plt.title('Classificador KNN (Dados Treinamento)')
plt.xlabel('Alcool')
plt.ylabel('Ácido Málico')
plt.legend()
plt.show()

print(classreport)
print (confmatriz)

"""Resultados: Para K = 21 Vizinhos mais próximos:
   
                precision    recall   f1-score   support

           1       0.82      0.82      0.82        17
           2       0.90      0.90      0.90        20
           3       0.67      0.67      0.67         9

Resultados: Para K = 11 Vizinhos mais próximos:

                precision    recall  f1-score   support

           1       0.82      0.82      0.82        17
           2       0.89      0.90      0.90        20
           3       0.60      0.67      0.67         9

**Resultados:Para K = 7 Vizinhos mais próximos - Para vários casos de testes com diferentes valores de K Vizinhos mais próximos, K = 7 apresentou maior precisão geral de classificação para os dois primeiros atributos da base**

              precision     recall   f1-score    support

           1       0.88      0.82      0.85        17
           2       0.90      0.90      0.90        20
           3       0.70      0.78      0.74         9

Resultados:Para K = 3 Vizinhos mais próximos:

                 precision  recall  f1-score   support

           1       0.88      0.82      0.85        17
           2       0.85      0.85      0.85        20
           3       0.70      0.78      0.74         9

# **Conclusão**

Foram mostradas as principais etapas de visualização, interpretação e pré-processamento dos dados, verificando dados duplicados, inconsistentes, redundantes e principalmente outliers. Também foi realizada a normalização de dados e análise de forma estatística da média, desvio padrão, máximo, mínimo, etc. Por fim, foi aplicado o Algoritmos de Classificação KNN para classificação de alguns atributos de dados dentro dessa base considerando 'Álcool' e 'Ácido Málico'

---
## Referências

[1] R. A. Fisher. The use of multiple measurements in taxonomic problems. Annual Eugenics, 7, Part II, 179-188 (1936). DOI: [10.1111/j.1469-1809.1936.tb02137.x](http://dx.doi.org/10.1111/j.1469-1809.1936.tb02137.x).

[2] T. M. Mitchell.Machine Learning. McGraw-Hill, Inc.,New York, NY, USA, 1 edition, 1997.

[3] A. C. P. L. F. de Carvalho, et al. Inteligência Artificial - Uma Abordagem de Aprendizado de Máquina, 2a Edição, Rio de Janeiro, LTC, 2022.

---
"""