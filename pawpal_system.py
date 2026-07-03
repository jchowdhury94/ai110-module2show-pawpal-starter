"""PawPal+ logic layer.

Backend classes for PawPal+, based on diagrams/uml.mmd:
Pet, CareTask, OwnerPreferences, DailyPlan.

Class skeleton only: names, attributes, and empty method stubs (no logic yet).
"""


class Pet:
    def __init__(self, name, species, age, needs):
        self.name = name
        self.species = species
        self.age = age
        self.needs = needs

    def update_pet_info(self):
        pass


class CareTask:
    def __init__(self, task_name, category, time_needed, priority, completed=False):
        self.task_name = task_name
        self.category = category
        self.time_needed = time_needed
        self.priority = priority
        self.completed = completed

    def mark_complete(self):
        pass

    def update_task(self):
        pass


class OwnerPreferences:
    def __init__(self, available_time, preferred_times, task_priorities):
        self.available_time = available_time
        self.preferred_times = preferred_times
        self.task_priorities = task_priorities

    def update_preferences(self):
        pass


class DailyPlan:
    def __init__(self, date, selected_tasks, explanation):
        self.date = date
        self.selected_tasks = selected_tasks
        self.explanation = explanation

    def generate_plan(self):
        pass

    def show_plan(self):
        pass
