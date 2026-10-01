from flask import Blueprint, request, jsonify
from models import db, Task
from schemas import TaskSchema

bp = Blueprint("tasks", __name__)
schema = TaskSchema()

@bp.get("/tasks")
def list_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = Task.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [t.to_dict() for t in pagination.items],
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages
    })

@bp.post("/tasks")
def create_task():
    errors = schema.validate(request.get_json())
    if errors:
        return jsonify(errors), 400
    data = schema.load(request.get_json())
    t = Task(**data)
    db.session.add(t); db.session.commit()
    return jsonify(t.to_dict()), 201

@bp.put("/tasks/<int:id>")
def update_task(id):
    t = Task.query.get_or_404(id)
    data = schema.load(request.get_json(), partial=True)
    for k, v in data.items():
        setattr(t, k, v)
    db.session.commit()
    return jsonify(t.to_dict())

@bp.delete("/tasks/<int:id>")
def delete_task(id):
    t = Task.query.get_or_404(id)
    db.session.delete(t); db.session.commit()
    return "", 204
