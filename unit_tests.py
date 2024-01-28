import unittest
from models import *


class TestSensors(unittest.TestCase):

    def test_can_read_data(self):
        for sensor_type in [TemperatureSensor, AirHumiditySensor, SoilHumiditySensor]:
            sensor = sensor_type()

            self.assertEqual(sensor.sensor_value, sensor.read_data())

    def test_can_limit_value_min(self):
        for sensor_type in [TemperatureSensor, AirHumiditySensor, SoilHumiditySensor]:
            sensor = sensor_type()

            sensor.sensor_value = -1000

            sensor.limit_value()
            self.assertEqual(sensor.sensor_value, sensor.MIN)

    def test_can_limit_value_max(self):
        for sensor_type in [TemperatureSensor, AirHumiditySensor, SoilHumiditySensor]:
            sensor = sensor_type()

            sensor.sensor_value = 1000

            sensor.limit_value()
            self.assertEqual(sensor.sensor_value, sensor.MAX)

    def test_change_external(self):
        for sensor_type in [TemperatureSensor, AirHumiditySensor, SoilHumiditySensor]:
            sensor = sensor_type()
            sensor.sensor_value = 30
            self.assertEqual(sensor.sensor_value, 30)

            sensor.change(5)
            self.assertEqual(sensor.sensor_value, 30 + 5)


class TestTools(unittest.TestCase):

    def test_activate(self):
        for tool_type in [Heater, Humidifier, Watering, Cooling]:
            tool = tool_type()
            tool.activate()

            self.assertTrue(tool.state)

    def test_deactivate(self):
        for tool_type in [Heater, Humidifier, Watering, Cooling]:
            tool = tool_type()
            tool.deactivate()

            self.assertFalse(tool.state)

    def test_process(self):
        for tool_type in [Heater, Humidifier, Watering]:
            tool = tool_type()

            change = tool.process(tool.MIN - 10)
            self.assertTrue(tool.state)
            self.assertEqual(change, tool.CHANGE)

    def test_process_cooling(self):
        cooling = Cooling()

        change = cooling.process(cooling.MAX + 10)
        self.assertTrue(cooling.state)
        self.assertEqual(change, cooling.CHANGE)


if __name__ == '__main__':
    unittest.main()
