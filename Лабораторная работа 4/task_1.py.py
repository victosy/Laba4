if __name__ == "__main__":
    class BankAccount:
        """
        Базовый класс, представляющий стандартный банковский счет.
        Атрибуты:
            owner (str): Имя владельца счета.
            account_number (str): Уникальный номер счета.
            _balance (float): Текущий баланс счета.
                              Сделан защищенным (protected), чтобы предотвратить
                              прямое изменение извне и обеспечить контроль через методы.
        """
        def __init__(self, owner: str, account_number: str, initial_balance: float = 0.0) -> None:
            """
            Инициализация банковского счета.
            :param owner: Имя владельца счета.
            :param account_number: Номер счета в формате строки.
            :param initial_balance: Начальный баланс (по умолчанию 0.0).
            """
            self.owner = owner
            self.account_number = account_number
            # Инкапсуляция: атрибут _balance защищен, чтобы изменить его можно было
            # только через методы deposit/withdraw, где есть валидация.
            self._balance = initial_balance

        def __str__(self) -> str:
            """
            Возвращает строковое представление счета для пользователя.
            :return: Строка с информацией о владельце и номере счета.
            """
            return f"Счет {self.account_number} принадлежит {self.owner}"

        def __repr__(self) -> str:
            """
            Возвращает официальное строковое представление объекта (для отладки).
            :return: Строка, позволяющая воссоздать объект.
            """
            return f"BankAccount(owner='{self.owner}', account_number='{self.account_number}', balance={self._balance})"

        def deposit(self, amount: float) -> bool:
            """
            Пополнение счета.
            Метод будет унаследован дочерним классом без изменений.
            :param amount: Сумма для пополнения.
            :return: True если операция успешна, иначе False.
            """
            if amount > 0:
                self._balance += amount
                return True
            return False

        def withdraw(self, amount: float) -> bool:
            """
            Снятие средств со счета.
            Метод будет перегружен в дочернем классе.
            :param amount: Сумма для снятия.
            :return: True если операция успешна, иначе False.
            """
            if 0 < amount <= self._balance:
                self._balance -= amount
                return True
            return False


    class SavingsAccount(BankAccount):
        """
        Дочерний класс, представляющий накопительный счет.
        Наследует все свойства BankAccount, но добавляет процентную ставку
        и ограничения на снятие средств.
        """

        def __init__(self, owner: str, account_number: str, interest_rate: float, initial_balance: float = 0.0) -> None:
            """
            Инициализация накопительного счета.
            Расширяет конструктор базового класса, добавляя процентную ставку.
            :param owner: Имя владельца счета.
            :param account_number: Номер счета.
            :param interest_rate: Годовая процентная ставка (например, 0.05 для 5%).
            :param initial_balance: Начальный баланс.
            """
            super().__init__(owner, account_number, initial_balance)
            self.interest_rate = interest_rate
            # Инкапсуляция: минимальный остаток скрыт, так как это внутреннее правило банка
            self._min_balance: float = 1000.0

        def __str__(self) -> str:
            """
            Перегрузка метода __str__ для отображения специфичной информации о накопительном счете.
            :return: Строка с информацией о счете и процентной ставке.
            """
            base_str = super().__str__()
            return f"{base_str} (Накопительный, ставка: {self.interest_rate * 100}%)"

        # Метод __repr__ унаследован от базового класса без изменений

        def add_interest(self) -> None:
            """
            Начисление процентов на текущий баланс.
            Новый метод, специфичный для этого класса.
            """
            interest_amount = self._balance * self.interest_rate
            self._balance += interest_amount

        def withdraw(self, amount: float) -> bool:
            """
            Перегрузка метода снятия средств.
            Причина перегрузки: Для накопительных счетов часто существует правило
            неснижаемого остатка. Счет не должен опустошаться полностью,
            чтобы оставаться активным и начислять проценты.
            Валидация изменена по сравнению с базовым классом.
            :param amount: Сумма для снятия.
            :return: True если операция успешна и остаток сохранен, иначе False.
            """
            if 0 < amount <= (self._balance - self._min_balance):
                self._balance -= amount
                return True
            else:
                return False

        # Метод deposit унаследован от базового класса без изменений

    pass
