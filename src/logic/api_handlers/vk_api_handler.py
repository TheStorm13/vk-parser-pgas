import vk_api

from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class VKAPIHandler:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()

    def get_group_id(self, group_url):
        # todo: добавить логирование и типизацию
        """
        Получает ID группы по её короткому имени.
        """
        group_info = self.vk.utils.resolveScreenName(screen_name=group_url)

        if not group_info or group_info['type'] != 'group':
            raise ValueError("Группа не найдена!")

        return -group_info['object_id']

    def get_posts(self, owner_id, start_date, end_date, update_progress=None):
        # todo: добавить логирование и типизацию
        """
        Получает посты из группы за указанный период.
        """
        result_posts = []
        total_posts = 0
        progress = 0

        offset = 0
        count = 100  # Максимальное количество постов за один запрос

        get_time = 0
        process_time = 0

        while True:
            try:
                response = self.vk.wall.get(owner_id=owner_id,
                                            count=count,
                                            offset=offset)
                posts = response['items']

                if not posts:
                    break

                total_posts += len(posts)
                offset += count

                first_date = posts[0]['date']
                last_date = posts[-1]['date']

                if last_date > end_date:
                    continue

                if first_date < start_date:
                    return result_posts

                for post in posts:
                    progress += 1
                    post_date = (post['date'])

                    if update_progress:
                        update_progress(progress, total_posts)

                    if start_date <= post_date <= end_date:
                        if post['comments']['count'] > 0:
                            post['comments'] = self.vk.wall.getComments(owner_id=owner_id,
                                                                        post_id=post['id'])
                        result_posts.append(post)


            except vk_api.exceptions.ApiError as e:
                logger.error(f"Ошибка API: {e}")
                break

        return result_posts
