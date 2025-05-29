import cv2
import os
import numpy as np
import glob
import time
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk

class EmotionRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento de Emociones")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Configuración de fuentes
        self.title_font = font.Font(family='Helvetica', size=16, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=12)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="SISTEMA DE RECONOCIMIENTO DE EMOCIONES",
            font=self.title_font,
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Imagen de logo
        try:
            logo_img = Image.open("logo.png").resize((150, 150), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(main_frame, image=self.logo, bg='#2c3e50')
            logo_label.pack(pady=(0, 20))
        except:
            pass
        
        # Frame de botones
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Botón de inicio
        start_button = ttk.Button(
            button_frame,
            text="INICIAR RECONOCIMIENTO",
            command=self.start_recognition,
            style='Accent.TButton'
        )
        start_button.pack(pady=10, ipadx=20, ipady=10)
        
        # Botón de salida
        exit_button = ttk.Button(
            button_frame,
            text="SALIR",
            command=self.root.quit,
            style='TButton'
        )
        exit_button.pack(pady=10, ipadx=20, ipady=10)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=self.button_font, foreground='#2c3e50')
        self.style.configure('Accent.TButton', font=self.button_font, foreground='white', background='#3498db')
        self.style.map('Accent.TButton', background=[('active', '#2980b9')])
    
    def start_recognition(self):
        self.root.withdraw()  # Ocultar la ventana principal
        self.run_emotion_recognition()
    
    def run_emotion_recognition(self):
        try:
            # Inicializar reconocedor LBPH
            emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
            
            # Cargar modelo
            dataPath = 'C:/Users/HP/Desktop/PROF/CAPTURAS'
            models_path = os.path.join(dataPath, 'modelos')
            model_file = self.find_latest_model('LBPH', models_path)
            
            if model_file is None:
                print("No se encontró el modelo LBPH")
                return
            
            emotion_recognizer.read(model_file)
            print("Modelo LBPH cargado exitosamente")
            
            # Configuración de emociones (asegurar que Felicidad está en posición 1)
            emotions = ["Enojo", "Felicidad", "Sorpresa", "Tristeza"]
            print("Orden de emociones:", emotions)
            
            # Umbral ajustado para mejor detección de felicidad
            threshold = 55  # Más bajo para mayor sensibilidad
            
            # Inicializar cámara
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Calentamiento de cámara
            for _ in range(10):
                cap.read()
            time.sleep(0.5)
            
            # Cargar clasificador de rostros
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            # Crear ventana de visualización
            cv2.namedWindow('Reconocimiento de Emociones', cv2.WINDOW_NORMAL)
            
            # Variables para seguimiento de estado
            last_emotion = None
            emotion_counter = 0
            required_consecutive_frames = 3  # Para confirmar detección
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detección de rostros optimizada para felicidad
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=7,  # Más estricto para evitar falsos positivos
                    minSize=(120, 120),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                for (x, y, w, h) in faces:
                    # Extraer región de interés (ROI)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_gray = cv2.resize(roi_gray, (150, 150), interpolation=cv2.INTER_CUBIC)
                    
                    # Realizar predicción
                    label, confidence = emotion_recognizer.predict(roi_gray)
                    
                    # Mostrar información de diagnóstico
                    cv2.putText(frame, f'Conf: {confidence:.1f}', (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    # Lógica de detección mejorada para felicidad
                    if confidence < threshold and 0 <= label < len(emotions):
                        current_emotion = emotions[label]
                        
                        # Sistema de confirmación
                        if current_emotion == last_emotion:
                            emotion_counter += 1
                        else:
                            emotion_counter = 1
                            last_emotion = current_emotion
                        
                        # Solo mostrar si se detecta consistentemente
                        if emotion_counter >= required_consecutive_frames:
                            color = (0, 255, 0)  # Verde para detección confirmada
                            text = f"{current_emotion} ({confidence:.1f})"
                            
                            # Énfasis especial en felicidad
                            if current_emotion == "Felicidad":
                                color = (0, 255, 255)  # Amarillo para felicidad
                                text = f"😊 {text} 😊"
                            
                            cv2.putText(frame, text, (x, y-40), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    else:
                        cv2.putText(frame, "Analizando...", (x, y-40), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        last_emotion = None
                        emotion_counter = 0
                
                # Mostrar frame
                cv2.imshow('Reconocimiento de Emociones', frame)
                
                # Salir con ESC
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            
            # Liberar recursos
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.root.deiconify()  # Mostrar ventana principal nuevamente
    
    def find_latest_model(self, method, models_path):
        """Busca el modelo más reciente para LBPH"""
        try:
            if not os.path.exists(models_path):
                return None
            
            patterns = [
                os.path.join(models_path, f"modelo_{method}_*.xml"),
                os.path.join(models_path, f"modelo{method}.xml")
            ]
            
            for pattern in patterns:
                model_files = glob.glob(pattern)
                if model_files:
                    return max(model_files, key=os.path.getmtime)
            
            return None
        except:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionRecognizerApp(root)
    root.mainloop()