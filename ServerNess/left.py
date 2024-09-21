import datetime

def calculate_days_left(target_date):
    today = datetime.date.today()
    remaining_days = (target_date - today).days
    return remaining_days

# 示例用法
target_date = datetime.date(2025, 1, 1)
days_left = calculate_days_left(target_date)
print(f"距离目标日期还有 {days_left} 天。")
