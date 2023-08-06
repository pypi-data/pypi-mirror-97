from datetime import date, datetime
from enum import Enum

from .origin import Origin


class CashFlowType(Enum):
    DEBIT = 1
    CREDIT = 2


class CashFlow:

    def __init__(self,
                 name: str = 'N/A',
                 flow_type: CashFlowType = CashFlowType.DEBIT,
                 value: [float, str] = 0.0,
                 accrual_date: [date, datetime, str] = None,
                 cash_date: [date, datetime, str] = None,
                 origin: Origin = None):
        self.name = name
        self.flowType = flow_type
        self.value = value
        self.date = accrual_date
        self.cash_date = cash_date
        self.origin = origin

    @property
    def cash_date(self):
        return self.__cash_date

    @cash_date.setter
    def cash_date(self, value):
        self.__cash_date = self.__convert_date(value)

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = self.__convert_date(value)

    @staticmethod
    def __convert_date(value):
        if isinstance(value, datetime):
            return value.date()
        elif isinstance(value, date):
            return value
        elif isinstance(value, str):
            if value == 'N/A':
                return None
            try:
                return datetime.fromisoformat(value).date()
            except ValueError:
                return datetime.strptime(value, '%d/%m/%Y').date()
        else:
            return None

    @staticmethod
    def __is_valid_value(value):
        if value is None or value == 'nan':
            return False
        else:
            try:
                float(value)
                return True
            except ValueError:
                return False

    def __valid_dates(self):
        return self.cash_date and self.date and self.cash_date >= self.date

    def is_blank(self):
        return (
            self.name == "N/A" and
            self.flowType == CashFlowType.DEBIT and
            self.value == 0.0 and
            self.date is None and
            self.cash_date is None and
            self.origin is None
        )

    def is_valid(self):
        return (self.__is_valid_value(self.value) and self.__valid_dates() and
                isinstance(self.flowType, CashFlowType) and
                isinstance(self.origin, Origin) and
                type(self.name) == str)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name.strip() == other.name.strip() and
                self.value == other.value and self.date == other.date and
                self.cash_date == other.cash_date and
                self.origin == other.origin)

    def __repr__(self):
        return f'CashFlow: \
                \n\tName: {self.name} \
                \n\tType: {self.flowType.name} \
                \n\tValue: {self.value} \
                \n\tDate: {self.date} \
                \n\tCash date: {self.cash_date} \
                \n\tOrigin: {self.origin}'
