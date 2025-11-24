from collections import deque

def bfs(graph, start, end):

    visited = set(start)
    quque = deque([start])
    result = []

    while quque:
        v = quque.popleft()
        result.append(v)

        if v == end:
            break

        for neighbor in graph[v]:
            if neighbor not in visited:
                visited.add(neighbor)
                quque.append(neighbor)

    return result