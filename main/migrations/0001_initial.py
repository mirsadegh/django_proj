# Generated by Django 5.1.5 on 2025-02-13 12:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="دسته\u200cبندی"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, unique=True, verbose_name="آدرس یکتا"
                    ),
                ),
            ],
            options={
                "verbose_name": "دسته بندی",
                "verbose_name_plural": "دسته\u200cبندی\u200cها",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="عنوان")),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, unique=True, verbose_name="آدرس یکتا"
                    ),
                ),
                ("description", models.TextField(verbose_name="توضیحات")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="قیمت"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="product_images",
                        verbose_name="تصویر محصول",
                    ),
                ),
                ("available", models.BooleanField(default=True, verbose_name="موجود")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="main.category",
                        verbose_name="دسته\u200cبندی",
                    ),
                ),
            ],
            options={
                "verbose_name": "محصول",
                "verbose_name_plural": "محصولات",
            },
        ),
        migrations.CreateModel(
            name="Laptop",
            fields=[
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="laptop_details",
                        serialize=False,
                        to="main.product",
                        verbose_name="محصول مرتبط",
                    ),
                ),
                ("cpu", models.CharField(max_length=100, verbose_name="پردازنده")),
                ("ram", models.CharField(max_length=50, verbose_name="حافظه رم")),
                (
                    "storage",
                    models.CharField(max_length=50, verbose_name="حافظه داخلی"),
                ),
                (
                    "screen_size",
                    models.CharField(max_length=50, verbose_name="اندازه صفحه نمایش"),
                ),
            ],
            options={
                "verbose_name": "لپ تاپ",
                "verbose_name_plural": "لپتاپ ها",
            },
        ),
        migrations.CreateModel(
            name="Mobile",
            fields=[
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="mobile_details",
                        serialize=False,
                        to="main.product",
                        verbose_name="محصول مرتبط",
                    ),
                ),
                ("os", models.CharField(max_length=50, verbose_name="سیستم عامل")),
                ("camera", models.CharField(max_length=50, verbose_name="دوربین")),
                ("battery", models.CharField(max_length=50, verbose_name="باتری")),
                (
                    "screen_resolution",
                    models.CharField(max_length=50, verbose_name="رزولوشن صفحه نمایش"),
                ),
            ],
            options={
                "verbose_name": "گوشی",
                "verbose_name_plural": "گوشیها",
            },
        ),
    ]
