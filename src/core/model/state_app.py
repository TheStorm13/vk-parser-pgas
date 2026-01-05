from dataclasses import dataclass

from src.infrastructure.utils.data_utils import DateUtils


@dataclass
class StateApp:
    """Хранит состояние и параметры запуска.

    Attributes:
        is_run: Флаг выполнения.
        progress: Текст прогресса.
        post_count: Количество постов.
        vk_token: Токен VK.
        vk_group_url: URL группы VK.
        full_name: Полное имя пользователя.
        start_date: Начальная дата в UNIX-времени.
        end_date: Конечная дата в UNIX-времени.

    """

    is_run: bool = False
    progress: str = "Опять работать?"
    post_count: int = 0

    vk_token: str = ""
    vk_group_url: str = "https://vk.com/svarog_samara"
    full_name: str = "Иванов Иван Иванович"
    start_date: float = DateUtils.get_days_before_date(
        365, DateUtils.get_current_date(),
    ).timestamp()
    end_date: float = DateUtils.get_current_date().timestamp()
