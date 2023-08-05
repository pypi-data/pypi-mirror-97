import adafruit_dht
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from baseutils_phornee import ManagedClass
from datetime import datetime

class Sensors(ManagedClass):

    def __init__(self):
        super().__init__(execpath=__file__)

        token = self.config['influxdbconn']['token']
        self.org = self.config['influxdbconn']['org']
        self.bucket = self.config['influxdbconn']['bucket']

        self.conn = InfluxDBClient(url=self.config['influxdbconn']['url'], token=token)

    @classmethod
    def getClassName(cls):
        return "sensors"

    def sensorRead(self):
        """
        Read sensors information
        """
        try:
            dhtSensor = adafruit_dht.DHT22(self.config['pin'])

            humidity = dhtSensor.humidity
            temp_c = dhtSensor.temperature

            if temp_c:
                write_api = self.conn.write_api(write_options=SYNCHRONOUS)

                point = Point('DHT22') \
                    .tag('sensorid', self.config['id']) \
                    .field('temp', temp_c) \
                    .field('humidity', humidity) \
                    .time(datetime.utcnow(), WritePrecision.NS)

                write_api.write(self.bucket, self.org, point)
                # print(SENSOR_LOCATION_NAME + " Temperature(C) {}".format(temp_c))
                # print(SENSOR_LOCATION_NAME + " Humidity(%) {}".format(humidity,".2f"))

        except Exception as e:
            self.logger.error("RuntimeError: {}".format(e))


if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensorRead()





