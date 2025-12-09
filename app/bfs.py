from collections import deque

def bfs(graph, start, end):

    visited = set(start)
    quque = deque([start])
    result = [[]]

    while quque:
        node = quque.popleft()
        result.append(result[-1] + [node])

        if node == end:
            break

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                quque.append(neighbor)

    return result