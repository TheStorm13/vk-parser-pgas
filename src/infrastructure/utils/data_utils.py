from datetime import datetime, timedelta


class DateUtils:
    """Утилиты для работы с датами и временем."""

    @staticmethod
    def timestamp_to_datetime(timestamp) -> datetime:
        """Преобразует UNIX-метку в datetime.

        Args:
            timestamp (float | int): UNIX-метка времени.

        Returns:
            datetime: Объект datetime.

        """
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def datetime_to_timestamp(date: datetime) -> float:
        """Преобразует datetime в UNIX-метку.

        Args:
            date (datetime): Объект даты и времени.

        Returns:
            float: Метка UNIX.

        """
        return date.timestamp()

    @staticmethod
    def datetime_to_string(data: datetime) -> str:
        """Форматирует datetime как 'DD.MM.YYYY'.

        Args:
            data (datetime): Объект даты и времени.

        Returns:
            str: Строка в формате 'DD.MM.YYYY'.

        """
        return data.strftime("%d.%m.%Y")

    @staticmethod
    def timestamp_to_str(date: float) -> str:
        """Форматирует UNIX-метку как 'DD.MM.YYYY'.

        Args:
            date (float): UNIX-метка времени.

        Returns:
            str: Строка в формате 'DD.MM.YYYY'.

        """
        return datetime.fromtimestamp(date).strftime("%d.%m.%Y")

    @staticmethod
    def str_to_timestamp(date: str, is_end_of_day: bool = False) -> float:
        """Преобразует дату 'DD.MM.YYYY' в UNIX-метку.

        Args:
            date (str): Дата в формате 'DD.MM.YYYY'.
            is_end_of_day (bool): Установить конец суток.

        Returns:
            float: Метка UNIX.

        Raises:
            ValueError: Неверный формат даты.

        """
        dt = datetime.strptime(date, "%d.%m.%Y")
        if is_end_of_day:
            dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=1)
        return dt.timestamp()

    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> tuple[float, float] | None:
        """Проверяет и сравнивает две даты.

        Args:
            start_date (str): Дата начала 'DD.MM.YYYY'.
            end_date (str): Дата конца 'DD.MM.YYYY'.

        Returns:
            tuple[float, float] | None: Метки начала и конца или None.

        """
        try:
            start_dt = datetime.strptime(start_date, "%d.%m.%Y").timestamp()
            end_dt = datetime.strptime(end_date, "%d.%m.%Y").timestamp()

            if end_dt < start_dt:
                return None

            return start_dt, end_dt
        except ValueError:
            return None

    @staticmethod
    def get_current_date() -> datetime:
        """Возвращает текущую дату и время.

        Returns:
            datetime: Текущие дата и время.

        """
        return datetime.now()

    @staticmethod
    def get_days_before_date(days: int, date: datetime) -> datetime:
        """Возвращает дату на N дней раньше.

        Args:
            days (int): Количество дней.
            date (datetime): Базовая дата.

        Returns:
            datetime: Итоговая дата.

        """
        future_datetime = date - timedelta(days=days)
        return future_datetime
