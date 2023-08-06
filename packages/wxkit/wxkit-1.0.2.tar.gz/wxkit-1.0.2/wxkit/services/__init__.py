from abc import ABC, abstractmethod


class WeatherService(ABC):
    def __init__(self, credential):
        self.credential = credential

    @abstractmethod
    def get_current_weather_by_location(self, location):
        pass

    @abstractmethod
    def get_forecast_weather_by_location(self, location, period):
        pass

    @abstractmethod
    def handle_error(self, exception):
        pass
