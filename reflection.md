# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design included four classes: Pet, CareTask, OwnerPreferences, and DailyPlan. The Pet class stores information about the pet, CareTask manages tasks like feeding and walks, OwnerPreferences stores the owner's schedule and preferences, and DailyPlan generates a daily schedule by selecting tasks based on the pet's needs and the owner's preferences.

3 core actions a user is able to perform: Add a pet, Schedule a care task, See today's pet care plan.

| Object               | Attributes                                            | Methods                        |
| -------------------- | ----------------------------------------------------- | ------------------------------ |
| **Pet**              | name, age, needs                                      | update_pet_info()              |
| **CareTask**         | task_name, category, time_needed, priority, completed | mark_complete(), update_task() |
| **OwnerPreferences** | available_time, preferred_times, task_priorities      | update_preferences()           |
| **DailyPlan**        | date, selected_tasks, explanation                     | generate_plan(), show_plan()   |

- What classes did you include, and what responsibilities did you assign to each?
I included four classes: Pet, CareTask, OwnerPreferences, and DailyPlan. The Pet class stores information about the pet, such as its name and needs. The CareTask class manages tasks like feeding, walks, and medication. The OwnerPreferences class stores the owner's available time and task preferences. The DailyPlan class is responsible for generating and displaying the pet's daily schedule based on the pet's tasks and the owner's preferences.
**b. Design changes**

- Did your design change during implementation?
Yes, my design changed significantly during implementation.
- If yes, describe at least one change and why you made it.
The biggest change was restructuring the whole class layout: CareTask, OwnerPreferences, and DailyPlan became Task, Owner, and Scheduler, with Owner holding multiple Pets, each Pet holding multiple Tasks, and Scheduler pulling from both instead of being a mostly-standalone object. I made this change because OwnerPreferences had no clean way to hold multiple pets and DailyPlan had no real link back to whose preferences it was using — the original split didn't hold up once I started implementing the scheduler for an owner with more than one pet. This is described in more detail in section 3b, including how I verified the new structure before adopting it.

I removed the add_pet() method from the Pet class because creating a Pet object already adds the pet to the system, so the class should focus on storing and updating pet information instead.

I changed the completed attribute in the CareTask class to default to False because new pet care tasks are usually incomplete when they are created, and this makes creating new tasks simpler and more realistic.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler considers task time, completion status, due date, frequency, pet name, and possible time conflicts.
- How did you decide which constraints mattered most?
I focused on time and completion status first because the main goal is to show what tasks still need to be done and in what order. I also added frequency and due dates because recurring pet care tasks, like feeding or walks, need to repeat over time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is in how `find_conflicts()` detects scheduling conflicts: it groups pending tasks by the exact pair `(due_date, minutes)` and only flags a conflict when two or more tasks land on that exact same start time. It does not look at how long each task takes, so it can't detect overlapping durations — for example, a 60-minute walk starting at 8:00 AM and a separate task starting at 8:15 AM would genuinely overlap, but since their start times don't match exactly, the scheduler would not warn about it.

I think this tradeoff is reasonable for now because exact-match detection is simple to implement and reason about, and it still catches the most obvious case (two tasks scheduled for the identical time). Real interval-overlap detection would require tracking a duration for every task and comparing time ranges pairwise, which adds real complexity for a scenario where most conflicts in practice are exact double-bookings. The known gap is that back-to-back or partially overlapping tasks can silently slip through, so this is something I'd want to improve if I extended the project.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I leaned on AI at almost every stage of this project, but the way I used it shifted as the project moved forward. Early on it was mostly a design sounding board — I'd describe the scenario (a pet owner juggling feeding, walks, and meds across multiple pets) and talk through whether four classes was the right split, or whether OwnerPreferences should be its own object instead of just fields on Pet. Once I had the UML skeleton, AI helped me translate it into actual Python: turning attributes into `__init__` signatures and stubbing out methods like `mark_complete()` and `generate_plan()` before I filled in the real logic myself. It was also useful for algorithm planning specifically around the scheduler — I asked it to help me reason through how recurring tasks should spawn their next occurrence (daily vs. weekly vs. monthly) and how to structure `find_conflicts()` around grouping by `(due_date, time)` rather than jumping straight to full interval-overlap math, which would've been overkill for this stage of the project.

