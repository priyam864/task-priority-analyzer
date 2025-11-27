from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from datetime import date

from .serializers import TaskInputSerializer
from .scoring import calculate_task_score
from .dependency_checker import detect_cycle


def home(request):
    return HttpResponse(
        "<h1>Task Priority Analyzer Backend</h1>"
        "<p>Use <b>/api/analyze/</b> or <b>/api/suggest/</b></p>"
    )


class AnalyzeTasksView(APIView):

    def post(self, request):
        tasks = request.data

        if not isinstance(tasks, list):
            return Response({"error": "Input must be a list of tasks"}, status=400)

        validated = []

        for task in tasks:
            serializer = TaskInputSerializer(data=task)
            if serializer.is_valid():
                validated.append(serializer.validated_data)
            else:
                return Response(serializer.errors, status=400)

        # CIRCULAR DEPENDENCY CHECK
        cycle = detect_cycle(validated)
        if cycle:
            return Response(
                {"error": f"Circular dependency detected starting at '{cycle}'"},
                status=400
            )

        # SCORING
        results = []
        for d in validated:
            score = calculate_task_score(d)
            results.append({**d, "priority_score": score})

        # SORTING STRATEGIES
        strategy = request.query_params.get("strategy", "balanced")

        if strategy == "deadline":
            results.sort(key=lambda x: (x["due_date"] is None, x["due_date"]))
        elif strategy == "fastest":
            results.sort(key=lambda x: (x["estimated_hours"] is None, x["estimated_hours"]))
        elif strategy == "impact":
            results.sort(key=lambda x: x["importance"], reverse=True)
        else:
            results.sort(key=lambda x: x["priority_score"], reverse=True)

        return Response({"results": results}, status=200)


class SuggestTasksView(APIView):

    def post(self, request):
        tasks = request.data

        if not isinstance(tasks, list):
            return Response({"error": "Input must be a list of tasks"}, status=400)

        validated = []
        results = []

        for task in tasks:
            serializer = TaskInputSerializer(data=task)
            if serializer.is_valid():
                validated.append(serializer.validated_data)
            else:
                return Response(serializer.errors, status=400)

        for task_data in validated:
            score = calculate_task_score(task_data)
            explanation = []

            # URGENCY
            due_date = task_data.get("due_date")
            if due_date:
                days_left = (due_date - date.today()).days
                if days_left <= 0:
                    explanation.append("Task is overdue or due today — very urgent.")
                elif days_left <= 3:
                    explanation.append(f"Due very soon ({days_left} days left).")
                elif days_left <= 7:
                    explanation.append(f"Due this week ({days_left} days left).")
                else:
                    explanation.append(f"Due later ({days_left} days left).")
            else:
                explanation.append("No due date provided.")

            # IMPORTANCE
            importance = task_data.get("importance", 5)
            if importance >= 8:
                explanation.append(f"High importance ({importance}/10).")
            elif importance >= 5:
                explanation.append(f"Medium importance ({importance}/10).")
            else:
                explanation.append(f"Low importance ({importance}/10).")

            # EFFORT
            hours = task_data.get("estimated_hours")
            if hours is not None:
                if hours <= 2:
                    explanation.append(f"Quick task — only {hours} hours.")
                elif hours <= 5:
                    explanation.append(f"Moderate effort task ({hours} hours).")
                else:
                    explanation.append(f"Large task — needs more time ({hours} hours).")
            else:
                explanation.append("Effort not provided.")

            # DEPENDENCIES
            deps = task_data.get("dependencies", [])
            if deps:
                explanation.append(f"Has {len(deps)} dependent tasks: {', '.join(deps)}.")
            else:
                explanation.append("No dependent tasks.")

            # OVERALL
            if score > 0.75:
                explanation.append("Overall: Very high priority.")
            elif score > 0.5:
                explanation.append("Overall: Medium priority.")
            else:
                explanation.append("Overall: Lower priority.")

            results.append({
                **task_data,
                "priority_score": score,
                "explanation": explanation
            })

        results.sort(key=lambda x: x["priority_score"], reverse=True)
        top_three = results[:3]

        return Response({"suggestions": top_three}, status=200)
