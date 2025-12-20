from collections import deque

def bfs(graph, start, end):
    visited = set()
    queue = deque([[start]])
    
    steps = []
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        steps.append({
            'current_path': path.copy(),
            'visited': visited.copy(),
            'queue': [list(path) for path in queue],
            'current_node': node
        })
        
        if node == end:
            break
        
        if node not in visited:
            visited.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append(new_path)
    
    return steps