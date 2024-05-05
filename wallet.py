import json
from typing import Dict, List, Union
from transaction import Transaction


class Wallet:
    """
    Класс, представляющий файловый менеджер кошелька.

    Атрибуты:
        filename (str): Имя файла данных кошелька.

    Методы:
        create_data_file: Создает файл данных, если он не существует.
        get_next_record_id: Возвращает следующий доступный идентификатор.
        add_transaction: Добавляет новую транзакцию в файл данных.
        read_data: Считывает данные из файла и возвращает список словарей.
        get_balance: Рассчитывает текущий баланс и возвращает его.
        edit_transaction: Редактирует запись с указанным идентификатором.
        search_transactions: Выполняет поиск транзакций по заданным критериям.
    """

    def __init__(self, name: str):
        self.filename = f"{name}_data.json"
        self.create_data_file()

    def create_data_file(self) -> None:
        """
        Создает файл данных, если его не существует.
        """
        try:
            with open(self.filename, "x", encoding="utf-8") as file:
                json.dump([], file)
        except FileExistsError:
            pass

    def get_next_record_id(self) -> int:
        """
        Возвращает следующий доступный идентификатор записи.
        """
        data = self.read_data()
        existing_ids = {int(record["Идентификатор"]) for record in data}
        if existing_ids:
            next_id = max(existing_ids) + 1
        else:
            next_id = 1
        return next_id

    def add_transaction(self, record: Transaction) -> None:
        """
        Добавляет новую транзакцию в файл данных.
        """
        with open(self.filename, "r+", encoding="utf-8") as file:
            data = json.load(file)
            id_counter = self.get_next_record_id()
            record_dict = {
                "Идентификатор": id_counter,
                "Дата": record.date,
                "Категория": record.category,
                "Сумма": record.amount,
                "Описание": record.description
            }
            data.append(record_dict)
            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)

    def read_data(self) -> List[Dict[str, Union[int, str, float]]]:
        """
        Считывает данные из файла и возвращает список словарей.
        """
        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_balance(self) -> str:
        """
        Рассчитывает текущий баланс и возвращает его.
        """
        data = self.read_data()
        total_income = sum(record["Сумма"] for record in data
                           if record["Категория"] == "Доход")
        total_expense = sum(record["Сумма"] for record in data
                            if record["Категория"] == "Расход")
        balance = total_income - total_expense
        return (f"Баланс: {balance}\n"
                f"Общий доход: {total_income}\n"
                f"Общий расход: {total_expense}\n")

    def edit_transaction(self, record_id: int, new_data: Transaction) -> None:
        """
        Редактирует существующую запись с указанным идентификатором.

        Параметры:
            record_id (int): Идентификатор записи для редактирования.
            new_data (Transaction): Новые данные для записи.

        Исключения:
            ValueError: Если указанный идентификатор не найден.
        """
        data = self.read_data()
        for record in data:
            if record["Идентификатор"] == record_id:
                record["Дата"] = new_data.date
                record["Категория"] = new_data.category
                record["Сумма"] = new_data.amount
                record["Описание"] = new_data.description
                break

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def search_transactions(self, **kwargs: Union[int, str, float]
                            ) -> List[Dict[str, Union[int, str, float]]]:
        """
        Выполняет поиск транзакций по заданным критериям.

        Параметры:
            **kwargs: Ключевые аргументы для критериев поиска.
                Возможные ключи: Идентификатор, Дата, Категория, Сумма.

        Возвращает:
            List[Dict[str, Union[int, str, float]]]: Список словарей,
            содержащих данные найденных транзакций.
        """
        data = self.read_data()
        results = []
        search_keys = {
            "id": "Идентификатор",
            "date": "Дата",
            "category": "Категория",
            "amount": "Сумма",
        }

        for record in data:
            match = True
            for key, value in kwargs.items():
                if value is not None:
                    if record.get(search_keys.get(key)) != value:
                        match = False
                        break
            if match:
                results.append(record)

        return results
