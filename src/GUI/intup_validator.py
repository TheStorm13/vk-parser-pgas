from datetime import datetime


class InputValidator:
    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> tuple[datetime, datetime] | None:
        # todo: переписать метод валидации ввода и вызвать в коде
        try:
            start_dt = datetime.strptime(start_date, "%d.%m.%Y")
            end_dt = datetime.strptime(end_date, "%d.%m.%Y")

            if end_dt < start_dt:
                return None

            return start_dt, end_dt
        except ValueError:
            return None
