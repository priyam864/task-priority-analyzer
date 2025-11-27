# 🧠 Task Priority Analyzer

A smart task analysis system that calculates priority scores using urgency, importance, effort, and dependency factors.
Built with **Django + Django REST Framework** and a clean HTML/JS frontend.

---

## 🚀 Features

### 🔹 **Backend**

* Priority score calculation based on:

  * Due date urgency
  * Importance level
  * Estimated effort
  * Task dependencies
* Circular dependency detection (A → B → A)
* API-based suggestions (top 3 tasks)
* Multiple sorting strategies:

  * **Balanced** (default)
  * **Deadline Driven**
  * **Fastest First**
  * **High Impact**
* Detailed explanations for each task
* Full validation (edge cases handled)

### 🔹 **Frontend**

* JSON task input
* Sorting strategy dropdown
* Color-coded task cards (High / Medium / Low)
* Processing loader
* Clean modern UI

### 🔹 **Tests**

* Scoring logic tests
* Circular dependency tests
* Analyze API tests
* Suggest API tests

---

## 📁 Project Structure

```
Task_analyzer/
│
├── backend/                 # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tasks/                   # Django app (core business logic)
│   ├── scoring.py
│   ├── serializers.py
│   ├── dependency_checker.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py             # scoring & circular dependency tests
│   └── tests_api.py         # API tests
│
├── frontend/                # HTML, CSS, JS UI
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── venv/                    # virtual environment
├── requirements.txt
├── .gitignore
├── manage.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <your-repository-url>
cd Task_analyzer
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

### 3️⃣ Activate venv

**Windows**

```bash
venv\Scripts\activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Django server

```bash
python manage.py runserver
```

Backend will run at:

```
http://127.0.0.1:8000/
```

---

## 🌐 Frontend Usage

Open:

```
frontend/index.html
```

Features:

* Paste JSON input
* Choose sorting strategy
* Click **Analyze** or **Suggest Top Tasks**
* See color-coded results with explanations

---

## 📡 API Endpoints

### 🔍 **POST /api/analyze/**

Returns priority score for each task.

#### Sample Request:

```json
[
  {
    "title": "Finish assignment",
    "due_date": "2025-12-01",
    "importance": 8,
    "estimated_hours": 3,
    "dependencies": []
  }
]
```

#### Sample Response:

```json
{
  "results": [
    {
      "title": "Finish assignment",
      "due_date": "2025-12-01",
      "importance": 8,
      "estimated_hours": 3,
      "dependencies": [],
      "priority_score": 0.73
    }
  ]
}
```

---

### 💡 **POST /api/suggest/**

Returns the **top 3 tasks** with clear explanations.

---

## 🎛 Sorting Strategies

| Strategy | Query Example                     | Description                  |
| -------- | --------------------------------- | ---------------------------- |
| Balanced | `/api/analyze/?strategy=balanced` | Sort by final priority score |
| Deadline | `/api/analyze/?strategy=deadline` | Closest deadline first       |
| Fastest  | `/api/analyze/?strategy=fastest`  | Lowest hours first           |
| Impact   | `/api/analyze/?strategy=impact`   | Highest importance first     |

---

## 🧪 Running Tests

Run:

```bash
python manage.py test
```

Expected output:

```
Ran 8 tests in X.XXXs
OK
```

---

# 🧮 Algorithm Explanation

The priority scoring algorithm is designed to simulate real-world decision-making by balancing four major factors: urgency, importance, effort, and dependencies. Each task receives a normalized score between **0 and 1**, where higher scores indicate higher priority. The goal is to capture how humans naturally decide what to do next, while keeping the logic simple, explainable, and deterministic.

### **1. Urgency (due date proximity)**

Urgency captures how soon a deadline is approaching. A task due tomorrow should outrank a task due in 30 days. Urgency is computed using:

```
urgency = 1 - (days_left / 30)
```

This ensures a smooth decline in urgency as deadlines move farther away. A cap of 30 days prevents extremely distant deadlines from skewing the score. Tasks without a due date get urgency = 0.

### **2. Importance (impact level)**

Importance reflects business or personal significance and ranges from 1–10. It is normalized as:

```
importance_weight = importance / 10
```

This means higher-importance tasks naturally get higher scores. Importance serves as an equal partner to urgency in the scoring system.

### **3. Effort (estimated hours)**

Quick tasks often create momentum. To encourage completing smaller tasks earlier, effort is inverted:

```
effort_weight = 1 − (estimated_hours / max_hours)
```

Thus, low-effort tasks get higher scores, while extremely time-consuming tasks receive lower ones.

### **4. Dependencies**

Tasks that depend on others cannot be executed immediately. The system penalizes such tasks:

```
dependency_penalty = 0.1 * number_of_dependencies
```

This prevents blocked tasks from dominating the priority list.

### **Final Composite Score**

```
score = 0.4*urgency + 0.4*importance_weight + 0.2*effort_weight − dependency_penalty
```

The weights (0.4, 0.4, 0.2) were chosen to prioritize urgency and importance while still accounting for effort. These weights can be easily tuned.

### **Circular Dependency Detection**

Before scoring, the system checks for cycles in dependency chains using DFS graph search. If A → B → A is detected, the API returns a clear error. This ensures the algorithm only scores valid, executable tasks.

This combined scoring model is predictable, transparent, and strongly aligned with real-world prioritization workflows.

---

# 🧩 Design Decisions

### **1. Simplicity Over Complexity**

A deterministic weighted model was chosen instead of machine learning because:

* No training data exists
* Rules must be explainable
* Weights offer full transparency
* Fast and reliable in all inputs

### **2. Django REST Framework**

Chosen for:

* Serializer-based validation
* Clean URL routing
* Easy error handling
* Rapid API prototyping

### **3. No Database Storage**

The assignment is stateless and focuses on pure computation, so task storage was intentionally omitted.

### **4. Lightweight Frontend**

Plain JavaScript was used to avoid distracting from core logic and ensure easy execution without build tools.

---

# ⏱ Time Breakdown

| Task                          | Time         |
| ----------------------------- | ------------ |
| Backend setup                 | 30 min       |
| Scoring algorithm             | 1 hour       |
| Circular dependency detection | 30 min       |
| API development               | 45 min       |
| Frontend UI + styling         | 1 hour       |
| Sorting strategies            | 45 min       |
| Writing tests                 | 1 hour       |
| README + polishing            | 30 min       |
| **Total Time**                | **~6 hours** |

---

# Challenges

✔ Circular dependency detection
✔ Sorting strategies (Balanced, Deadline, Fastest, Impact)
✔ Detailed explanations
✔ API tests
✔ Loader animation
✔ Priority color coding
✔ Clean UI

---

# 🚀 Future Improvements

* Add user accounts and persistent task storage
* Add drag-and-drop UI for managing tasks
* Add more advanced scoring models
* Add a mobile UI version
* Deploy backend + frontend online for public use
* Allow users to customize scoring weights

---

## 👩‍💻 Tech Stack

* Python, Django
* Django REST Framework
* HTML, CSS, JavaScript
* JSON-based APIs

---
<img width="1140" height="605" alt="image" src="https://github.com/user-attachments/assets/918b30d7-fc62-410d-8f57-744dcef64f06" />


## ⭐ Author

**Priyam Kumari**


