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
