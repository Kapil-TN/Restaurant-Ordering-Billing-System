# Restaurant Ordering & Billing System

A collaborative, modular Restaurant Ordering & Billing System codebase with a Flask backend.

## Development Setup

Follow these integration instructions to set up the backend service locally for development.

### 1. Clone the Repository
```bash
git clone https://github.com/Kapil-TN/Restaurant-Ordering-Billing-System.git
cd Restaurant-Ordering-Billing-System
```

### 2. Create the Configuration File
Create a `.env` file inside the `backend/` directory to configure environment secrets:
```bash
# Place inside: backend/.env
SECRET_KEY=your-flask-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

### 3. Install Dependencies
Set up your virtual environment and install the required Python packages:
```bash
cd backend
# Create virtual environment if not already created
python -m venv venv
# Activate virtual environment
# Windows (PowerShell): .\venv\Scripts\Activate.ps1
# Windows (CMD): .\venv\Scripts\activate.bat
# Linux/macOS: source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4. Run Database Migrations
Apply the existing database schema migration scripts:
```bash
flask --app run.py db upgrade
```

### 5. Start the Backend Development Server
Run the Flask application:
```bash
# Option 1: Run via run.py (runs in debug mode on port 5000)
python run.py

# Option 2: Run via Flask CLI
flask --app run.py run
```
The server will start at `http://127.0.0.1:5000/`.

### 6. Run the Test Suite
Ensure everything is working correctly by running tests:
```bash
pytest
```

---

## Codebase Branch Architecture
All development is structured around the `develop` branch.
* To start working on your module, check out `develop`, pull the latest code, and branch off:
  ```bash
  git checkout develop
  git pull
  git checkout -b feature/your-module-name
  ```

---

## Branch Workflow

Repository flow:

main → stable / demo-ready branch

develop → integration branch

feature/* → individual work branches

Example:

```bash
git checkout develop
git pull

git checkout -b feature/menu
```

After completing work:

```bash
git push origin feature/menu
```

Open Pull Request:

```plaintext
feature/menu → develop
```

---

## Team Ownership

Member 1
- Authentication
- Config
- Database migrations
- Backend integration

Member 2
- Menu
- Table management

Member 3
- Orders
- Billing

Member 4
- Dashboard
- Analytics

---

## Integration Rules

Before opening PR:

```bash
git checkout develop
git pull
```

Requirements:
- Work only inside assigned module
- Do not modify auth routes unless discussed
- Do not modify config.py unless discussed
- Avoid editing existing migrations
- Pull latest develop before merging

---

## API Contract

Authentication endpoints are documented in:

```plaintext
docs/api-contract.md
```

If API behavior changes:

1. Update api-contract.md
2. Mention API changes in PR

---

## Verification Checklist

Before submitting Pull Request:

```plaintext
[ ] Backend starts successfully
[ ] Database migration succeeds
[ ] Tests pass
[ ] No merge conflicts
[ ] API contract updated
```
