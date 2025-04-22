from src.mapper.post_mapper import PostMapper
from src.post_processing import PostCategorizer
from src.post_processing.author_validator import AuthorValidator


class PostAnalyzer:
    def __init__(self, fio):
        self.author_validator = AuthorValidator(fio)
        self.post_mapper = PostMapper()

    def posts_analyze(self, posts):
        list_of_posts = []

        for post in posts:
            if self.author_validator.validate_author(post):
                post_model = self.post_mapper.to_post_model(post)
                list_of_posts.append(post_model)

        sorted_posts = sorted(list_of_posts, key=lambda post: post.date)

        categorized_posts = PostCategorizer.categorize_posts(sorted_posts)

        return categorized_posts
