from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Room(models.Model):
    """
    Represents a classroom with a specified number of rows and columns.
    It includes an optional gap in the seating arrangement and maintains a matrix representation.

    Warning:
        Currently, only a **single** gap is supported

    Attributes:
        rows (int):
            The number of rows in the room.
        columns (int):
            The number of columns in the room.
        gap (int, optional):
            Specifies after which column a gap should be inserted. Defaults to None.
        type (int):
            A unique identifier assigned incrementally based on the number of created rooms.
        matrix (list[list[str]]):
            A 2D list representing the seating arrangement, stored as a JSON field.
    """
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    columns = models.IntegerField(validators=[MinValueValidator(1)])
    gap = models.IntegerField(validators=[MinValueValidator(1)], null=True, default=None)
    type = models.IntegerField(null=True, blank=True)
    matrix = models.JSONField(null=True, blank=True)
    
    def Meta():
        unique_together = ('rows', 'columns', 'gap') 

    def generate_matrix(self):
        """
        Generates the seating matrix based on the current room attributes.
        Ensures that gaps are properly inserted if specified.

        Returns:
            list[list[str]]: A 2D list representing the seating arrangement.
        """
        if self.gap is not None and self.gap < self.columns:
            return [
                ["______"] * self.gap + ["    "] + ["______"] * (self.columns - self.gap)
                for _ in range(self.rows)
            ]
        else:
            return [["______"] * self.columns for _ in range(self.rows)]
        
    def clean(self):
        if self.gap > self.columns:
            raise ValidationError({'gap': 'Gap cannot be greater than the number of columns.'})
    
    def save(self, *args, **kwargs):
        """
        Modifies the instance before saving to database:
        
        - Auto-increments the `type` field when *new* object is created.
        - Generates and assigns a seating matrix when object is created or edited.
        """
        self.clean()

        if self.type is None:
            last_room = Room.objects.order_by('-type').first()
            self.type = 1 if last_room is None else last_room.type + 1


        self.matrix = self.generate_matrix()

        super().save(*args, **kwargs)
    
    def __str__(self):
        """
        Returns a string representation of the room instance.

        Returns:
            str: A formatted string displaying the room type.
        """
        return f"Type {self.type}"
    
    def display(self):
        """
        Returns a string representation of the room's seating arrangement.
        
        Returns:
            str: A formatted string where each row is joined with spaces to represent the matrix.
        """
        return "\n".join(" ".join(row) for row in self.matrix)
    

class Branch(models.Model):
    """
    Represents an Academic Branch with a specific year and student strength.

    Warning:
        - `name` can only contain **2** characters
        - `year` can only contain **2** characters

    Attributes:
        name (str): 
            The name of the branch (e.g., "CS", "CC", "EE").
        year (str): 
            The academic year (e.g., "24", "23", "25", "YY").
        strength (int): 
            The total number of students in the branch.

    Notes:
        - The combination of `year` and `name` must be unique.
        - Equality comparison (`==`) checks if two branches have the same `year` and `name`.
    """
    name = models.CharField(max_length=2)
    year = models.CharField(max_length=2)
    strength = models.IntegerField()

    class Meta:
        unique_together = ('year', 'name') # Enforces Uniqueness
        verbose_name = "Academic Branch" # Name for Admin Interface
        verbose_name_plural = "Academic Branches" # Plural Name for Admin Interface

    def __str__(self):
        """
        Returns:
            str: A string representation of the branch: (`year` + `name`).
        """
        return f"{self.year}{self.name}"
    
    def __eq__(self, other):
        """
        Checks equality between two Branch instances.

        Args:
            other (Branch): Another branch instance to compare with.

        Returns:
            bool: True if `year` and `name` are the same, False otherwise.
        """
        if isinstance(other, Room):
            return self.year == other.year and self.name == other.name
        return False
    
