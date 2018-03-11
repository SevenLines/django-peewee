from django.apps import AppConfig
import django.apps
import peewee
from django.db.models import DecimalField
from peewee import SqliteDatabase, PostgresqlDatabase, DeferredForeignKey, ManyToManyField, ManyToManyQuery
from django.db import connections

DATA_TYPES = {
    'AutoField': peewee.AutoField,
    'BigAutoField': peewee.BigIntegerField,
    'BigIntegerField': peewee.BigIntegerField,
    'BooleanField': peewee.BooleanField,
    'BinaryField': peewee.BlobField,
    'CharField': peewee.FixedCharField,
    'CommaSeparatedIntegerField': peewee.CharField,
    'DateField': peewee.DateField,
    'DateTimeField': peewee.DateTimeField,
    'DecimalField': lambda *args, **kwargs: peewee.DecimalField(*args, **kwargs),
    # 'DurationField': '',
    'EmailField': peewee.CharField,

    'FileField': peewee.CharField,
    'FilePathField': peewee.CharField,
    'FloatField': peewee.FloatField,
    'ForeignKey': peewee.DeferredForeignKey,  # для избежания циклических зависимостей

    'GenericIPAddressField': peewee.CharField,
    'IPAddressField': peewee.IPField,
    'ImageField': peewee.CharField,
    'IntegerField': peewee.IntegerField,
    'ManyToManyField': ManyToManyField,
    'NullBooleanField': lambda *args, **kwargs: peewee.BooleanField(null=True, *args, **kwargs),
    'OneToOneField': peewee.DeferredForeignKey,
    # 'OrderWrt': '',
    'PositiveIntegerField': peewee.IntegerField,
    'PositiveSmallIntegerField': peewee.SmallIntegerField,
    'SlugField': peewee.CharField,
    'SmallIntegerField': peewee.SmallIntegerField,
    'TextField': peewee.TextField,
    'TimeField': peewee.TimeField,
    'URLField': peewee.CharField,
    'UUIDField': peewee.UUIDField,
}

DATABASE_DRIVERS = {
    'sqlite': SqliteDatabase,
    'postgresql': PostgresqlDatabase,
}


class DatabaseProxy(object):
    def __init__(self, database):
        self.database = database
        self.connection = getattr(connections._connections, database)
        self.Klass = DATABASE_DRIVERS[self.connection.vendor](database)
        self.Klass._connect = self._connect

    def __getattr__(self, name):
        return getattr(self.Klass, name)

    def _connect(self):
        return self.connection.connection

    def execute(self, *args, **kwargs):
        return getattr(self.Klass, 'execute')(commit=False, *args, **kwargs)


class ProxyModel(peewee.Model):
    @classmethod
    def select(cls, *fields):
        query = super().select(*fields)
        query._database = DatabaseProxy(cls._meta.peewee_database_alias)
        return query


# class ProxyManyToManyQuery(ManyToManyQuery):


class DjangoPeeweeConfig(AppConfig):
    name = 'django_peewee'

    PEEWEE_MODELS_CACHE = {}

    def get_klass_name(self, model):
        return "Peewee{}".format(model._meta.object_name)

    def get_many_to_many_model(self, many_to_many_descriptor):
        model = many_to_many_descriptor.through
        class_inner = self.get_peewee_class_inner(model, use_deffered=False)
        return type(
            self.get_klass_name(model),
            (ProxyModel,),
            class_inner
        )

    def get_peewee_class_inner(self, model, use_deffered=True):
        class_inner = {}

        for field in model._meta.fields:
            if field.__class__.__name__ in DATA_TYPES:
                data_type = DATA_TYPES[field.__class__.__name__]
                args = []
                kwargs = {
                    "column_name": field.column
                }
                if field.related_model:
                    if use_deffered:
                        args.append(self.get_klass_name(field.related_model))
                    else:
                        args.append(self.PEEWEE_MODELS_CACHE[field.related_model])
                        data_type = peewee.ForeignKeyField
                elif isinstance(field, DecimalField):
                    kwargs['decimal_places'] = field.decimal_places
                    kwargs['max_digits'] = field.max_digits

                class_inner[field.name] = data_type(*args, **kwargs)
            class_inner['Meta'] = type('Meta', (object,), {
                "table_name": model._meta.db_table,
                "peewee_database_alias": getattr(model._meta, 'peewee_database_alias', 'default'),
            })

        return class_inner

    def ready(self):
        models = [model for model in django.apps.apps.get_models() if not model._meta.proxy]

        # resolve simple fields
        for model in models:
            model.pw = type(
                self.get_klass_name(model),
                (ProxyModel,),
                self.get_peewee_class_inner(model)
            )
            self.PEEWEE_MODELS_CACHE[model] = model.pw

        # resolve deferred foreign keys
        for model in models:
            DeferredForeignKey.resolve(model.pw)

        # resolve many_to_many fields
        for model in models:
            meta = model._meta
            for field in meta.many_to_many:
                peewee_model = self.PEEWEE_MODELS_CACHE[model]
                through_model = self.get_many_to_many_model(getattr(model, field.column))
                peewee_model._meta.add_field(field.column, peewee.ManyToManyField(
                    self.PEEWEE_MODELS_CACHE[field.related_model],
                    through_model=through_model
                ))



