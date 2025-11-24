from collections import deque

def bfs(graph, start):

    visited = set(start)
    quque = deque([start])
    result = []

    while quque:
        v = quque.popleft()
        result.append(v)

        for neighbor in graph[v]:
            if neighbor not in visited:
                visited.add(neighbor)
                quque.append(neighbor)

    return result