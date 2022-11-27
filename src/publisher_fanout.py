from abc import ABC, abstractmethod
import os
import requests


class Publisher(ABC):
    @abstractmethod
    def publish(self, api_key, title, content):
        pass


class MediumPublisher(Publisher):
    def publish(self, title, content, publish_status="public"):
        MEDIUM_API_KEY = os.environ["MEDIUM_API_KEY"]
        MEDIUM_USER_ID = os.environ["MEDIUM_USER_ID"]

        post_data = {
            "title": title,
            "content": content,
            "contentFormat": "html",
            "publishStatus": publish_status,
        }
        headers = {
            "Authorization": f"Bearer {MEDIUM_API_KEY}",
            "Content-Type": "application/json",
        }

        url = f"https://api.medium.com/v1/users/{MEDIUM_USER_ID}/posts"
        return requests.post(url, json=post_data, headers=headers)


class DevtoPublisher(Publisher):
    def publish(self, title, content):
        DEVTO_API_KEY = os.environ["DEVTO_API_KEY"]

        post_data = {
            "article": {
                "title": title,
                "published": False,
                "body_markdown": content,
                "tags": [],
            }
        }
        headers = {
            "Content-Type": "application/json",
            "api-key": DEVTO_API_KEY,
        }

        url = "https://dev.to/api/articles"
        return requests.post(url, json=post_data, headers=headers)

def send_message(title,content):
    MediumPublisher().publish(title,content)
    # print("GOT: ", message)


if __name__ == "__main__":
    title = "Test Article"
    content = "lorem ipsum"

    print(DevtoPublisher().publish(title, content))
    print(MediumPublisher().publish(title, content))
