import csv, io
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from core.decorators import role_required
from .forms import TestForm, CSVTestQuestionUploadForm
from .models import Test, Question

@role_required("teacher")
def teacher_create_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save()
            messages.success(request, f"Test '{test.title}' created.")
            return redirect("assessments:teacher_bulk_test_upload")
    else:
        form = TestForm()
    return render(request, "assessments/teacher_create_test.html", {"form": form})

@role_required("teacher")
def teacher_bulk_test_upload(request):
    if request.method == "POST":
        form = CSVTestQuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            return _handle_csv(request, form)
    else:
        form = CSVTestQuestionUploadForm()
    return render(request, "assessments/teacher_bulk_test_upload.html", {"form": form})

def _handle_csv(request, form):
    f = form.cleaned_data["csv_file"]
    default_test = form.cleaned_data.get("default_test")
    replace_existing = form.cleaned_data.get("replace_existing") or False

    try:
        reader = csv.DictReader(io.TextIOWrapper(f.file, encoding="utf-8"))
    except Exception as e:
        messages.error(request, f"Invalid CSV: {e}")
        return redirect("assessments:teacher_bulk_test_upload")

    grouped, errors = {}, []
    for i, row in enumerate(reader, start=2):
        test_id = (row.get("test_id") or "").strip()
        if test_id:
            test = Test.objects.filter(id=test_id).first()
            if not test:
                errors.append(f"Line {i}: test_id '{test_id}' not found")
                continue
        else:
            if not default_test:
                errors.append(f"Line {i}: no 'test_id' and no default Test selected")
                continue
            test = default_test

        prompt = (row.get("prompt") or "").strip()
        answer = (row.get("answer") or "").strip()
        if not prompt or not answer:
            errors.append(f"Line {i}: prompt and answer required")
            continue

        choices = (row.get("choices") or "").strip()
        explanation = (row.get("explanation") or "").strip()
        order = row.get("order")
        try:
            order = int(order) if order else None
        except:
            errors.append(f"Line {i}: order must be integer")
            continue

        grouped.setdefault(test, []).append({
            "prompt": prompt, "answer": answer,
            "choices": choices, "explanation": explanation, "order": order
        })

    if errors:
        for e in errors: messages.error(request, e)
        return redirect("assessments:teacher_bulk_test_upload")

    created = 0
    with transaction.atomic():
        for test, rows in grouped.items():
            if replace_existing:
                Question.objects.filter(test=test).delete()
            for d in rows:
                Question.objects.create(
                    test=test, prompt=d["prompt"],
                    correct_answer=d["answer"], choices=d["choices"],
                    explanation=d["explanation"], order=d["order"]
                )
                created += 1

    messages.success(request, f"Imported {created} test questions.")
    return redirect("assessments:teacher_bulk_test_upload")
