"""Tipos e ValueObjects basic compartilhados"""
from typing import TypeVar, Generic

T = TypeVar("T")


class ValueObject:
    """Base class para todos Value Objects"""
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Entity:
    """Base class para todas Entities"""
    
    def __init__(self, id: int = None):
        self.id = id
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


class AggregateRoot(Entity):
    """Base class para Aggregate Roots"""
    
    def __init__(self, id: int = None):
        super().__init__(id)
        self._domain_events: list = []
    
    def add_domain_event(self, event):
        """Adiciona um domain event"""
        self._domain_events.append(event)
    
    def get_domain_events(self):
        """Retorna e limpa domain events"""
        events = self._domain_events[:]
        self._domain_events = []
        return events


class Result(Generic[T]):
    """Result type para operações que podem falhar"""
    
    def __init__(self, success: bool, value: T = None, error: str = None):
        self.success = success
        self.value = value
        self.error = error
    
    @staticmethod
    def ok(value: T) -> "Result[T]":
        return Result(success=True, value=value)
    
    @staticmethod
    def fail(error: str) -> "Result":
        return Result(success=False, error=error)
