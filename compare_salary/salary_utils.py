

def predict_rub_salary(salaries_range):
    tax = salaries_range[2]
    salaries_range = list(map(lambda x: x if x is not None else 0, salaries_range))
    if salaries_range[0] != 0 and salaries_range[1] != 0:
        return (salaries_range[0] + salaries_range[1]) / 2 * tax
    elif salaries_range[0] == 0:
        return salaries_range[1] * 0.8 * tax
    else:
        return salaries_range[0] * 1.2 * tax
