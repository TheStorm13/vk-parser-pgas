from dataclasses import dataclass

from src.infrastructure.utils.data_utils import DateUtils


@dataclass
class StateApp:
    is_run: bool = False
    progress: str = "Опять работать?"
    post_count: int = 0

    vk_token: str = ""
    vk_group_url: str = "https://vk.com/svarog_samara"
    full_name: str = "Иванов Иван Иванович"
    start_date: float = DateUtils.get_days_before_date(
        365, DateUtils.get_current_date()
    ).timestamp()
    end_date: float = DateUtils.get_current_date().timestamp()
