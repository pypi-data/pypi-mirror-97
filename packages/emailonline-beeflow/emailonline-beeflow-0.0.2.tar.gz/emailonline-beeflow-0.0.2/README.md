# Email Online App

This app allows you to add 'see online' link to any email you are sending to users.

## Configuration

1. Add `emailonline` to `INSTALLED_APPS` in `settings.py` file.
2. Add `DEFAULT_MAIN_PAGE="[name of default main page to redirect]"` into the `settings.py` file. 
2. Add `path("emailonline/", include("emailonline.urls")),` to the main `urls.py` file 

## Usage

Here is an example for creating email online:

```python
email_online = EmailOnline()
email_online.user = user                            # optional
email_online.content = render_to_string(
    "your_template_name.html",
    {
        ...,
        "online_message_uid": str(email_online.id),
    }
)      # prepare HTML / TXT message to send.
email_online.save()
```

HTML template example:
```html
See this <a href="{% url 'emailonline:see_email id=online_message_uid %}'">email on webpage</a>
```
