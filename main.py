import time
import random
from collections import deque

# Límite máximo de registros en memoria
MAX_SIZE = 1000

# Estructura eficiente con tamaño limitado
RAW_DATA_STORAGE = deque(maxlen=MAX_SIZE)

def process_and_save(sensor_id, value):
    """
    Procesa y guarda datos de sensores con validación y manejo de excepciones.
    
    Args:
        sensor_id (str): Identificador del sensor
        value (float): Valor del sensor
        
    Raises:
        TypeError: Si el tipo de dato es incorrecto
        ValueError: Si el valor es None o inválido
    """
    global RAW_DATA_STORAGE

    try:
        # Validar que sensor_id sea string
        if not isinstance(sensor_id, str):
            raise TypeError(f"sensor_id debe ser string, recibido: {type(sensor_id).__name__}")
        
        # Validar que value no sea None
        if value is None:
            raise ValueError("El valor del sensor no puede ser None")
        
        # Validar que value sea numérico
        if not isinstance(value, (int, float)):
            raise TypeError(f"value debe ser numérico (int/float), recibido: {type(value).__name__}")
        
        # Validar que no sea NaN o infinito
        if isinstance(value, float):
            if value != value:  # NaN check
                raise ValueError("El valor no puede ser NaN")
            if value == float('inf') or value == float('-inf'):
                raise ValueError("El valor no puede ser infinito")
        
        timestamp = time.time()
        entry = {"id": sensor_id, "val": value, "ts": timestamp}
        RAW_DATA_STORAGE.append(entry)
        
        # Calcular promedio solo con valores válidos
        total = 0
        count = 0
        for item in RAW_DATA_STORAGE:
            try:
                if isinstance(item["val"], (int, float)) and item["val"] is not None:
                    total += item["val"]
                    count += 1
            except (KeyError, TypeError):
                continue
        
        if count > 0:
            avg = total / count
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
                    # Generar valor aleatorio (incluye None para pruebas de excepciones)
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