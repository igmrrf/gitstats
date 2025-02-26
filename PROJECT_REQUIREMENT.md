# Project Requirements: GitHub Stats Application

## Overview

The GitHub Stats Application is a web-based application that allows users to log in with their GitHub accounts to gain insights into their programming habits. It collects data from both private and public repositories to generate detailed statistics, charts, and a resume based on the user's GitHub profile. Users can also share their profiles with unique links and get a rating for each language they use.

## Features

### 1. User Authentication
- **Requirement**: The application must allow users to log in using their GitHub accounts.
- **Implementation**: Use GitHub OAuth for authentication.
- **Endpoints**:
  - **GET /auth/login**: Display the login page.
  - **POST /auth/login**: Handle GitHub OAuth login.
  - **GET /auth/logout**: Log out the user.

### 2. Permission Requests
- **Requirement**: The application must request access to both private and public repositories of the user.
- **Implementation**: Configure GitHub OAuth scopes to include `repo` (full control of private repositories) and `public_repo` (access to public repositories).

### 3. Language Statistics
- **Requirement**: The application must collect and display statistics on the languages used in all accessed repositories.
- **Implementation**: Use the GitHub API to fetch repository data and aggregate language statistics.

### 4. Charts
- **Requirement**: The application must generate and display charts based on language usage and other statistics.
- **Implementation**: Use a charting library (e.g., Chart.js) to visualize the data.

### 5. AI-Generated Resume
- **Requirement**: The application must integrate an AI model to generate a resume based on the user's GitHub profile.
- **Implementation**: Use a pre-trained AI model or API (e.g., OpenAI's GPT-3) to generate the resume.

### 6. Programming Insights
- **Requirement**: The application must provide insights into user programming habits, such as peak programming times, total lines of code, average lines of code, etc.
- **Implementation**: Analyze commit history and other GitHub data to generate insights.

### 7. Profile Sharing
- **Requirement**: The application must allow users to share their profiles with unique links.
- **Implementation**: Generate and provide a unique URL for each user's profile that can be shared.

### 8. Language Rating System
- **Requirement**: The application must generate a rating system for each language used by the user.
- **Implementation**: Create a scoring algorithm based on language usage, expertise, and other factors.

