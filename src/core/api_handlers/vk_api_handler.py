import vk_api

from src.core.exception.task_interrupted_error import TaskInterruptedError
from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class VKAPIHandler:
    """Инкапсулирует вызовы VK API.

    Args:
        state_manager (StateManager): Состояние приложения.
        task_manager (TaskManager): Управление задачей.

    """

    def __init__(self, state_manager: StateManager, task_manager: TaskManager):
        """Создаёт клиент VK API.

        Args:
            state_manager (StateManager): Менеджер состояния.
            task_manager (TaskManager): Менеджер задач.

        """
        self.state_manager = state_manager
        self.task_manager = task_manager

        self.vk_session = vk_api.VkApi(token=state_manager.state.vk_token)
        self.vk = self.vk_session.get_api()

    def extract_group_name_from_url(self, url: str) -> str:
        """Извлекает screen name сообщества из URL.

        Args:
            url (str): Полный URL сообщества.

        Returns:
            str: Имя сообщества.

        Raises:
            ValueError: Пустой URL или имя не найдено.

        """
        if not url or not isinstance(url, str):
            logger.error("URL is empty.")
            raise ValueError("URL должен быть непустой строкой!")

        # Берём часть после последнего "/"; rstrip удаляет хвостовой "/"
        group_name = url.rstrip("/").split("/")[-1]

        if not group_name:
            logger.error("Failed to extract the name of the group from the URL.")
            raise ValueError("Не удалось извлечь имя группы из URL!")

        return group_name

    def get_group_id(self, group_name: str) -> int:
        """Получает owner_id сообщества по screen name.

        Args:
            group_name (str): Имя сообщества.

        Returns:
            int: Отрицательный owner_id.

        Raises:
            ValueError: Сообщество не найдено или ошибка API.

        """
        try:
            group_info = self.vk.utils.resolveScreenName(screen_name=group_name)

            if not group_info or group_info["type"] != "group":
                logger.error("The community is not found.")
                raise ValueError("Сообщество не найдена!")

            return -group_info["object_id"]
        except vk_api.exceptions.ApiError as e:
            logger.error(f"Ошибка API: {e}")
            raise ValueError("Ошибка API. Проверьте VK TOKEN!")

    def handler_posts(self, owner_id: int, start_date: float, end_date: float) -> list:
        """Запрашивает посты стены в диапазоне дат.

        Args:
            owner_id (int): ID владельца стены.
            start_date (int | float): Начало диапазона (unix).
            end_date (int | float): Конец диапазона (unix).

        Returns:
            list: Список постов.

        Raises:
            ValueError: Ошибка VK API.
            Exception: Прочие ошибки запроса.

        """
        result_posts = []
        total_posts = 0

        offset = 0
        count = 100  # Максимум постов за запрос

        self.state_manager.update_state("progress", "Стучимся в сообщество Вконтакте")

        while True:
            try:
                self.task_manager.raise_if_stopped()

                response = self.vk.wall.get(
                    owner_id=owner_id, count=count, offset=offset,
                )
                posts = response["items"]

                if not posts:
                    break

                total_posts += len(posts)
                offset += count

                # Даты первого и последнего поста для ранней остановки
                first_date = posts[0]["date"]
                last_date = posts[-1]["date"]

                # Пропустить, если последний пост новее конца диапазона
                if last_date > end_date:
                    continue

                # Остановить, если первый пост старше начала диапазона
                if first_date < start_date:
                    break

                result_posts.extend(posts)

            except vk_api.exceptions.ApiError as e:
                logger.error(f"Ошибка API: {e}")
                raise ValueError("Ошибка API. Проверьте VK TOKEN!")
            except Exception as e:
                logger.error(e)
                raise e

        logger.info("Posts are fetched")

        return result_posts

    def get_posts(self) -> list:
        """Возвращает посты сообщества с комментариями в диапазоне дат.

        Returns:
            list: Отфильтрованные посты.

        Raises:
            TaskInterruptedError: Задача прервана пользователем.
            Exception: Неожиданная ошибка обработки.

        """
        group_url = self.state_manager.state.vk_group_url
        start_date = self.state_manager.state.start_date
        end_date = self.state_manager.state.end_date

        result_posts = []
        progress = 0

        group_name = self.extract_group_name_from_url(group_url)
        owner_id = self.get_group_id(group_name)

        posts = self.handler_posts(owner_id, start_date, end_date)

        for post in posts:
            try:
                self.task_manager.raise_if_stopped()

                progress += 1
                self.state_manager.update_state(
                    "progress", f"Обработано: {progress} постов",
                )
                post_date = post["date"]

                # Фильтровать посты строго по диапазону
                if start_date <= post_date <= end_date:
                    # Загружать комментарии только при наличии
                    if post["comments"]["count"] > 0:
                        post["comments"] = self.vk.wall.getComments(
                            owner_id=owner_id, post_id=post["id"],
                        )
                    result_posts.append(post)

            except TaskInterruptedError:
                raise TaskInterruptedError("Задача была прервана пользователем!")
            except Exception as e:
                logger.error(e)
                raise e

        logger.info("Posts filtered by date")

        return result_posts
