import os
import cv2
import numpy as np
import random
from glob import glob
import csv
from sklearn.model_selection import train_test_split

# Rutas entrada/salida
carpeta_Entrada = "D:\\Documentos\\Octavio\\TEC\\OCTAVO SEMESTRE\\Inteligencia Artificial\\CLASIFICADOR DE EMOCIONES\\img_emociones\\train"
carpeta_Salida = "D:\\Documentos\\Octavio\\TEC\\OCTAVO SEMESTRE\\Inteligencia Artificial\\CLASIFICADOR DE EMOCIONES\\img_emociones\\preprocesamiento"
os.makedirs(carpeta_Salida, exist_ok=True)

# Lista de emociones
emociones = ["angry", "distress", "happy", "sad", "surprise"]

# Estructura de carpetas de salida
for carpetas in ['train', 'val', 'test']:
    for emocion in emociones:
        os.makedirs(os.path.join(carpeta_Salida, carpetas, emocion), exist_ok=True)

# Funciones de transformacion
def ajusteBrillo(img, factor):
    return np.clip(img * factor, 0, 255).astype(np.uint8)

def rotarImagen(img, angulo):
    (h, w) = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

# Procesamiento principal
with open(os.path.join(carpeta_Salida, 'etiquetas_preprocesadas.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['imagen', 'etiqueta', 'conjunto', 'transformacion'])
    
    todasImagenes = glob(os.path.join(carpeta_Entrada, "**/*.jpg"), recursive=True)
    
    # train 80 y temp 20
    train_images, temp_images = train_test_split(todasImagenes, test_size=0.2, random_state=42)
    
    # temp 15 y test 5
    val_images, test_images = train_test_split(temp_images, test_size=0.25, random_state=42)
    
    # Funcion para procesar cada conjunto
    def procesar_conjunto(imagenes, conjunto):
        for rutaImg in imagenes:
            img = cv2.imread(rutaImg, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
                
            # tamaño para emociones 48x48
            img = cv2.resize(img, (48, 48))
            
            emocion = os.path.basename(os.path.dirname(rutaImg))
            img_name = os.path.basename(rutaImg)
            
            # condicion para aplicar transformaciones
            if conjunto == 'train':
                transformaciones = [
                    (img, f"original_{img_name}", "original"),
                    (ajusteBrillo(img, 0.6), f"dark_{img_name}", "brillo_reducido"),
                    (ajusteBrillo(img, 1.4), f"bright_{img_name}", "brillo_aumentado"),
                    (rotarImagen(img, 15), f"rot15_{img_name}", "rotacion_15"),
                    (rotarImagen(img, -15), f"rotneg15_{img_name}", "rotacion_-15")
                ]
            else:                
                transformaciones = [(img, f"original_{img_name}", "original")]
            # guardamos imagenes transformadas
            for img_transformado, nombre, tipo in transformaciones:
                rutaSalida = os.path.join(carpeta_Salida, conjunto, emocion, nombre)
                cv2.imwrite(rutaSalida, img_transformado)
                writer.writerow([nombre, emocion, conjunto, tipo])
    
    # Procesar cada conjunto
    procesar_conjunto(train_images, 'train')
    procesar_conjunto(val_images, 'val')
    procesar_conjunto(test_images, 'test')

print("Preprocesamiento completado")