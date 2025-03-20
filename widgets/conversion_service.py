# File: conversion_service.py
import requests

class CurrencyConverter:
    def __init__(self, base_currency="EUR"):
        self.base_currency = base_currency.upper()
        self.rates = {}
        self._fetch_rates()
        self.i = 0

    def _fetch_rates(self):
        """Fetches exchange rates once at initialization and stores them."""
        api_url = f"https://api.exchangerate-api.com/v4/latest/{self.base_currency}"
        try:
            response = requests.get(api_url)
            data = response.json()
            self.rates = data.get("rates", {})
            print(f"Fetched exchange rates")
        except Exception as e:
            print(f"Error fetching exchange rates during initialization: {e}")
            # Fallback: use a default rate of 1.0 for any currency.
            self.rates = {}

    def get_rate(self, target_currency: str) -> float:
        """Returns the stored rate for the target currency or 1.0 if not found."""
        target_currency = target_currency.upper()
        return self.rates.get(target_currency, 1.0)


class UnitConverter:
    def __init__(self):
        # Conversion factors relative to a standard unit:
        # For weight: kilograms; for volume: liters.
        self.weight_conversion = {"kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495}
        self.volume_conversion = {"l": 1, "ml": 0.001, "fl oz": 0.0295735, "gal": 3.78541}

    def convert(self, unit: str, quantity: float) -> float:
        unit_lower = unit.lower()
        if unit_lower in self.weight_conversion:
            return quantity * self.weight_conversion[unit_lower]
        elif unit_lower in self.volume_conversion:
            return quantity * self.volume_conversion[unit_lower]
        else:
            return quantity  # If unknown, no conversion


class ConversionService:
    def __init__(self, base_currency="EUR"):
        self.currency_converter = CurrencyConverter(base_currency)
        self.unit_converter = UnitConverter()

    def convert_currency(self, amount: float, target_currency: str) -> float:
        """Converts the given amount from the base currency (EUR) to the target currency."""
        rate = self.currency_converter.get_rate(target_currency)
        return amount * rate

    def convert_unit(self, unit: str, quantity: float) -> float:
        """Converts the given quantity into its standardized unit (kg for weight, l for volume)."""
        return self.unit_converter.convert(unit, quantity)
