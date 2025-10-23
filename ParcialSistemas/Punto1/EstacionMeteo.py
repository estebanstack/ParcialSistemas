import csv, queue, random, threading, time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path                     # Manejo de rutas de archivos
from collections import deque

import tkinter as tk                         # Libreria grafica estandar de Python
from tkinter import ttk                      # Libreria para mejorar la apariencia
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   # Para integrar Matplotlib en Tkinter
from matplotlib.figure import Figure          # Objeto principal grafico en Matplotlib

# Clase de datos
@dataclass                                   # genera constructor
class Medida:                                
    t: datetime                              
    temp: float                              
    hum: float                               
    pres: float                              

# Simulador de sensores
class Sensor:                                # Clase que simula un sensor con valores aleatorios realistas
    def __init__(self, v, paso, mn, mx):
        self.v, self.paso, self.mn, self.mx = v, paso, mn, mx   # Asigna los parametros a los atributos del objeto
    def next(self):                          # Calcula el siguiente valor del sensor
        self.v += random.uniform(-self.paso, self.paso)          # Aplica un cambio aleatorio entre ±paso
        self.v += random.uniform(-self.paso*0.15, self.paso*0.15) # Añade un ruido adicional
        self.v = min(self.mx, max(self.mn, self.v))              # Asegura que el valor quede dentro de los limites
        return self.v                                         

# Hilo de adquisicion
class HiloAdq(threading.Thread):         
    def __init__(self, q, buf, lock, stop):  # Recibe una cola, un buffer, un candado y un evento de parada
        super().__init__(daemon=True)        # Llama al constructor de Thread y lo marca como "daemon"
        self.q, self.buf, self.lock, self.stop = q, buf, lock, stop  # Guarda las referencias
        # Crea tres sensores con rangos y pasos adecuados
        self.st = Sensor(24, 0.4, -5, 42)    # Sensor de temperatura
        self.sh = Sensor(60, 1.5, 5, 100)    # Sensor de humedad
        self.sp = Sensor(1013, 0.8, 980, 1050) # Sensor de presión
    def run(self):                           # Metodo para iniciar el hilo
        while not self.stop.is_set():        # Bucle hasta que se active la señal de parada
            m = Medida(datetime.now(), self.st.next(), self.sh.next(), self.sp.next()) # Genera nueva muestra
            try: self.q.put_nowait(m)        # Intenta colocar la muestra en la cola sin bloquear
            except queue.Full: pass          # Si la cola esta llena, la descarta
            with self.lock:                  # Bloquea el acceso al buffer
                self.buf.append(m)           # Agrega la nueva muestra al final del buffer
                if len(self.buf) > 300: self.buf.popleft()  # Mantiene maximo 300 elementos
            time.sleep(1)                    # Espera 1 segundo antes de generar la siguiente medida

# Hilo de registro
class HiloLog(threading.Thread):             # Hilo encargado de guardar los datos en CSV
    def __init__(self, q, stop, out=Path("logs")):  
        super().__init__(daemon=True)        # Inicializa el hilo como daemon
        self.q, self.stop, self.batch = q, stop, [] # Guarda la cola, evento y lote temporal
        out.mkdir(parents=True, exist_ok=True)       # Crea la carpeta "logs" si no existe
        self.csv = out / f"clima_{datetime.now().strftime('%Y%m%d')}.csv"
        if not self.csv.exists():            # Si el archivo no existe aun lo creea
            with self.csv.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["fecha","hora","temp_c","hum_pct","pres_hpa"])  # encabezado
    def run(self):                           # Metodo que ejecuta el hilo
        last = time.time()                   # Guarda el momento del ultimo guardado
        while not self.stop.is_set():        # Bucle hasta recibir señal de parada
            try: self.batch.append(self.q.get(timeout=0.2))  # Toma una muestra de la cola
            except queue.Empty: pass         # Si no hay datos, ignora y continua
            if time.time() - last >= 5 and self.batch:  # Si pasaron 5 s y hay datos en el lote llama a flush() y actualiza tiempo
                self.flush(); last = time.time()        
        if self.batch: self.flush()          # guarda los datos restantes
    def flush(self):                         # Guarda el lote acumulado en el archivo CSV
        with self.csv.open("a", newline="", encoding="utf-8") as f:  
            w = csv.writer(f)                
            for m in self.batch:             # Recorre cada medida acumulada
                w.writerow([m.t.strftime("%Y-%m-%d"), m.t.strftime("%H:%M:%S"),  # Fecha y hora
                            f"{m.temp:.2f}", f"{m.hum:.2f}", f"{m.pres:.2f}"]) 
        self.batch.clear()                   # Limpia el lote en memoria

