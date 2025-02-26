from flask import Blueprint, jsonify, render_template, request

from src.auth.models.user import User
from src.common.error import ValidationError

from src.common.db import db
from .models.insight import Insight

core_bp = Blueprint("core", __name__, template_folder="templates")


@core_bp.route("/")
def index():
    return render_template("index.html")


@core_bp.route("/health")
def health():
    return jsonify({"health": "healthy"})


@core_bp.route("/profile/<profile_id>")
def profile(profile_id):
    user = User.query.filter_by(profile_url=profile_id).first_or_404()
    return render_template("shared_profile.html", user=user)


@core_bp.route("/get_insight")
def get_insight():
    insight = Insight(page="home")
    db.session.add(insight)
    db.session.commit()
    return jsonify(
        {"message": "success", "insight": {"id": insight.id, "page": insight.page}}
    )


@core_bp.route("/add_insight", methods=["POST"])
def add_insight():
    data = request.get_json()
    print(data)
    if "page" not in data:
        raise ValidationError("missing page field")

    insight = Insight(page=data["page"])
    db.session.add(insight)
    db.session.commit()
    return jsonify(
        {"message": "success", "insight": {"id": insight.id, "page": insight.page}}
    )
