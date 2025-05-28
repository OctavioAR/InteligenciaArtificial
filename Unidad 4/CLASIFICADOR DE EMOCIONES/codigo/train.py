import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import cv2
import os
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from modelo import EmocionCNN
from torchvision import transforms

# configuracion del dispositivo
dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dir_datos = "D:\\Documentos\\Octavio\\TEC\\OCTAVO SEMESTRE\\Inteligencia Artificial\\CLASIFICADOR DE EMOCIONES\\preprocesamiento"
datosCsv = os.path.join(dir_datos, "etiquetas_preprocesadas.csv")
# clase para cargar el dataset
class emocionesDataset(Dataset):
    def __init__(self, datos_df, transformaciones=None):
        self.datos = datos_df
        self.transformaciones = transformaciones
        self.idEmociones = {"angry": 0, "distress": 1, "happy": 2, "sad": 3, "surprise": 4}
       
    def __len__(self):
        return len(self.datos)
    # funcion para optener un elemento del dataset
    def __getitem__(self, idx):
        rutImagen = os.path.join(dir_datos, 
                              self.datos.iloc[idx]['conjunto'],
                              self.datos.iloc[idx]['etiqueta'],
                              self.datos.iloc[idx]['imagen'])
        
        img = cv2.imread(rutImagen, cv2.IMREAD_GRAYSCALE)
        etiqueta = self.idEmociones[self.datos.iloc[idx]['etiqueta']]
        
        if self.transformaciones:
            img = self.transformaciones(img)
            
        return img, etiqueta
# transformaciones para el datset
transformacionesTrain = transforms.Compose([
    transforms.ToPILImage(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

transformacionesVal = transforms.Compose([
    transforms.ToPILImage(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

def main():
    # cargar el csv
    datos = pd.read_csv(datosCsv)
    
    # dividir el dataset en train y test
    datosTrain = datos[datos['conjunto'] == 'train']
    datosVal = datos[datos['conjunto'] == 'val']
    
    # cargar el dataset y aplicar las transformaciones
    datasetTrain = emocionesDataset(datosTrain, transformacionesTrain)
    datasetVal = emocionesDataset(datosVal, transformacionesVal)
    
    # cargar los dataLoaders para el entrenamiento y validacion
    cargaTrain = DataLoader(datasetTrain, batch_size=64, shuffle=True)
    cargaVal = DataLoader(datasetVal, batch_size=64, shuffle=False)
    
    # inicializar el modelo, criterio y optimizador
    modelo = EmocionCNN(num_classes=5).to(dispositivo)
    criterio = nn.CrossEntropyLoss()
    optimizador = optim.Adam(modelo.parameters(), lr=0.001)
    
    # entrenar el modelo
    for epoch in range(30):  
        # inicializar la mejor perdida de validacion
        modelo.train()
        perdidaTrain = 0.0
        
        for entrada, etiqueta in cargaTrain:
            entrada, etiqueta = entrada.to(dispositivo), etiqueta.to(dispositivo)
            # 
            optimizador.zero_grad()
            salida = modelo(entrada)
            perdida = criterio(salida, etiqueta)
            perdida.backward()
            optimizador.step()
            
            perdidaTrain += perdida.item()
        
        # calcular la perdida de validacion
        modelo.eval()
        perdidaVal = 0.0
        predicciones = []
        etiquetas = []
        # calcular las predicciones
        with torch.no_grad():
            for entrada, etiqueta in cargaVal:
                entrada, etiqueta = entrada.to(dispositivo), etiqueta.to(dispositivo)
                salida = modelo(entrada)
                perdida = criterio(salida, etiqueta)
                perdidaVal += perdida.item()
                
                _, preds = torch.max(salida, 1)
                predicciones.extend(preds.cpu().numpy())
                etiquetas.extend(etiqueta.cpu().numpy())
        
        # mostrar resultados 
        print(f'Epoch {epoch+1}/30')
        print(f'Train Loss: {perdidaTrain/len(cargaTrain):.4f} | Val Loss: {perdidaVal/len(cargaVal):.4f}')
        print(classification_report(etiquetas, predicciones, target_names=["angry", "distress", "happy", "sad", "surprise"]))
        
        # guarda el mejor modelo
        # guarda el modelo si la perdida de validacion es menor que la mejor perdida
        if epoch == 0 or perdidaVal < best_val_loss:
            best_val_loss = perdidaVal
            torch.save(modelo.state_dict(), 'modeloEmociones.pth')
    
    print("Entrenamiento completado")

if __name__ == "__main__":
    main()