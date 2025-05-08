import logging
import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Set, Tuple, Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sistema_experto.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SistemaExpertoRespiratorio")

class LogicaProposicional:
    """Sistema de inferencia basado en lógica proposicional para diagnósticos respiratorios"""
    
    def __init__(self):
        self.logger = logging.getLogger("LogicaProposicional")
        self.predicados = {}  # Mapeo de código a descripción
        self.respuestas = {}  # Estado actual de los predicados (verdadero/falso)
        self.reglas = {}      # Reglas de inferencia para cada enfermedad
        self._inicializar_predicados()
        self._inicializar_reglas()
    
    def _inicializar_predicados(self):
        """Inicializa todos los predicados atómicos en el sistema"""
        self.predicados = {
            "A": "Fiebre >38.5°C (inicio brusco)",
            "B": "Mialgias severas",
            "C": "Cefalea frontal",
            "D": "Tos no productiva",
            "E": "Linfadenopatías",
            "F": "Exantema",
            "G": "Anosmia/ageusia súbita",
            "H": "Fatiga incapacitante",
            "I": "Saturación de O₂ <94%",
            "J": "Adenopatías cervicales",
            "K": "Sibilancias espiratorias",
            "L": "Taquipnea (>30 rpm en adultos)",
            "M": "Historia de contacto con niños",
            "N": "Consolidación pulmonar en RX",
            "O": "Escalofríos con temblores",
            "P": "Dolor pleurítico",
            "Q": "Esputo purulento",
            "R": "Crepitantes en auscultación",
            "S": "Mejora con antivirales",
            "T": "Tos >3 semanas",
            "U": "Hemoptisis",
            "V": "Sudores nocturnos",
            "W": "Pérdida de peso >10%",
            "X": "Respuesta a antibióticos estándar",
            "Y": "Tos paroxística (>5 golpes)",
            "Z": "Gallo inspiratorio post-tos",
            "A1": "Vómito postusivo",
            "B1": "Fiebre alta",
            "C1": "Sibilancias variables",
            "D1": "Mejora con broncodilatadores",
            "E1": "Historial atópico",
            "F1": "Fiebre concomitante",
            "G1": "Disnea progresiva",
            "H1": "Volumen Espiratorio Forzado <70%",
            "I1": "Paquete-año tabáquico >10",
            "J1": "Eosinofilia en esputo",
            "K1": "Crepitantes velcro",
            "L1": "Patrón reticular en TAC",
            "M1": "Disminución DLCO",
            "N1": "Exposición a alérgenos",
            "O1": "Dolor pleurítico súbito",
            "P1": "Taquicardia inexplicada",
            "Q1": "D-dímero >500 ng/mL",
            "R1": "Consolidación en RX",
            "S1": "Dolor punzante unilateral",
            "T1": "Hipersonoridad a percusión",
            "U1": "Disminución murmullo vesicular",
            "V1": "Fiebre asociada",
            "W1": "Pico Flujo <50% basal",
            "X1": "Uso de músculos accesorios",
            "Y1": "Palidez/cianosis",
            "Z1": "Foco infeccioso",
            "A2": "Hemoptisis recurrente",
            "B2": "Insuficiencia renal",
            "C2": "ANCA positivo",
            "D2": "Cultivos bacterianos negativos",
            "E2": "Asma + eosinofilia >10%",
            "F2": "Neuropatía periférica",
            "G2": "Infiltrados pulmonares migratorios",
            "H2": "ANCA negativo"
        }
        self.logger.info(f"Inicializados {len(self.predicados)} predicados atómicos")
    
    def _inicializar_reglas(self):
        """Inicializa las reglas de inferencia basadas en lógica proposicional
        
        Cada regla representa una implicación lógica: si todos los predicados 
        requeridos son verdaderos Y todos los predicados excluidos son falsos,
        entonces la enfermedad es verdadera.
        
        ∀x(A(x)∧B(x)∧...∧¬Y(x)→Enfermedad(x))
        """
        self.reglas = {
            "Influenza": {
                "requeridos": ["A", "B", "C", "D"],
                "excluidos": ["E", "F"]
            },
            "COVID-19": {
                "requeridos": ["G", "H", "I"],
                "excluidos": ["J"]
            },
            "RSV": {
                "requeridos": ["K", "L", "M"],
                "excluidos": ["N"]
            },
            "Neumonía Bacteriana": {
                "requeridos": ["O", "P", "Q", "R"],
                "excluidos": ["S"]
            },
            "Tuberculosis": {
                "requeridos": ["T", "U", "V", "W"],
                "excluidos": ["X"]
            },
            "Tos Ferina": {
                "requeridos": ["Y", "Z", "A1"],
                "excluidos": ["B1"]
            },
            "Asma": {
                "requeridos": ["C1", "D1", "E1"],
                "excluidos": ["F1"]
            },
            "EPOC": {
                "requeridos": ["G1", "H1", "I1"],
                "excluidos": ["J1"]
            },
            "Fibrosis Pulmonar": {
                "requeridos": ["K1", "L1", "M1"],
                "excluidos": ["N1"]
            },
            "Embolia Pulmonar": {
                "requeridos": ["O1", "P1", "Q1"],
                "excluidos": ["R1"]
            },
            "Neumotórax": {
                "requeridos": ["S1", "T1", "U1"],
                "excluidos": ["V1"]
            },
            "Crisis Asmática Grave": {
                "requeridos": ["W1", "X1", "Y1"],
                "excluidos": ["Z1"]
            },
            "Granulomatosis": {
                "requeridos": ["A2", "B2", "C2"],
                "excluidos": ["D2"]
            },
            "Churg-Strauss": {
                "requeridos": ["E2", "F2", "G2"],
                "excluidos": ["H2"]
            }
        }
        self.logger.info(f"Inicializadas {len(self.reglas)} reglas de inferencia")
    
    def establecer_hecho(self, predicado: str, valor: bool) -> None:
        """Establece el valor de verdad de un predicado atómico
        
        Args:
            predicado: Código del predicado atómico
            valor: Valor de verdad (True/False)
        """
        if predicado not in self.predicados:
            self.logger.warning(f"Predicado desconocido: {predicado}")
            return
        
        self.respuestas[predicado] = valor
        self.logger.info(f"Establecido predicado {predicado} = {valor}")
    
    def evaluar_regla(self, enfermedad: str) -> Tuple[bool, float, Dict[str, bool]]:
        """Evalúa una regla lógica para una enfermedad
        
        Implementa la fórmula: ∀x(A(x)∧B(x)∧...∧¬Y(x)→Enfermedad(x))
        
        Args:
            enfermedad: Nombre de la enfermedad a evaluar
            
        Returns:
            Tupla con (cumple_regla, porcentaje_cumplimiento, detalles)
        """
        if enfermedad not in self.reglas:
            self.logger.warning(f"Enfermedad no definida: {enfermedad}")
            return False, 0.0, {}
        
        regla = self.reglas[enfermedad]
        requeridos_totales = len(regla["requeridos"])
        excluidos_totales = len(regla["excluidos"])
        total_predicados = requeridos_totales + excluidos_totales
        
        if total_predicados == 0:
            return False, 0.0, {}
        
        # Verificar predicados requeridos (conjunción)
        requeridos_cumplidos = 0
        estado_requeridos = {}
        for pred in regla["requeridos"]:
            valor = self.respuestas.get(pred, False)
            estado_requeridos[pred] = valor
            if valor:
                requeridos_cumplidos += 1
        
        # Verificar predicados excluidos (negación)
        excluidos_cumplidos = 0
        estado_excluidos = {}
        for pred in regla["excluidos"]:
            valor = not self.respuestas.get(pred, True)  # Negación lógica
            estado_excluidos[pred] = valor
            if valor:
                excluidos_cumplidos += 1
        
        # Calcular cumplimiento total
        predicados_cumplidos = requeridos_cumplidos + excluidos_cumplidos
        porcentaje = (predicados_cumplidos / total_predicados) * 100 if total_predicados > 0 else 0
        
        # Verificar si se cumple la regla completamente
        regla_cumplida = (requeridos_cumplidos == requeridos_totales and 
                          excluidos_cumplidos == excluidos_totales)
        
        detalles = {
            "requeridos": estado_requeridos,
            "excluidos": estado_excluidos
        }
        
        return regla_cumplida, porcentaje, detalles
    
    def evaluar_todas_reglas(self) -> List[Tuple[str, bool, float, Dict]]:
        """Evalúa todas las reglas y devuelve los resultados ordenados por probabilidad
        
        Returns:
            Lista de tuplas (enfermedad, cumple_regla, porcentaje, detalles)
        """
        resultados = []
        
        for enfermedad in self.reglas:
            cumple, porcentaje, detalles = self.evaluar_regla(enfermedad)
            resultados.append((enfermedad, cumple, porcentaje, detalles))
        
        # Ordenar por porcentaje de cumplimiento (descendente)
        resultados.sort(key=lambda x: x[2], reverse=True)
        return resultados
    
    def diagnosticos_probables(self, umbral: float = 30.0) -> List[Tuple[str, float]]:
        """Devuelve las enfermedades que superan cierto umbral de probabilidad
        
        Args:
            umbral: Porcentaje mínimo para considerar una enfermedad (por defecto 30%)
            
        Returns:
            Lista de tuplas (enfermedad, porcentaje) ordenadas por probabilidad
        """
        resultados = self.evaluar_todas_reglas()
        diagnosticos = [(enf, porc) for enf, _, porc, _ in resultados if porc >= umbral]
        return diagnosticos
    
    def explicar_diagnostico(self, enfermedad: str) -> Dict:
        """Explica el diagnóstico para una enfermedad específica
        
        Args:
            enfermedad: Nombre de la enfermedad
            
        Returns:
            Diccionario con explicación del diagnóstico
        """
        _, porcentaje, detalles = self.evaluar_regla(enfermedad)
        
        # Generar explicación
        req_presentes = [p for p, v in detalles["requeridos"].items() if v]
        req_ausentes = [p for p, v in detalles["requeridos"].items() if not v]
        excl_cumplidos = [p for p, v in detalles["excluidos"].items() if v]
        excl_incumplidos = [p for p, v in detalles["excluidos"].items() if not v]
        
        explicacion = {
            "enfermedad": enfermedad,
            "probabilidad": porcentaje,
            "descripcion_predicados": {
                "req_presentes": {p: self.predicados[p] for p in req_presentes},
                "req_ausentes": {p: self.predicados[p] for p in req_ausentes},
                "excl_cumplidos": {p: self.predicados[p] for p in excl_cumplidos},
                "excl_incumplidos": {p: self.predicados[p] for p in excl_incumplidos}
            },
            "formula_logica": self._generar_formula_logica(enfermedad)
        }
        
        return explicacion
    
    def _generar_formula_logica(self, enfermedad: str) -> str:
        """Genera la fórmula lógica para una enfermedad
        
        Args:
            enfermedad: Nombre de la enfermedad
            
        Returns:
            Cadena con la fórmula lógica
        """
        regla = self.reglas[enfermedad]
        requeridos = " ∧ ".join([f"{p}" for p in regla["requeridos"]])
        excluidos = " ∧ ".join([f"¬{p}" for p in regla["excluidos"]])
        
        if requeridos and excluidos:
            return f"({requeridos}) ∧ ({excluidos}) → {enfermedad}"
        elif requeridos:
            return f"({requeridos}) → {enfermedad}"
        elif excluidos:
            return f"({excluidos}) → {enfermedad}"
        else:
            return f"{enfermedad} (sin condiciones)"

