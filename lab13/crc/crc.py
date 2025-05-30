import random


G = 0b100101
R = 5
PACKAGE_SIZE = 40


def findRemains(p):
    p %= G
    if p >= 2 ** R:
        p ^= G
    return p


def checkData(data):
    r = data % 2 ** R
    data -= r
    return findRemains(data) == r


def frameData(data):
    extendedData = data * 2 ** R
    return extendedData + findRemains(extendedData)


def mutate(data, k):
    indexes = [i for i in range(PACKAGE_SIZE)]
    random.shuffle(indexes)
    mutationData = 0
    for i in range(k):
        mutationData += 2 ** indexes[i]
    return data ^ mutationData


def unite(inputStr):
    res = 0
    for c in inputStr:
        res *= 256
        res += ord(c)
    return res


text = '\n'.join(['Never gonna give you up', 'Never gonna let you down', 'Never gonna run around and desert you',
                'Never gonna make you cry', 'Never gonna say goodbye', 'Never gonna tell a lie and hurt you'])

print('Data, Encoded, CRC, AfterMutation, IsMutated, Error')
for i in range(0, len(text), 5):
    data = unite(text[i:i+5])
    encodedData = frameData(data)
    crc = encodedData % 2 ** R
    mutated = random.randint(0, 1) == 1
    resultData = encodedData
    if mutated:
        resultData = mutate(resultData, random.randint(1, R))
    isError = not checkData(resultData)
    if isError != mutated:
        print("Mistake in the following package")
    print(f"'{text[i:i+5]}'", bin(encodedData), bin(crc), bin(resultData), mutated, isError)
