def detect_cycle(tasks):
    graph = {task["title"]: task.get("dependencies", []) for task in tasks}

    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return node
        if node in visited:
            return None

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            if dep in graph:
                found = dfs(dep)
                if found:
                    return found

        stack.remove(node)
        return None

    for t in graph:
        result = dfs(t)
        if result:
            return result

    return None
