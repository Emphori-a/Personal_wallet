from transaction import Transaction
from wallet import Wallet


def main() -> None:
    """
    Главная функция для управления личным кошельком.

    Вводит пользователя в интерактивное меню для доступа к функциям кошелька.

    Возвращает:
        None
    """
    print("Добро пожаловать в 'Личный кошелек'!")
    name = input("Введите имя вашего кошелька: ")
    wallet = Wallet(name)

    while True:
        print("Меню:")
        print("1. Вывести баланс")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск по записям")
        print("0. Выход")

        choice = input("Выберите опцию (введите номер пункта меню): ")

        if choice == "1":
            print(wallet.get_balance())
        elif choice == "2":
            date = input("Укажите дату новой записи в формате DD.MM.YYYY: ")
            category = input("Укажите категорию новой записи (Доход/Расход): ")
            amount = input("Укажите сумму: ")
            description = input("Добавьте описание (не длиннее 20 символов): ")
            try:
                new_record = Transaction(date, category, amount, description)
                wallet.add_transaction(new_record)
                print(f"Добавлена запись: {new_record}")
            except ValueError as error:
                print(error)
        elif choice == "3":
            record_id = int(
                input("Укажите идентификатор записи для редактирования: "))
            record = wallet.search_transactions(id=record_id)
            try:
                print(f"Запись для редактирования: {record[0]}")
                new_data = input("Укажите новую дату записи: ")
                new_category = input("Укажите новую категорию записи: ")
                new_amount = input("Укажите новую сумму: ")
                new_description = input("Добавьте новое описание: ")
                try:
                    new_record = Transaction(
                        new_data, new_category, new_amount, new_description)
                    wallet.edit_transaction(record_id, new_record)
                    print("Запись успешно изменена. "
                          f"Новая запись: {new_record}")
                except ValueError as error:
                    print(error)
            except IndexError:
                print("Запись не найдена")
        elif choice == "4":
            search_keys = {
                "id": None,
                "date": None,
                "category": None,
                "amount": None,
            }
            print("Выберите критерий для поиска:")
            print("1. Идентификатор")
            print("2. Дата")
            print("3. Категория")
            print("4. Сумма")
            numb_criteria = input("Введите номер критерия: ")
            if numb_criteria == "1":
                search_keys["id"] = int(
                    input("Укажите идентификатор записи для поиска: "))
            elif numb_criteria == "2":
                search_keys["date"] = input("Укажите дату записи для поиска: ")
            elif numb_criteria == "3":
                search_keys["category"] = input(
                    "Укажите категорию записи для поиска: ")
            elif numb_criteria == "4":
                search_keys["amount"] = float(
                    input("Укажите сумму записи для поиска: "))
            else:
                print("Неверный ввод. Пожалуйста, выберите опцию из меню.")
            try:
                search_result = wallet.search_transactions(**search_keys)
                print(f"Результаты поиска: {search_result}")
            except Exception as error:
                print(error)
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите опцию из меню.")


if __name__ == "__main__":
    main()
