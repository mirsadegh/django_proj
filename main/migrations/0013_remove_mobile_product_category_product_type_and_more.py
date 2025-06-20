# Generated by Django 5.1.5 on 2025-06-04 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_product_discount_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobile',
            name='product',
        ),
        migrations.AddField(
            model_name='category',
            name='product_type',
            field=models.CharField(choices=[('general', 'عمومی'), ('laptop', 'لپ تاپ'), ('mobile', 'گوشی')], default='general', max_length=10, verbose_name='نوع محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='battery',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='باتری'),
        ),
        migrations.AddField(
            model_name='product',
            name='camera',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='دوربین'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='پردازنده'),
        ),
        migrations.AddField(
            model_name='product',
            name='os',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='سیستم عامل'),
        ),
        migrations.AddField(
            model_name='product',
            name='ram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='حافظه رم'),
        ),
        migrations.AddField(
            model_name='product',
            name='screen_resolution',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='رزولوشن صفحه نمایش'),
        ),
        migrations.AddField(
            model_name='product',
            name='screen_size',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='اندازه صفحه نمایش'),
        ),
        migrations.AddField(
            model_name='product',
            name='storage',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='حافظه داخلی'),
        ),
        migrations.DeleteModel(
            name='Laptop',
        ),
        migrations.DeleteModel(
            name='Mobile',
        ),
    ]
