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


please be on the most recent but most stable version on python

to run code: 

libraries:
pip install PyPDF2 to read pdfs using python

flush database: 
python manage.py flush
type yes if prompted. 

run scripts:
curriculum/management/scripts
python manage.py import_pdf_curriculum 

practice/management/commands
python manage.py import_pdf_practice fixtures/multiplication_grade3.pdf --skillset "Grade 3 Multiplication Practice (PDF Import)" --standard "Multiplication and division within 100"

just in case: 
python manage.py makemigrations
python manage.py migrate

then runsever
python manage.py runserver
