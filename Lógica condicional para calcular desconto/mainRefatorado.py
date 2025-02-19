from abc import ABC, abstractmethod

# === Padrão Strategy: Cálculo de Desconto === 
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, amount):
        pass

class RegularDiscount(DiscountStrategy):
    def calculate_discount(self, amount):
        return amount * 0.05

class PremiumDiscount(DiscountStrategy):
    def calculate_discount(self, amount):
        return amount * 0.1

class NoDiscount(DiscountStrategy):
    def calculate_discount(self, amount):
        return 0

# === Padrão Factory: Criação de Pedidos ===
class OrderFactory:
    @staticmethod
    def create_order(order_type, total):
        if order_type == "online":
            return OnlineOrder(total)
        elif order_type == "in-store":
            return InStoreOrder(total)
        else:
            return Order(total)

# === Padrão Observer: Notificações desacopladas ===
class Observer(ABC):
    @abstractmethod
    def update(self, order):
        pass

class EmailNotifier(Observer):
    def update(self, order):
        print(f"Email: Seu pedido de R$ {order.total} foi processado.")

class SMSNotifier(Observer):
    def update(self, order):
        print(f"SMS: Seu pedido de R$ {order.total} foi processado.")

class NotificationSubject:
    def __init__(self):
        self.observers = []

    def register(self, observer: Observer):
        self.observers.append(observer)

    def notify(self, order):
        for observer in self.observers:
            observer.update(order)

# === Classes de Pedido ===
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

# === Classe Principal Refatorada ===
class OrderProcessor:
    def __init__(self, order_type, discount_strategy: DiscountStrategy, amount):
        self.order_type = order_type
        self.discount_strategy = discount_strategy
        self.amount = amount
        self.notification_subject = NotificationSubject()

    def process_order(self):
        # Calcula o desconto utilizando o Strategy
        discount = self.discount_strategy.calculate_discount(self.amount)
        final_amount = self.amount - discount

        # Cria o pedido utilizando a Factory
        order = OrderFactory.create_order(self.order_type, final_amount)

        # Registra os observadores (notificadores) conforme o valor final
        self.notification_subject.register(EmailNotifier())
        if final_amount > 100:
            self.notification_subject.register(SMSNotifier())

        # Notifica os observadores
        self.notification_subject.notify(order)
        return order

# === Uso do Código Refatorado ===
processor = OrderProcessor("online", PremiumDiscount(), 200)
order = processor.process_order()
