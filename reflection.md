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
Yes, my design changed during implementation.
- If yes, describe at least one change and why you made it.
I removed the add_pet() method from the Pet class because creating a Pet object already adds the pet to the system, so the class should focus on storing and updating pet information instead.

I changed the completed attribute in the CareTask class to default to False because new pet care tasks are usually incomplete when they are created, and this makes creating new tasks simpler and more realistic.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
