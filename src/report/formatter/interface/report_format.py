from abc import ABC, abstractmethod

from src.model.post import Post


class ReportFormat(ABC):
    @abstractmethod
    def format_header(self, count_posts: int) -> str:
        pass

    @abstractmethod
    def format_category_header(self, category_name: str, count_posts: int, category_point: int) -> str:
        pass

    @abstractmethod
    def format_post(self, post: Post) -> str:
        pass

    @abstractmethod
    def format_category_posts(self, posts: list[Post]) -> str:
        pass
