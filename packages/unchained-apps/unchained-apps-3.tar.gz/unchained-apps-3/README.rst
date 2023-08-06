==============
unchained apps
==============
This is a package that contains many of unchained apps:
- unchained_auth
- unchained_chat
- unchained_notification

** to be separated when its more mature and we have more manpower to maintain separate packages.

Quick start
-----------

1. Install the lib: 

     pip install django-unchained-apps


1. Add "foo" to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = [
        ...
        'unchained_auth',
        'unchained_chat',
        'unchained_notification'
        ...
    ]

2. Include the foo URLconf in your project ``urls.py`` like this::

    path('', include('unchained_auth')),
