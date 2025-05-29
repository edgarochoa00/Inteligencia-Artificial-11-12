import sys
import os
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QWidget)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class EmotionCaptureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturador de Emociones")
        self.setGeometry(100, 100, 900, 600)
        
        # Configuración
        self.dataPath = 'C:/Users/HP/Desktop/PROF/CAPTURAS'
        self.emotionName = ""
        self.count = 0
        self.capturing = False
        self.max_images = 200
        
        # Inicializar cámara
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Configurar UI
        self.initUI()
        
        # Timer para actualizar la cámara
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    
    def initUI(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panel de la cámara
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        main_layout.addWidget(self.camera_label)
        
        # Panel de control
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        
        # Selector de emoción
        self.emotion_combo = QComboBox()
        self.emotion_combo.addItems(["Enojo", "Felicidad", "Sorpresa", "Tristeza"])
        
        # Botones
        self.start_btn = QPushButton("Iniciar Captura")
        self.start_btn.clicked.connect(self.start_capture)
        
        self.stop_btn = QPushButton("Detener Captura")
        self.stop_btn.clicked.connect(self.stop_capture)
        self.stop_btn.setEnabled(False)
        
        # Contador
        self.counter_label = QLabel("Imágenes capturadas: 0/200")
        
        # Estado
        self.status_label = QLabel("Estado: Listo")
        
        # Añadir widgets al layout
        control_layout.addWidget(QLabel("Seleccione la emoción:"))
        control_layout.addWidget(self.emotion_combo)
        control_layout.addSpacing(20)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addSpacing(20)
        control_layout.addWidget(self.counter_label)
        control_layout.addWidget(self.status_label)
        control_layout.addStretch()
        
        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel)
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detección de rostros
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceClassif.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(rgb_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                if self.capturing:
                    # Guardar rostro
                    rostro = frame[y:y+h, x:x+w]
                    rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                    emotion_folder = os.path.join(self.dataPath, self.emotionName)
                    os.makedirs(emotion_folder, exist_ok=True)
                    cv2.imwrite(os.path.join(emotion_folder, f'rostro_{self.count}.jpg'), rostro)
                    self.count += 1
                    self.counter_label.setText(f"Imágenes capturadas: {self.count}/{self.max_images}")
                    
                    if self.count >= self.max_images:
                        self.stop_capture()
                        self.status_label.setText("Estado: Captura completada")
            
            # Mostrar imagen en la interfaz
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qt_image))
    
    def start_capture(self):
        self.emotionName = self.emotion_combo.currentText()
        self.count = 0
        self.capturing = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText(f"Estado: Capturando {self.emotionName}")
        self.counter_label.setText(f"Imágenes capturadas: 0/{self.max_images}")
        
        # Crear carpeta si no existe
        emotion_folder = os.path.join(self.dataPath, self.emotionName)
        os.makedirs(emotion_folder, exist_ok=True)
    
    def stop_capture(self):
        self.capturing = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(f"Estado: Captura detenida ({self.count} imágenes)")
    
    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmotionCaptureApp()
    window.show()
    sys.exit(app.exec_())