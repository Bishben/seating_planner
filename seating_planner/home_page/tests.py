from django.test import TestCase
from .models import Event, Branch, Subject, Room, Exam, ExamRoom, ExamBranchRollRange
from datetime import date
# Create your tests here.

class ExamBranchRollRangeTestCase(TestCase):
    def setUp(self):
        # Create a branch
        self.branch = Branch.objects.create(
            name="Test Branch", 
            year=2023, 
            roll_ranges=[[1, 10], [11, 20]]
        )

        # Create a subject
        self.subject = Subject.objects.create(code="TESTT101")
        self.subject.branches.add(self.branch)
        
        # Create an event for the exam
        self.event = Event.objects.create(
            name="Test Event", 
            start_date=date(2023, 10, 1), 
            end_date=date(2023, 10, 5)
        )
        
        # Create an exam
        self.exam = Exam.objects.create(
            subject=self.subject,
            event=self.event,
            branch=self.branch,
            roll_ranges=[[1, 10], [12, 20]], # 19 rolls in total
        )
        
    def test_exam_branch_roll_range_creation(self):
        roll_range = ExamBranchRollRange.objects.create(
            exam=self.exam,
            roll_start=1,
            roll_end=5
        )

        self.assertEqual(roll_range.exam, self.exam)
        self.assertEqual(roll_range.roll_start, 1)
        self.assertEqual(roll_range.roll_end, 5)

        self.assertEqual(len(self.exam.unassigned_rolls), 14) # 19 - 5 = 14 unassigned rolls
        self.assertEqual(self.exam.unassigned_rolls, [6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20])