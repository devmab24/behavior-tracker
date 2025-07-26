# Behavior Tracker

A Flask-based app for tracking personal behavior, setting goals, sharing progress in groups, and collaborating via group messages and challenges.  
This app uses Flask-SQLAlchemy for robust data storage and Flask-Login for user authentication.

---

## Features

- Track behaviors, logs, moods, and notes
- Set personal goals and reminders
- Create and join groups
- Share progress, goals, badges (optional privacy controls)
- Group chat/messages and challenges
- Secure user authentication
- Paginated views for logs and group messages

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- git (optional)

### Setup

1. **Clone the repo:**
    ```bash
    git clone https://github.com/devmab24/behavior-tracker.git
    cd behavior-tracker
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure secrets:**
    - Set environment variables for `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`.
    - Never commit secrets to the repo!

5. **Initialize the database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6. **Run the app:**
    ```bash
    flask run
    ```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues and pull requests.

---

## Security

Never commit secrets or production credentials.  
Please see [SECURITY.md](SECURITY.md) for responsible disclosure guidelines and security best practices.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Community

- Open an issue or discussion for ideas, feedback, or help!