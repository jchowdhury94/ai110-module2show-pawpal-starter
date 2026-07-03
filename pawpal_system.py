"""PawPal+ logic layer.

Backend classes for PawPal+, based on diagrams/uml.mmd:
Pet, Task, Owner, Scheduler.

Class skeleton only: names, attributes, and empty method stubs (no logic yet).
"""


class Pet:
    """Represents a pet and the care tasks associated with it."""

    def __init__(self, name, species, age, needs):
        """Initialize a pet with its basic info and an empty task list."""
        self.name = name
        self.species = species
        self.age = age
        self.needs = needs
        self.tasks = []

    def update_pet_info(self):
        """Update the pet's stored information (not yet implemented)."""
        pass

    def add_task(self, task):
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, description):
        """Remove any task matching the given description."""
        self.tasks = [task for task in self.tasks if task.description != description]

    def get_tasks(self):
        """Return this pet's list of tasks."""
        return self.tasks

    def get_summary(self):
        """Return a short summary string describing the pet and its task count."""
        return f"{self.name} the {self.species}, age {self.age} - {len(self.tasks)} task(s)"


class Task:
    """Represents a single care task with a schedule and completion state."""

    def __init__(self, description, time, frequency, completed=False):
        """Initialize a task with its description, time, frequency, and completion state."""
        self.description = description
        self.time = time
        self.frequency = frequency
        self.completed = completed

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.completed = False

    def update_task(self, description=None, time=None, frequency=None):
        """Update any provided fields (description, time, frequency) on this task."""
        if description is not None:
            self.description = description
        if time is not None:
            self.time = time
        if frequency is not None:
            self.frequency = frequency

    def get_summary(self):
        """Return a short summary string describing the task and its status."""
        status = "completed" if self.completed else "not completed"
        return f"{self.description} - {self.frequency}, {self.time} ({status})"


class Owner:
    """Represents a pet owner, their scheduling preferences, and their pets."""

    def __init__(self, available_time, preferred_times, task_priorities):
        """Initialize an owner with their scheduling preferences and an empty pet list."""
        self.available_time = available_time
        self.preferred_times = preferred_times
        self.task_priorities = task_priorities
        self.pets = []

    def update_preferences(self):
        """Update the owner's scheduling preferences (not yet implemented)."""
        pass

    def add_pet(self, pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, name):
        """Remove the pet matching the given name."""
        self.pets = [pet for pet in self.pets if pet.name != name]

    def get_pet(self, name):
        """Return the pet matching the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self):
        """Return a combined list of tasks across all of this owner's pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


class Scheduler:
    """Builds and displays a daily task schedule for an owner's pets."""

    def __init__(self, owner, date=None):
        """Initialize a scheduler for the given owner and optional date."""
        self.owner = owner
        self.date = date
        self.selected_tasks = []
        self.explanation = ""

    def generate_plan(self):
        """Order the owner's tasks by pending status and time, storing the result."""
        tasks = self.owner.get_all_tasks()
        pending = sorted((t for t in tasks if not t.completed), key=lambda t: t.time)
        completed = sorted((t for t in tasks if t.completed), key=lambda t: t.time)

        self.selected_tasks = pending + completed
        self.explanation = (
            f"{len(pending)} task(s) still pending, "
            f"{len(completed)} already completed, "
            f"ordered by time."
        )
        return self.selected_tasks

    def show_plan(self):
        """Return a formatted, human-readable string of the generated schedule."""
        title = f"Daily Schedule - {self.date}" if self.date else "Daily Schedule"
        width = max(40, len(title) + 4)
        lines = ["=" * width, title.center(width), "=" * width, ""]

        if not self.selected_tasks:
            lines.append("  No tasks scheduled.")
        else:
            num_width = len(str(len(self.selected_tasks)))
            desc_width = max(len("Task"), *(len(t.description) for t in self.selected_tasks))
            freq_width = max(len("Frequency"), *(len(t.frequency) for t in self.selected_tasks))

            header = (
                f"  {'#':>{num_width}}  {'Time':<5} {'Task'.ljust(desc_width)}  "
                f"{'Frequency'.ljust(freq_width)}  Completed"
            )
            lines.append(header)
            lines.append("  " + "-" * (len(header) - 2))

            for i, task in enumerate(self.selected_tasks, start=1):
                completed = "Yes" if task.completed else "No"
                lines.append(
                    f"  {str(i).rjust(num_width)}  {task.time:<5} "
                    f"{task.description.ljust(desc_width)}  "
                    f"{task.frequency.ljust(freq_width)}  {completed}"
                )

        lines.append("")
        lines.append("-" * width)
        if self.explanation:
            lines.append(self.explanation)

        return "\n".join(lines)
