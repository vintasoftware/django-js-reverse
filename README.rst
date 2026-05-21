=================
Django JS Reverse
=================

.. image:: https://img.shields.io/pypi/v/django-js-reverse.svg
   :target: https://pypi.org/project/django-js-reverse/

.. image:: https://github.com/vintasoftware/django-js-reverse/actions/workflows/main.yml/badge.svg?branch=main
   :target: https://github.com/vintasoftware/django-js-reverse/actions/workflows/main.yml

.. image:: https://img.shields.io/github/license/vintasoftware/django-js-reverse.svg
    :target: https://raw.githubusercontent.com/vintasoftware/django-js-reverse/main/LICENSE

.. image:: https://img.shields.io/pypi/wheel/django-js-reverse.svg


**Javascript url handling for Django that doesn’t hurt.**

This package is now maintained by `Vinta Software <https://vintasoftware.com.br>`__ but it was originally created by `@ierror <https://github.com/ierror>`__. Many thanks to you, Bernhard.


Overview
--------

Django JS Reverse is a small django app that makes url handling of
`named urls <https://docs.djangoproject.com/en/stable/topics/http/urls/#naming-url-patterns>`__ in javascript easy and non-annoying..

For example you can retrieve a named url:

urls.py:

::

    from django.urls import path

    urlpatterns = [
        path("betterliving/<slug:category_slug>/<int:entry_pk>/", get_house, name="betterliving_get_house"),
    ]

in javascript like:

::

    Urls.betterlivingGetHouse('house', 12)

Result:

::

    /betterliving/house/12/


Requirements
------------

+----------------+--------------------+
| Python version | Django versions    |
+================+====================+
| 3.14           | 6.0, 5.2           |
+----------------+--------------------+
| 3.13           | 6.0, 5.2           |
+----------------+--------------------+
| 3.12           | 6.0, 5.2           |
+----------------+--------------------+
| 3.11           | 5.2                |
+----------------+--------------------+
| 3.10           | 5.2                |
+----------------+--------------------+

Django 5.2 is the current LTS release.


Installation
------------

Install using ``pip`` …

::

    pip install django-js-reverse

… or clone the project from github.

::

    git clone https://github.com/vintasoftware/django-js-reverse.git

Add ``'django_js_reverse'`` to your ``INSTALLED_APPS`` setting.

::

    INSTALLED_APPS = (
        ...
        'django_js_reverse',
    )


Usage with webpack
------------------

Install using ``npm``

::

    npm install --save django-js-reverse


Include none-cached view …

::

    from django.urls import path
    from django_js_reverse.views import urls_json

    urlpatterns = [
        path("jsreverse.json", urls_json, name="js_reverse"),
    ]

… or a cached one that delivers the urls JSON

::

    from django.urls import path
    from django_js_reverse.views import urls_json

    urlpatterns = [
        path("jsreverse.json", cache_page(3600)(urls_json), name="js_reverse"),
    ]

Include JavaScript in your bundle:

::

    // utils/djangoReverse.mjs
    import _ from 'lodash/fp';
    import djangoJsReverse from 'django-js-reverse';

    export default _.once(
      async () => {
        const res = await fetch('/jsreverse.json');
        const data = await res.json();
        return djangoJsReverse(data);
      }
    )

::

    // somePlace.mjs
    import djangoReverse from './utils/djangoReverse';

    (async () => {
      const urls = await djangoReverse();
      const url = urls.someViewName('some-arg');
      ...
    })();


Usage as static file
--------------------

First generate static file by

::

    ./manage.py collectstatic_js_reverse

If you change some urls or add an app and want to update the reverse.js file,
run the command again.

After this add the file to your template

::

    <script src="{% static 'django_js_reverse/js/reverse.js' %}"></script>


Usage with views
----------------

Include none-cached view …

::

    from django.urls import path
    from django_js_reverse.views import urls_js

    urlpatterns = [
        path("jsreverse/", urls_js, name="js_reverse"),
    ]

… or a cached one that delivers the urls javascript

::

    from django.urls import path
    from django_js_reverse.views import urls_js

    urlpatterns = [
        path("jsreverse/", cache_page(3600)(urls_js), name="js_reverse"),
    ]

Include javascript in your template

::

    <script src="{% url 'js_reverse' %}" type="text/javascript"></script>


Usage as template tag
_____________________

You can place the js_reverse JavaScript inline into your templates,
however use of inline JavaScript is not recommended, because it
will make it impossible to deploy a secure Content Security Policy.
See `django-csp <https://django-csp.readthedocs.io/>`__

::

    {% load js_reverse %}

    <script type="text/javascript" charset="utf-8">
        {% js_reverse_inline %}
    </script>


Use the urls in javascript
--------------------------

If your url names are valid javascript identifiers ([$A-Z\_][-Z\_$]\*)i
you can access them by the Dot notation:

::

    Urls.betterlivingGetHouse('house', 12)

If the named url contains invalid identifiers use the Square bracket
notation instead:

::

    Urls['betterliving-get-house']('house', 12)
    Urls['namespace:betterliving-get-house']('house', 12)

You can also pass javascript objects to match keyword aguments like the
examples bellow:

::

    Urls['betterliving-get-house']({ category_slug: 'house', entry_pk: 12 })
    Urls['namespace:betterliving-get-house']({ category_slug: 'house', entry_pk: 12 })

Options
-------

Optionally, you can overwrite the default javascript variable ‘Urls’ used
to access the named urls by django setting

::

    JS_REVERSE_JS_VAR_NAME = 'Urls'

Optionally, you can change the name of the global object the javascript variable
used to access the named urls is attached to. Default is :code:`this`

::

    JS_REVERSE_JS_GLOBAL_OBJECT_NAME = 'window'


Optionally, you can disable the minfication of the generated javascript file
by django setting

::

    JS_REVERSE_JS_MINIFY = False


By default all namespaces are included

::

    JS_REVERSE_EXCLUDE_NAMESPACES = []

To exclude any namespaces from the generated javascript file, add them to the `JS_REVERSE_EXCLUDE_NAMESPACES` setting

::

    JS_REVERSE_EXCLUDE_NAMESPACES = ['admin', 'djdt', ...]

If you want to include only specific namespaces add them to the `JS_REVERSE_INCLUDE_ONLY_NAMESPACES` setting
tips:
* Use "" (empty string) for urls without namespace
* Use "foo\0" to include urls just from "foo" namaspace and not from any subnamespaces (e.g. "foo:bar")

::

    JS_REVERSE_INCLUDE_ONLY_NAMESPACES = ['poll', 'calendar', ...]

If you run your application under a subpath, the collectstatic_js_reverse needs to take care of this.
Define the prefix in your django settings:

::

   JS_REVERSE_SCRIPT_PREFIX = '/myprefix/'

By default collectstatic_js_reverse writes its output (reverse.js) to your project's STATIC_ROOT.
You can change the output path:

::

    JS_REVERSE_OUTPUT_PATH = 'some_path'


Running the test suite
----------------------

::

    tox

License
-------

`MIT <https://raw.githubusercontent.com/vintasoftware/django-js-reverse/main/LICENSE>`__


Support
-------

This project is currently maintained by `Vinta Software <https://vintasoftware.com>`__. If you need support please contact us on `contact@vintasoftware.com <mailto:contact@vintasoftware.com>`__.

--------------

Enjoy!
