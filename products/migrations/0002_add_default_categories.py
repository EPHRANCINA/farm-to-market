from django.db import migrations

def add_default_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    categories = [
        ('Vegetables', 'Fresh vegetables from local farms'),
        ('Fruits', 'Fresh fruits from local farms'),
        ('Dairy', 'Fresh dairy products'),
        ('Meat', 'Fresh meat products'),
        ('Grains', 'Fresh grains and cereals'),
        ('Other', 'Other farm products')
    ]
    for name, description in categories:
        Category.objects.get_or_create(name=name, description=description)

def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
    ] 