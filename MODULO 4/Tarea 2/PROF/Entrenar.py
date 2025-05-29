import cv2
import os
import numpy as np
import time
from datetime import datetime

class EmotionTrainer:
    def __init__(self, data_path='C:/Users/HP/Desktop/PROF/CAPTURAS'):
        self.data_path = data_path
        self.emotions = ["Enojo", "Felicidad", "Sorpresa", "Tristeza"]
        
    def train_models(self):
        """Carga los datos y entrena los tres modelos de reconocimiento"""
        try:
            print("\n=== INICIANDO ENTRENAMIENTO DE MODELOS ===")
            
            # Verificar si existe el directorio de datos
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"No se encontró el directorio de datos: {self.data_path}")
            
            # Cargar datos
            faces, labels = self._load_data()
            
            if len(faces) == 0:
                raise ValueError("No se encontraron imágenes para entrenamiento")
            
            print(f"\nDatos cargados correctamente:")
            print(f"- Total de imágenes: {len(faces)}")
            print(f"- Distribución por emociones:")
            
            # Mostrar distribución de imágenes por emoción
            for i, emotion in enumerate(self.emotions):
                count = labels.count(i)
                print(f"  {emotion}: {count} imágenes")
            
            # Entrenar modelos
            self._train_and_save('EigenFaces', faces, labels)
            self._train_and_save('FisherFaces', faces, labels)
            self._train_and_save('LBPH', faces, labels)
            
            print("\nEntrenamiento completado exitosamente!")
            
        except Exception as e:
            print(f"\nError durante el entrenamiento: {str(e)}")
    
    def _load_data(self):
        """Carga las imágenes y etiquetas desde las carpetas de emociones"""
        faces = []
        labels = []
        
        for label, emotion in enumerate(self.emotions):
            emotion_path = os.path.join(self.data_path, emotion)
            
            if not os.path.exists(emotion_path):
                print(f"Advertencia: No se encontró la carpeta para {emotion}")
                continue
                
            print(f"\nProcesando imágenes de {emotion}...")
            
            for file in os.listdir(emotion_path):
                if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                    
                file_path = os.path.join(emotion_path, file)
                
                try:
                    # Leer imagen en escala de grises y redimensionar
                    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (150, 150), interpolation=cv2.INTER_AREA)
                    
                    faces.append(img)
                    labels.append(label)
                    
                except Exception as e:
                    print(f"Error al procesar {file}: {str(e)}")
                    continue
        
        return faces, labels
    
    def _train_and_save(self, method, faces, labels):
        """Entrena y guarda un modelo específico"""
        print(f"\nEntrenando modelo {method}...")
        inicio = time.time()
        
        # Crear el modelo adecuado
        if method == 'EigenFaces':
            model = cv2.face.EigenFaceRecognizer_create()
        elif method == 'FisherFaces':
            model = cv2.face.FisherFaceRecognizer_create()
        elif method == 'LBPH':
            model = cv2.face.LBPHFaceRecognizer_create()
        else:
            raise ValueError(f"Método desconocido: {method}")
        
        # Entrenar el modelo
        model.train(faces, np.array(labels))
        
        # Guardar el modelo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_dir = os.path.join(self.data_path, "modelos")
        os.makedirs(model_dir, exist_ok=True)
        
        model_file = os.path.join(model_dir, f"modelo_{method}_{timestamp}.xml")
        model.write(model_file)
        
        tiempo = time.time() - inicio
        print(f"- Modelo {method} entrenado en {tiempo:.2f} segundos")
        print(f"- Guardado en: {model_file}")

if __name__ == "__main__":
    # Configurar y ejecutar el entrenamiento
    trainer = EmotionTrainer()
    trainer.train_models()