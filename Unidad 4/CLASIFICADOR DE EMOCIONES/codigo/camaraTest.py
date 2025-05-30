import cv2
import torch
import numpy as np
from modelo import EmocionCNN
from torchvision import transforms

class DetectorEmociones:
    # constructor de la clase
    def __init__(self, rutModelo):
        self.dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.modelo = self.cargarModelo(rutModelo)
        
        self.transformaciones = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
        # lista de emociones que se van a detectar
        self.emociones = ["enojado", "angustia", "feliz", "triste", "sorpresa"]
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # funcion para cargar el modelo de emociones
    def cargarModelo(self, rutaModelo):
        modelo = EmocionCNN(num_clases=5)
        modelo.load_state_dict(torch.load(rutaModelo, map_location=self.dispositivo))
        modelo.eval()
        return modelo.to(self.dispositivo)
    # funcion para detectar emociones en una imagen de la cara usando el modelo cargado
    def detectarEmocion(self, imgCara):
        imgCara = cv2.resize(imgCara, (48, 48))
        tensor_img = self.transformaciones(imgCara).unsqueeze(0).to(self.dispositivo)
        # realiza la prediccion de la emocion
        with torch.no_grad():
            salidas = self.modelo(tensor_img)
            _, predicted = torch.max(salidas, 1)
            emocion = self.emociones[predicted.item()]
        
        return emocion
    # funcion para capturar video desde la camara y detectar emociones en tiempo real
    def video(self):
        camara = cv2.VideoCapture(0)
        
        while True:
            ret, frame = camara.read()
            if not ret:
                break
            # convertimos el frame a escala de grises para la deteccion de caras
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            caras = self.detector.detectMultiScale(gris, 1.3, 5)
            # bucle para recorrer la cara detectada
            for (x, y, w, h) in caras:
                imgCara = gris[y:y+h, x:x+w]
                emocion = self.detectarEmocion(imgCara)
                # dubujamos la cara y la emocion detectada
                color = (0, 255, 0) if emocion in ["feliz", "sorpresa"] else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, emocion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            cv2.imshow('Detectar Emociones', frame)
            if cv2.waitKey(1) & 0xFF == ord('x'): 
                break

        camara.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # inicializamos el detector de emociones con el modelo preentrenado
    detector = DetectorEmociones('modelo/modeloEmociones.pth')
    detector.video()