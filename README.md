# 🧠 Task Priority Analyzer  
A smart task analysis system that calculates priority scores using urgency, importance, effort, and dependency factors.  
Built with **Django + Django REST Framework** and a clean HTML/JS frontend.

---

## 🚀 Features

### 🔹 **Backend**
- Priority score calculation based on:
  - Due date urgency  
  - Importance level  
  - Estimated effort  
  - Task dependencies  
- Circular dependency detection (A → B → A)  
- API-based suggestions (top 3 tasks)  
- Multiple sorting strategies:
  - **Balanced** (default)
  - **Deadline Driven**
  - **Fastest First**
  - **High Impact**
- Detailed explanations for each task
- Full validation (edge cases handled)

### 🔹 **Frontend**
- JSON input box  
- Strategy dropdown  
- Color-coded priority cards:
  - 🟢 High
  - 🟡 Medium
  - 🔴 Low  
- Loading animation  
- Clean responsive UI  

### 🔹 **Tests**
- Scoring tests  
- Circular dependency tests  
- Analyze API tests  
- Suggest API tests  

---

## 📁 Project Structure
