print("Starting ...")

print("import system")
import time, gc, os
import board
import busio
import time

print("import libraries")

import freedomrobotics
import adafruit_bme680
import adafruit_sgp30
import adafruit_tsl2591
import adafruit_scd30
import seeed_mcgasv2
import dfrobot_ozone
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_pm25.i2c import PM25_I2C

#i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
#bno = adafruit_bno08x.BNO08X(i2c)

print("init net")
from net import requests

print("init link")
link = freedomrobotics.NanoLink(requests = requests, auto_sync = False)

print("init i2c")
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
link.log("info", "i2c initialized")
link.sync()

i2c1 = busio.I2C(board.IO17, board.IO18, frequency=100000)
link.log("info", "i2c1 initialized")
link.sync()

print("init bno08x")
bno = None
bno = BNO08X_I2C(i2c)

if bno is not None:
    bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
    bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
    bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
    bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)

link.log("info", "bno08x initialized")
link.sync()

print("init gas")
gas = None
gas = seeed_mcgasv2.Gas(i2c)

link.log("info", "mcgasv2 initialized")
link.sync()

print("init bme680")
bme680 = None
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

link.log("info", "bme680 initialized")
link.sync()

print("init sgp30")
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
if sgp30 is not None:
    print("SGP30 serial #", [hex(i) for i in sgp30.serial])
    sgp30.iaq_init()
    sgp30.set_iaq_baseline(0x8973, 0x8AAE)

link.log("info", "sgp30 initialized")
link.sync()

print("init scd30")
scd30 = None
scd30 = adafruit_scd30.SCD30(i2c)

link.log("info", "scd30 initialized")
link.sync()

print("init ozone")
ozone = None
ozone = dfrobot_ozone.DFRobot_Ozone(i2c)
if ozone is not None:
    ozone.set_mode(dfrobot_ozone.MEASURE_MODE_AUTOMATIC)

link.log("info", "ozone initialized")
link.sync()

print("init pm25")
pm25 = None
pm25 = PM25_I2C(i2c1, None)

link.log("info", "pm25 initialized")
link.sync()

while True:
    t = time.monotonic_ns()

    if pm25 is not None:
        try:
            aqdata_filtered = {}
            aqdata = pm25.read()
            for key in aqdata:
               aqdata_filtered[key.replace(" ", "_")] = aqdata[key]
            link.message("/pmsa003i/raw", "pmsa003i_msgs/RawData", aqdata_filtered)
            link.message("/pmsa003i/pm10_standard", "std_msgs/Float32", {"data": aqdata_filtered["pm10_standard"]})
            link.message("/pmsa003i/pm25_standard", "std_msgs/Float32", {"data": aqdata_filtered["pm25_standard"]})
            link.message("/pmsa003i/pm100_standard", "std_msgs/Float32", {"data": aqdata_filtered["pm100_standard"]})
        except RuntimeError:
            print("error reading pm25 data")

    if sgp30 is not None:
        try:
            link.message("/sgp30/tvoc", "std_msgs/Float32", {"data": sgp30.TVOC})
        except:
            print("error reading sgp30 data")

    if scd30 is not None:
        try:
            if scd30.data_available:
                link.message("/scd30/co2", "std_msgs/Float32", {"data": scd30.eCO2})
                link.message("/scd30/humidity", "std_msgs/Float32", {"data": scd30.relative_humidity})
                link.message("/scd30/temp", "std_msgs/Float32", {"data": scd30.temperature})
        except:
            print("error reading scd30 data")

    if gas is not None:
        try:
            gas_data = gas.measure_all()
            link.message("/mcgasv2/raw", "mcgasv2_msgs/RawData", {"gm102b": gas_data[0], "gm302b": gas_data[1], "gm502b": gas_data[2], "gm702b": gas_data[3]})
        except:
            print("error reading mcgasv2 data")

    if ozone is not None:
        try:
            ozone_ppb = ozone.get_ozone_data(10)
            link.message("/sen0321/ozone", "std_msgs/Float32", {"data": ozone_ppb})
        except:
            print("error reading ozone data")

    if bme680 is not None:
        try:
            link.message("/bme680/pressure", "std_msgs/Float32", {"data": bme680.pressure})
        except:
            print("error reading bme680 data")

    if bno is not None:
        pass
        # do something
        # print("acc", bno.acceleration)
        # print("gyr", bno.gyro)
        # print("mag", bno.magnetic)
        # print("quat", bno.quaternion)

    print("loop time", (time.monotonic_ns() - t)/1.0e6, "ms")

    link.sync()
    time.sleep(2)


