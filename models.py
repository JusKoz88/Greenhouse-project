import random
import time


class Sensor:
    MIN = 0
    MAX = 100
    TYPE = ''

    def __init__(self):
        self.sensor_value = random.randint(self.MIN, self.MAX)

    def read_data(self):
        return self.sensor_value

    def limit_value(self):
        # nie pozwol wyjsc poza gorna/dolna granice

        if self.sensor_value < self.MIN:
            self.sensor_value = self.MIN
        elif self.sensor_value > self.MAX:
            self.sensor_value = self.MAX

    def change(self, tool_change):
        # zmien na podstawie dzialania urzadzenia lub losowa zmiana

        if tool_change:
            self.sensor_value = self.sensor_value + tool_change
            print(f'External change {self.TYPE} by {tool_change}')
        else:
            change = random.randint(-5, 5)
            self.sensor_value = self.sensor_value + change
            print(f'Random change {self.TYPE} by {change}')

        self.limit_value()


class TemperatureSensor(Sensor):
    MIN = -30
    MAX = 100
    TYPE = 'temperature'

class AirHumiditySensor(Sensor):
    MIN = 10
    MAX = 100
    TYPE = 'air humidity'

class SoilHumiditySensor(Sensor):
    MIN = 20
    MAX = 40
    TYPE = 'soil humidity'


class Tools:
    MIN = 0
    MAX = 100
    TYPE = ''
    CHANGE = 0

    def __init__(self):
        self.state = False
        self.sensor_value = 0

    def change(self):
        # jesli urzadzenie jest aktywne to dokonaj zmiany

        if self.state:
            return self.CHANGE
        else:
            return 0

    def activate(self):
        self.state = True

    def deactivate(self):
        self.state = False

    def process(self, sensor_value):
        # wlacz lub wylacz urzadzenie na podstawie reguly
        # wypisz stan urzadzenia
        # a nastepnie dokonaj zmiany

        self.sensor_value = sensor_value
        if self.sensor_value < self.MIN:
            self.activate()
        else:
            self.deactivate()

        self.get_state()

        return self.change()

    def get_state(self):
        # wypisuje stan urzadzenia
        print(f'Tool {self.TYPE}: {self.state}')


class Heater(Tools):
    MIN = 10
    TYPE = 'heater'
    CHANGE = 5


class Humidifier(Tools):
    MIN = 30
    TYPE = 'humidifier'
    CHANGE = 3


class Watering(Tools):
    MIN = 25
    TYPE = 'watering'
    CHANGE = 2


class Cooling(Tools):
    MAX = 40
    TYPE = 'cooling'
    CHANGE = 2

    def process(self, sensor_value):
        # chlodzenie dziala na odwrot niz inne urzadzenia

        self.sensor_value = sensor_value
        if self.sensor_value > self.MAX:
            self.activate()
        else:
            self.deactivate()

        self.get_state()

        return self.change()


class Greenhouse:

    def __init__(self):
        # inicjalizacja miernikow
        self.temperature_sensor = TemperatureSensor()
        self.humidity_sensor = AirHumiditySensor()
        self.soil_sensor = SoilHumiditySensor()

        # inicjalizacja urzadzen
        self.heater = Heater()
        self.humidifier = Humidifier()
        self.watering = Watering()
        self.cooling = Cooling()

        # wartosci bazowe
        self.temperature = 0
        self.soil = 0
        self.humidity = 0


    def read_state(self):
        # zaczytujemy dane z miernikow
        self.temperature = self.temperature_sensor.read_data()
        self.humidity = self.humidity_sensor.read_data()
        self.soil = self.soil_sensor.read_data()

        print()
        print('=' * 20)
        print(f'Temperature: {self.temperature}')
        print(f'Humidity: {self.humidity}')
        print(f'Soil: {self.soil}')
        print('=' * 20)

    def check_state(self):
        # prosimy urzadzenia o dzialanie w zaleznosci od stanu z miernikow

        print()
        print('-' * 20)

        temperature_change = self.heater.process(self.temperature)
        humidity_change = self.humidifier.process(self.humidity)
        soil_change = self.watering.process(self.soil)

        if temperature_change == 0:
            temperature_change = self.cooling.process(self.temperature)

        print('-' * 20)

        return temperature_change, humidity_change, soil_change

    def update_sensors(self, temperature_change, humidity_change, soil_change):
        # aktualizujemy dane miernikow na bazie tego co zwrocilo urzadzenie

        print()
        print('.' * 20)
        self.temperature_sensor.change(temperature_change)
        self.humidity_sensor.change(humidity_change)
        self.soil_sensor.change(soil_change)
        print('.' * 20)

    def run(self):
        temperature_change = 0
        humidity_change = 0
        soil_change = 0

        runs = 0

        while runs < 10:
            # aktualizuje sensory po zmianie, jesli brak zmiany to robi losowa zmiane z otoczenia
            self.update_sensors(temperature_change, humidity_change, soil_change)

            # odczyt stanu
            self.read_state()

            # akcje urzadzen
            temperature_change, humidity_change, soil_change = self.check_state()

            # spij
            time.sleep(5)

            runs = runs + 1
