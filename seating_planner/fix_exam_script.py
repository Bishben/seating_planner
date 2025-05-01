# resave_exams.py

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seating_planner.settings")
django.setup()

from home_page.models import Exam

def resave_all_exams():
    exams = Exam.objects.all()
    count = 0
    for exam in exams:
        exam.save()
        count += 1
    print(f"Re-saved {count} exams successfully.")

if __name__ == "__main__":
    resave_all_exams()
