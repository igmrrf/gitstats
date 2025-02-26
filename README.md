# GitHub Stats Application

A powerful Flask-based web application that provides detailed insights into GitHub profiles and programming habits. The application analyzes both private and public repositories to generate comprehensive statistics, visualizations, and AI-powered insights.

## Features

- **GitHub Authentication**: Secure login with GitHub OAuth
- **Repository Analysis**: Access and analyze both private and public repositories
- **Language Statistics**: 
  - Detailed breakdown of programming language usage
  - Language proficiency ratings
  - Lines of code statistics per language
- **Programming Insights**:
  - Peak programming time analysis
  - Commit patterns and frequency
  - Code addition/deletion metrics
- **AI-Generated Resume**: Automatically generate technical resumes based on GitHub profile data
- **Profile Sharing**: Share insights via unique profile links
- **Repository Details**:
  - Star counts
  - Fork statistics
  - Contributor information
  - Issue tracking

## Technology Stack

- **Backend**: Flask 3.1.0
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Caching**: Flask-Caching
- **Rate Limiting**: Flask-Limiter
- **AI Integration**: OpenAI GPT-3.5
- **API Integration**: GitHub REST API

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/github-stats.git
cd github-stats
```
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up environment variables:
Edit .env with your credentials:

```bash
FLASK_APP=run.py
FLASK_ENV=development
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
SECRET_KEY=your_secret_key
```

5. Initialize the database: (you can also run `make db-setup` )
```bash
flask init-db
```
## Running the Application

### Development
```bash
flask run
```
### Docker
```bash
docker-compose up
```
The application will be available at http://localhost:5000

## API Endpoints

### Authentication

- GET /auth/login : Initiate GitHub OAuth login
- GET /auth/callback : GitHub OAuth callback
- GET /auth/logout : Logout user

### Insights

- GET /insights/lang : Language usage statistics
- GET /insights/top-languages : Top 5 most used languages
- GET /insights/repositories : Repository overview
- GET /insights/commit-patterns : Commit frequency analysis
- GET /insights/code-frequency : Code addition/deletion metrics
- GET /insights/repo/<repo_name> : Individual repository insights

### Dashboard

- GET /dashboard/ : User dashboard
- GET /dashboard/settings : User preferences
- GET /dashboard/generate-resume : AI-generated technical resume
- GET /dashboard/generate-share-link : Generate profile sharing link

## Testing
Run the test suite:
```bash
pytest
 ```

## Contributing
1. Fork the repository
2. Create your feature branch ( git checkout -b feature/amazing-feature )
3. Commit your changes ( git commit -m 'Add amazing feature' )
4. Push to the branch ( git push origin feature/amazing-feature )
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

```plaintext
This README.md provides a comprehensive overview of the application, its features, setup instructions, and usage guidelines. It's structured to help both users and potential contributors understand and work with the application effectively.
```
