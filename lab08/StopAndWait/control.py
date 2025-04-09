K = 16


def get_raw_sum(arr):
    arr = list(map(int, ''.join(list(map(lambda x: bin(x)[2:].rjust(8, '0'), arr)))))
    s = 0
    for i in range(0, len(arr), K):
        s += int("".join(list(map(str, arr[i: i + K]))), 2)
    s %= 2 ** K
    return s


def get_sum(arr):
    s = get_raw_sum(arr)
    s ^= int('1' * K, 2)
    return s


def check_sum(arr, N):
    s = get_raw_sum(arr)
    check = s ^ N
    return check == 2 ** K - 1


if __name__ == "__main__":
    data = [0, 5, 10, 23]
    if not check_sum(data, get_sum(data)):
        print("Test 1 error")
    data = [1]
    if not check_sum(data, get_sum(data)):
        print("Test 2 error")
    data = [255, 255, 255]
    if not check_sum(data, get_sum(data)):
        print("Test 3 error")
    if check_sum([0] * 16, 0):
        print("Test 4 error")
    if check_sum([1, 1, 1, 1, 0, 1], get_sum([1, 1, 1, 0, 0, 1])):
        print("Test 5 error")
