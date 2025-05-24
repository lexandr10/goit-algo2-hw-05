import time
import re
from hyperloglog import HyperLogLog

def load_ip_addresses_from_log(file_path: str) -> list[str]:
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    ip_addresses = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ip_addresses.append(match.group(0))

    return ip_addresses

def count_unique_ips_exact(ip_list: list[str]) -> tuple[int, float]:
    start = time.time()
    unique_ips = set(ip_list)
    duration = time.time() - start
    return len(unique_ips), duration

def count_unique_ips_hll(ip_list: list[str], error_rate: float = 0.01) -> tuple[float, float]:
    start = time.time()
    hll = HyperLogLog(error_rate)
    for ip in ip_list:
        hll.add(ip)
    duration = time.time() - start
    return float(len(hll)), duration

def print_comparison_table(exact_count: int, exact_time: float, hll_count: float, hll_time: float):
    print("\nРезультати порівняння:")
    print(f"{'':<30}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<30}{exact_count:<20}{round(hll_count, 2):<20}")
    print(f"{'Час виконання (сек.)':<30}{round(exact_time, 4):<20}{round(hll_time, 4):<20}")

if __name__ == "__main__":
    file_path = "lms-stage-access.log"  # Переконайся, що файл знаходиться тут

    print("Завантаження IP-адрес із лог-файлу...")
    ip_addresses = load_ip_addresses_from_log(file_path)
    print(f"Загальна кількість записів: {len(ip_addresses)}")

    print("\nВиконуємо точний підрахунок...")
    exact_count, exact_time = count_unique_ips_exact(ip_addresses)

    print("Виконуємо підрахунок за допомогою HyperLogLog...")
    hll_count, hll_time = count_unique_ips_hll(ip_addresses)

    print_comparison_table(exact_count, exact_time, hll_count, hll_time)