import requests
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BlogPost

MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ0MTUwNzQ5NSwiYWFpIjoxMSwidWlkIjo2OTAwMzc1MywiaWFkIjoiMjAyNC0xMS0yNlQxNjoxNDoyMC4yMjZaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjY2OTgzMzMsInJnbiI6InVzZTEifQ.8xqSrt_mKvPBrPzTRbrT3ZuBeXxqFFHkgTlabE_JbmU"
MONDAY_BOARD_ID = "7932295992"

def send_to_monday(item_name, column_values):
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json",
    }
    query = """
    mutation ($itemName: String!, $boardId: Int!, $columnValues: JSON!) {
        create_item (board_id: $boardId, item_name: $itemName, column_values: $columnValues) {
            id
        }
    }
    """
    data = {
        "query": query,
        "variables": {
            "itemName": item_name,
            "boardId": MONDAY_BOARD_ID,
            "columnValues": column_values,
        },
    }
    requests.post(url, json=data, headers=headers)

@receiver(post_save, sender=BlogPost)
def handle_blog_save(sender, instance, created, **kwargs):
    status = "Created" if created else "Updated"
    column_values = {
        "author": {"text": instance.author.username},
        "status": {"label": status},
        "updated_at": {"date": instance.updated_at.strftime("%Y-%m-%d")},
    }
    send_to_monday(instance.title, column_values)

@receiver(post_delete, sender=BlogPost)
def handle_blog_delete(sender, instance, **kwargs):
    column_values = {
        "author": {"text": instance.author.username},
        "status": {"label": "Deleted"},
        "updated_at": {"date": instance.updated_at.strftime("%Y-%m-%d")},
    }
    send_to_monday(f"Deleted: {instance.title}", column_values)
