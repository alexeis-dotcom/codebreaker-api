from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="attempts_used",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="game",
            name="is_solved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="game",
            name="max_attempts",
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.CreateModel(
            name="GameGuess",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guess", models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex="^\\d{4}$", message="Guess must be exactly 4 digits.")])),
                ("well_placed", models.PositiveSmallIntegerField()),
                ("misplaced", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("game", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="guesses", to="games.game")),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
    ]

