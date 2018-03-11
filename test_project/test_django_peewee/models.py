from django.db import models

# Create your models here.
from django.db import models
from django.db.models import SET_NULL


class OtherTestModel(models.Model):
    text = models.TextField()


class TestModel(models.Model):
    # auto_field = models.AutoField(null=True)
    # big_auto_field = models.BigAutoField(null=True)
    big_integer_field = models.BigIntegerField(null=True)
    boolean_field = models.BooleanField(default=False)
    binary_field = models.BinaryField(null=True)
    char_field = models.CharField(null=True, max_length=50)
    # comma_separated_integer_field = models.CommaSeparatedIntegerField(null=True) # depricated
    date_field = models.DateField(null=True)
    date_time_field = models.DateTimeField(null=True)
    decimal_field = models.DecimalField(null=True, decimal_places=5, max_digits=10)
    email_field = models.EmailField(null=True)
    file_field = models.FileField(null=True)
    file_path_field = models.FilePathField(null=True)
    float_field = models.FloatField(null=True)
    foreign_key = models.ForeignKey("OtherTestModel", on_delete=SET_NULL, null=True)
    generic_ipaddress_field = models.GenericIPAddressField(null=True)
    image_field = models.ImageField(null=True)
    integer_field = models.IntegerField(null=True)
    null_boolean_field = models.NullBooleanField(null=True)
    positive_integer_field = models.PositiveIntegerField(null=True)
    positive_small_integer_field = models.PositiveSmallIntegerField(null=True)
    slug_field = models.SlugField(null=True)
    small_integer_field = models.SmallIntegerField(null=True)
    text_field = models.TextField(null=True)
    text_field_with_custom_column = models.TextField(null=True, db_column='text_field_with_custom_column')
    time_field = models.TimeField(null=True)
    urlfield = models.URLField(null=True)
    uuidfield = models.UUIDField(null=True)

    others_models = models.ManyToManyField(OtherTestModel, through='TestThroughModel', related_name="test_models")


class TestThroughModel(models.Model):
    value = models.CharField(max_length=100, null=True)
    other_test_model = models.ForeignKey(OtherTestModel, on_delete=SET_NULL, null=True)
    test_model = models.ForeignKey(TestModel, on_delete=SET_NULL, null=True)


class TestModelWithCustomTableName(models.Model):
    text = models.CharField(max_length=100)

    class Meta:
        db_table = "custom_table_name"
