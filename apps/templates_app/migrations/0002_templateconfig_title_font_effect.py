from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templates_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateconfig',
            name='title_font_effect',
            field=models.CharField(default='none', max_length=30),
        ),
    ]
