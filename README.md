
---

# ⚖️ Master Of Judges (MoJ)

A modern, full-featured online judge built with **Django** and **Docker**, designed for solving coding problems, managing submissions, and receiving AI-powered code reviews. The system supports real-time code execution, admin-controlled problem management, and user dashboards with analytics and submission history.

---

## 🌟 Live Demo

**🔗 Project URL**: [http://3.110.27.40:8000/OJ](http://3.110.27.40:8000/OJ)

---

## 🏗 System Architecture

```
[Frontend - HTML/CSS/Bootstrap (Django Templates)]
         |
         v
[Django Backend - Python]
         |
         ├── SQLite Database (users, problems, submissions)
         ├── Django Admin Panel (test case management)
         └── Compiler Server (code execution)
                 |
                 └──  Docker container deployed locally or on cloud
```

---

## 📌 Features

✅ Solve coding problems in C++, Python, and C
🧪 Automatic code evaluation with hidden test cases
🧠 AI Code Review system (via Google Gemini API)
🧑‍🏫 Admin dashboard for adding/editing/deleting problems
🗃 User submission history with verdicts and timestamps
🔐 Django Auth with session-based login/logout
🐳 Dockerized compiler microservice for secure execution
📁 Test case management handled via Django Admin using database-backed models for easy input/output storage and evaluation

---

## 🧰 Tech Stack

### **Frontend:**

* Django Templates
* Bootstrap 5
* Custom CSS

### **Backend:**

* Django Framework
* SQLite (default)

### **Compiler Service:**

* Python
* Docker (isolated code execution)
* `subprocess` for code running and judging

### **AI Integration:**

* Gemini API (Google Generative AI)

---


## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/adarshp22/OJ .git
cd OnlineJudge
```

### 2️⃣ Setup Backend (Django)

```bash
python -m venv ven
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
python manage.py runserver
```


### 4️⃣ AI Review Integration

Set your Gemini API key in `.env` or `settings.py`:

```env
GEMINI_API_KEY=your_gemini_key
```

---


## 🖼 Screenshots

| Home Page                                                                                | Problem Pages                                                                                                                                                                                                              | Submission History                                                                              | AI Review Panel                                                                               |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| ![Home](https://github.com/user-attachments/assets/5c917b57-0306-40d0-9e5a-c58b152c9d78) | <img src="https://github.com/user-attachments/assets/dc6379d1-4b67-431b-924b-a1162d193356" width="200"/> <br><br> <img src="https://github.com/user-attachments/assets/c5d1f1b9-f727-4bc3-a394-4ec0b7823d2d" width="200"/> | ![Submissions](https://github.com/user-attachments/assets/4e5290e6-2f43-46e0-b7df-191bd7f01932) | ![AI Review](https://github.com/user-attachments/assets/57ac51dd-c01c-4e8e-a9e8-f0ace5fd9683) |

---

## 🙌 Contributing

Pull requests are welcome :) ! 

---

## 👨‍💻 Author

Made with ❤️ by **Adarsh Pal**
🔗 GitHub: [github.com/adarshp22](https://github.com/adarshp22)

---

