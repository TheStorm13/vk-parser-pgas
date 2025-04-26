import vk_api

from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class VKAPIHandler:
    def __init__(self, token):
        # Initiate VK API session
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()

    def get_group_id(self, group_name):
        # Resolves VK group ID from its name
        group_info = self.vk.utils.resolveScreenName(screen_name=group_name)

        if not group_info or group_info['type'] != 'group':
            raise ValueError("Группа не найдена!")

        return -group_info['object_id']

    def handler_posts(self, owner_id, start_date, end_date):
        result_posts = []
        total_posts = 0

        offset = 0
        count = 100  # Maximum number of posts per request

        while True:
            try:
                # Fetch posts from the VK wall
                response = self.vk.wall.get(owner_id=owner_id,
                                            count=count,
                                            offset=offset)
                posts = response['items']

                if not posts:
                    break

                total_posts += len(posts)
                offset += count

                # Dates of the first and last posts
                first_date = posts[0]['date']
                last_date = posts[-1]['date']

                # Skip posts older than the end_date
                if last_date > end_date:
                    continue

                # Stop fetching if posts are before the start_date
                if first_date < start_date:
                    break

                result_posts.extend(posts)

            except vk_api.exceptions.ApiError as e:
                logger.error(f"Ошибка API: {e}")
                break

        logger.info("Posts are fetched")

        return result_posts

    def get_posts(self, group_name, start_date, end_date, update_progress=None):
        result_posts = []
        progress = 0

        owner_id = self.get_group_id(group_name)

        posts = self.handler_posts(owner_id, start_date, end_date)

        for post in posts:
            progress += 1
            post_date = (post['date'])

            if update_progress:
                update_progress(progress, len(posts))

            # Filter posts within the date range
            if start_date <= post_date <= end_date:
                # Fetch comments if any are available
                if post['comments']['count'] > 0:
                    post['comments'] = self.vk.wall.getComments(owner_id=owner_id,
                                                                post_id=post['id'])
                result_posts.append(post)

        logger.info("Posts filtered by date")

        return result_posts
