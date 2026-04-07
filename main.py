import time
import random

RAW_DATA_STORAGE = []
def process_and_save ( sensor_id , value ):
global RAW_DATA_STORAGE
timestamp = time . time ()
entry = {"id": sensor_id , "val": value , "ts":
timestamp }
RAW_DATA_STORAGE . append ( entry )
RAW_DATA_STORAGE . append ( entry )
total = 0
for item in RAW_DATA_STORAGE :
total += item ["val"]
avg = total / len( RAW_DATA_STORAGE )
print (f" Sensor ␣{ sensor_id }␣-␣ Promedio ␣ Actual :␣{
avg}")
def main_loop ():
sensors = [" TORQUE ", "RPM ", " PUMP_PRES "]
while True :
for s in sensors :
val = random . choice ([100.5 , 200.8 , None , 150.2])
process_and_save (s, val )
time . sleep (0.1)
if __name__ == " __main__ ":
main_loop ()