class InterfazSistemaExperto:
    """Interfaz gráfica para el sistema experto de diagnóstico respiratorio"""
    
    def __init__(self, root):
        self.logger = logging.getLogger("InterfazSistemaExperto")
        self.root = root
        self.root.title("Sistema Experto Diagnóstico Respiratorio")
        self.root.geometry("1200x800")
        
        self.sistema = LogicaProposicional()
        self.checkboxes = {}
        self._inicializar_ui()
        
        self.logger.info("Interfaz de usuario inicializada")
    
    def _inicializar_ui(self):
        """Inicializa todos los componentes de la interfaz de usuario"""
        # Panel principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema Experto para Diagnóstico de Enfermedades Respiratorias", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        
        subtitulo = ttk.Label(main_frame, text="Seleccione los síntomas y signos del paciente", 
                             font=("Arial", 12))
        subtitulo.pack(pady=5)
        
        # Contenedor para panel de síntomas y resultados
        panel_contenedor = ttk.Frame(main_frame)
        panel_contenedor.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Panel de síntomas (scrollable)
        panel_izquierdo = ttk.Frame(panel_contenedor)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        canvas_sintomas = tk.Canvas(panel_izquierdo)
        scrollbar = ttk.Scrollbar(panel_izquierdo, orient="vertical", command=canvas_sintomas.yview)
        frame_sintomas = ttk.Frame(canvas_sintomas)
        
        frame_sintomas.bind(
            "<Configure>",
            lambda e: canvas_sintomas.configure(scrollregion=canvas_sintomas.bbox("all"))
        )
        
        canvas_sintomas.create_window((0, 0), window=frame_sintomas, anchor="nw")
        canvas_sintomas.configure(yscrollcommand=scrollbar.set)
        
        canvas_sintomas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear checkboxes para cada predicado
        predicados_ordenados = sorted(list(self.sistema.predicados.items()))
        self._crear_checkboxes(frame_sintomas, predicados_ordenados)
        
        # Panel de resultados (lado derecho)
        panel_derecho = ttk.Frame(panel_contenedor)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Botón para evaluar
        btn_evaluar = ttk.Button(panel_derecho, text="Evaluar Diagnósticos", 
                               command=self._evaluar_diagnosticos)
        btn_evaluar.pack(pady=10)
        
        # Área de resultados
        ttk.Label(panel_derecho, text="Resultados:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        
        self.resultado_frame = ttk.Frame(panel_derecho)
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de explicación
        ttk.Label(panel_derecho, text="Explicación del diagnóstico:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        
        self.explicacion_text = tk.Text(panel_derecho, height=15, width=50, wrap="word")
        self.explicacion_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.explicacion_text.config(state="disabled")
        
        # Botones de acción
        frame_botones = ttk.Frame(main_frame)
        frame_botones.pack(fill=tk.X, pady=10)
        
        btn_limpiar = ttk.Button(frame_botones, text="Limpiar Todo", command=self._limpiar_todo)
        btn_limpiar.pack(side=tk.RIGHT, padx=5)
        
        btn_guardar = ttk.Button(frame_botones, text="Guardar Diagnóstico", command=self._guardar_diagnostico)
        btn_guardar.pack(side=tk.RIGHT, padx=5)
    
    def _crear_checkboxes(self, frame_padre, predicados):
        """Crea checkboxes para cada predicado en el sistema
        
        Args:
            frame_padre: Frame contenedor para los checkboxes
            predicados: Lista de tuplas (código, descripción)
        """
        for i, (codigo, descripcion) in enumerate(predicados):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                frame_padre, 
                text=f"{codigo}: {descripcion}",
                variable=var,
                command=lambda c=codigo, v=var: self._actualizar_predicado(c, v.get())
            )
            cb.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            self.checkboxes[codigo] = var
    
    def _actualizar_predicado(self, codigo, valor):
        """Actualiza el valor de un predicado en el sistema experto
        
        Args:
            codigo: Código del predicado
            valor: Valor booleano (True/False)
        """
        self.sistema.establecer_hecho(codigo, valor)
    
    def _evaluar_diagnosticos(self):
        """Evalúa todos los diagnósticos y muestra los resultados"""
        try:
            # Limpiar frame de resultados
            for widget in self.resultado_frame.winfo_children():
                widget.destroy()
            
            # Obtener diagnósticos probables
            diagnosticos = self.sistema.diagnosticos_probables(umbral=10.0)
            
            if not diagnosticos:
                ttk.Label(self.resultado_frame, 
                         text="No hay diagnósticos que cumplan con el umbral mínimo").pack(anchor="w")
                return
            
            # Crear lista de diagnósticos con barras de progreso
            for i, (enfermedad, probabilidad) in enumerate(diagnosticos):
                frame = ttk.Frame(self.resultado_frame)
                frame.pack(fill=tk.X, pady=2)
                
                # Nombre de la enfermedad como botón para ver explicación
                btn = ttk.Button(
                    frame, 
                    text=f"{enfermedad}",
                    command=lambda e=enfermedad: self._mostrar_explicacion(e)
                )
                btn.pack(side=tk.LEFT, padx=5)
                
                # Barra de progreso para la probabilidad
                prog = ttk.Progressbar(
                    frame, 
                    orient=tk.HORIZONTAL, 
                    length=200, 
                    value=probabilidad
                )
                prog.pack(side=tk.LEFT, padx=5)
                
                # Etiqueta con el porcentaje
                ttk.Label(frame, text=f"{probabilidad:.1f}%").pack(side=tk.LEFT, padx=5)
                
                # Si cumple 100%, marcar como diagnóstico principal
                if probabilidad >= 99.9:
                    ttk.Label(frame, text="★ DIAGNÓSTICO PRINCIPAL", 
                             foreground="green").pack(side=tk.LEFT, padx=5)
            
            # Mostrar explicación del primer diagnóstico
            if diagnosticos:
                self._mostrar_explicacion(diagnosticos[0][0])
                
        except Exception as e:
            self.logger.error(f"Error al evaluar diagnósticos: {e}")
            self.logger.error(traceback.format_exc())
            messagebox.showerror("Error", f"Error al evaluar diagnósticos: {str(e)}")
    
    def _mostrar_explicacion(self, enfermedad):
        """Muestra la explicación detallada de un diagnóstico
        
        Args:
            enfermedad: Nombre de la enfermedad a explicar
        """
        try:
            # Obtener explicación
            explicacion = self.sistema.explicar_diagnostico(enfermedad)
            
            # Habilitar y limpiar el área de texto
            self.explicacion_text.config(state="normal")
            self.explicacion_text.delete(1.0, tk.END)
            
            # Añadir información
            self.explicacion_text.insert(tk.END, f"DIAGNÓSTICO: {enfermedad}\n", "titulo")
            self.explicacion_text.insert(tk.END, f"Probabilidad: {explicacion['probabilidad']:.1f}%\n\n")
            
            # Fórmula lógica
            self.explicacion_text.insert(tk.END, "Fórmula lógica:\n", "subtitulo")
            self.explicacion_text.insert(tk.END, f"{explicacion['formula_logica']}\n\n")
            
            # Factores presentes requeridos
            self.explicacion_text.insert(tk.END, "Factores presentes que apoyan el diagnóstico:\n", "subtitulo")
            if explicacion['descripcion_predicados']['req_presentes']:
                for codigo, desc in explicacion['descripcion_predicados']['req_presentes'].items():
                    self.explicacion_text.insert(tk.END, f"✓ {codigo}: {desc}\n", "presente")
            else:
                self.explicacion_text.insert(tk.END, "Ninguno\n")
            
            # Factores ausentes que deberían estar presentes
            self.explicacion_text.insert(tk.END, "\nFactores ausentes que deberían estar presentes:\n", "subtitulo")
            if explicacion['descripcion_predicados']['req_ausentes']:
                for codigo, desc in explicacion['descripcion_predicados']['req_ausentes'].items():
                    self.explicacion_text.insert(tk.END, f"✗ {codigo}: {desc}\n", "ausente")
            else:
                self.explicacion_text.insert(tk.END, "Ninguno\n")
            
            # Factores correctamente ausentes
            self.explicacion_text.insert(tk.END, "\nFactores correctamente ausentes:\n", "subtitulo")
            if explicacion['descripcion_predicados']['excl_cumplidos']:
                for codigo, desc in explicacion['descripcion_predicados']['excl_cumplidos'].items():
                    self.explicacion_text.insert(tk.END, f"✓ {codigo}: {desc}\n", "presente")
            else:
                self.explicacion_text.insert(tk.END, "Ninguno\n")
            
            # Factores presentes que deberían estar ausentes
            self.explicacion_text.insert(tk.END, "\nFactores presentes que contradicen el diagnóstico:\n", "subtitulo")
            if explicacion['descripcion_predicados']['excl_incumplidos']:
                for codigo, desc in explicacion['descripcion_predicados']['excl_incumplidos'].items():
                    self.explicacion_text.insert(tk.END, f"! {codigo}: {desc}\n", "contradice")
            else:
                self.explicacion_text.insert(tk.END, "Ninguno\n")
            
            # Configurar estilos
            self.explicacion_text.tag_configure("titulo", font=("Arial", 12, "bold"))
            self.explicacion_text.tag_configure("subtitulo", font=("Arial", 10, "bold"))
            self.explicacion_text.tag_configure("presente", foreground="green")
            self.explicacion_text.tag_configure("ausente", foreground="red")
            self.explicacion_text.tag_configure("contradice", foreground="orange")
            
            # Deshabilitar edición
            self.explicacion_text.config(state="disabled")
            
        except Exception as e:
            self.logger.error(f"Error al mostrar explicación: {e}")
            self.logger.error(traceback.format_exc())
            messagebox.showerror("Error", f"Error al mostrar explicación: {str(e)}")
     
    def _limpiar_todo(self):
        """Limpia todas las selecciones y resultados"""
        # Limpiar checkboxes
        for var in self.checkboxes.values():
            var.set(False)
        
        # Limpiar respuestas en el sistema
        self.sistema.respuestas.clear()
        
        # Limpiar resultados
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()
        
        # Limpiar explicación
        self.explicacion_text.config(state="normal")
        self.explicacion_text.delete(1.0, tk.END)
        self.explicacion_text.config(state="disabled")
        
        self.logger.info("Interfaz limpiada completamente")
    
    def _guardar_diagnostico(self):
        """Guarda el diagnóstico actual a un archivo"""
        # Implementación futura
        messagebox.showinfo("Información", "Funcionalidad de guardado en desarrollo")


def main():
    try:
        root = tk.Tk()
        app = InterfazSistemaExperto(root)
        root.mainloop()
    except Exception as e:
        logger.critical(f"Error fatal en la aplicación: {e}")
        logger.critical(traceback.format_exc())
        messagebox.showerror("Error Fatal", f"Error en la aplicación: {str(e)}")


if __name__ == "__main__":
    main()