import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import messagebox

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

# Función de predicción 
def predecirSpam(emisor, receptor, mensaje):
    # Combinar todos los campos para el análisis 
    texto_completo = f"{emisor} {receptor} {mensaje}"
    
    # Preprocesamiento 
    texto = texto_completo.lower()
    texto = " ".join([word for word in texto.split() if len(word) > 2 and word not in palabrasVacias])
    
    # Vectorizar y predecir 
    correo_vectorizado = vectorizar.transform([texto])
    prediccion = modeloBayes.predict(correo_vectorizado)
    return "Spam" if prediccion[0] == 1 else "No Spam"

# Interfaz gráfica
def crearInterfaz():
    ventana = tk.Tk()
    ventana.title("Detector de Correos Spam")
    ventana.geometry("500x500")

    # Emisor
    tk.Label(ventana, text="Correo Emisor:").pack(pady=5)
    entrada_emisor = tk.Entry(ventana, width=50)
    entrada_emisor.pack(pady=5)

    # Receptor
    tk.Label(ventana, text="Correo Receptor:").pack(pady=5)
    entrada_receptor = tk.Entry(ventana, width=50)
    entrada_receptor.pack(pady=5)

    # Mensaje
    tk.Label(ventana, text="Cuerpo del Mensaje:").pack(pady=5)
    entrada_mensaje = tk.Text(ventana, height=10, width=50)
    entrada_mensaje.pack(pady=5)

    # Funcion para el boton de analisis
    def analizarCorreo():
        emisor = entrada_emisor.get().strip()
        receptor = entrada_receptor.get().strip()
        mensaje = entrada_mensaje.get("1.0", tk.END).strip()
        
        if not emisor or not receptor or not mensaje:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        
        try:
            resultado = predecirSpam(emisor, receptor, mensaje)
            messagebox.showinfo("Resultado", f"El correo es: {resultado}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    # Boton de analisis
    tk.Button(ventana, text="Analizar Correo", command=analizarCorreo).pack(pady=10)

    ventana.mainloop()

# Evaluacion del modelo 
precision = modeloBayes.score(vecPruebaX, prueba_Y)
y_pred = modeloBayes.predict(vecPruebaX)
recuperacion = np.sum((y_pred == 1) & (prueba_Y == 1)) / np.sum(prueba_Y == 1)

print(f"Precisión: {precision:}")
print(f"Recuperación: {recuperacion:}\n")

crearInterfaz()