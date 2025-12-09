from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app import db
from app.models import Assignment, CourseMaterial
from flask_login import login_required, current_user

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
