from pawpal_system import Pet, Task, Owner, Scheduler

owner = Owner(
    available_time="2 hours",
    preferred_times=["morning", "evening"],
    task_priorities=["feeding", "walking"],
)

pet1 = Pet(name="Biscuit", species="Dog", age=4, needs=["walking", "feeding", "grooming"])
pet2 = Pet(name="Whiskers", species="Cat", age=2, needs=["feeding", "litter box cleaning"])

owner.add_pet(pet1)
owner.add_pet(pet2)

task1 = Task(description="Morning walk", time="07:00", frequency="daily")
task2 = Task(description="Feed breakfast", time="08:00", frequency="daily")
task3 = Task(description="Clean litter box", time="18:00", frequency="weekly")
task4 = Task(description="Feed Whiskers breakfast", time="07:00", frequency="daily")

pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)
pet2.add_task(task4)

scheduler = Scheduler(owner, date="Today")
scheduler.generate_plan()


def task_priority(task):
    description = task.description.lower()
    for keyword in owner.task_priorities:
        keyword = keyword.lower()
        stem = keyword[:-3] if keyword.endswith("ing") else keyword
        if stem in description:
            return "High"
    return "Normal"


def print_schedule(scheduler):
    title = f"Daily Schedule - {scheduler.date}" if scheduler.date else "Daily Schedule"
    width = max(40, len(title) + 4)
    print("=" * width)
    print(title.center(width))
    print("=" * width)

    tasks = scheduler.selected_tasks
    if not tasks:
        print()
        print("  No tasks scheduled.")
    else:
        num_width = len(str(max(len(pet.get_tasks()) for pet in owner.pets if pet.get_tasks())))
        desc_width = max(len("Task"), *(len(t.description) for t in tasks))
        freq_width = max(len("Frequency"), *(len(t.frequency) for t in tasks))
        priority_width = max(len("Priority"), *(len(task_priority(t)) for t in tasks))

        for pet in owner.pets:
            pet_tasks = [t for t in tasks if t in pet.get_tasks()]
            if not pet_tasks:
                continue

            print()
            print(f"Daily plan for {pet.name} ({pet.species}):")

            header = (
                f"  {'#':>{num_width}}  {'Time':<5} {'Task'.ljust(desc_width)}  "
                f"{'Frequency'.ljust(freq_width)}  {'Priority'.ljust(priority_width)}  Completed"
            )
            print(header)
            print("  " + "-" * (len(header) - 2))

            for i, task in enumerate(pet_tasks, start=1):
                completed = "Yes" if task.completed else "No"
                print(
                    f"  {str(i).rjust(num_width)}  {task.time:<5} "
                    f"{task.description.ljust(desc_width)}  "
                    f"{task.frequency.ljust(freq_width)}  "
                    f"{task_priority(task).ljust(priority_width)}  {completed}"
                )

    print()
    print("-" * width)
    if scheduler.explanation:
        print(scheduler.explanation)


print_schedule(scheduler)

conflict_warnings = [w for w in scheduler.get_conflict_warnings() if w.startswith("Conflict at")]
if conflict_warnings:
    print()
    print("!" * 60)
    print("WARNING: SCHEDULING CONFLICT(S) DETECTED")
    print("!" * 60)
    for warning in conflict_warnings:
        print(f"  - {warning}")

all_tasks = owner.get_all_tasks()
total_tasks = len(all_tasks)
completed_tasks = sum(1 for task in all_tasks if task.completed)
pending_tasks = total_tasks - completed_tasks

print()
print("Summary")
print("-------")
print(f"Total tasks: {total_tasks}")
print(f"Pending: {pending_tasks}")
print(f"Completed: {completed_tasks}")


def print_task_list(title, tasks):
    print()
    print(title)
    print("-" * len(title))
    if not tasks:
        print("  No tasks found.")
        return
    for task in tasks:
        pet = next((p for p in owner.pets if task in p.get_tasks()), None)
        pet_label = f" ({pet.name})" if pet else ""
        completed = "Yes" if task.completed else "No"
        print(f"  {task.time:<5} {task.description}{pet_label} - {task.frequency}, Due: {task.due_date}, Completed: {completed}")


pending_only = owner.get_all_tasks(completed=False)
print_task_list("Pending Tasks", pending_only)

biscuit_tasks = owner.get_all_tasks(pet_name="Biscuit")
print_task_list("Biscuit's Tasks", biscuit_tasks)


print()
print("Recurring Task Demo")
print("===================")
print_task_list("Biscuit's Tasks (before completing 'Morning walk')", pet1.get_tasks())

pet1.complete_task("Morning walk")

print_task_list("Biscuit's Tasks (after completing 'Morning walk')", pet1.get_tasks())
