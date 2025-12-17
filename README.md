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
Build SQLAlchemy models, Configure and initialize the database, and implement main entity CRUD routes.

Person 2 (Brian) – Authentication, WTForms, Edit/Update Routes
Create authentication and main entity forms, Implement Flask-Login authentication, and implement edit/update routes for assignments and materials

Person 3 (Sohum) – Unit Testing, Documentation (PDF), README, Tagging
Create tests/ folder structure, Write unit, regression, and implementation tests, create documentation, complete the full README, tag github, final verification for the app to be functional

##Milestone 3 - Final Release

Home Page Logged In 
<img width="2861" height="1619" alt="image" src="https://github.com/user-attachments/assets/b21322ff-9cfd-4a26-90a8-5b747a9fa4a2" />

Home Page Logged Out
<img width="2875" height="1590" alt="image" src="https://github.com/user-attachments/assets/29f8991e-b202-4af6-81de-d372e0308661" />

Assignments List
<img width="2861" height="1579" alt="image" src="https://github.com/user-attachments/assets/d92939f9-9acd-4f32-b96b-0b90e50f9853" />

Assignment Creation
<img width="2836" height="1583" alt="image" src="https://github.com/user-attachments/assets/1acb98ca-1861-4534-a21b-97f469985e90" />

Testing Results
<img width="2840" height="1173" alt="image" src="https://github.com/user-attachments/assets/d2c9059a-bb58-4fed-be20-4c9cb0f6631d" />


Test Report

Model Tests
  - These were for User, Assignment, CourseMaterial creation
  - Relationship tests (between instructor and materials)

Form Tests
  - LoginForm validation for:
  - Valid credentials
  - Missing Fields
  - Incorrect Data

Route Tests
  - Public list routes return HTTP 200
  - Protected routes redirect when the user is unauthenticated
  - Instructor-only access is verified

Integration Tests
  - Login is successful
  - Login fails
  - Assignment creation and deletion
  - Material Creation
  - An unauthorized user is attempting to access routes that are protected.

```

```
