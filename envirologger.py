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

while True:
 results = {
  "temp": bme280.get_temperature(),
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
