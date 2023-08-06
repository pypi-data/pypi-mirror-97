def a2_min_b2(a, b):
    return (a - b) * (a + b)


def a2_plu_b2(a, b):
    return ((a + b) ** 2) - (2 * a * b)


def a3_min_b3(a, b):
    return (a - b) * (a ** 2 + (a * b) + b ** 2)


def a3_plu_b3(a, b):
    return (a + b) * (a ** 2 - (a * b) + b ** 2)


def a4_min_b4(a, b):
    return (a - b) * (a + b) * (a ** 2 + b ** 2)


def a5_min_b5(a, b):
    return (a - b) * (a ** 4 + ((a ** 3) * b) + ((a ** 2) * (b ** 2)) + (a * (b ** 3)) + b ** 4)


def a_plu_b_2(a, b):
    return a ** 2 + (2 * a * b) + b ** 2


def a_min_b_2(a, b):
    return a ** 2 - (2 * a * b) + b ** 2


def a_plu_b_3(a, b):
    return (a ** 3) + (b ** 3) + (3 * a * b * (a + b))


def a_min_b_3(a, b):
    return (a ** 3) - (b ** 3) - (3 * a * b * (a - b))


def a_plu_b_4(a, b):
    return (a ** 4) + (4 * (a ** 3) * b) + (6 * (a ** 2) * (b ** 2)) + (4 * a * (b ** 3)) + (b ** 4)


def a_min_b_4(a, b):
    return (a ** 4) - (4 * (a ** 3) * b) + (6 * (a ** 2) * (b ** 2)) - (4 * a * (b ** 3)) + (b ** 4)


def a_plu_b_plu_c_2(a, b, c):
    return (a ** 2) + (b ** 2) + (c ** 2) + (2 * a * b) + (2 * b * c) + (2 * c * a)


def a_min_b_min_c_2(a, b, c):
    return (a ** 2) + (b ** 2) + (c ** 2) - (2 * a * b) + (2 * b * c) - (2 * c * a)

