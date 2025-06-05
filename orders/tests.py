import pytest

from orders.models import Product, Order, OrderItem
from accounting.tests.test_api_accounts import get_authenticated_client

@pytest.mark.django_db
def test_create_order():
    client = get_authenticated_client()

    # Создаём продукты
    product1 = Product.objects.create(name="Product A", price=10.00)
    product2 = Product.objects.create(name="Product B", price=5.00)

    # Отправляем POST-запрос на создание заказа
    response = client.post("/api/orders/", {
        "items": [
            {"product": product1.id, "quantity": 2},
            {"product": product2.id, "quantity": 3},
        ]
    }, format="json")

    assert response.status_code == 201
    order_id = response.data["id"]
    total = response.data["total_price"]

    # Проверим общую сумму
    expected_total = 2 * 10.00 + 3 * 5.00
    assert float(total) == expected_total

    # Проверим количество записей
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 2
    
    
    
@pytest.mark.django_db
def test_confirm_order():
    client = get_authenticated_client()

    product = Product.objects.create(name="Product C", price=20.00)

    response = client.post("/api/orders/", {
        "items": [
            {"product": product.id, "quantity": 1}
        ]
    }, format="json")
    order_id = response.data["id"]

    confirm_url = f"/api/orders/{order_id}/confirm/"
    confirm_response = client.post(confirm_url)

    assert confirm_response.status_code == 200
    assert confirm_response.data["status"] == "Order confirmed"

    # Проверим статус в базе
    from orders.models import Order
    order = Order.objects.get(id=order_id)
    assert order.status == "confirmed"

