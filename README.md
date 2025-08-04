## Hi there 👋

<!--
**MathLearningSite/MathLearningSite** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->


# Math Learning Django Project - Internal Setup Guide

## Python Version
Use the latest stable Python 3 (e.g. 3.11.x). 
Avoid preview or experimental builds like 3.13.

## Required Libraries
Install dependencies:

If missing PDF parsing support:
    pip install PyPDF2

## Fresh Setup (from scratch)

1. Flush the database (optional full reset):
    python manage.py flush
    # Type 'yes' if prompted

2. Run migrations to create tables:
    python manage.py makemigrations
    python manage.py migrate

3. Import the curriculum (Grades, Domains, Standards):
    python manage.py import_pdf_curriculum

4. Apply correct domain ordering for each grade:
    python manage.py set_domain_order

5. Import topics for Standards:
    # Uses fixtures/grade3_math_topics.json + topics_map.json
    python manage.py import_topics

6. Import practice questions (optional):
    python manage.py import_pdf_practice fixtures/multiplication_grade3.pdf \
      --skillset "Grade 3 Multiplication Practice (PDF Import)" \
      --standard "Multiplication and division within 100"

7. Run the development server:
    python manage.py runserver
    # Open http://127.0.0.1:8000/

## Data Flow
- Curriculum.txt → populates Grades, Domains, Standards
- set_domain_order → fixes Domain sort order by grade
- grade3_math_topics.json + topics_map.json → creates Topics linked to Standards
- PDFs → creates Practice Questions linked to Standards

## One-liner for full reset
    python manage.py flush && python manage.py makemigrations && python manage.py migrate && python manage.py import_pdf_curriculum && python manage.py set_domain_order && python manage.py import_topics && python manage.py runserver



==============================
🌱 Gamification API - Frontend Integration Guide
==============================

This file explains how to connect the frontend of the Garden Dashboard to the backend gamification system.

------------------------------
✅ Requirements
------------------------------
- User must be logged in (session-based).
- All endpoints return JSON in this format:

{
  "status": "success",
  "data": { ... }
}

------------------------------
📡 API Endpoints
------------------------------

1. /gamification/dashboard/
- Method: GET
- Returns all gamification data:
  - plants
  - login streak
  - badges
  - garden health

Sample response:
{
  "status": "success",
  "data": {
    "plants": [
      { "category": "fractions", "growth_stage": "budding" }
    ],
    "streaks": {
      "current_streak": 5,
      "longest_streak": 12
    },
    "badges": [
      { "badge_type": "first_login", "unlocked_on": "2025-07-30T15:00:00Z" }
    ],
    "garden": {
      "health_score": 87,
      "visual_theme": "spring"
    }
  }
}


2. /gamification/streak/
- Method: POST
- Use this to update login streak (should be triggered on login or load)

Response:
{
  "status": "success",
  "data": {
    "current_streak": 5,
    "longest_streak": 12
  }
}


3. /gamification/progress/
- Method: POST
- Body example:
{
  "category": "fractions",
  "skill_mastered": true
}
- Tracks skill mastery and updates plant growth

Response:
{
  "status": "success",
  "data": {
    "updated_progress": {
      "category": "fractions",
      "percent_complete": 40.0,
      "skills_mastered": 2
    },
    "new_stage": "budding"
  }
}


4. /gamification/badges/
- Method: GET
- Returns list of all unlocked badges for the user


5. /gamification/garden/
- Method: GET
- Returns all plants and their current growth stages

Response:
{
  "status": "success",
  "data": [
    { "category": "fractions", "growth_stage": "bloomed" }
  ]
}


6. /gamification/categories/
- Method: GET
- Returns list of all categories the user can progress in

Sample:
{
  "status": "success",
  "data": [
    { "slug": "fractions", "name": "Fractions", "grade": "Grade 4" }
  ]
}

------------------------------
🧠 Frontend Ideas
------------------------------
- Show garden health score and theme
- Visualize plants using growth_stage (seedling, budding, bloomed)
- Display streak and badges with icons
- Use slugs to match categories with progress

------------------------------
🛠 Dev Notes
------------------------------
- All views require user to be logged in
- JSON responses follow REST conventions
- Can use fetch(), Axios, or HTMX to access


