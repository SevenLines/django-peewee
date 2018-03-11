from datetime import date, datetime, time
from decimal import Decimal

from django.contrib.auth.models import User, Permission
from django.test import TestCase

# Create your tests here.
from test_django_peewee.models import TestModel, TestModelWithCustomTableName, OtherTestModel


class TestModelBase(TestCase):
    # def get_all_subclassess(self, cls):
    #     out = []
    #     for subclass in cls.__subclasses__():
    #         out.append(subclass)
    #         out.extend(self.get_all_subclassess(subclass))
    #     return out

    def test_list_class(self):
        other = OtherTestModel.objects.create(text="OtherTestModel")

        data = dict(
            big_integer_field=123,
            boolean_field=True,
            binary_field=b'',
            char_field='',
            date_field=date(2018, 1, 2),
            date_time_field=datetime(2018, 1, 1, 11, 11),
            decimal_field=Decimal("123.5555"),
            email_field='',
            file_field='',
            file_path_field='',
            float_field=123.123,
            foreign_key=other,
            generic_ipaddress_field='255.255.1.1',
            image_field='',
            integer_field=12,
            null_boolean_field=True,
            positive_integer_field=12,
            positive_small_integer_field=12,
            slug_field='',
            small_integer_field=-12,
            text_field='text_field_value',
            text_field_with_custom_column='text_field_with_custom_column_value',
            time_field=time(1, 1, 50),
            urlfield='',
        )

        model = TestModel.objects.create(**data)

        item = TestModel.pw[model.id]
        for key, value in data.items():
            if key == 'date_time_field':
                date_format = "{:%Y-%m-%d %H:%M:%S}"
                self.assertEqual(date_format.format(value), date_format.format(getattr(item, key)))
            elif key == 'foreign_key':
                self.assertEqual(value.id, item.foreign_key_id)
                self.assertEqual(value.id, item.foreign_key.id)
            else:
                self.assertEqual(value, getattr(item, key), "wrong {}".format(key))

    def test_many_to_many_permissions(self):
        user = User.objects.create_user("m", "email@email.ru", "123")
        user.user_permissions.add(*Permission.objects.all())

        user_pw = User.pw[user.id]
        for permission in user_pw.user_permissions.where(Permission.pw.name.contains('add')):
            self.assertIn('add', permission.name)
            self.assertEqual(permission.users.first().email, user.email)
            self.assertEqual(1, permission.users.count())
            self.assertTrue(permission.users.exists())

    def test_custom_table_name(self):
        TestModelWithCustomTableName.objects.create(
            text='hello'
        )

        TestModelWithCustomTableName.objects.create(
            text='hello2'
        )
        data = list(TestModelWithCustomTableName.pw.select().execute())[0]
        self.assertEqual('hello', data.text)

        TestModelWithCustomTableName.objects.create(
            text='hello2'
        )
        data = list(TestModelWithCustomTableName.pw.select()
                    .order_by(TestModelWithCustomTableName.pw.id.desc()).execute())[0]

        self.assertEqual('hello2', data.text)
