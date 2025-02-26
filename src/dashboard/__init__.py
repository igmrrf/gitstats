import uuid
from collections import defaultdict

import openai
from flask import Blueprint, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from src.auth.models.user import User
from src.common.cache import cache
from src.common.db import db
from src.services.github import GitHubApi

from .models.stats import Stats

dashboard_bp = Blueprint("dashboard", __name__)


def calculate_rating(stats):

    # Simple rating algorithm based on lines of code and repository count
    # Scale: 0-100
    lines_weight = 0.7
    repos_weight = 0.3

    # Normalize lines of code (assume max 1M lines)
    lines_score = min(stats["lines_of_code"] / 1000000 * 100, 100)

    # Normalize repository count (assume max 50 repos)
    repos_score = min(stats["repos_count"] / 50 * 100, 100)

    return (lines_score * lines_weight) + (repos_score * repos_weight)


@dashboard_bp.route("/")
@login_required
def profile(profile_id):
    user = User.query.filter_by(profile_url=profile_id).first_or_404()
    return render_template("dashboard.dashboard.html", user=user)


@dashboard_bp.route("/settings", methods=["GET"])
@login_required
def get_settings():
    default = {
        "theme": "light",  # Default settings
        "chart_colors": "default",
        "default_view": "repositories",
        "private_repos_visible": True,
    }
    return jsonify(current_user.preferences or default)


@dashboard_bp.route("/settings", methods=["POST"])
@login_required
def update_settings():
    data = request.get_json()
    current_user.preferences = {
        "theme": data.get("theme", "light"),
        "chart_colors": data.get("chart_colors", "default"),
        "default_view": data.get("default_view", "overview"),
        "private_repos_visible": data.get("private_repos_visible", True),
    }
    db.session.commit()
    # Here you would typically save these to the database
    return jsonify({"status": "success"})


@dashboard_bp.route("/refresh_stats")
@login_required
@cache.memoize(timeout=3600)
def refresh_stats():
    github = GitHubApi(current_user.access_token)

    # Get all repositories
    repos = github.get_repos()

    # Aggregate language statistics
    language_stats = {}
    for repo in repos:
        language = github.get_repo_languages(repo["full_name"])
        for lang, bytes_count in language.items():
            if lang not in language_stats:
                language_stats[lang] = {"lines_of_code": 0, "repos_count": 0}
            language_stats[lang]["lines_of_code"] += bytes_count
            language_stats[lang]["repos_count"] += 1

    # Update database
    for lang, stats in language_stats.items():
        lang_stat = (
            db.session.query(Stats)
            .filter_by(user_id=current_user.id, language=lang)
            .first()
        )
        if not lang_stat:
            lang_stat = Stats(user_id=current_user.id, language=lang)
            db.session.add(lang_stat)

        lang_stat.lines_of_code = stats["lines_of_code"]
        lang_stat.repositories_count = stats["repos_count"]

        lang_stat.rating = calculate_rating(stats)

    db.session.commit()
    return jsonify({"message": "success", "success": True})


@dashboard_bp.route("/generate-share-link")
@login_required
def generate_share_link():
    if not current_user.profile_url:
        current_user.profile_url = str(uuid.uuid4())
        db.session.commit()

    share_url = url_for(
        "dashboard.profile", profile_id=current_user.profile_url, _external=True
    )
    return jsonify({"share_url": share_url})


@dashboard_bp.route("/generate-resume")
@login_required
@cache.memoize(timeout=3600)
def generate_resume():
    github = GitHubApi(current_user.access_token)
    repos = github.get_repos()

    # Prepare context for AI
    context = {
        "repositories": [
            {
                "name": repo["name"],
                "description": repo["description"],
                "languages": github.get_repo_languages(repo["full_name"]),
                "stars": repo["stargazers_count"],
            }
            for repo in repos[:5]  # Use top 5 repos
        ]
    }

    # Generate resume using OpenAI
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume writer. Create a technical resume based on GitHub profile data.",
            },
            {
                "role": "user",
                "content": f"Create a technical resume for a developer with the following GitHub repositories: {context}",
            },
        ],
    )

    return jsonify({"resume": response.choices[0].message.content})
