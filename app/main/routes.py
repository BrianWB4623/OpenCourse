from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app import db
from app.models import Assignment, CourseMaterial
from app.models import Submission, Grade, Course, User
from flask_login import login_required, current_user
from flask import abort
from ..forms import SubmissionForm, GradeForm


def instructor_required():
    """helper to check instructor role"""
    if current_user.role != 'instructor':
        flash('This page is for instructors only.', 'error')
        return False
    return True

@main_bp.route("/")
def index():
    return render_template("main/index.html")

@main_bp.route("/feature")
def feature():
    return render_template("main/feature.html")

# ========== ASSIGNMENTS ROUTES ==========

@main_bp.route("/assignments")
def list_assignments():
    """List all assignments"""
    assignments = Assignment.query.all()
    return render_template("main/assignments/list.html", assignments=assignments)

@main_bp.route("/assignments/<int:id>")
def assignment_detail(id):
    """View assignment details"""
    assignment = Assignment.query.get_or_404(id)
    return render_template("main/assignments/detail.html", assignment=assignment)

@main_bp.route("/assignments/create", methods=["GET", "POST"])
@login_required
def create_assignment():
    """Create a new assignment"""
    # Only instructors can create assignments
    if current_user.role != 'instructor':
        flash("Only instructors can create assignments.", "error")
        return redirect(url_for("main.list_assignments"))
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        course_id = request.form.get("course_id") or None
        
        if not title or not description:
            flash("Title and description are required.", "error")
            return redirect(url_for("main.create_assignment"))
        
        assignment = Assignment(
            title=title,
            description=description,
            instructor_id=current_user.id
            , course_id=course_id
        )
        db.session.add(assignment)
        db.session.commit()
        flash(f"Assignment '{title}' created successfully!", "success")
        return redirect(url_for("main.list_assignments"))
    
    return render_template("main/assignments/create.html")

@main_bp.route("/assignments/<int:id>/delete", methods=["POST"])
@login_required
def delete_assignment(id):
    """Delete an assignment"""
    assignment = Assignment.query.get_or_404(id)
    
    # Check if user is the instructor who created this assignment
    if assignment.instructor_id != current_user.id or current_user.role != 'instructor':
        flash("You do not have permission to delete this assignment.", "error")
        return redirect(url_for("main.list_assignments"))
    
    title = assignment.title
    db.session.delete(assignment)
    db.session.commit()
    flash(f"Assignment '{title}' deleted successfully!", "success")
    return redirect(url_for("main.list_assignments"))

# ========== COURSE MATERIALS ROUTES ==========

@main_bp.route("/materials")
def list_materials():
    """List all course materials"""
    materials = CourseMaterial.query.all()
    return render_template("main/materials/list.html", materials=materials)

@main_bp.route("/materials/<int:id>")
def material_detail(id):
    """View material details"""
    material = CourseMaterial.query.get_or_404(id)
    return render_template("main/materials/detail.html", material=material)

