from math import sqrt

# 总体思路，先做聚类，后做协同过滤

def cosine(xs, ys):
    length_1 = len(xs)
    length_2 = len(ys)
    if length_1 != length_2 or length_1 == 0:
        return 0
    x_quadratic_sum = 0  # xs的平方和
    y_quadratic_sum = 0  # ys的平方和
    dot_metrix = 0  # 点积

    x_quadratic_sum = sum([pow(i, 2) for i in xs])
    y_quadratic_sum = sum([pow(i, 2) for i in ys])
    dot_metrix = sum([xs[i] * ys[i] for i in range(length_1)])

    return dot_metrix / sqrt(x_quadratic_sum * y_quadratic_sum)


# -------------------   余弦    -------------------


def euclid(xs, ys):
    length_1 = len(xs)
    length_2 = len(ys)
    if length_1 != length_2 or length_1 == 0:
        return 0
    dvalue = [xs[i] - ys[i] for i in range(length_1)]
    return 1 / (1 + sqrt(sum([pow(dvalue[i], 2) for i in range(len(dvalue))])))


# -------------------   欧几里得距离    -------------------

def pearson(xs, ys):
    length_1 = len(xs)
    length_2 = len(ys)
    if length_1 != length_2 or length_1 == 0:
        return 0
    x_quadratic_sum = 0  # xs的平方和
    y_quadratic_sum = 0  # ys的平方和
    x_sum = 0  # xs的和
    y_sum = 0  # ys的和
    dot_metrix = 0  # 点积

    x_sum = sum(xs)
    y_sum = sum(ys)
    x_quadratic_sum = sum([pow(i, 2) for i in xs])
    y_quadratic_sum = sum([pow(i, 2) for i in ys])
    dot_metrix = sum([xs[i] * ys[i] for i in range(length_1)])

    # 标准差为零
    if length_1 * x_quadratic_sum - pow(x_sum, 2) == 0 or length_1 * y_quadratic_sum - pow(y_sum, 2) == 0:
        return 0

    return (length_1 * dot_metrix - x_sum * y_sum) / sqrt(
        (length_1 * x_quadratic_sum - pow(x_sum, 2)) * (length_1 * y_quadratic_sum - pow(y_sum, 2)))


# -------------------   皮尔逊相关系数    -------------------


def user_correlation_calculation(matrix, method='pearson'):
    users = len(matrix)
    if users == 0:
        return []
    tasks = len(matrix[0])
    m = [[0] * users for i in range(users)]
    for i in range(users):
        for j in range(users):
            if method == 'pearson':
                m[i][j] = pearson(matrix[i], matrix[j])
            if method == 'cos':
                m[i][j] = cosine(matrix[i], matrix[j])
            if method == "eu":
                m[i][j] = euclid(matrix[i], matrix[j])
    return m


if __name__ == '__main__':
    m = [[1, 0, 1], [1, 1, 1], [0, 1, 1]]
    print(user_correlation_calculation(m, method='eu'))
