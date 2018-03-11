Django-Peewee
=============

About
-----

Django application which adds support for peewee-orm http://docs.peewee-orm.com/en/latest/


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

Now you can access peewee model through **.pw** field

.. code-block:: python

    class SomeModel(db.Model):
        text = db.CharField()

    for item in SomeModel.pw.select(SomeModel.pw.text):
        print(item.text)


More examples
------------

You are free to use related fields

.. code-block:: python

    class TestPeeWeeModels(TestCase):
        def test_user_permissions(self):
            # create using default django methods
            user = User.objects.create_user("user", "email@email.ru", "123")
            user.user_permissions.add(*Permission.objects.all())

            # we can use attribute accessor to get object by id
            user_pw = User.pw[user.id]

            # get user permission using peewee orm
            permissions = user_pw.user_permissions \
                    .where(Permission.pw.name.contains('add')) \
                    .offset(2) \
                    .limit(5)

            # you still can access user binded to permission from related field
            for permission in permissions:
                self.assertIn('add', permission.name)
                self.assertEqual(permission.users.first().email, user.email)
                self.assertEqual(1, permission.users.count())
                self.assertTrue(permission.users.exists())