@main_bp.route("/materials/create", methods=["GET", "POST"])
@login_required
def create_material():
    """Create a new course material"""
    # only instructors
    if current_user.role != 'instructor':
        flash("Only instructors can upload materials.", "error")
        return redirect(url_for("main.list_materials"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        course_id = request.form.get("course_id") or None
        
        if not title or not description:
            flash("Title and description are required.", "error")
            return redirect(url_for("main.create_material"))
        
        material = CourseMaterial(
            title=title,
            description=description,
            instructor_id=current_user.id
            , course_id=course_id
        )
        db.session.add(material)
        db.session.commit()
        flash(f"Material '{title}' created successfully!", "success")
        return redirect(url_for("main.list_materials"))
    
    return render_template("main/materials/create.html")


# ========== SUBMISSIONS & GRADES ==========


@main_bp.route('/assignments/<int:id>/submit', methods=['GET', 'POST'])
@login_required
def submit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    # only students submit
    if current_user.role != 'student':
        flash('Only students can submit assignments.', 'error')
        return redirect(url_for('main.assignment_detail', id=id))

    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(
            assignment_id=assignment.id,
            student_id=current_user.id,
            content=form.content.data
        )
        db.session.add(submission)
        db.session.commit()
        flash('Submission uploaded successfully.', 'success')
        return redirect(url_for('main.assignment_detail', id=id))

    return render_template('main/submissions/create.html', assignment=assignment, form=form)


@main_bp.route('/assignments/<int:id>/submissions')
@login_required
def list_submissions(id):
    assignment = Assignment.query.get_or_404(id)
    # instructors who own the assignment can view all submissions; students can view their own
    if current_user.role == 'instructor' and assignment.instructor_id == current_user.id:
        submissions = Submission.query.filter_by(assignment_id=assignment.id).all()
    elif current_user.role == 'student':
        submissions = Submission.query.filter_by(assignment_id=assignment.id, student_id=current_user.id).all()
    else:
        abort(403)

    return render_template('main/submissions/list.html', assignment=assignment, submissions=submissions)


@main_bp.route('/submissions/<int:id>', methods=['GET', 'POST'])
@login_required
def submission_detail(id):
    submission = Submission.query.get_or_404(id)
    assignment = submission.assignment
    grade = submission.grade

    # authorization: instructor of assignment or the student owner
    if not (current_user.role == 'instructor' and assignment.instructor_id == current_user.id) and not (current_user.id == submission.student_id):
        abort(403)

    form = GradeForm()
    if form.validate_on_submit():
        # only instructor can grade
        if current_user.role != 'instructor' or assignment.instructor_id != current_user.id:
            flash('Only the assignment instructor can grade submissions.', 'error')
            return redirect(url_for('main.submission_detail', id=id))

        # create or update grade
        if not grade:
            grade = Grade(submission_id=submission.id, grader_id=current_user.id, score=form.score.data, feedback=form.feedback.data)
            db.session.add(grade)
        else:
            grade.score = form.score.data
            grade.feedback = form.feedback.data
            grade.grader_id = current_user.id
        db.session.commit()
        flash('Grade saved.', 'success')
        return redirect(url_for('main.submission_detail', id=id))

    # pre-fill form if grade exists
    if grade and request.method == 'GET':
        form.score.data = grade.score
        form.feedback.data = grade.feedback

    return render_template('main/submissions/detail.html', submission=submission, form=form, grade=grade)


# ========== DASHBOARD ==========


@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Instructor dashboard
    if current_user.role == 'instructor':
        courses = Course.query.join(Assignment, isouter=True).filter((Assignment.instructor_id == current_user.id) | (Course.id == None)).all()
        courses = Course.query.filter(Course.id.in_([c.id for c in Course.query.all() if any(a.instructor_id == current_user.id for a in c.assignments) or any(m.instructor_id == current_user.id for m in c.materials)])).all() if Course.query.count() else []
        assignments = Assignment.query.filter_by(instructor_id=current_user.id).all()
        materials = CourseMaterial.query.filter_by(instructor_id=current_user.id).all()
        return render_template('main/dashboard_instructor.html', courses=courses, assignments=assignments, materials=materials)

    # Student dashboard
    else:
        # if enrollment isn't implemented show all courses and assignments
        courses = Course.query.all()
        assignments = Assignment.query.all()
        materials = CourseMaterial.query.all()
        return render_template('main/dashboard_student.html', courses=courses, assignments=assignments, materials=materials)

@main_bp.route("/materials/<int:id>/delete", methods=["POST"])
@login_required
def delete_material(id):
    """Delete a course material"""
    material = CourseMaterial.query.get_or_404(id)
    
    # Check if user is the instructor who created this material
    if material.instructor_id != current_user.id:
        flash("You do not have permission to delete this material.", "error")
        return redirect(url_for("main.list_materials"))
    
    title = material.title
    db.session.delete(material)
    db.session.commit()
    flash(f"Material '{title}' deleted successfully!", "success")
    return redirect(url_for("main.list_materials"))
