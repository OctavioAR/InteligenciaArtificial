import cv2
import torch
import numpy as np
from modelo import EmocionCNN
from torchvision import transforms

class DetectorEmociones:
    def __init__(self, rutModelo):
        self.dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.modelo = self.cargarModelo(rutModelo)
        self.transformaciones = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
        self.emociones = ["enojado", "angustia", "feliz", "triste", "sorpresa"]
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def cargarModelo(self, rutaModelo):
        modelo = EmocionCNN(num_clases=5)
        modelo.load_state_dict(torch.load(rutaModelo, map_location=self.dispositivo))
        modelo.eval()
        return modelo.to(self.dispositivo)
    
    def detectarEmocion(self, imgCara):
        imgCara = cv2.resize(imgCara, (48, 48))
        tensor_img = self.transformaciones(imgCara).unsqueeze(0).to(self.dispositivo)
        
        with torch.no_grad():
            salidas = self.modelo(tensor_img)
            _, predicted = torch.max(salidas, 1)
            emocion = self.emociones[predicted.item()]
        
        return emocion
    
    def video(self):
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            caras = self.detector.detectMultiScale(gris, 1.3, 5)
            
            for (x, y, w, h) in caras:
                imgCara = gris[y:y+h, x:x+w]
                emocion = self.detectarEmocion(imgCara)
                
                color = (0, 255, 0) if emocion in ["feliz", "sorpresa"] else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, emocion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            cv2.imshow('Detectar Emociones', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = DetectorEmociones('modelo/modeloEmociones.pth')
    detector.video()