Later, AI's role shifted more toward debugging, refactoring, and polish. When my pytest suite failed in ways I didn't immediately understand — like a recurring task not showing up after `mark_complete()` — I'd paste the failure and walk through the logic with AI until I could pinpoint whether the bug was in the task's date math or in how the owner's task list was being filtered. It was also helpful for refactoring once things got messy, like cleaning up repeated filtering logic between `Pet.get_tasks` and `Owner.get_all_tasks`. Toward the end, I used it to tighten up the README — turning my rough notes about features and algorithms into the tables and CLI walkthrough section. The prompts that worked best weren't generic ones like "fix my code" — they were ones where I described the specific behavior I expected versus what I was actually seeing, or pasted a real function and asked "does this handle X edge case?" Being specific about what I already understood versus what I was unsure about got me much more useful answers than just asking it to write something from scratch.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One clear moment was the class design itself. My first UML draft had CareTask, OwnerPreferences, and DailyPlan, and when I ran that past AI early on, it went along with the split and helped me flesh out attributes and methods for each class. But once I started actually implementing the scheduler and thinking through how an owner manages multiple pets, the design didn't hold up: OwnerPreferences was really just a bag of scheduling preferences with no clean way to hold multiple pets, and DailyPlan had no real link back to whose preferences it was using. I brought this back to AI, and it suggested renaming CareTask to Task, OwnerPreferences to Owner, and DailyPlan to Scheduler, and restructuring the relationships so Owner holds multiple Pets, each Pet holds multiple Tasks, and Scheduler pulls from both Owner and Task instead of being a mostly-standalone object.

