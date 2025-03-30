import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.corpus import stopwords

# Cargar los datos
datos = pd.read_csv("spam_assassin.csv")

# Preprocesamiento 
datos = datos.drop_duplicates(subset=["text"]).copy()
datos["text"] = datos["text"].str.lower()
datos["text"] = datos["text"].str.replace(r"[^a-zA-Z\s]", " ", regex=True)
datos["text"] = datos["text"].apply(lambda x: " ".join([word for word in x.split() if len(word) > 2]))

# Obtener stopwords 
palabrasVaciasEs = set(stopwords.words("spanish"))
palabrasVaciasEn = set(stopwords.words("english"))
palabrasVacias = palabrasVaciasEs.union(palabrasVaciasEn)

# Filtrar stopwords 
datos["text"] = datos["text"].apply(lambda x: " ".join([word for word in x.split() if word not in palabrasVacias]))

# Dividir datos en entrenamiento y prueba
entrena_X, prueba_X, entrena_Y, prueba_Y = train_test_split(
    datos["text"], datos["target"], test_size=0.2, random_state=42
)

# Vectorización 
vectorizar = CountVectorizer()
vecEntreamientoX = vectorizar.fit_transform(entrena_X)
vecPruebaX = vectorizar.transform(prueba_X)

# Entrenar modelo Bayes
modeloBayes = MultinomialNB()
modeloBayes.fit(vecEntreamientoX, entrena_Y)

# Evaluacion del modelo 
precision = modeloBayes.score(vecPruebaX, prueba_Y)
y_pred = modeloBayes.predict(vecPruebaX)
recuperacion = np.sum((y_pred == 1) & (prueba_Y == 1)) / np.sum(prueba_Y == 1)

print(f"Precisión: {precision:}")
print(f"Recuperación: {recuperacion:}\n")