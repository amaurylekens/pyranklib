def part(n, k, basic):

    if n < k or k <= 0:
        return 0

    if k == n or k == 1:
        return 1

    if basic:
        return part(n - 1, k - 1, basic=True) + part(n - k, k, basic=True)
    else:
        return part(n - 2, k - 1, basic=False) + part(n - 2*k, k, basic=True)


print(part(9, 4, False))
