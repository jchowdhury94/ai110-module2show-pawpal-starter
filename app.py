import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        available_time=120, preferred_times=["morning"], task_priorities=[]
    )
owner = st.session_state.owner

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=50, value=2)
needs = st.text_input("Pet needs (comma-separated)", value="walk, feed")

if st.button("Add pet"):
    pet = Pet(
        name=pet_name,
        species=species,
        age=int(age),
        needs=[need.strip() for need in needs.split(",") if need.strip()],
    )
    owner.add_pet(pet)
    st.success(f"Added {pet.name} to {owner_name}'s pets.")

st.markdown("### Tasks")
st.caption("Add a few tasks. Tasks are attached to the selected pet.")

if not owner.pets:
    st.info("Add a pet above before creating tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = owner.get_pet(selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        description = st.text_input("Task description", value="Morning walk")
    with col2:
        time = st.text_input("Time", value="07:00")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])

    if st.button("Add task"):
        task = Task(description=description, time=time, frequency=frequency)
        selected_pet.add_task(task)
        st.success(f"Added task to {selected_pet.name}.")

st.divider()

st.subheader("Current Pets & Tasks")

if not owner.pets:
    st.info("No pets yet. Add one above.")
else:
    for pet in owner.pets:
        st.markdown(f"**{pet.get_summary()}**")
        tasks = pet.get_tasks()
        if tasks:
            for task in tasks:
                st.write(f"- {task.get_summary()}")
        else:
            st.caption("No tasks yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not owner.pets:
        st.info("Add a pet and some tasks before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        scheduler.generate_plan()

        st.table(
            [
                {
                    "Time": task.time,
                    "Task": task.description,
                    "Pet": task.pet.name if task.pet else "",
                    "Frequency": task.frequency,
                    "Completed": "Yes" if task.completed else "No",
                }
                for task in scheduler.selected_tasks
            ]
        )

        for tasks in scheduler.conflicts:
            details = ", ".join(
                f"{t.description} ({t.pet.name})" if t.pet else t.description
                for t in tasks
            )
            st.warning(f"Conflict at {tasks[0].time}: {details}.")
