from typing import Final


class TargetTransactionErrors:
    """Class for validate errors for TargetTransaction model."""

    NOT_USERS_TARGET: Final[str] = 'У пользователя нет такой цели'


class TargetErrors:
    """Class for validate errors for Target model."""

    NOT_CORRECT_INITIAL_DEPOSIT: Final[str] = (
        'Нельзя внести на цель средств больше, чем на счету'
    )
    CHANGE_TARGET_AMOUNT: Final[str] = (
        'Нельзя изменить ожидаемую сумму цели на значение, '
        'меньше текущей накопленной суммы'
    )
    CHANGE_DEPOSIT_TERM: Final[str] = (
        'Новый срок завершения цели может быть раньше '
        'изначально запланированного'
    )
    REQUIRED_AMOUNT: Final[str] = (
        'Нужная сумма еще не набрана'
    )
