#!/usr/bin/env python3
import time
import sqlite3
from enviroplus import gas
from bme280 import BME280
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559


bme280 = BME280()

gas.enable_adc()
gas.set_adc_gain(4.096)
t1 = time.time()
wait = 360

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

cpu_temps = [get_cpu_temperature()] * 5

#  "temp": bme280.get_temperature(),

while True:
 cpu_temp = get_cpu_temperature()
 # Smooth out with some averaging to decrease jitter
 cpu_temps = cpu_temps[1:] + [cpu_temp]
 avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
 raw_temp = bme280.get_temperature()
 comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
 results = {
  "temp": comp_temp,
  "humid": bme280.get_humidity(),
  "press": bme280.get_pressure(),
  "light": ltr559.get_lux(),
  "nh3": gas.read_nh3(),
  "oxidising": gas.read_oxidising(),
  "reducing": gas.read_reducing()
 }
 t2 = time.time() - t1
 mod = t2%t1
 if mod >= wait:
  print(results)
  sqliteConnection = sqlite3.connect('/home/pi/database/enviro.db')
  cursor = sqliteConnection.cursor()
  cursor.execute("INSERT INTO enviro (temp,pressure,humidity,light,nh3,oxidising,reducing) values(?, ?, ?, ?, ? ,? ,?)", (results['temp'],results['press'],results['humid'],results['light'],results['nh3'],results['oxidising'],results['reducing']))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()
  t1 = time.time()
