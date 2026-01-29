import csv, io, os
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.core.management import call_command
from django.conf import settings
from core.decorators import role_required

from .forms import CSVPracticeUploadForm, PDFPracticeUploadForm
from .models import PracticeQuestion, SkillSet

@role_required("teacher")
def teacher_upload_practice(request):
    csv_form = CSVPracticeUploadForm()
    pdf_form = PDFPracticeUploadForm()

    if request.method == "POST":
        if "submit_csv" in request.POST:
            csv_form = CSVPracticeUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                return _handle_csv(request, csv_form)
        elif "submit_pdf" in request.POST:
            pdf_form = PDFPracticeUploadForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                return _handle_pdf(request, pdf_form)

    return render(request, "practice/teacher_upload_practice.html", {
        "csv_form": csv_form, "pdf_form": pdf_form
    })

def _handle_csv(request, form):
    f = form.cleaned_data["csv_file"]
    default_skill = form.cleaned_data.get("default_skill_set")
    replace_existing = form.cleaned_data.get("replace_existing") or False

    try:
        reader = csv.DictReader(io.TextIOWrapper(f.file, encoding="utf-8"))
    except Exception as e:
        messages.error(request, f"Invalid CSV: {e}")
        return redirect("practice:teacher_upload_practice")

    grouped, errors = {}, []
    for i, row in enumerate(reader, start=2):
        skillname = (row.get("skill_set") or "").strip()
        if skillname:
            skill = SkillSet.objects.filter(title__iexact=skillname).first()
            if not skill:
                errors.append(f"Line {i}: SkillSet '{skillname}' not found")
                continue
        else:
            if not default_skill:
                errors.append(f"Line {i}: no 'skill_set' and no default Skill Set selected")
                continue
            skill = default_skill

        prompt = (row.get("prompt") or "").strip()
        answer = (row.get("answer") or "").strip()
        if not prompt or not answer:
            errors.append(f"Line {i}: prompt and answer are required")
            continue

        choices = (row.get("choices") or "").strip()
        explanation = (row.get("explanation") or "").strip()
        order = row.get("order")
        try:
            order = int(order) if order else None
        except:
            errors.append(f"Line {i}: order must be integer")
            continue

        grouped.setdefault(skill, []).append({
            "prompt": prompt, "answer": answer,
            "choices": choices, "explanation": explanation, "order": order
        })

    if errors:
        for e in errors: messages.error(request, e)
        return redirect("practice:teacher_upload_practice")

    created = 0
    with transaction.atomic():
        for skill, rows in grouped.items():
            if replace_existing:
                PracticeQuestion.objects.filter(skill_set=skill).delete()
            for d in rows:
                PracticeQuestion.objects.create(
                    skill_set=skill,
                    prompt=d["prompt"],
                    correct_answer=d["answer"],
                    choices=d["choices"],          # "" or "A||B||C"
                    explanation=d["explanation"],
                    order=d["order"]
                )
                created += 1

    messages.success(request, f"Imported {created} practice questions.")
    return redirect("practice:teacher_upload_practice")

def _handle_pdf(request, form):
    pdf_file = form.cleaned_data["pdf_file"]
    skillset_title = form.cleaned_data["skillset_title"].strip()
    standard_code = form.cleaned_data["standard_code"].strip()
    reset = form.cleaned_data.get("reset") or False

    upload_dir = settings.MEDIA_ROOT / "teacher_uploads"
    os.makedirs(upload_dir, exist_ok=True)
    dest = upload_dir / pdf_file.name
    with open(dest, "wb") as out:
        for chunk in pdf_file.chunks():
            out.write(chunk)

    args = [str(dest), "--skillset", skillset_title, "--standard-code", standard_code]
    if reset: args.append("--reset")

    try:
        call_command("import_pdf_practice", *args)
    except Exception as e:
        import traceback
        messages.error(request, f"PDF import failed: {e}\n{traceback.format_exc()}")
        return redirect("practice:teacher_upload_practice")

    messages.success(request, "PDF imported into Practice successfully.")
    return redirect("practice:teacher_upload_practice")
