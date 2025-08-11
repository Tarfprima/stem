from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stem', '0002_alter_task_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
    ]

