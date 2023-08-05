
from abc import ABCMeta, abstractmethod


class CalculatorStore(metaclass=ABCMeta):

    @abstractmethod
    def insert_computed_notification(self):
        pass

    @abstractmethod
    def fetch_computed_notification_before_date(self):
        pass