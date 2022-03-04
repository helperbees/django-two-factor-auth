import django.db.models.deletion
import django_otp.util
from django.conf import settings
from django.db import migrations, models

from two_factor.abstracts import key_validator


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                ('throttling_failure_timestamp', models.DateTimeField(
                    blank=True, default=None,
                    help_text='A timestamp of the last failed verification attempt. Null if last attempt succeeded.',
                    null=True
                )),
                ('throttling_failure_count',
                 models.PositiveIntegerField(default=0, help_text='Number of successive failed attempts.')),
                ('key', models.CharField(
                    default=django_otp.util.random_hex, help_text='Hex-encoded secret key', max_length=40,
                    validators=[key_validator]
                )),
                ('user', models.ForeignKey(
                    help_text='The user that this device belongs to.',
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]
