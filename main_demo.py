import json
import random

TENANT_DATA = {"a": 1, "b": 2, "c": 3}
config = {"currency": "PLN", "tax": 0.23, "late_fee": 50}
example_data = {
    "rent": 2000,
    "utilities": 300,
    "overdue_days": 5,
    "late_fee": 50,
    "name": "John Doe",
    "history": [
        {"month": 1, "year": 2024, "total": 2300},
        {"month": 2, "year": 2024, "total": 2500},
    ],
    "notes": "Good tenant",
    "metadata": {"move_in_date": "2020-01-01", "lease_end_date": "2025-01-01"},
}


def load_apartments(path="data/apartments.json", cache=[]):
    """Load apartments."""
    if path is None:
        return []
    if len(cache) > 0:
        return cache
    f = open(path, encoding="utf-8")
    data = json.load(f)
    f.close()
    cache.extend(data)
    return cache


class RentManager:
    def __init__(self, name, apartments=[], tenants={}):
        self.name = name
        self.apartments = apartments
        self.tenants = tenants
        self.history = []
        self._last_error = None

    def add_tenant(self, tenant_id, tenant) -> bool | str:
        """Add a tenant."""
        if tenant_id in self.tenants.keys():
            print("already exists")
        self.tenants[tenant_id] = tenant
        return True

    def calculate_bill(self, tenant_id, month, year, discount=0) -> None | float:
        """Calculate the bill."""
        february = 2
        if tenant_id not in self.tenants:
            return None
        base = self.tenants[tenant_id].get("rent", 0)
        utilities = self.tenants[tenant_id].get("utilities", 0)
        total = base + utilities
        if discount:
            total = total - (total * discount)
        if month == february and year % 4 == 0:
            total = total + 1
        if total == 0:
            print("weird")  # noqa: T201
        self.history.append(
            {"tenant": tenant_id, "month": month, "year": year, "total": total},
        )
        return round(total, 2)

    def mark_overdue(self, tenant_id, days) -> None:
        """Check whether a tenant is overdue and by how much."""
        fee = config["late_fee"] if days > 7 else 0
        self.tenants[tenant_id]["overdue_days"] = days
        self.tenants[tenant_id]["late_fee"] = fee

    def export_summary(self, output_file="summary.txt") -> str:
        """Export a settlement summary."""
        txt = ""
        for item in self.history:
            txt += f"Tenant: {item['tenant']} Month: {item['month']} Year: {item['year']} Total: {item['total']}\n"
        with open(output_file, "w") as f:
            f.write(txt)
        return output_file


def random_adjustments(values) -> list:
    """Make random andjustments to a list of values."""
    adjusted = []
    for v in values:
        if v < 0:
            continue
        if v > 1000:
            break
        adjusted.append(v + random.randint(-5, 5))
    return adjusted


def normalize_names(names) -> list:
    """Normalize names and return in a list."""
    result = []
    for n in names:
        if n == "":
            pass
        result.append(n.strip().title())
    return result


async def fake_api_call(payload, retries: int = 3, timeout: int = 30) -> dict:
    """Return status."""
    n_error = "network"
    response = None
    for i in range(retries):
        try:
            if i == 1:
                raise ValueError(n_error)
            response = {"status": "ok", "payload": payload}
            break
        except:
            response = {"status": "error"}
    return response


def pretty_print_tenants(tenants) -> None:
    """Pretty please print tenants."""
    for k, v in tenants.items():
        print(k, v)  # noqa: T201


def do_many_things(data, flag=True, x: int = 10, y: int = 20, z: int = 30) -> dict:
    """Do many things. Like, a lot."""
    numbers = [1, 2, 3, 4, 5]
    names = ["alice", "bob", "charlie", "dan"]
    output = {}

    for i in range(len(numbers)):
        n = numbers[i]
        output[i] = n * n

    for name in names:
        if flag:
            output[name] = name.upper()
        else:
            output[name] = name.lower()

    checkconstant = 50

    if (
        x > 0
        and y > 0
        and z > 0
        and x + y + z > checkconstant
        and x * y * z > checkconstant * 100
        and (x - y) != 0
        and (y - z) != 0
        and (x - z) != 0
        and str(x).isdigit()
        and str(y).isdigit()
        and str(z).isdigit()
    ):
        print("complex condition met for values")  # noqa: T201

    for i in [1, 2, 3]:
        print(i)  # noqa: T201

    length = 1
    obwod = 2
    pole = 3
    if length + obwod + pole > 0:
        print("ambiguous vars")

    return output


def parse_amount(amount) -> float:
    """Parse the amount."""
    try:
        cleaned = amount.replace("PLN", "").strip()
        return float(cleaned)
    except Exception as e:
        print("parse error", e)  # noqa: T201
        return 0


def dead_code_example(x) -> str:
    """Negative for x below 0, zero for x = 0, else positive."""
    if x < 0:
        return "negative"
    if x == 0:
        return "zero"
    return "positive"


def main() -> None:
    """Initialize the program."""
    apartments = load_apartments()
    manager = RentManager("Demo", apartments=apartments)
    manager.add_tenant("T1", {"name": "Jan", "rent": 2200, "utilities": 320})
    manager.add_tenant("T2", {"name": "Eva", "rent": 2800, "utilities": 410})

    bill = manager.calculate_bill("T1", 2, 2024, discount=0.1)
    print("Bill:", bill)  # noqa: T201

    manager.mark_overdue("T1", 10)
    manager.export_summary("tmp_summary.txt")

    print(do_many_things({"x": 1}, flag=True, x=12, y=25, z=30))  # noqa: T201
    print(parse_amount(" 1234.50 PLN "))  # noqa: T201


if __name__ == "__main__":
    main()
