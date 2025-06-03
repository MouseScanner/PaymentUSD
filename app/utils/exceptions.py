class PaymentAPIException(Exception):
    """Базовое исключение для платежной системы"""
    pass


class AccountNotFoundError(PaymentAPIException):
    """Аккаунт не найден"""
    pass


class AccountAlreadyExistsError(PaymentAPIException):
    """Аккаунт уже существует"""
    pass


class InsufficientBalanceError(PaymentAPIException):
    """Недостаточно средств"""
    pass


class TransferNotFoundError(PaymentAPIException):
    """Перевод не найден"""
    pass


class TransferProcessingError(PaymentAPIException):
    """Ошибка обработки перевода"""
    pass 