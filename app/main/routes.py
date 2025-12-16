from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app import db
from app.models import Assignment, CourseMaterial
from flask_login import login_required, current_user
from app.forms import AssignmentForm, MaterialForm
from app.forms import SubmissionForm, GradeForm
from app.models import Submission, Grade, Course
from flask import abort

#Helper method to determine if instructor or not
INSTRUCTOR_ROLES= ("teacher","ta","instructor")
def is_instructor(user):
    return user.is_authenticated and user.role in INSTRUCTOR_ROLES
#Allow other files to use
@main_bp.app_context_processor
def inject_role_helpers():
    return dict(is_instructor=is_instructor)

@main_bp.route("/")
def index():
    return render_template("main/index.html")

@main_bp.route("/feature")
def feature():
    return render_template("main/feature.html")

# ========== ASSIGNMENTS ROUTES ==========

@main_bp.route("/assignments")
@login_required
def list_assignments():
    """List all assignments"""
    assignments = Assignment.query.all()
    return render_template("main/assignments/list.html", assignments=assignments)

@main_bp.route("/assignments/<int:id>")
@login_required
def assignment_detail(id):
    """View assignment details"""
    assignment = Assignment.query.get_or_404(id)
    student_submission = None
    if current_user.is_authenticated and current_user.role == 'student':
        student_submission = Submission.query.filter_by(assignment_id=id, student_id=current_user.id).first()
    return render_template("main/assignments/detail.html", assignment=assignment, student_submission=student_submission)

@main_bp.route("/assignments/create", methods=["GET", "POST"])
@login_required
def create_assignment():
    """Create a new assignment"""
    #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to create assignments", "danger")#displayu error
        return redirect(url_for("main.list_assignments"))
    courses = Course.query.all()
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        course_id = request.form.get('course_id') or None
        
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
    
    return render_template("main/assignments/create.html", courses=courses)

@main_bp.route("/assignments/<int:id>/delete", methods=["POST"])
@login_required
def delete_assignment(id):
    """Delete an assignment"""
    #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to delete assignments", "danger")#display error
        return redirect(url_for("main.assignment_detail"))
    assignment = Assignment.query.get_or_404(id)
    
    # Check if user is the instructor who created this assignment
    if assignment.instructor_id != current_user.id:
        flash("You do not have permission to delete this assignment.", "error")
        return redirect(url_for("main.list_assignments"))
    
    title = assignment.title
    db.session.delete(assignment)
    db.session.commit()
    flash(f"Assignment '{title}' deleted successfully!", "success")
    return redirect(url_for("main.list_assignments"))


