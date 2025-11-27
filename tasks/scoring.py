from datetime import date

def calculate_task_score(task):
    today = date.today()

    # URGENCY
    due_date = task.get("due_date")
    if due_date:
        days_left = (due_date - today).days
        if days_left <= 0:
            urgency = 1.0
        elif days_left >= 30:
            urgency = 0.0
        else:
            urgency = 1 - (days_left / 30)
    else:
        urgency = 0.3

    # IMPORTANCE
    importance = task.get("importance", 5) / 10

    # EFFORT
    hours = task.get("estimated_hours")
    if hours is None:
        effort = 0.5
    else:
        effort = 1 - min(hours / 10, 1)

    # DEPENDENCIES
    deps = task.get("dependencies", [])
    dep_score = min(len(deps) * 0.1, 0.5)

    score = (
        0.4 * urgency +
        0.3 * importance +
        0.2 * effort +
        0.1 * dep_score
    )
    return round(score, 4)
