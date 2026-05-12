from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('category', models.CharField(choices=[('Food','Food'),('Transport','Transport'),('Shopping','Shopping'),('Health','Health'),('Entertainment','Entertainment'),('Bills','Bills'),('Education','Education'),('Salary','Salary'),('Freelance','Freelance'),('Other','Other')], default='Other', max_length=100)),
                ('date', models.DateField()),
                ('txn_type', models.CharField(choices=[('expense','Expense'),('income','Income')], default='expense', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-date', '-created_at']},
        ),
    ]
