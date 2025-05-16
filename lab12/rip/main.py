import random
import threading
import copy


def create_graph(minN, maxN, p=0.5):
    n = random.randint(minN, maxN)
    edges = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            isNewEdge = random.random()
            if isNewEdge < p:
                edges[i].append(j)
                edges[j].append(i)
    return edges


def create_ips(n):
    s = set()
    for i in range(n):
        ip = create_ip()
        while ip in s:
            ip = create_ip()
        s.add(ip)
    return list(s)


def create_ip():
    return '.'.join([str(random.randint(0, 255)) for _ in range(4)])


def printTable(step):
    global distances, ips, inf, nextHops
    ipSize = 16
    for i in range(n):
        if step == -1:
            print(f'Final table for router {ips[i]}:')
        else:
            print(f'Step {step} table for router {ips[i]}:')
        print('[Source IP]      [Destination IP]    [Next Hop]       [Metric]')
        for j in range(n):
            if i == j:
                continue
            dist = distances[i][j]
            hop = ips[nextHops[i][j]].ljust(ipSize, ' ')
            if dist == inf:
                dist = -1
                hop = str(-1).ljust(ipSize, ' ')
            print(ips[i].ljust(ipSize, ' '), ips[j].ljust(ipSize, ' '), '  ', hop, dist)
    print()


def updateDistances(source):
    global prevDistances, distances, edges, nextHops, changed
    localChanged = False
    for dest in range(n):
        for middle in edges[source]:
            newVal = distances[middle][dest] + 1
            if newVal < prevDistances[source][dest]:
                prevDistances[source][dest] = newVal
                nextHops[source][dest] = middle
                localChanged = True
    return localChanged


def update(source):
    global prevDistances, distances, changedLock, barrier, nextHops, changed
    localChanged = True
    step = 1
    while localChanged:
        localChanged = updateDistances(source)
        if localChanged:
            changedLock.acquire()
            changed = True
            changedLock.release()
        barrier.wait()
        distances[source] = prevDistances[source].copy()
        if source == 0:
            printTable(step)
        localChanged = changed
        step += 1
        barrier.wait()
        if source == 0:
            changedLock.acquire()
            changed = False
            changedLock.release()
        barrier.wait()


edges = create_graph(3, 8)
n = len(edges)
ips = create_ips(n)
print('Generated ips:')
print(*ips, sep='\n')
print('Generated graph:')
for i in range(n):
    for j in edges[i]:
        if i < j:
            print(ips[i], ' ----- ', ips[j])
changed = True
inf = 10 ** 9
distances = [[0 if i == j else inf for j in range(n)] for i in range(n)]
prevDistances = copy.deepcopy(distances)
nextHops = [[i if i == j else -1 for j in range(n)] for i in range(n)]
for i in range(n):
    for j in edges[i]:
        distances[i][j] = 1
        nextHops[i][j] = j
printTable(0)
changedLock = threading.Lock()
threads = [threading.Thread(target=update, args=(i,)) for i in range(n)]
barrier = threading.Barrier(n)
for i in range(n):
    threads[i].start()
for i in range(n):
    threads[i].join()
printTable(-1)
