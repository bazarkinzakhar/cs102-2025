def longest_common_substring(a: str, b: str, i=None, j=None, count=0):
    if i is None:
        best_len, end = longest_common_substring(a, b, len(a), len(b), 0)
        return a[end - best_len : end]

    if i == 0 or j == 0:
        return count, i

    best = (count, i)

    if a[i - 1] == b[j - 1]:
        cand = longest_common_substring(a, b, i - 1, j - 1, count + 1)
        if cand[0] > best[0]:
            best = cand

    cand = longest_common_substring(a, b, i - 1, j, 0)
    if cand[0] > best[0]:
        best = cand

    cand = longest_common_substring(a, b, i, j - 1, 0)
    if cand[0] > best[0]:
        best = cand

    return best


a = longest_common_substring("ababc", "abcdaba")
print(a)
