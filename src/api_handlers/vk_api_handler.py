from datetime import datetime

import vk_api


class VKAPIHandler:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()

    def get_group_id(self, group_url):
        """
        Получает ID группы по её короткому имени.
        """
        group_info = self.vk.utils.resolveScreenName(screen_name=group_url)
        if not group_info or group_info['type'] != 'group':
            raise ValueError("Группа не найдена!")
        return -group_info['object_id']

    def get_posts(self, owner_id, start_date, end_date, update_progress=None):
        """
        Получает посты из группы за указанный период.
        """
        posts = []
        offset = 0
        count = 100  # Максимальное количество постов за один запрос
        total_posts = 0
        progress = 0

        while True:
            try:
                response = self.vk.wall.get(owner_id=owner_id, count=count, offset=offset)
                if not response['items']:
                    break

                total_posts += len(response['items'])

                for post in response['items']:
                    progress += 1
                    if update_progress:
                        update_progress(progress, total_posts)
                    if post['comments']['count'] > 0:
                        post['comments'] = self.vk.wall.getComments(owner_id=owner_id, post_id=post['id'])
                    post_date = datetime.fromtimestamp(post['date'])
                    if start_date <= post_date <= end_date:
                        posts.append(post)
                    elif post_date < start_date:
                        return posts  # Прекращаем, если посты старше начала периода

                offset += count

            except vk_api.exceptions.ApiError as e:
                print(f"Ошибка API: {e}")
                break

        return posts
