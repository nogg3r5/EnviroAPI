#!/usr/bin/env python3
import time
import sqlite3
import schedule
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

def scheduledJob():
  sqliteConnection = sqlite3.connect('/home/pi/database/enviro.db')
  cursor = sqliteConnection.cursor()
  cursor.execute("INSERT INTO enviro (temp,pressure,humidity,light,nh3,oxidising,reducing) values(?, ?, ?, ?, ? ,? ,?)", (results['temp'],results['press'],results['humid'],results['light'],results['nh3'],results['oxidising'],results['reducing']))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()

schedule.every(5).minutes.do(scheduledJob)

while True:
 temp = bme280.get_temperature() - 12
 humidity = bme280.get_humidity() + 20
 results = {
  "temp": temp,
  "humid": humidity,
  "press": bme280.get_pressure(),
  "light": ltr559.get_lux(),
  "nh3": gas.read_nh3(),
  "oxidising": gas.read_oxidising(),
  "reducing": gas.read_reducing()
 }
 schedule.run_pending()
 time.sleep(1)
