import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CMSLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "action",
                    models.PositiveIntegerField(
                        max_length=10,
                        choices=[
                            (0, b"Save"),
                            (2, b"Delete"),
                            (3, b"Published"),
                            (4, b"Unpublished"),
                            (5, b"Scheduled"),
                        ],
                    ),
                ),
                ("action_date", models.DateTimeField(null=True, blank=True)),
                ("model_repr", models.CharField(max_length=255)),
                ("object_repr", models.CharField(max_length=255)),
                ("url", models.CharField(max_length=255, blank=True)),
                ("section", models.CharField(max_length=255, blank=True)),
                ("user_name", models.CharField(max_length=255)),
                ("when", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
