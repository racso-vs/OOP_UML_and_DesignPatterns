from abc import ABC, abstractmethod


# 1. The Interface (The Blueprint)

class PaymentProcessor(ABC):
    """Abstract base class ensuring all processors have the same methods."""
    
    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Validates the payment details."""
        pass

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        """Processes the payment and calculates fees."""
        pass


# 2. Concrete Implementations

class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        
        if not card_number or len(card_number) != 16:
            return False
        if not cvv or len(cvv) != 3:
            return False
        return True

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid credit card details"}

        # Simulate processing
        fee = amount * 0.029  # 2.9% fee
        total = amount + fee
        return {"success": True, "method": "credit_card", "amount": total, "fee": fee}


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        if not iban or len(iban) < 15:
            return False
        return True

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid bank transfer details"}

        # Simulate processing
        fee = 1.50  # flat fee
        total = amount + fee
        return {"success": True, "method": "bank_transfer", "amount": total, "fee": fee}


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        email = details.get("email")
        if not email or "@" not in email:
            return False
        return True

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal details"}

        # Simulate processing
        fee = amount * 0.034 + 0.30  # 3.4% + 0.30€
        total = amount + fee
        return {"success": True, "method": "paypal", "amount": total, "fee": fee}


# The Factory (The Middleman)

class PaymentFactory:
    """Creates and returns the appropriate payment processor."""
    
    def __init__(self):
        # Dictionary mapping avoids the long if/elif chain
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor
        }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        """Returns an instance of the requested processor."""
        processor_class = self._processors.get(payment_type)
        
        if not processor_class:
            raise ValueError(f"Unknown payment type: {payment_type}")
            
        return processor_class()


# Usage

if __name__ == "__main__":
    # Initialize the factory once
    factory = PaymentFactory()

    # Test Credit Card
    try:
        cc_processor = factory.get_processor("credit_card")
        result = cc_processor.process(100.0, {
            "card_number": "1234567890123456", 
            "cvv": "123"
        })
        print(f"Credit Card Result: {result}")
    except ValueError as e:
        print(e)

    # Test Bank Transfer
    try:
        bank_processor = factory.get_processor("bank_transfer")
        result = bank_processor.process(100.0, {
            "iban": "FR7630006000011234567890189", 
            "bic": "BNPAFRPP"
        })
        print(f"Bank Transfer Result: {result}")
    except ValueError as e:
        print(e)
        
    # Test Invalid Type
    try:
        crypto_processor = factory.get_processor("crypto")
    except ValueError as e:
        print(f"Error Caught: {e}")