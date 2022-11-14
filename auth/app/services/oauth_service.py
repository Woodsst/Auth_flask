from urllib.parse import urlencode

from requests import get, post

from config.settings import Yandex, VK
from core.jwt_api import decode_yandex_jwt
from services.service_base import OauthBase


class YandexOauth(OauthBase, Yandex):
    """Класс для получения и обработки данных
    при работе с провайдером Yandex"""

    def get_client_info(self, tokens: dict):
        """Запрос на получение данных о пользователе от yandex"""

        client_jwt = get(
            self.get_user_info_url,
            headers={"Authorization": f"Oauth {tokens.get('access_token')}"},
        )

        client_info = decode_yandex_jwt(client_jwt.content.decode())
        return {
            "login": client_info.get("login"),
            "password": client_info.get("psuid"),
            "email": client_info.get("email"),
        }

    def get_tokens(self, code: str):
        """Запрос на получение токена доступа к информации
        о пользователе от Яндекса"""

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        data = urlencode(data)
        tokens = post(f"{self.baseurl}token", data)
        tokens = tokens.json()
        return tokens


class VKOauth(OauthBase, VK):
    """Класс для получения и обработки данных
    при работе с провайдером VK"""

    def get_tokens(self, code: str) -> dict:
        """Запрос на получение токена доступа к информации
        о пользователе от Вконтакте"""
        get_token = get(
            f"{self.baseurl}"
            f"client_id={self.client_id}"
            f"&client_secret={self.client_secret}"
            f"&redirect_uri={self.redirect_url.redirect_url}"
            f"&code={code}"
        )
        return get_token.json()

    def get_client_info(self, tokens: dict) -> dict:
        """Запрос на получение данных о пользователе из Вконтакте"""

        token = tokens.get("access_token")
        user_id = tokens.get("user_id")

        get_client_info = get(
            f"{self.get_user_info_url}"
            f"user_ids={user_id}"
            "&fields=first_name"
            f"&access_token={token}"
            "&lang=en"
            f"{self.api_version}"
        )
        client_info = get_client_info.json()
        return {
            "login": (
                f'{client_info.get("response")[0].get("last_name")}'
                f'_{client_info.get("response")[0].get("id")}'
            ),
            "password": (
                f'{client_info.get("response")[0].get("first_name")}'
                f'&{client_info.get("response")[0].get("id")}'
            ),
            "email": tokens.get("email"),
        }
