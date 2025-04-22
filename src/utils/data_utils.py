from datetime import datetime


class DataUtils:
    @staticmethod
    def convert_date(timestamp) -> datetime:
        """
        Форматирует дату в формате DD.MM.YYYY.
        """
        return datetime.fromtimestamp(timestamp)

    def format_date(data):
        """
        Форматирует дату в формате DD.MM.YYYY.
        """
        return data.strftime('%d.%m.%Y')
