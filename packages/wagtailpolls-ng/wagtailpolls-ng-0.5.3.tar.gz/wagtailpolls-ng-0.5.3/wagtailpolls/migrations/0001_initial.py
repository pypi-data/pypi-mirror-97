from __future__ import unicode_literals

from typing import List, Tuple

import django.utils.timezone
import modelcluster.fields
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies: List[Tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Poll",
            fields=[
                ("id", models.AutoField(verbose_name="ID", auto_created=True, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=128)),
                ("date_created", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.AutoField(verbose_name="ID", auto_created=True, primary_key=True, serialize=False)),
                ("question", models.CharField(max_length=128)),
                ("poll", modelcluster.fields.ParentalKey(to="wagtailpolls.Poll", related_name="questions")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                ("id", models.AutoField(verbose_name="ID", auto_created=True, primary_key=True, serialize=False)),
                ("ip", models.GenericIPAddressField()),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("question", modelcluster.fields.ParentalKey(to="wagtailpolls.Question", related_name="votes")),
            ],
        ),
    ]