# Interfaz grafica
class App(tk.Tk):                            # Clase principal de la interfaz
    def __init__(self, buf, lock, stop):     # Recibe el buffer, el candado y el evento de parada
        super().__init__()                   # Inicializa la ventana principal
        self.title("Estación meteo (demo)")  # Título 
        self.geometry("900x520")             # Tamaño inicial
        self.minsize(760, 480)               # Tamaño minimo
        self.buf, self.lock, self.stop = buf, lock, stop  # Guarda referencias

        # Barra superior con etiquetas
        top = ttk.Frame(self)                # Crea un contenedor
        top.pack(fill=tk.X, padx=12, pady=8) # Lo acomoda en la parte superior
        # Crea etiquetas para mostrar lecturas actuales
        self.ltemp = ttk.Label(top, text="Temp: -- °C", font=("Segoe UI", 11, "bold"))
        self.lhum  = ttk.Label(top, text="Hum: -- %", font=("Segoe UI", 11, "bold"))
        self.lpres = ttk.Label(top, text="Pres: -- hPa", font=("Segoe UI", 11, "bold"))
        self.ldesc = ttk.Label(top, text="Desc: …")
        # Las organiza horizontalmente con separación
        for w in (self.ltemp, self.lhum, self.lpres, self.ldesc): 
            w.pack(side=tk.LEFT, padx=(0,12))

        # Graficos
        fig = Figure(figsize=(8,4.2), dpi=100)           # Crea figura de Matplotlib
        self.ax1 = fig.add_subplot(211)                  # Subgrafico (temperatura)
        self.ax2 = fig.add_subplot(212)                  # Subgrafico (humedad)
        self.ax1.set_ylabel("°C")                        # Etiqueta eje Y
        self.ax2.set_ylabel("%")                         # Etiqueta eje Y
        self.ax2.set_xlabel("Tiempo (~5 min)")           # Etiqueta eje X
        self.canvas = FigureCanvasTkAgg(fig, master=self) # Enlaza la figura a Tkinter
        self.canvas.draw()                               # Dibuja inicialmente
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=12, pady=8)  # Muestra grafico

        self.after(200, self.tick)                       # Programa primera actualizacion
        self.protocol("WM_DELETE_WINDOW", self.cerrar)   # Define accion al cerrar la ventana

    def tick(self):                                     # Actualiza interfaz cada segundo
        with self.lock: data = list(self.buf)            # Copia segura del buffer
        if data:                                         # Si hay datos disponibles, toma la ultima medida
            last = data[-1]                            
            # Actualiza las etiquetas con los ultimos valores
            self.ltemp.config(text=f"Temp: {last.temp:.1f} °C")
            self.lhum.config(text=f"Hum:  {last.hum:.1f} %")
            self.lpres.config(text=f"Pres: {last.pres:.1f} hPa")
            self.ldesc.config(text=self.desc(last))      # Actualiza descripcion textual
            # Extrae listas para graficar
            xs = [m.t for m in data]
            t  = [m.temp for m in data]
            h  = [m.hum  for m in data]
            for ax in (self.ax1, self.ax2): ax.cla(); ax.grid(True, alpha=.3) # Limpia y activa cuadrícula
            self.ax1.plot(xs, t)                        # Grafica temperatura
            self.ax1.set_ylabel("°C")
            self.ax2.plot(xs, h)                        # Grafica humedad
            self.ax2.set_ylabel("%")
            self.ax2.set_xlabel("Tiempo (~5 min)")
            self.canvas.draw_idle()                     # Redibuja sin bloquear
        if not self.stop.is_set(): self.after(1000, self.tick)  # Repite cada segundo

    @staticmethod
    def desc(m: Medida) -> str:                         # Genera texto descriptivo simple
        t = "frio" if m.temp < 12 else "templado" if m.temp < 22 else "cálido" if m.temp < 28 else "caluroso"
        h = "seco" if m.hum < 40 else "humedo" if m.hum < 70 else "muy humedo"
        p = "baja" if m.pres < 1005 else "normal" if m.pres < 1020 else "alta"
        return f"Ambiente {t}, {h}, presion {p}."       # Devuelve la descripcion final

    def cerrar(self):                                   # Cierra la aplicación y detiene hilos
        self.stop.set()                                 # Activa el evento de parada
        self.destroy()                                  # Cierra la ventana

# Funcion principal
def main():                                             # Funcion que inicia todo
    stop = threading.Event()                            # Evento para detener los hilos
    lock = threading.Lock()                             # Candado para proteger el buffer
    buf = deque()                                       # Cola doble que guarda las medidas recientes
    q = queue.Queue(maxsize=1000)                       # Cola para comunicacion entre hilos
    HiloAdq(q, buf, lock, stop).start()                 # Inicia el hilo de adquisicion
    HiloLog(q, stop).start()                            # Inicia el hilo de registro
    App(buf, lock, stop).mainloop()                     # Lanza la interfaz grafica
    stop.set()                                          # Cuando se cierra la ventana, detiene los hilos

# Punto de entrada
if __name__ == "__main__":        
    main()                                    
