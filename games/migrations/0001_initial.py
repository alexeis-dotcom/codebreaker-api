from django.db import migrations, models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=4, unique=True, validators=[django.core.validators.RegexValidator(regex="^\\d{4}$", message="Code must be exactly 4 digits.")])),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

