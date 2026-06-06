"""Simple Stock Portfolio Tracker

Scope (simplified):
- User inputs stock names and quantity (interactive CLI)
- Hardcoded dictionary of stock prices (USD)
- Calculates total investment
- Optionally saves result to .txt or .csv

Run:
  python stock_tracker.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple


PRICE_DICT: Dict[str, float] = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 420,
    "AMZN": 170,
}


@dataclass(frozen=True)
class Holding:
    symbol: str
    quantity: float
    unit_price: float

    @property
    def cost(self) -> float:
        return self.quantity * self.unit_price


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def prompt_holdings(prices: Dict[str, float]) -> List[Holding]:
    holdings: List[Holding] = []

    print("Enter your holdings. Type 'done' when finished.\n")
    while True:
        symbol_raw = input("Stock symbol (e.g., AAPL) or 'done': ").strip()
        if symbol_raw.lower() == "done":
            break

        symbol = normalize_symbol(symbol_raw)
        if symbol not in prices:
            print(f"Unknown symbol '{symbol}'. Available: {', '.join(sorted(prices.keys()))}\n")
            continue

        qty_raw = input(f"Quantity for {symbol}: ").strip()
        try:
            quantity = float(qty_raw)
        except ValueError:
            print("Invalid quantity. Please enter a number.\n")
            continue

        if quantity < 0:
            print("Quantity cannot be negative.\n")
            continue

        holdings.append(Holding(symbol=symbol, quantity=quantity, unit_price=prices[symbol]))
        print("Added.\n")

    return holdings


def compute_total(holdings: List[Holding]) -> float:
    return sum(h.cost for h in holdings)


def prompt_save_option() -> Optional[str]:
    print("\nOptional: save results to a file")
    choice = input("Save? Type 'txt', 'csv', or 'none': ").strip().lower()

    if choice in {"none", "no", "skip", ""}:
        return None
    if choice in {"txt", "csv"}:
        return choice
    print("Unrecognized option. No file will be saved.")
    return None


def save_to_txt(path: str, holdings: List[Holding], total: float) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"Stock Portfolio Tracker ({now})",
        "-" * 40,
    ]
    for h in holdings:
        lines.append(
            f"{h.symbol}: qty={h.quantity:g} @ {h.unit_price:g} => cost={h.cost:g}"
        )
    lines.append("-" * 40)
    lines.append(f"TOTAL INVESTMENT: {total:g}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def save_to_csv(path: str, holdings: List[Holding], total: float) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["generated_at", now])
        writer.writerow([])
        writer.writerow(["symbol", "quantity", "unit_price", "cost"])
        for h in holdings:
            writer.writerow([h.symbol, h.quantity, h.unit_price, h.cost])
        writer.writerow([])
        writer.writerow(["TOTAL_INVESTMENT", total])


def main() -> None:
    print("=== Simple Stock Portfolio Tracker ===")

    holdings = prompt_holdings(PRICE_DICT)
    total = compute_total(holdings)

    print("\n=== Results ===")
    if not holdings:
        print("No holdings entered. Total investment = 0")
    else:
        for h in holdings:
            print(f"{h.symbol}: qty={h.quantity:g}, unit_price={h.unit_price:g}, cost={h.cost:g}")
        print(f"TOTAL INVESTMENT: {total:g}")

    save_choice = prompt_save_option()
    if save_choice is None or not holdings:
        print("No file saved.")
        return

    filename_base = "portfolio_result"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if save_choice == "txt":
        path = f"{filename_base}_{timestamp}.txt"
        save_to_txt(path, holdings, total)
        print(f"Saved: {path}")
    elif save_choice == "csv":
        path = f"{filename_base}_{timestamp}.csv"
        save_to_csv(path, holdings, total)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()

