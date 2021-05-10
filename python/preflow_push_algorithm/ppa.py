import numpy as np
import queue 


graph = np.array([])
straight = np.array([])
reversed = np.array([])
 
vertices = list()
 
height = np.array([])
excess = np.array([])
 
capacity = list()
 
source = -1
runoff = -1
opt = 0
 
n = int()
m = int()
u = int()
c = int()
v = int()

def add_elem(arr, elem):
    arr.append(elem)
    arr.sort(key=lambda tup: tup[1], reverse=True)

def bfs():
    dist = np.full(len(graph), -1)
    dist1 = np.full(len(graph), -1)
    used = np.full(len(graph), False)
    q = queue.Queue()
    q.put(runoff)
    used[runoff] = True
    dist[runoff] = 0
 
    while not q.empty():
        for i in reversed[q.queue[0]]:
            if not used[i] and get_value(capacity, i, q.queue[0]):
                used[i] = True
                q.put(i)
                dist[i] = dist[q.queue[0]] + 1
        q.get()
    q.put(source)
    used = np.full(len(graph), False)
    used[source] = True
    dist1[source] = 0
    while not q.empty():
        for i in straight[q.queue[0]]:
            if not used[i] and get_value(capacity, i, q.queue[0]):
                used[i] = True
                q.put(i)
                dist1[i] = dist1[q.queue[0]] + 1
        q.get()
    
    for i in range(len(dist)):
        if dist[i] == -1:
            dist[i] = dist1[i]
    dist[source] = len(graph)
    height = dist
    vertices.clear()
    for i in range(len(graph) - 1):
        if excess[i] != 0:
            add_elem(vertices, [i, height[i]])


def f():
    global opt
    while len(vertices) != 0:
        if opt == m:
            bfs()
            opt = 0
        tmp = vertices[0]
        for i in graph[tmp[0]]:
            if height[i] == height[tmp[0]] - 1:
                flow = min(excess[tmp[0]], get_value(capacity, tmp[0], i))
                excess[tmp[0]] -= flow
                excess[i] += flow
                if flow != 0 and i != runoff and excess[i] == flow:
                    add_elem(vertices, [i, height[i]])
                set_value(capacity, tmp[0], i, get_value(capacity, tmp[0], i) - flow)
                set_value(capacity, i, tmp[0], get_value(capacity, i, tmp[0]) + flow)
        
        min_height = len(graph)
        for i in graph[tmp[0]]:
            if get_value(capacity, tmp[0], i) > 0:
                min_height = min(min_height, height[i])
        
        vertices.remove(vertices[0])
        height[tmp[0]] = min_height + 1


        tmp[1] = height[tmp[0]]
        
        if height[tmp[0]] == len(graph) + 1:
            excess[tmp[0]] = 0
        if excess[tmp[0]] != 0: 
            add_elem(vertices, tmp)
        opt += 1

def set_value(arr, u, v, c):
    elem = None
    for i in arr:
        if i['u'] == u and i['v'] == v:
            elem = i
    if elem is not None:
        elem['c'] = c
    else:
        arr.append({'u': u, 'v': v, 'c': c})

def get_value(arr, u, v):
    c = None
    for i in arr:
        if i['u'] == u and i['v'] == v:
            c = i['c']
    if c is not None: 
        return c
    else:
        raise Exception("Edge doesn't exist")

if __name__ == '__main__':
    t = open("input.txt", "r")
    n, m = t.readline().split()
    n = int(n)
    m = int(m)

    graph = [[] for i in range(n)]
    straight = [[] for i in range(n)]
    reversed = [[] for i in range(n)]

    height = [0] * n
    excess = [0] * n

    for i in range(m):
        u, v, c = t.readline().split()
        u = int(u)
        v = int(v)
        c = int(c)

        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)
        straight[u - 1].append(v - 1) 
        reversed[v - 1].append(u - 1)
        set_value(capacity, u - 1, v - 1, c)
        set_value(capacity, v - 1, u - 1, 0)
    
    t.close()
    
    for i in range(n):
        if len(straight[i]) == 0:
            runoff = i
        if len(reversed[i]) == 0:
            source = i
    height[source] = n
    for i in graph[source]:
        excess[i] = get_value(capacity, source, i)
        if i != runoff:
            add_elem(vertices, [i, height[i]])
        c1 = get_value(capacity, i, source)
        c2 = get_value(capacity, source, i)
        set_value(capacity, i, source, c2)
        set_value(capacity, source, i, c1)
    x = 0
    f()
    print(excess[runoff])


