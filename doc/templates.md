## HTML, CSS, JS, Images

All CSS, JS, and Image files are contained in `mooches/static` and organized by what they are.
To someone messing with these files, hopefully they'll be self-explanatory.

### HTML Templates

The HTML templates are contained in `mooches/templates`

Python-Flask uses Jinja to template HTML files for the end user.
Jinja allows you to use variables, conditional logic, etc. to format the template before delivering it to the requestor.
You can also use `base` files and extend off them with `blocks` or use `include` statements to include the contents of another template.
They can also just be straight HTML, as long as no Jinja syntax errors are present.

It's best to just look at the templates that are there, as well as Jinja documentation when you get stuck, to get your feel for how to use them.
Hopefully, they are mostly straight-forward.


### The Base Template

The base template is mostly block definitions and include files

```html
<!doctype html>
<html lang="en">

  <head>

    {% block head %}

      {% include "head.html" %}
      <title>{% block title %}{% endblock %} 45 Chaos</title>

    {% endblock %}

  </head>

  <body>

    <nav class="navbar navbar-expand-md navbar-light fixed-top bg-light">
    {% block navbar %}
      {% include "navbar.html" %}
    {% endblock %}
    </nav>

    {% block scripts %}
      {% include "base_scripts.html" %}
    {% endblock %}

    {% block content %}
    {% endblock %}

    <footer class="page-footer font-small blue pt-4 mt-4">
    {% block footer %}
      {% include "footer.html" %}
    {% endblock %}
    </footer>

  </body>

</html>

```

If you wanted to extend off this base and have all the main themes in place you could do something like this:

```html
{% extends "base.html" %}

{% block content %}
  <p>Hello World!</p>
{% endblock %}
```

Say you want to extend, instead of replace, one of the previously defined blocks. You can use `super()`.
For example, to make an addition to the head:

```html
{% extends "base.html" %}

{% block head %}
{% super() %}
  <h3>Another heading</h3>
{% endblock %}

{% block content %}
  <p>Hello World!</p>
{% endblock %}
```

Variables passed in from the python runtime can be referenced as `{{ var }}`, whereas logical functions use `{% function %}`.
