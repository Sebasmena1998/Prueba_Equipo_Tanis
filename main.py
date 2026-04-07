import time
import random
from collections import deque, defaultdict

# Límite por sensor (restricción RAM)
MAX_SIZE = 100

# Estructura por sensor (dinámica y escalable)
RAW_DATA_STORAGE = defaultdict(lambda: deque(maxlen=MAX_SIZE))

# Métricas O(1) por sensor
RUNNING_SUM = defaultdict(float)
COUNT = defaultdict(int)

def process_and_save(sensor_id, value):
    """
    Procesa y guarda datos de sensores con validación, manejo de excepciones
    y cálculo de promedio en O(1).
    """
    global RAW_DATA_STORAGE, RUNNING_SUM, COUNT

    try:
        # Validaciones
        if not isinstance(sensor_id, str):
            raise TypeError(f"sensor_id debe ser string, recibido: {type(sensor_id).__name__}")
        
        if value is None:
            raise ValueError("El valor del sensor no puede ser None")
        
        if not isinstance(value, (int, float)):
            raise TypeError(f"value debe ser numérico (int/float), recibido: {type(value).__name__}")
        
        if isinstance(value, float):
            if value != value:  # NaN
                raise ValueError("El valor no puede ser NaN")
            if value == float('inf') or value == float('-inf'):
                raise ValueError("El valor no puede ser infinito")

        timestamp = time.time()
        entry = {"id": sensor_id, "val": value, "ts": timestamp}

        sensor_queue = RAW_DATA_STORAGE[sensor_id]

        # Ajuste si se va a eliminar un elemento (por límite)
        if len(sensor_queue) == MAX_SIZE:
            removed = sensor_queue[0]
            try:
                RUNNING_SUM[sensor_id] -= removed["val"]
                COUNT[sensor_id] -= 1
            except (KeyError, TypeError):
                pass

        # Insertar nuevo dato
        sensor_queue.append(entry)

        RUNNING_SUM[sensor_id] += value
        COUNT[sensor_id] += 1

        # Promedio en O(1)
        if COUNT[sensor_id] > 0:
            avg = RUNNING_SUM[sensor_id] / COUNT[sensor_id]
            print(f"Sensor {sensor_id} - Promedio Actual: {avg:.2f}")
        else:
            print(f"Sensor {sensor_id} - Sin datos válidos para calcular promedio")

    except TypeError as e:
        print(f"❌ ERROR de tipo en sensor {sensor_id}: {e}")
    except ValueError as e:
        print(f"❌ ERROR de valor en sensor {sensor_id}: {e}")
    except Exception as e:
        print(f"❌ ERROR inesperado en sensor {sensor_id}: {e}")

def main_loop():
    """
    Bucle principal que simula lectura de sensores con manejo de errores.
    """
    sensors = ["TORQUE", "RPM", "PUMP_PRES"]
    
    try:
        while True:
            for s in sensors:
                try:
                    val = random.choice([100.5, 200.8, None, 150.2])
                    process_and_save(s, val)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"⚠️  Error procesando sensor {s}: {e}")
                    continue
    except KeyboardInterrupt:
        print("\n✅ Programa interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico en main_loop: {e}")

if __name__ == "__main__":
    main_loop()