from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app import db
from app.models import Assignment, CourseMaterial
from flask_login import login_required, current_user
from app.forms import AssignmentForm, MaterialForm

#Helper method to determine if instructor or not
INSTRUCTOR_ROLES= ("teacher","ta")
def is_instructor(user):
    return user.is_authenticated and user.role in INSTRUCTOR_ROLES


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
    return render_template("main/assignments/detail.html", assignment=assignment)

@main_bp.route("/assignments/create", methods=["GET", "POST"])
@login_required
def create_assignment():
    """Create a new assignment"""
    #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to create assignments", "danger")#displayu error
        return redirect(url_for("main.list_assignments"))
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        
        if not title or not description:
            flash("Title and description are required.", "error")
            return redirect(url_for("main.create_assignment"))
        
        assignment = Assignment(
            title=title,
            description=description,
            instructor_id=current_user.id
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
@main_bp.route("/assignments/<int:id>/edit", methods=["GET","POST"])
@login_required
def edit_assignment(id):
    #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to create assignments", "danger")#display error message
        return redirect(url_for("main.assignment_detail"))
    assignment=Assignment.query.get_or_404(id)
    if assignment.instructor_id != current_user.id:
        flash("You dont have permission to edit this assignment")
        return redirect(url_for("main.list_assignments"))
    form = AssignmentForm(obj=assignment)
    if form.validate_on_submit():
        assignment.title=form.title.data
        assignment.description=form.description.data
        db.session.commit()
        flash(f"Assignment '{assignment.title}' updated successfully!")
        return redirect(url_for("main.assignment_detail", id=assignment.id))
    return render_template("main/edit_assignment.html", form=form, assignment=assignment)



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
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        
        if not title or not description:
            flash("Title and description are required.", "error")
            return redirect(url_for("main.create_material"))
        
        material = CourseMaterial(
            title=title,
            description=description,
            instructor_id=current_user.id
        )
        db.session.add(material)
        db.session.commit()
        flash(f"Material '{title}' created successfully!", "success")
        return redirect(url_for("main.list_materials"))
    
    return render_template("main/materials/create.html")

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

@main_bp.route("/materials/<int:id>/edit",methods=["GET","POST"])
@login_required
def edit_material(id):
    #check if instructor
    if not is_instructor(current_user):
        flash("You do not have permission to edit materials", "danger")#display error message
        return redirect(url_for("main.material_detail"))
    material=CourseMaterial.query.get_or_404(id)
    if material.instructor_id != current_user.id:
        flash("You dont have permission to edit this material")
        return redirect(url_for("main.list_materials"))
    form = MaterialForm(obj=material)
    if form.validate_on_submit():
        material.title=form.title.data
        material.description=form.description.data
        db.session.commit()
        flash(f"Material '{material.title}' updated successfully!")
        return redirect(url_for("main.material_detail", id=material.id))
    return render_template("main/edit_material.html", form=form, material=material)

