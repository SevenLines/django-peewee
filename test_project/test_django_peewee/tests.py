import uuid
from datetime import date, datetime, time
from decimal import Decimal

from django.contrib.auth.models import User, Permission
from django.test import TestCase

from test_django_peewee.models import TestModel, TestModelWithCustomTableName, OtherTestModel, TestThroughModel


class TestPeeWeeModels(TestCase):
    def test_all_fields(self):
        other = OtherTestModel.objects.create(text="OtherTestModel")

        data = dict(
            big_integer_field=123,
            boolean_field=True,
            binary_field=b'',
            char_field='char_text',
            date_field=date(2018, 1, 2),
            date_time_field=datetime(2018, 1, 1, 11, 11),
            decimal_field=Decimal("123.5555"),
            email_field='email@email.com',
            file_field='file',
            file_path_field='file_path',
            float_field=123.123,
            foreign_key=other,
            generic_ipaddress_field='255.255.1.1',
            image_field='image',
            integer_field=12,
            null_boolean_field=True,
            positive_integer_field=12,
            positive_small_integer_field=12,
            slug_field='slug',
            small_integer_field=-12,
            text_field='text_field_value',
            text_field_with_custom_column='text_field_with_custom_column_value',
            time_field=time(1, 1, 50),
            urlfield='https://github.com/SevenLines/django-peewee',
            uuidfield=uuid.uuid4(),
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
                self.assertEqual(other.text, item.foreign_key.text)
            else:
                self.assertEqual(value, getattr(item, key), "wrong {}".format(key))

    def test_many_to_many_permissions(self):
        user = User.objects.create_user("m", "email@email.ru", "123")
        user.user_permissions.add(*Permission.objects.all())

        user_pw = User.pw[user.id]
        for permission in user_pw.user_permissions.where(Permission.pw.name.contains('add')).offset(2).limit(5):
            self.assertIn('add', permission.name)
            self.assertEqual(permission.users.first().email, user.email)
            self.assertEqual(1, permission.users.count())
            self.assertTrue(permission.users.exists())

    def test_through_model(self):
        test_model = TestModel.objects.create()
        other_test_model = OtherTestModel.objects.create(
            text="test_text"
        )

        TestThroughModel.objects.create(
            value="test_value",
            test_model=test_model,
            other_test_model=other_test_model
        )

        through_info = TestModel.pw[test_model.id].others_models.first()
        self.assertEqual("test_text", through_info.text)
        self.assertEqual(1, TestModel.pw[test_model.id].others_models.count())

    def test_custom_table_name(self):
        TestModelWithCustomTableName.objects.create(
            text='hello'
        )

        data = TestModelWithCustomTableName.pw.select().first()
        self.assertEqual('hello', data.text)

        TestModelWithCustomTableName.objects.create(
            text='hello2'
        )

        data = TestModelWithCustomTableName.pw \
            .select(TestModelWithCustomTableName.pw.text) \
            .order_by(TestModelWithCustomTableName.pw.id.desc())\
            .execute()

        self.assertEqual([i.text for i in data], ['hello2', 'hello'])
        self.assertEqual(2, TestModelWithCustomTableName.pw.select().count())