@main_bp.route('/assignments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if current_user.role != 'instructor' or assignment.instructor_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title or not description:
            flash('Title and description are required.', 'error')
            return redirect(url_for('main.edit_assignment', id=id))
        assignment.title = title
        assignment.description = description
        db.session.commit()
        flash('Assignment updated.', 'success')
        return redirect(url_for('main.assignment_detail', id=id))

    return render_template('main/assignments/edit.html', assignment=assignment)



@main_bp.route('/assignments/<int:id>/submit', methods=['GET', 'POST'])
@login_required
def submit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    # only students
    if not current_user.is_authenticated or current_user.role != 'student':
        abort(403)
    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(assignment_id=assignment.id, student_id=current_user.id, content=form.content.data)
        db.session.add(submission)
        db.session.commit()
        flash('Submission created.', 'success')
        return redirect(url_for('main.assignment_detail', id=id))
    return render_template('main/submissions/create.html', assignment=assignment, form=form)


@main_bp.route('/assignments/<int:id>/submissions')
@login_required
def list_submissions(id):
    assignment = Assignment.query.get_or_404(id)
    # instructor can see all submissions for their assignment
    if current_user.role == 'teacher' or current_user.role == 'ta':
        if assignment.instructor_id != current_user.id:
            abort(403)
        subs = Submission.query.filter_by(assignment_id=assignment.id).all()
    else:
        # student can see only their submissions
        subs = Submission.query.filter_by(assignment_id=assignment.id, student_id=current_user.id).all()
    return render_template('main/submissions/list.html', assignment=assignment, submissions=subs)


@main_bp.route('/submissions/<int:id>', methods=['GET', 'POST'])
@login_required
def submission_detail(id):
    submission = Submission.query.get_or_404(id)
    assignment = submission.assignment
    # authorization
    if not (current_user.id == submission.student_id or (current_user.is_authenticated and current_user.role in INSTRUCTOR_ROLES and assignment.instructor_id == current_user.id)):
        abort(403)
    form = GradeForm()
    if form.validate_on_submit():
        # only instructor can grade
        if not (current_user.is_authenticated and current_user.role in INSTRUCTOR_ROLES and assignment.instructor_id == current_user.id):
            abort(403)
        # create or update grade
        if submission.grade:
            submission.grade.score = float(form.score.data)
            submission.grade.feedback = form.feedback.data
        else:
            g = Grade(submission_id=submission.id, grader_id=current_user.id, score=float(form.score.data), feedback=form.feedback.data)
            db.session.add(g)
        db.session.commit()
        flash('Grade saved.', 'success')
        return redirect(url_for('main.submission_detail', id=id))

    # prefill
    if submission.grade and request.method == 'GET':
        form.score.data = str(submission.grade.score)
        form.feedback.data = submission.grade.feedback

    return render_template('main/submissions/detail.html', submission=submission, form=form, grade=submission.grade)


@main_bp.route('/submissions/<int:id>/delete', methods=['POST'])
@login_required
def delete_submission(id):
    submission = Submission.query.get_or_404(id)
    if not (current_user.id == submission.student_id or (current_user.is_authenticated and current_user.role in INSTRUCTOR_ROLES and submission.assignment.instructor_id == current_user.id)):
        abort(403)
    aid = submission.assignment_id
    db.session.delete(submission)
    db.session.commit()
    flash('Submission deleted.', 'success')
    return redirect(url_for('main.assignment_detail', id=aid))


# ========== COURSES ==========


@main_bp.route('/courses')
@login_required
def list_courses():
    courses = Course.query.all()
    return render_template('main/courses/list.html', courses=courses)


@main_bp.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if not is_instructor(current_user):
        abort(403)
    if request.method == 'POST':
        name = request.form.get('course_name')
        if not name:
            flash('Course name required', 'error')
            return redirect(url_for('main.create_course'))
        c = Course(course_name=name)
        db.session.add(c)
        db.session.commit()
        flash('Course created', 'success')
        return redirect(url_for('main.list_courses'))
    return render_template('main/courses/create.html')


@main_bp.route('/courses/<int:id>')
@login_required
def course_detail(id):
    course = Course.query.get_or_404(id)
    assignments = Assignment.query.filter_by(course_id=course.id).all()
    materials = CourseMaterial.query.filter_by(course_id=course.id).all()
    return render_template('main/courses/detail.html', course=course, assignments=assignments, materials=materials)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    # instructor view
    if current_user.role in INSTRUCTOR_ROLES:
        assignments = Assignment.query.filter_by(instructor_id=current_user.id).all()
        materials = CourseMaterial.query.filter_by(instructor_id=current_user.id).all()
        # count ungraded submissions per assignment
        ungraded = {a.id: Submission.query.filter_by(assignment_id=a.id).filter(Submission.grade == None).count() for a in assignments}
        return render_template('main/dashboard_instructor.html', assignments=assignments, materials=materials, ungraded=ungraded)

    # student view
    else:
        # assignments student hasn't submitted yet
        subs = Submission.query.filter_by(student_id=current_user.id).all()
        submitted_assignment_ids = [s.assignment_id for s in subs]
        pending = Assignment.query.filter(~Assignment.id.in_(submitted_assignment_ids)).all()
        materials = CourseMaterial.query.all()
        return render_template('main/dashboard_student.html', assignments=pending, materials=materials)



# ========== COURSE MATERIALS ROUTES ==========

@main_bp.route("/materials")
@login_required
def list_materials():
    """List all course materials"""
    materials = CourseMaterial.query.all()
    return render_template("main/materials/list.html", materials=materials)

@main_bp.route("/materials/<int:id>")
@login_required
def material_detail(id):
    """View material details"""
    material = CourseMaterial.query.get_or_404(id)
    return render_template("main/materials/detail.html", material=material)

@main_bp.route("/materials/create", methods=["GET", "POST"])
@login_required
def create_material():
    """Create a new course material"""
    #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to create materials", "danger")#display error message
        return redirect(url_for("main.list_materials"))
    courses = Course.query.all()
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        course_id = request.form.get('course_id') or None
        
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
    
    return render_template("main/materials/create.html", courses=courses)

@main_bp.route("/materials/<int:id>/delete", methods=["POST"])
@login_required
def delete_material(id):
    """Delete a course material"""
     #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to delete materials", "danger")#display error message
        return redirect(url_for("main.material_detail"))
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


@main_bp.route('/materials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_material(id):
    material = CourseMaterial.query.get_or_404(id)
    if current_user.role != 'instructor' or material.instructor_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title or not description:
            flash('Title and description are required.', 'error')
            return redirect(url_for('main.edit_material', id=id))
        material.title = title
        material.description = description
        db.session.commit()
        flash('Material updated.', 'success')
        return redirect(url_for('main.material_detail', id=id))

    return render_template('main/materials/edit.html', material=material)



