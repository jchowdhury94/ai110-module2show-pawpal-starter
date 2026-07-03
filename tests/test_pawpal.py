from pawpal_system import Pet, Task


def test_mark_complete_sets_completed_true():
    task = Task("Feed the cat", "08:00", "daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Whiskers", "cat", 3, "low-maintenance")
    task = Task("Feed the cat", "08:00", "daily")
    initial_count = len(pet.get_tasks())

    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_count + 1
