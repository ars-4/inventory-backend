import json
from core.models import Balance, OrderProduct, Product

def get_total_cash():
    cashed_in_balance_objects = Balance.objects.filter(balance='cashed')
    current_cash = 0
    for cash in cashed_in_balance_objects:
        current_cash = current_cash + int(cash.bill)
    return current_cash

def equalize(bill, expense, special_field="null"):
    cashed_objects = Balance.objects.filter(balance='cashed')
    current_cash = bill - expense
    equal_amount = current_cash / cashed_objects.count()
    for cash in cashed_objects:
        balance = Balance.objects.get(id=cash.id)
        balance.bill = str(int(equal_amount))
        balance.save()
    

def generate_balances(sale, purchase):
    current_cash = get_total_cash()
    sale = sale
    purchase = purchase
    profit = sale - purchase
    expense = purchase
    equalize(current_cash, expense)
    generate_sale(sale)
    generate_expense(expense)
    generate_profit(profit)


def generate_sale(bill, special_field="null"):
    Balance.objects.create(
        title="Auto Generated Sale Balance",
        description="generated_automatically_for_sales",
        bill=str(bill),
        balance="sale",
        special_field=special_field
    ).save()

def generate_expense(bill, special_field="null"):
    Balance.objects.create(
        title="Auto Generated Expense",
        description="generated_automatically_for_calculating_expense",
        bill=str(bill),
        balance="expense",
        special_field=special_field
    ).save()

def generate_profit(bill, special_field="null"):
    Balance.objects.create(
        title="Auto Generated Profit",
        description="generated_automatically_for_calculating_profit",
        bill=str(bill),
        balance="profit",
        special_field=special_field
    ).save()


def generate_from_order_product(product_id, quantity):
    cash_in_hand = get_total_cash()
    product = Product.objects.get(id=product_id)
    product.stock = str(int(product.stock) - int(quantity))
    product.save()
    sale_bill = int(product.sale_price) * int(quantity)
    purchase_bill = int(product.purchase_price) * int(quantity)
    order_product = OrderProduct.objects.create(
        product=product,
        quantity=quantity,
        sale_bill=str(sale_bill),
        purchase_bill=str(purchase_bill)
    )
    order_product.save()
    special_field = f"order_product_id_{order_product.id}"
    generate_sale(sale_bill, special_field)
    generate_profit(sale_bill-purchase_bill, special_field)
    # equalize(cash_in_hand, purchase_bill, special_field)
    return order_product