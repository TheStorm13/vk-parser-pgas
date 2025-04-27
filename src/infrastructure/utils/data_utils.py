from datetime import datetime, timedelta


class DateUtils:
    @staticmethod
    def timestamp_to_datetime(timestamp) -> datetime:
        """Convert a UNIX timestamp to a datetime object."""
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def datetime_to_timestamp(date: datetime) -> float:
        """Convert a datetime object to a UNIX timestamp."""
        return date.timestamp()

    @staticmethod
    def datetime_to_string(data: datetime) -> str:
        """Format a datetime object as a string in the format 'DD.MM.YYYY'."""
        return data.strftime('%d.%m.%Y')

    @staticmethod
    def timestamp_to_str(date: float) -> str:
        return datetime.fromtimestamp(date).strftime('%d.%m.%Y')

    @staticmethod
    def str_to_timestamp(date: str) -> float:
        return datetime.strptime(date, "%d.%m.%Y").timestamp()

    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> tuple[float, float] | None:
        """Validate and compare two date strings. Ensure end_date is not earlier than start_date."""
        try:
            start_dt = datetime.strptime(start_date, "%d.%m.%Y").timestamp()
            end_dt = datetime.strptime(end_date, "%d.%m.%Y").timestamp()

            if end_dt < start_dt:
                return None  # Return None if the end date is earlier than the start date

            return start_dt, end_dt
        except ValueError:
            return None  # Return None for invalid date format inputs

    @staticmethod
    def get_current_date() -> datetime:
        return datetime.now()

    @staticmethod
    def get_days_before_date(days: int, date: datetime) -> datetime:
        future_datetime = date - timedelta(days=days)
        return future_datetime
