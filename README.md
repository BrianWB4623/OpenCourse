# OpenCourse

Milestone 1 — non-functional Flask-based LMS prototype.

## Installation

1. Create a virtual environment and activate it.

   **Windows (PowerShell):**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

2. Install all the requirements from requirements.txt

   **Windows (PowerShell):**

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app

   **Windows (PowerShell):**

   ```powershell
   python run.py
   ```

## Testing Instructions

### 1. Activate the virtual environment

```powershell
venv\Scripts\activate
```

### 2.

```
pytest
```

## Screenshots

1. Home Page
   <img width="1919" height="863" alt="image" src="Homepage.png" />

2. Assignments Page
   <img width="1919" height="860" alt="image" src="Assignments.png" />

3. Course Materials Page
   <img width="1919" height="863" alt="image" src="CourseMaterials.png" />

4.Registration Page
<img width="1919" height="863" alt="image" src="Registration.png" />

5.Login Page
<img width="1919" height="863" alt="image" src="Login.png" />

## Team Roles

Person 1 (Rachel) – Backend Models, Database, Create/Delete Routes
Build SQLAlchemy models, Configure and initialize the database, implement main entity CRUD routes.

Person 2 (Brian) – Authentication, WTForms, Edit/Update Routes
Create authentication and main entity forms, Implement Flask-Login authentication, Implement edit/update routes for assignments and materials

Person 3 (Sohum) – Unit Testing, Documentation (PDF), README, Tagging
Create tests/ folder structure, Write unite, regression, and implementation tests, create documentation, complete the full README, tag github, final verification for the app to be functional

```

```
