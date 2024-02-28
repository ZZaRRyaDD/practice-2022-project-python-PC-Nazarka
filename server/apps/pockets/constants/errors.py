from typing import Final


class TransactionErrors:
    NOT_USERS_CATEGORY: Final[str] = 'У пользователя нет такой категории'
    INCOME_CANT_HAVE_CATEGORY: Final[str] = (
        'Операция типа "Доход" не может иметь категорию'
    )


class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[str] = (
        'У пользователя уже существует категория с таким названием и типом'
    )
