import torch
import torch.nn as nn
import torch.nn.functional as F

class EmocionCNN(nn.Module):
    def __init__(self, num_clases=5):
        super(EmocionCNN, self).__init__()
        
        # Capa convolucionales
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        
        # Capas completamente conectadas
        # 48x48 -> 24x24 -> 12x12
        self.fc1 = nn.Linear(64 * 12 * 12, 128)  
        self.fc2 = nn.Linear(128, num_clases)
        
        self.dropout = nn.Dropout(0.25)
        
    def forward(self, x):
        # Primer bloque convolucion1 + relu + agrupar
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)  # 48x48 -> 24x24
        
        # Segundo bloque convolucion2 + relu + agrupar
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)  # 24x24 -> 12x12
        
        # Aplanar
        x = x.view(-1, 64 * 12 * 12)
        
        # Capas FC
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x