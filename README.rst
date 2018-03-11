Django-Peewee
=============

About
-----

Django application which adds support for Peewee ORM http://docs.peewee-orm.com/en/latest/


Install
-------

.. code-block:: python
    pip install git+https://github.com/SevenLines/django-peewee.git

add to INSTALLED_APPS

.. code-block:: python
    INSTALLED_APPS = [
        ...

        'django_peewee',
    ]

Now you can access peewee model through **.pw**

.. code-block:: python
    class SomeModel(db.Model):
        text = db.CharField()

    SomeModel.pw.select(SomeModel.text).execute()
