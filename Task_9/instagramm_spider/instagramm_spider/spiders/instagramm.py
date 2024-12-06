import json
from copy import deepcopy
from urllib.parse import urlencode
from Task_9.instagramm_spider.instagramm_spider.items import InstagrammSpiderItem
import scrapy
from scrapy.http import HtmlResponse

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://instagram.com"]
    inst_login_link = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'
    inst_login = 'gamer_udm18'
    user_for_parse = {'name': 'machinelearning', 'id': 27790588603}

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            url=self.inst_login_link,
            method="POST",
            callback=self.authorize,
            formdata={
                'username': self.inst_login,
                'enc_password': '#PWD_INSTAGRAM_BROWSER:10:1733513545:ATRQAOyVWuGS6co9633Vh0XipA4TKwVYWcokSvFPeJmOEHESDTlO48dUTExi7NPzjpquhETyFD8F4QgRbSkooIe6K1cX8vnan2QQ/wjTTFFN/XdtbaaL88/pxHEMkI0hp6X8IyCWytypEcCt5Rky8QvJ'
            },
            headers={
                'X-Csrftoken': 'T3uf0RC2IVRyFQ4ka2UgXUIVzCYGJBAf'
            }
        )

    def authorize(self, response: HtmlResponse):
        print()
        j_data = response.json()
        if j_data.get('authenticated'):
            yield response.follow(
                url=f"/{self.user_for_parse.get('name')}",
                callback=self.user_data_parse,
                cb_kwargs={'username': self.user_for_parse.get('name')}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.user_for_parse.get('id')
        params = {'count': 12}
        url_posts = f"https://www.instagram.com/api/v1/feed/user/{user_id}/?{urlencode(params)}"

        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'params': deepcopy(params)},
            headers={'User-Agent': 'Instagram 244.0.0.17.110'}
        )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, params):
        j_data = response.json()
        next_page = j_data.get("more_available")
        if next_page:
            next_max_id = j_data.get("next_max_id")
            params["max_id"] = next_max_id
            url_posts = f"https://www.instagram.com/api/v1/feed/user/{user_id}/?{urlencode(params)}"

            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    "params": deepcopy(params)
                },
                headers={"User-Agent": "Instagram 244.0.0.17.110"}
            )
        posts = j_data.get('items')
        for post in posts:
            item = InstagrammSpiderItem(
                text=post.get('caption').get('text').replace('\n', ' '),
                photo=post.get('image_versions2').get('candidates')[0].get('url'),
                post_data=post,
                username=username,
                user_id=user_id
            )
            yield item

    def save_to_json(self, text):
        with open('page.json', 'w') as f:
            json.dump(text, f)






















