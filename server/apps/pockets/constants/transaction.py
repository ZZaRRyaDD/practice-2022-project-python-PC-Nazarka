from typing import Final


class TransactionTypes:
    INCOME: Final[str] = 'income'
    EXPENSE: Final[str] = 'expense'

    CHOICES: Final[tuple[tuple[str, str], ...]] = (
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    )

    CHOICES_DICT: Final[dict[str, str]] = dict(CHOICES)


class TransactionFile:
    CATEGORY_NAME_COLUMN: Final[int] = 1
    TRANSACTION_DATE_COLUMN: Final[int] = 2
    AMOUNT_COLUMN: Final[int] = 3
    TRANSACTION_TYPE_COLUMN: Final[int] = 4

    COLUMNS: Final[tuple[tuple[int, str], ...]] = (
        (CATEGORY_NAME_COLUMN, 'Название категории'),
        (TRANSACTION_DATE_COLUMN, 'Дата транзакции'),
        (AMOUNT_COLUMN, 'Сумма транзакции'),
        (TRANSACTION_TYPE_COLUMN, 'Тип транзакции'),
    )

    CHOICES_DICT: Final[dict[int, str]] = dict(COLUMNS)
