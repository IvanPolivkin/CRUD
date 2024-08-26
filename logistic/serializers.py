from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta: # настройте сериализатор для продукта
        model = Product
        fields = ['title', 'description']
    pass


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta: # настройте сериализатор для позиции продукта на складе
        model = StockProduct
        fields = ['product', 'quantity', 'price']
    pass


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address', 'positions']
    # настройте сериализатор для склада



    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for i in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': i['quantity'], 'price': i['price']},
                                                  product=i['product'], stock=stock)


        return stock
