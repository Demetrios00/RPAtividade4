# Código com problemas: muita lógica condicional, acoplamento e notificações "hard-coded"

class OrderProcessor:
    def __init__(self, order_type, customer_type, amount):
        self.order_type = order_type
        self.customer_type = customer_type
        self.amount = amount

    def process_order(self):
        # Cálculo de desconto utilizando condicionais
        if self.customer_type == "regular":
            discount = self.amount * 0.05
        elif self.customer_type == "premium":
            discount = self.amount * 0.1
        else:
            discount = 0

        final_amount = self.amount - discount

        # Instanciação de pedidos com base no tipo (condicional)
        if self.order_type == "online":
            order = OnlineOrder(final_amount)
        elif self.order_type == "in-store":
            order = InStoreOrder(final_amount)
        else:
            order = Order(final_amount)

        # Notificação: lógica acoplada ao processamento do pedido
        if final_amount > 100:
            self.send_email_notification(order)
            self.send_sms_notification(order)
        else:
            self.send_email_notification(order)

        return order

    def send_email_notification(self, order):
        print(f"Email: Seu pedido de R$ {order.total} foi processado.")

    def send_sms_notification(self, order):
        print(f"SMS: Seu pedido de R$ {order.total} foi processado.")

class Order:
    def __init__(self, total):
        self.total = total

class OnlineOrder(Order):
    def __init__(self, total):
        super().__init__(total)
        self.delivery = "Envio por correio"

class InStoreOrder(Order):
    def __init__(self, total):
        super().__init__(total)
        self.pickup = "Retirar na loja"

# Uso do código problemático
processor = OrderProcessor("online", "premium", 200)
order = processor.process_order()
