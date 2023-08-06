Quart-Csrf
==========

Quart-Csrf is an extension for [Quart](https://gitlab.com/pgjones/quart) to provide CSRF protection.
The code is taked from [Flask-WTF](https://github.com/lepture/flask-wtf).

Usage
-----

To enable CSRF protection globally for a Quart app, you have to create an CSRFProtect and
initialise it with the application,
```python
from quart_csrf import CSRFProtect

app = Quart(__name__)
CSRFProtect(app)
```

or via the factory pattern,
```python
csrf = CSRFProtect()

def create_app():
    app = Quart(__name__)
    csrf.init_app(app)
    return app
```

Note: CSRF protection requires a secret key to securely sign the token. By default this will
use the QUART app's SECRET_KEY. If you'd like to use a separate token you can set QUART_CSRF_SECRET_KEY.

HTML Forms: render a hidden input with the token in the form.
```html
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
</form>
```

JavaScript Requests: When sending an AJAX request, add the X-CSRFToken header to it. For example, in jQuery you can configure all requests to send the token.
```html
<meta name="csrf-token" content="{{ csrf_token() }}">

<script>
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // var csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
</script>
```

Contributing
------------

Quart-Csrf is developed on [GitLab](https://gitlab.com/wcorrales/quart-csrf). You are very welcome to
open [issues](https://gitlab.com/wcorrales/quart-csrf/issues) or
propose [merge requests](https://gitlab.com/wcorrales/quart-csrf/merge_requests).

Help
----

This README is the best place to start, after that try opening an
[issue](https://gitlab.com/wcorrales/quart-csrf/issues).
