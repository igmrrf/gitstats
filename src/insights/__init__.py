from collections import defaultdict
from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from src.common.cache import cache
from src.common.db import db
from src.dashboard.models.stats import Stats
from src.services.github import GitHubApi

insights_bp = Blueprint("insights", __name__)


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


@insights_bp.route("/lang")
@login_required
@cache.memoize(timeout=3600)
def get_language_insights():
    stats = db.session.query(Stats).filter_by(user_id=current_user.id).all()

    return jsonify(
        {
            "languages": [stat.language for stat in stats],
            "lines_of_code": [stat.lines_of_code for stat in stats],
            "ratings": [stat.rating for stat in stats],
            "repos_count": [stat.repositories_count for stat in stats],
        }
    )


@insights_bp.route("/top-languages")
@login_required
def get_top_languages():
    stats = (
        Stats.query.filter_by(user_id=current_user.id)
        .order_by(Stats.lines_of_code.desc())
        .limit(5)
        .all()
    )

    return jsonify(
        [
            {
                "language": stat.language,
                "lines_of_code": stat.lines_of_code,
                "rating": stat.rating,
            }
            for stat in stats
        ]
    )


@insights_bp.route("/repositories")
@login_required
def get_repository_insights():
    github = GitHubApi(current_user.access_token)
    repos = github.get_repos()

    return jsonify(
        {
            "repositories": [
                {
                    "name": repo["name"],
                    "description": repo["description"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo["language"],
                }
                for repo in repos
            ]
        }
    )


@insights_bp.route("/commit-patterns")
@login_required
@cache.memoize(timeout=3600)
def get_commit_patterns():
    github = GitHubApi(current_user.access_token)
    repos = github.get_repos()

    commit_days = defaultdict(int)

    for repo in repos:
        activity = github.get_commit_activity(repo["full_name"])
        if activity:
            for week in activity:
                for day, count in enumerate(week.get("days", [])):
                    commit_days[day] += count

    return jsonify(
        {
            "daily_patterns": commit_days,
            "peak_day": max(commit_days.items(), key=lambda x: x[1])[0],
        }
    )


@insights_bp.route("/code-frequency")
@login_required
@cache.memoize(timeout=3600)
def get_code_frequency():
    github = GitHubApi(current_user.access_token)
    repos = github.get_repos()

    total_additions = 0
    total_deletions = 0
    frequency_data = []

    for repo in repos:
        stats = github.get_repo_stats(repo["full_name"])
        if stats:
            for stat in stats:
                total_additions += stat[1]
                total_deletions += stat[2]
                frequency_data.append(
                    {"week": stat[0], "additions": stat[1], "deletions": stat[2]}
                )

    return jsonify(
        {
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "frequency_data": frequency_data,
        }
    )


@insights_bp.route("/repo/<repo_name>")
@login_required
@cache.memoize(timeout=1800)
def get_repo_insights(repo_name):
    github = GitHubApi(current_user.access_token)

    # Get repository details
    repo_data = github.get_repo_details(repo_name)
    commit_data = github.get_repo_commits(repo_name)

    return jsonify(
        {
            "name": repo_data["name"],
            "stars": repo_data["stargazers_count"],
            "forks": repo_data["forks_count"],
            "issues": repo_data["open_issues_count"],
            "commit_frequency": commit_data,
            "contributors": github.get_repo_contributors(repo_name),
        }
    )
