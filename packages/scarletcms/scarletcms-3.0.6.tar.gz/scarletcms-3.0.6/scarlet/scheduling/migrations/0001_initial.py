from django.db import migrations, models

import scarlet.scheduling.fields


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
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
                ("object_args", scarlet.scheduling.fields.JSONField()),
                ("when", models.DateTimeField()),
                ("action", models.CharField(max_length=255, null=True)),
                ("json_args", scarlet.scheduling.fields.JSONField()),
                (
                    "content_type",
                    models.ForeignKey(
                        to="contenttypes.ContentType",
                        on_delete=models.deletion.CASCADE,
                    ),
                ),
            ],
        ),
    ]
