from typing import Any, List
from flask import current_app
import requests
import time
from ..common.const import (
    github_client_id,
    github_client_secret,
    github_base_url,
    github_api_url,
)


class GitHubApi:
    def __init__(self, access_token):
        self.session = requests.session()
        self.session.headers.update({"Authorization": f"token {access_token}"})
        self.access_token = access_token
        self.headers = {"Authorization": f"token {access_token}"}

    def get_repos(self):
        try:
            response = self.session.get(f"{github_api_url}/user/repos?per_page=100")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return []

    def get_repo_languages(self, repo_full_name) -> List[Any]:
        try:
            response = self.session.get(
                f"{github_api_url}/repos/{repo_full_name}/languages"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return []

    def get_commit_activity(self, repo_full_name):
        try:
            response = self.session.get(
                f"{github_api_url}/repos/{repo_full_name}/stats/commit_activity"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return None

    def get_repo_stats(self, repo_name):
        try:
            url = f"{github_api_url}/repos/{repo_name}/stats/code_frequency"
            response = self.session.get(url)
            if response.status_code == 202:
                time.sleep(2)
                response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return []

    def get_repo_details(self, repo_name):
        try:
            response = self.session.get(f"{github_api_url}/repos/{repo_name}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return None

    def get_repo_commits(self, repo_name):
        try:
            response = self.session.get(f"{github_api_url}/repos/{repo_name}/commits")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return None

    def get_repo_contributors(self, repo_name):
        try:
            response = self.session.get(
                f"{github_api_url}/repos/{repo_name}/contributors"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            current_app.logger.error(f"error fetching repositories: {str(exception)}")
            return None
