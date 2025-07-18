# 📰 Django News Application

A Django-based news platform that supports independent journalists, curated publications, and user subscriptions. This application includes role-based user access, article approval workflows, REST API support, and social sharing functionality.

---

## 📌 Features

- 🔐 Custom user roles: **Reader**, **Journalist**, **Editor**
- 📝 Journalists can submit articles for editor approval
- ✅ Editors can approve/reject submitted articles
- 🗞 Readers can subscribe to publishers and journalists
- 💌 Optional newsletter feature for readers
- 🐦 Twitter integration for auto-tweeting new content (if enabled)
- 📂 RESTful API for listing and retrieving articles
- 🧪 Unit testing using `pytest` and `pytest-django`
- 🛠 Admin dashboard for managing users and content

---

## ⚙️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/django-news-app.git
cd django-news-app

2. Create and Activate a Virtual Environment
bash
Copy
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
3. Install Dependencies
bash
Copy
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in your project root and include:

env
Copy
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
🗄️ Database Setup
bash
Copy
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
🚀 Run the Server
bash
Copy
python manage.py runserver
Visit: http://127.0.0.1:8000

🔐 User Roles
Role	Permissions
Reader	Browse articles, subscribe to journalists
Journalist	Submit articles, view publisher options
Editor	Approve/reject articles
Admin	Full access to Django admin panel

📂 API Endpoints
Endpoint	Method	Description
/api/articles/	GET	List all articles
/api/articles/<id>/	GET	Retrieve single item

🧪 Running Tests
Ensure test packages are installed:

bash
Copy
pip install pytest pytest-django
Create a pytest.ini file:

ini
Copy
[pytest]
DJANGO_SETTINGS_MODULE = news_project.settings
python_files = tests.py test_*.py *_tests.py
Then run:

bash
Copy
pytest
🛠 Admin Panel
Visit: http://127.0.0.1:8000/admin/

Add Publishers

Add Users and assign them to groups (Reader, Journalist, Editor)

Create/edit/delete articles manually for testing

📝 Notes
Template logic shows Login/Signup only if not authenticated.

Twitter auto-posting requires developer API credentials.

Newsletter model is present; template/views may be needed for full implementation.

Remember to register all models in admin.py.

📄 License
MIT License

👩‍💻 Author
Giulia Damascena — Capstone project for Software Engineering.