import time
import random
from collections import deque

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
MAX_SIZE = 100
SENSORS = ["TORQUE", "RPM", "PUMP_PRES"]
SLEEP_TIME = 0.1


# ============================================================================
# MÓDULO 1: ALMACENAMIENTO (Storage)
# ============================================================================
class DataStorage:
    
    def __init__(self, max_size=MAX_SIZE):
        self.storage = deque(maxlen=max_size)
    
    def add_entry(self, entry):
        self.storage.append(entry)
    
    def get_all(self):
        return list(self.storage)
    
    def get_size(self):
        return len(self.storage)
    
    def clear(self):
        self.storage.clear()


# ============================================================================
# MÓDULO 2: ADQUISICIÓN (Acquisition)
# ============================================================================
class DataAcquisition:
    """Simula la lectura de sensores y adquiere datos."""
    
    def __init__(self, sensors):
        self.sensors = sensors
    
    def acquire_sensor_data(self, sensor_id):

        try:
            # Simular lectura (incluye None para pruebas)
            value = random.choice([100.5, 200.8, None, 150.2])
            return {"sensor_id": sensor_id, "value": value}
        except Exception as e:
            print(f"Error en adquisición de sensor {sensor_id}: {e}")
            return None
    
    def acquire_all_sensors(self):
        """
        Lee datos de todos los sensores disponibles.
        
        Returns:
            list: Lista de diccionarios con datos de sensores
        """
        data = []
        for sensor in self.sensors:
            sensor_data = self.acquire_sensor_data(sensor)
            if sensor_data:
                data.append(sensor_data)
        return data


# ============================================================================
# MÓDULO 3: PROCESAMIENTO (Processing)
# ============================================================================
class DataProcessor:
    """Procesa, valida y analiza los datos de sensores."""
    
    @staticmethod
    def validate_data(sensor_id, value):
        # Validar sensor_id
        if not isinstance(sensor_id, str):
            raise TypeError(f"sensor_id debe ser string, recibido: {type(sensor_id).__name__}")
        
        # Validar None
        if value is None:
            raise ValueError("El valor del sensor no puede ser None")
        
        # Validar tipo numérico
        if not isinstance(value, (int, float)):
            raise TypeError(f"value debe ser numérico, recibido: {type(value).__name__}")
        
        # Validar NaN e infinito
        if isinstance(value, float):
            if value != value:  # NaN check
                raise ValueError("El valor no puede ser NaN")
            if value == float('inf') or value == float('-inf'):
                raise ValueError("El valor no puede ser infinito")
    
    @staticmethod
    def create_entry(sensor_id, value):
        DataProcessor.validate_data(sensor_id, value)
        return {
            "id": sensor_id,
            "val": value,
            "ts": time.time()
        }
    
    @staticmethod
    def calculate_average(storage):
        data = storage.get_all()
        total = 0
        count = 0
        
        for item in data:
            try:
                if isinstance(item["val"], (int, float)) and item["val"] is not None:
                    total += item["val"]
                    count += 1
            except (KeyError, TypeError):
                continue
        
        if count > 0:
            avg = total / count
            return {"average": avg, "count": count}
        else:
            return {"average": None, "count": 0}


# ============================================================================
# PIPELINE: INTEGRACIÓN DE MÓDULOS
# ============================================================================
def process_and_save(storage, processor, acquisition, sensor_id, value):
    """
    Pipeline integrado: Adquisición → Procesamiento → Almacenamiento.
    
    Args:
        storage (DataStorage): Módulo de almacenamiento
        processor (DataProcessor): Módulo de procesamiento
        acquisition (DataAcquisition): Módulo de adquisición
        sensor_id (str): Identificador del sensor
        value: Valor del sensor
    """
    try:
        # 1. PROCESAMIENTO: Validar y crear entrada
        entry = processor.create_entry(sensor_id, value)
        
        # 2. ALMACENAMIENTO: Guardar entrada
        storage.add_entry(entry)
        
        # 3. ANÁLISIS: Calcular estadísticas
        stats = processor.calculate_average(storage)
        
        if stats["average"] is not None:
            print(f"Sensor {sensor_id} - Promedio: {stats['average']:.2f} (n={stats['count']})")
        else:
            print(f"Sensor {sensor_id} - Sin datos válidos")
    
    except TypeError as e:
        print(f"ERROR de tipo en sensor {sensor_id}: {e}")
    except ValueError as e:
        print(f"ERROR de valor en sensor {sensor_id}: {e}")
    except Exception as e:
        print(f"ERROR inesperado en sensor {sensor_id}: {e}")


# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================
def main_loop():
    """Bucle principal que orquesta los módulos."""
    
    # Instanciar módulos
    storage = DataStorage(MAX_SIZE)
    acquisition = DataAcquisition(SENSORS)
    processor = DataProcessor()
    
    print(f"Iniciando monitoreo de {len(SENSORS)} sensores...\n")
    
    try:
        while True:
            # Adquirir datos de todos los sensores
            sensor_data = acquisition.acquire_all_sensors()
            
            # Procesar y guardar cada sensor
            for data in sensor_data:
                if data:
                    process_and_save(
                        storage,
                        processor,
                        acquisition,
                        data["sensor_id"],
                        data["value"]
                    )
            
            # Mostrar estado del almacenamiento
            print(f"Almacenamiento: {storage.get_size()}/{MAX_SIZE} registros\n")
            
            time.sleep(SLEEP_TIME)
    
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
        print(f"Total de registros procesados: {storage.get_size()}")
    except Exception as e:
        print(f"Error crítico en main_loop: {e}")


if __name__ == "__main__":
    main_loop()