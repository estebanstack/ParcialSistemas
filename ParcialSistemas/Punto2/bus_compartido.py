import multiprocessing as mp
import time
import random
import os
from datetime import datetime

# Funcion que muestra mensajes con formato de bitacora
def log(dispositivo_id, mensaje):
    ahora = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ahora}] [PID {os.getpid():>6}] [Disp {dispositivo_id:02}] {mensaje}", flush=True)

# Funcion que ejecuta cada proceso
def usar_bus(dispositivo_id: int, semaforo: mp.Semaphore):

    # Simula que cada dispositivo llega en momentos distintos
    time.sleep(random.uniform(0.0, 1.0))

    log(dispositivo_id, "Intentando acceder al bus (adquiriendo semaforo)...")

    # Verificar si el semáforo está disponible (espera si está ocupado)
    semaforo_acceso = semaforo.acquire(block=False)  # Non-blocking acquire

    if semaforo_acceso:
        try:
            log(dispositivo_id, "ACCESO CONCEDIDO: utilizando el bus")

            tiempo_uso = 1.0
            intervalos = 4

            # Bucle que simula el progreso del uso del bus
            for i in range(intervalos):
                time.sleep(tiempo_uso / intervalos)   # Espera 1 segundo entre cada mensaje
                log(dispositivo_id, f"Transfiriendo datos... ({(i+1)*(tiempo_uso/intervalos):.2f}s)")

            # Una vez completada la transferencia, se informa el tiempo total
            log(dispositivo_id, f"Transferencia finalizada. Tiempo total de uso: {tiempo_uso:.2f}s")

        finally:
            # Siempre se ejecuta, incluso si ocurre un error: libera el semáforo
            log(dispositivo_id, "Liberando el bus (liberando semáforo).")
            semaforo.release()  # Libera el semáforo para que otro proceso pueda usarlo
    else:
        # Si no pudo adquirir el semáforo, se indica que el bus ya está siendo utilizado
        log(dispositivo_id, "NO ACCESADO: El bus ya está ocupado, esperando turno...")

# Funcion crea e inicia los procesos
def main():
    NUM_DISPOSITIVOS = 6

    print("\nSimulacion de Bus Compartido con Semaforo\n", flush=True)
    print(f"Dispositivos: {NUM_DISPOSITIVOS} | Cada uno usa el bus por 1 segundo\n", flush=True)

    # Crea un semáforo binario
    # Solo un proceso a la vez puede acceder al bus
    semaforo_bus = mp.Semaphore(1)

    # Lista para guardar los procesos creados
    procesos = []

    # Crea los procesos, cada uno representa un dispositivo independiente
    for disp_id in range(1, NUM_DISPOSITIVOS + 1):
        p = mp.Process(                       # Crea un nuevo proceso
            target=usar_bus,                  # Funcion que ejecuta el proceso
            args=(disp_id, semaforo_bus),     # Argumentos que se pasan a la funcion
            name=f"Dispositivo-{disp_id}"     
        )
        procesos.append(p)                    # Agrega el proceso a la lista

    # Inicia todos los procesos creados
    for p in procesos:
        p.start()

    # Espera a que todos los procesos terminen
    for p in procesos:
        p.join()

    print("\nSimulación finalizada: acceso concurrente controlado y ordenado.\n", flush=True)


if __name__ == "__main__":
    # Establece el metodo de inicio de procesos 
    mp.set_start_method("spawn", force=True)
    main()
