# 🛠️ Behavior Tracker App: Step-by-Step Setup & Deployment Guide

This guide walks you through setting up, running, and deploying the Flask-based Behavior Tracker app with Flask-SQLAlchemy and user authentication.

---

## 1. **System Requirements**

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Git**: (optional, for cloning repo)

---

## 2. **Clone the Repository**

```bash
git clone https://github.com/your-username/behavior-tracker.git
cd behavior-tracker
```

---

## 3. **Set Up a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

## 4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

**Sample `requirements.txt`**  
```
flask
flask-login
flask-sqlalchemy
flask-migrate
```

---

## 5. **Configure Environment Variables (Optional but Recommended)**

Create a `.env` file for secrets (or use real env vars):

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///behavior_tracker.db
```

---

## 6. **Initialize the Database**

Make sure your `app.py` includes:

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///behavior_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

Then run:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 7. **Seed the Database (Optional)**

Create an admin user or initial data as needed.  
You can do this in a Python shell:

```bash
flask shell
```

```python
from models import db, User
admin = User(username='admin', password='hashed_admin_password')
db.session.add(admin)
db.session.commit()
```

---

## 8. **Run the App Locally**

```bash
flask run
```
or
```bash
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 9. **Testing Functionality**

- Create users, behaviors, logs, goals, reminders, groups, etc.
- Use paginated views for logs and group messages.
- Test authentication and group sharing.

---

## 10. **Deploying to Production**

### **A. Prepare for Production**

- Change `FLASK_ENV=production`
- Use a stronger `SECRET_KEY`
- Use **PostgreSQL** or another production-grade database:
  ```python
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/database'
  ```
- Set up HTTPS for security.

### **B. Use Gunicorn or uWSGI as WSGI server**

```bash
pip install gunicorn
gunicorn -w 4 app:app
```

### **C. Deploy to a Cloud Platform**

- **Heroku**
- **Render**
- **Fly.io**
- **AWS Elastic Beanstalk**
- **DigitalOcean App Platform**

#### **Heroku Example**

```bash
heroku create my-behavior-tracker
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your_secret_key
git push heroku main
heroku run flask db upgrade
heroku open
```

#### **Render Example**

- Connect your repo.
- Add environment variables.
- Use `flask db upgrade` as a deploy hook.

---

## 11. **Maintaining & Migrating**

- When you change models, run:
  ```bash
  flask db migrate -m "Describe change"
  flask db upgrade
  ```
- Back up your database regularly.

---

## 12. **Next Steps**

- Set up email/password reset and security enhancements.
- Add Docker support for easy containerization.
- Monitor logs and errors with Sentry or similar.

---

## 13. **Troubleshooting**

- **Migration errors**: Delete `migrations/` and DB, re-init if necessary.
- **Database connection issues**: Check your URI and credentials.
- **Static file problems**: Ensure `static/` and `templates/` directories are correct.
- **WSGI errors**: Check logs for import/module errors.

---

## 14. **Useful Commands**

```bash
flask run                  # Run dev server
flask db migrate -m "msg"  # Create migration
flask db upgrade           # Apply migration
flask shell                # Open app shell
gunicorn app:app           # Run production server
deactivate                 # Exit virtual env
```

---

**Congratulations! Your Behavior Tracker app is ready to use and deploy.**  
For further customization, integrations, or scaling tips, consult the Flask, SQLAlchemy, and deployment platform documentation.