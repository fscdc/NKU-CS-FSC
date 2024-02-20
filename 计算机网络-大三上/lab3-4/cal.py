import decimal


def divide_numbers(divisor, *numbers):
    # 设置decimal为6位有效数字
    decimal.getcontext().prec = 6
    return [float(decimal.Decimal(divisor) / decimal.Decimal(num)) for num in numbers]


divisor = 1857353.2
numbers_to_divide = [6101]
results = divide_numbers(divisor, *numbers_to_divide)
print(results)