I didn't adopt that rename just because AI proposed it — I checked it against the project's actual requirements and against whether it simplified or complicated the relationships between classes. I traced the three core actions (add a pet, schedule a task, view today's plan) through the new class names by hand to confirm each action only touched the classes it needed, without one class reaching into another's internals. I also checked that the association arrows in the diagram (`Owner "1" --> "*" Pet`, `Pet "1" --> "*" Task`, `Scheduler "1" --> "1" Owner`) matched the method calls I actually planned to write, not just what looked clean visually. I also pushed back on part of the suggestion: AI initially proposed putting `add_pet()` on Scheduler, but I kept it on Owner instead, since logically the owner — not the scheduler — is what owns the collection of pets. Once the structure held up under that check, I adopted the rename, and it's the version reflected in `diagrams/uml.mmd` and the final `app.py` implementation today.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I wrote a pytest suite (`tests/test_pawpal.py`) covering five core behaviors of the scheduler:

- **Task completion** (`test_mark_complete_sets_completed_true`): confirms a new `Task` defaults to `completed = False` and that calling `mark_complete()` flips it to `True`. This was important because so much of the scheduler's logic — what shows up in `generate_plan()`, what counts as "still pending" — depends on `completed` being set correctly at the right moment.
- **Adding tasks to pets** (`test_add_task_increases_pet_task_count`): confirms `pet.add_task()` actually grows the pet's task list by one. This is the basic building block every other test relies on, so if it silently failed to store the task, every downstream test would be meaningless.
- **Recurring task creation** (`test_complete_task_creates_next_day_occurrence_for_daily_task`): confirms that completing a daily task marks the original as done *and* spawns a new task due the next day, while leaving the new occurrence incomplete. This was one of the trickiest parts of the implementation (date math plus object identity), and it's also the behavior most likely to silently break, since a bug here wouldn't crash anything — it would just quietly stop generating future tasks.
- **Sorting tasks by time** (`test_generate_plan_orders_tasks_chronologically`): adds tasks out of order (evening, morning, morning) and confirms `generate_plan()` returns them sorted chronologically by time. This matters because the whole point of the daily plan is to tell the owner what to do next — an unsorted plan would be actively misleading even if every task in it were individually correct.
- **Conflict detection** (`test_generate_plan_detects_conflict_between_pets`): confirms that two tasks (for different pets) due at the same exact time are flagged in `scheduler.conflicts`. This directly tests the tradeoff I describe in section 2b — exact-match conflict detection — so it verifies the one form of conflict the scheduler is actually designed to catch.

Together these tests cover the full lifecycle a task goes through — created, added to a pet, ordered into a plan, checked for conflicts, completed, and (if recurring) regenerated — so a regression in any one stage of that pipeline would surface as a failing test rather than a silent bug in the CLI output.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'd put my confidence at 4/5. The five passing tests cover the core lifecycle a task actually goes through in normal use — created, added to a pet, sorted into a plan, flagged for conflicts, and completed (with a daily recurrence correctly regenerating the next occurrence) — so I'm confident the "happy path" a user hits every day works as designed. `test_complete_task_creates_next_day_occurrence_for_daily_task` in particular checks object identity (`t is task` vs `t is not task`) and the exact due-date math, which is the part I was least sure about while writing `mark_complete()`, so having it pinned down by a test is a real source of confidence rather than just a guess.

It's not a 5/5 because the tests only exercise `"daily"` frequency and single-pet, no-filter scenarios — they don't touch several branches that already exist in `pawpal_system.py` but have never been run against an assertion. A few specific edge cases I'd test next:

- **Weekly recurrence**: `mark_complete()` has a `frequency == "weekly"` branch that adds 7 days instead of 1, but no test calls it. I'd write a weekly analog of `test_complete_task_creates_next_day_occurrence_for_daily_task` to confirm `next_due_date = due_date + timedelta(days=7)`.
- **Monthly tasks**: this is the one I'm most worried about. `is_due()` treats `"monthly"` as a real frequency (30-day interval via `FREQUENCY_INTERVAL_DAYS`), but `mark_complete()` only has `if/elif` branches for `"daily"` and `"weekly"` — anything else falls through to `return None`. That means completing a monthly task marks it done but silently never regenerates it, which contradicts what `is_due()` implies should happen. I suspect this is an actual bug rather than an intentional gap, and a test asserting a monthly task produces a next occurrence would catch it immediately.
- **Invalid time strings**: `_safe_parse_time()` already guards against malformed strings like `"25:99"` or `None` by catching `ValueError`/`AttributeError` and returning `None`, and `find_conflicts()` routes those tasks into `self.unparsed_tasks` with a warning instead of crashing. I'm fairly confident this works from reading the code, but I have no test that actually creates a `Task` with a bad time string and asserts it shows up in `unparsed_tasks` and in `get_conflict_warnings()` output rather than breaking `generate_plan()`.
- **Overlapping task durations**: this connects directly to the tradeoff in section 2b. Since tasks don't currently store a duration, I couldn't easily test true interval overlap today, but I'd at least want a test confirming the documented limitation — e.g., an 8:00 AM task and an 8:15 AM task are *not* flagged as conflicting even though they might realistically overlap — so that gap is captured as expected behavior rather than an unverified assumption.
- **More filtering scenarios**: `Owner.get_all_tasks()` supports filtering by `pet_name`, `completed`, or both, and `Pet.get_tasks()` supports filtering by `completed`, but the current suite only ever calls `generate_plan()` with no filters. I'd add tests for a multi-pet owner filtering by a single `pet_name`, filtering `completed=True` vs `completed=False`, and combining both filters at once, since those code paths are currently unverified by anything other than manual CLI testing.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with getting the recurring-task logic in `mark_complete()` working correctly, since it was the trickiest piece of the whole system. Making a daily task regenerate itself for the next day — while making sure the *original* task stayed marked complete and the *new* occurrence started `completed = False` — required careful date math and thinking clearly about object identity rather than just object equality. Seeing `test_complete_task_creates_next_day_occurrence_for_daily_task` pass, with its explicit `t is task` / `t is not task` assertions, felt like real confirmation that the behavior worked the way I intended rather than something that merely looked right when I eyeballed the output.

I'm also proud of `find_conflicts()`. Rather than reaching for full interval-overlap math right away, I made a deliberate choice to group pending tasks by the exact `(due_date, time)` pair, which kept the implementation simple while still catching the most realistic case: two pets' tasks landing on an owner's calendar at the exact same time. I like that this wasn't an accident — I reasoned through the tradeoff (documented in section 2b), decided exact-match detection was the right scope for this stage of the project, and then had a test (`test_generate_plan_detects_conflict_between_pets`) confirm it actually flags a real double-booking.

Finally, wiring the `Scheduler` into the Streamlit UI in `app.py` was satisfying because it's where all the backend logic finally became tangible. Clicking "Generate schedule" now actually calls `scheduler.generate_plan()` on the live `Owner`/`Pet`/`Task` objects built up through the UI, renders the sorted plan in a table, and surfaces any detected conflicts as `st.warning` messages inline. Watching tasks I added through simple text inputs come back out the other side correctly sorted and conflict-checked made the whole scheduler feel like a working product instead of just a set of classes that passed tests in isolation.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, the first thing I'd fix is duration-based conflict detection. As described in section 2b, `find_conflicts()` only flags tasks that share the exact same `(due_date, time)` pair, so a 60-minute walk at 8:00 AM and a separate task at 8:15 AM would genuinely overlap but slip through undetected. I'd add a `duration` attribute to `Task`, then rewrite `find_conflicts()` to compare time ranges pairwise instead of grouping by exact start time — sorting each pet's tasks by start time and checking whether one task's end time crosses into the next task's start time would catch real overlaps instead of only identical double-bookings.

Second, I'd expose the filtering that already exists in the backend but is invisible in the UI. `Owner.get_all_tasks()` already supports filtering by `pet_name` and `completed`, and `Pet.get_tasks()` supports filtering by `completed`, but `app.py` never surfaces these — it always calls `generate_plan()` unfiltered. Adding a pet-name dropdown and a "show completed tasks" toggle above the "Generate schedule" button would let an owner with multiple pets actually use logic that's already written and tested, instead of it only being reachable through pytest.

Third, I'd finish monthly recurrence properly. `is_due()` already treats `"monthly"` as a real frequency using a 30-day interval, and the Streamlit UI even lets a user pick "monthly" from the frequency dropdown, but `mark_complete()` only has `if/elif` branches for `"daily"` and `"weekly"` — anything else falls through and returns `None`. That means completing a monthly task marks it done but never regenerates it, which quietly contradicts what the UI and `is_due()` imply. I'd add a `frequency == "monthly"` branch that adds roughly 30 days (or uses proper calendar-month math), plus a test mirroring `test_complete_task_creates_next_day_occurrence_for_daily_task` to lock the behavior in.

Finally, I'd make task priority actually affect scheduling. Right now `Task` doesn't even store a priority (the original UML had a `priority` attribute on `CareTask`, but it didn't survive into the current `Task` class), and `generate_plan()` only sorts by time. In a real multi-pet household, an owner might want urgent tasks (like medication) surfaced above routine ones (like play time) even when a lower-priority task is scheduled earlier. I'd reintroduce a `priority` field on `Task` and change `generate_plan()`'s sort key to break ties — or even override strict time-ordering — using priority, so the plan reflects what actually matters most to the owner rather than pure chronological order.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that AI is fast at generating options, but it can't tell you which option is *right* for your specific system — that judgment has to stay with me. AI could draft a class diagram, write a `mark_complete()` stub, or propose a rename in seconds, and that speed was genuinely valuable: it let me try out ideas (like restructuring `OwnerPreferences`/`CareTask`/`DailyPlan` into `Owner`/`Pet`/`Task`/`Scheduler`, described in section 3b) far faster than I could have by sketching them out myself. But at every one of those moments, the AI's suggestion was a starting point, not a verdict. It didn't know that `Owner`, not `Scheduler`, should own the collection of pets — I decided that by tracing how the three core actions actually used each class. It didn't catch that `mark_complete()` silently drops monthly tasks even though `is_due()` and the UI both treat "monthly" as real — I found that by reading the code against its own assumptions, not by asking AI if it was correct. And it didn't decide that duration-based conflict detection or priority-based sorting belonged in this version of the system at all — those were scope calls I made based on what this project actually needed right now versus what would be a reasonable next iteration.

So the takeaway isn't "AI writes the code and I check it for typos" — it's that AI collapsed the cost of generating and exploring options, which freed me up to spend my time on the part that actually required judgment: deciding what the system's classes and responsibilities should be, verifying that a proposed design held up under the real use cases instead of just looking clean, and choosing which features were in scope versus which were honest, documented gaps. AI could hand me a design; only I could decide whether it was *this* system's design.
