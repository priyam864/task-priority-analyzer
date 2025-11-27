# 🧠 Task Priority Analyzer

A smart task analysis system that calculates priority scores using urgency, importance, effort, and dependency factors.
Built with **Django + Django REST Framework** and a clean HTML/JS frontend.



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



## 🌐 Frontend Usage

Open:

```
frontend/index.html
```

Features:

* Paste JSON input
* Choose sorting strategy
* Click **Analyze** or **Suggest Top Tasks**
* See color-coded results with explanation



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


### 💡 **POST /api/suggest/**

Returns the **top 3 tasks** with detailed explanations.

## 🎛 Sorting Strategies

| Strategy | Query Example                     | Description                  |
| -------- | --------------------------------- | ---------------------------- |
| Balanced | `/api/analyze/?strategy=balanced` | Sort by final priority score |
| Deadline | `/api/analyze/?strategy=deadline` | Closest deadline first       |
| Fastest  | `/api/analyze/?strategy=fastest`  | Lowest hours first           |
| Impact   | `/api/analyze/?strategy=impact`   | Highest importance first     |


## 🧪 Running Tests

Run all tests:

```bash
python manage.py test
```

Expected output:

```
Ran 8 tests in X.XXXs
OK



## 👩‍💻 Tech Stack

* Python, Django
* Django REST Framework
* HTML, CSS, JavaScript
* JSON-based APIs



## ⭐ Author

**Priyam Kumari**
