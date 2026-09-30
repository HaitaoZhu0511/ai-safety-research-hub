"""Hypothetical cost calculator; does not establish equal safety or cash savings."""
import argparse
import math


def calculate(requests=1_000_000, old_rate=0.10, new_rate=0.07,
              unit_cost=0.20, added_daily_cost=1800.0, investment=300_000.0):
    values = (requests, old_rate, new_rate, unit_cost, added_daily_cost, investment)
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or
           not math.isfinite(value) or value < 0 for value in values):
        raise ValueError("Inputs must be finite nonnegative numbers")
    if old_rate > 1 or new_rate > 1 or int(requests) != requests:
        raise ValueError("Rates must be in [0,1]; requests must be integral")
    capacity_value = requests * (old_rate - new_rate) * unit_cost
    net = capacity_value - added_daily_cost
    return {"currency": "CNY", "theoretical_daily_capacity_value": round(capacity_value, 2),
            "net_daily_hypothetical_value": round(net, 2),
            "simple_payback_days": math.ceil(investment / net) if net > 0 else None,
            "quality_validated": False, "cash_savings_validated": False,
            "notice": "Hypothesis only; excludes error losses, seasonality, financing and capacity cash-out."}


if __name__ == "__main__":
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=int, default=1_000_000)
    parser.add_argument("--old-rate", type=float, default=0.10)
    parser.add_argument("--new-rate", type=float, default=0.07)
    parser.add_argument("--unit-cost", type=float, default=0.20)
    parser.add_argument("--added-daily-cost", type=float, default=1800)
    parser.add_argument("--investment", type=float, default=300_000)
    try:
        result = calculate(**vars(parser.parse_args()))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