class Subject(models.Model):
    """
    Represents an exam with a specific code and associated branches.

    Warning:
        - The `code` attribute can only contain **7** characters

    Attributes:
        code (str): 
            The unique code of the examination (e.g., "GMAT101").
        branches (ManyToMany): 
            A many-to-many relationship with `Branch` to associate exams with multiple branches (Also Reverse Relation).
    """
    code = models.CharField(max_length=7, unique=True)
    branches = models.ManyToManyField(Branch, related_name="subjects")

    def __str__(self):
        """
        Returns:
            str: A string representation of the exam: `code`.
        """
        return self.code
    
    def display(self):
        """
        Returns:
            str: A formatted string displaying the exam details.
        """
        return f"Code: {self.code} | Date: {self.date} | Time: {self.time}"
    
class Event(models.Model):
    """
    Represents an examination event (e.g., Mid-Terms 2022, Finals 2023).

    Attributes:
        name (str): 
            The name of the examination event.
        start_date (date): 
            The start date of the examination event.
        end_date (date): 
            The end date of the examination event.
    """
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "Examination Event"
        verbose_name_plural = "Examination Events"

    def __str__(self):
        return self.name
    
class Exam(models.Model):
    """
    Represents an exam within an event, associated with a specific branch and subject.

    Attributes:
        event (Event):
            The associated examination event.
        branch (Branch):
            The branch participating in the exam.
        subject (Subject):
            The specific subject for the exam.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='exams')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='+')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='+')
    strength = models.IntegerField(default=0)

    class Meta:
        unique_together = ('event', 'branch', 'subject')\
        
    def save(self, *args, **kwargs):
        """
        Ensures that `strength` defaults to the `branch.strength` value if left as 0.
        If the user manually edits `strength`, it keeps the user-defined value.
        """
        if self.strength == 0 and self.branch:
            self.strength = self.branch.strength  # Default to branch's strength
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.event} | {self.branch} - {self.subject}"

class ExamRoom(models.Model):
    """
    Represents a room assigned for an exam.

    Warning:
        - Room Number has a maximum cap at 999

    Attributes:
        room (Room): 
            The associated Room instance.
        number (int): 
            The exam room number.
        matrix (JSONField): 
            The seating matrix copied from the associated room.
        branches (ManyToManyField): 
            A one-way many-to-many relationship storing multiple Branch instances, 
            but without linking back to ExamRoom.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='exam_rooms')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='+')
    exam_data = models.JSONField(default=list)
    number = models.IntegerField(validators=[MaxValueValidator(999)])
    matrix = models.JSONField(null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    class Meta:
        verbose_name = "Exam Room"
        verbose_name_plural = "Exam Rooms"

    def __str__(self):
        """
        Returns:
            str: A string representation of the exam: (Exam Room + `number`).
        """
        return f"Room {self.number}"

    def display_info(self):
        """
        Returns a formatted string containing details about the exam room.

        Returns:
            str: A string representation of the exam room details.
        """
        return f"Type: {self.room.type}\nNumber: {self.number}\nBranches: {self.branches_range}\n"

    def clear(self):
        """
        Resets the matrix to the current configuration of the associated room.
        This ensures that the exam room seating layout, when cleared, mirrors the latest setup
        of the selected room.
        """
        self.matrix = self.room.matrix
        self.save()

    def save(self, *args, **kwargs):
        # Fetch related exam entries
        if not self.pk:
            super().save(*args, **kwargs)
            
        self.exam_data = self.get_exam_entries()
        super().save(*args, **kwargs)  # Save updated data

    def get_exam_entries(self):
        # Fetch all related exams and format them as JSON
        return list(self.exam_entries.values("exam_id", "roll_start", "roll_end"))


class ExamEntry(models.Model):
    exam_room = models.ForeignKey(ExamRoom, related_name="exam_entries", on_delete=models.CASCADE)
    exam_id = models.IntegerField()  # Reference to the actual exam
    roll_start = models.IntegerField()
    roll_end = models.IntegerField()