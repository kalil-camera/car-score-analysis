"""Pricing domain - Value Objects"""
from enum import Enum
from decimal import Decimal
from datetime import datetime
from app.shared.types import ValueObject
from app.shared.exceptions import InvalidValueObjectError


class Currency(str, Enum):
    """Currency value object"""
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"


class PriceSource(str, Enum):
    """Price source value object"""
    FIPE = "FIPE"
    WEB_SCRAPE = "WebScrape"
    API = "API"
    USER = "User"


class MarketType(str, Enum):
    """Market type value object"""
    NOVO = "Novo"
    USADO = "Usado"


class Price(ValueObject):
    """Price value object (imutável)"""
    
    def __init__(self, amount: float, currency: Currency = Currency.BRL):
        if amount < 0:
            raise InvalidValueObjectError(f"Price cannot be negative: {amount}")
        self.amount = Decimal(str(amount))
        self.currency = currency
    
    def __float__(self):
        return float(self.amount)
    
    def __str__(self):
        return f"{self.currency.value} {self.amount}"


class PriceRecord(ValueObject):
    """Price record - imutável, representa um ponto no tempo"""
    
    def __init__(
        self,
        price: Price,
        source: PriceSource,
        market_type: MarketType,
        recorded_at: datetime = None
    ):
        self.price = price
        self.source = source
        self.market_type = market_type
        self.recorded_at = recorded_at or datetime.utcnow()
    
    def __str__(self):
        return f"{self.price} ({self.source.value}, {self.market_type.value}) at {self.recorded_at}"
