*****************
Django CSS inline
*****************

.. image:: https://img.shields.io/pypi/v/django-css-inline
    :target: https://pypi.org/project/django-css-inline/

.. image:: https://img.shields.io/pypi/pyversions/django-css-inline
    :target: https://pypi.org/project/django-css-inline/


Simple helper for loading CSS files as inline in HTML with Django.

Example :

::

    {% load css_inline %}

    ...

    <head>
        ...

        {% css_inline %}
            <link rel="stylesheet" href="/static/django_css_inline/test-1.css">
            <link rel="stylesheet" href="/static/django_css_inline/test-2.css">
            <link rel="stylesheet" href="https://static.snoweb.fr/django-css-inline/test-3.css">
        {% end_css_inline %}
    </head>

Every <link> includes between {% css_inline %} and {% end_css_inline %} give this results :

::

    <head>
        ...

        <style type="text/css">

            /* test-1.css styles */
            /* test-2.css styles */
            /* test-3.css styles */

        </style>
    </head>


Setup
#####

Install with pip :

``pip install django-css-inline``


Add django_css_inline to django apps installed :
::

    INSTALLED_APPS = [
        ...
        'django_css_inline',
    ]

In settings.py, chose to enable or disable django_css_inline. For example :
::

    # Default True
    DJANGO_CSS_INLINE_ENABLE = not DEBUG

If you use static files with Django, don't forget to collect them with :
::

    python manage.py collectstatic
