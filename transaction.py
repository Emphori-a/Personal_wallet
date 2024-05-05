from datetime import datetime


class Transaction:
    """
    Класс, представляющий транзакцию.

    Атрибуты:
        date (str): Дата транзакции в формате 'DD.MM.YYYY'.
        category (str): Категория транзакции ('Доход' или 'Расход').
        amount (float): Сумма транзакции.
        description (str): Описание транзакции.

    Исключения:
        ValueError: Возникает, если данные транзакции не проходят валидацию.

    Методы:
        validate_date: Проверяет корректность формата даты и то,
            что дата не больше текущей.
        validate_category: Проверяет корректность категории транзакции.
        validate_amount: Проверяет корректность суммы транзакции.
        validate_description: Проверяет корректность описания транзакции.
        __str__: Возвращает строковое представление объекта транзакции.
    """

    def __init__(self, date: str, category: str,
                 amount: float, description: str):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, date: str) -> None:
        if not self.validate_date(date):
            raise ValueError("Неверная дата: дата не может быть больше текущей"
                             ", дата вводится в формате DD.MM.YYYY")
        self.__date = date

    def validate_date(self, date: str) -> bool:
        """
        Проверяет корректность формата даты и то, что дата не больше текущей.

        Параметры:
            date (str): Строка с датой в формате "DD.MM.YYYY".

        Возвращает:
            bool: True, если дата корректна и не больше текущей, иначе False.
        """

        try:
            parsed_date = datetime.strptime(date, "%d.%m.%Y")
            return parsed_date <= datetime.now()
        except ValueError:
            return False

    @property
    def category(self) -> str:
        return self.__category

    @category.setter
    def category(self, category: str) -> None:
        if not self.validate_category(category):
            raise ValueError("Неверная категория. Допустимые значения: "
                             "'Доход', 'Расход'")
        self.__category = category.capitalize()

    def validate_category(self, category: str) -> bool:
        """
        Проверяет корректность категории.

        Параметры:
            category (str): Строка с категорией транзакции.

        Возвращает:
            bool: True, если категория корректна, иначе False.
        """
        return category.lower() in ["доход", "расход"]

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, amount: str) -> None:
        if not self.validate_amount(amount):
            raise ValueError("Сумма должна быть положительным числом.")
        self.__amount = float(amount)

    def validate_amount(self, amount: str) -> bool:
        """
        Проверяет корректность суммы.

        Параметры:
            amount (str): Строка с суммой транзакции.

        Возвращает:
            bool: True, если сумма корректна, иначе False.
        """
        try:
            amount = float(amount)
            return amount > 0
        except ValueError:
            return False

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        if not self.validate_description(description):
            raise ValueError("Описание не может быть длиннее 20 символов")
        self.__description = description

    def validate_description(self, description: str) -> bool:
        """
        Проверяет корректность описания.

        Параметры:
            description (str): Строка с описанием транзакции.

        Возвращает:
            bool: True, если описание корректно, иначе False.
        """
        return len(description) <= 20

    def __str__(self) -> str:
        return (f"Дата: {self.date}\n"
                f"Категория: {self.category}\n"
                f"Сумма: {self.amount}\n"
                f"Описание: {self.description}")
