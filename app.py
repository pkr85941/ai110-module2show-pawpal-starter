import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart daily planner for pet owners.")

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None

# ---------------------------------------------------------------------------
# Section 1 — Owner setup
# ---------------------------------------------------------------------------
st.header("1. Owner Info")

with st.form("owner_form"):
    col1, col2 = st.columns(2)
    with col1:
        owner_name = st.text_input("Your name", value="Jordan")
    with col2:
        available = st.number_input("Minutes available today", min_value=10, max_value=480, value=90)
    submitted = st.form_submit_button("Save owner info")

if submitted:
    if st.session_state.owner is None:
        st.session_state.owner = Owner(name=owner_name, available_minutes=int(available))
    else:
        st.session_state.owner.name = owner_name
        st.session_state.owner.set_availability(int(available))
    st.success(f"Saved: {st.session_state.owner.summary()}")

if st.session_state.owner is None:
    st.info("Fill in your name and available time above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

# ---------------------------------------------------------------------------
# Section 2 — Add a pet
# ---------------------------------------------------------------------------
st.divider()
st.header("2. Add a Pet")

with st.form("pet_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Biscuit")
    with col2:
        breed = st.text_input("Breed", value="Golden Retriever")
    with col3:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    owner.add_pet(Pet(name=pet_name, breed=breed, species=species))
    st.success(f"Added {pet_name} to {owner.name}'s household.")

if owner.pets:
    for pet in owner.pets:
        st.write(f"- {pet.summary()}")

# ---------------------------------------------------------------------------
# Section 3 — Add a task
# ---------------------------------------------------------------------------
st.divider()
st.header("3. Add a Task")

if not owner.pets:
    st.info("Add at least one pet first.")
else:
    with st.form("task_form"):
        pet_names = [p.name for p in owner.pets]
        selected_pet_name = st.selectbox("Assign task to", pet_names)

        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("Task name", value="Morning walk")
            duration  = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col2:
            priority  = st.selectbox("Priority", ["high", "medium", "low"])
            category  = st.selectbox("Category", ["walk", "feed", "meds", "grooming", "enrichment", "other"])
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

        add_task = st.form_submit_button("Add task")

    if add_task:
        target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        target_pet.add_task(Task(
            name=task_name,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
            frequency=frequency,
        ))
        st.success(f"Added '{task_name}' to {selected_pet_name}.")

# ---------------------------------------------------------------------------
# Section 4 — Task overview with filtering
# Scheduler.filter_tasks() lets the owner zero in on specific pets or statuses.
# ---------------------------------------------------------------------------
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.divider()
    st.header("4. Task Overview")

    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox(
            "Filter by pet", ["All pets"] + [p.name for p in owner.pets]
        )
    with col2:
        filter_status = st.selectbox(
            "Filter by status", ["All", "Incomplete", "Completed"]
        )

    scheduler_for_filter = Scheduler(owner)
    pet_arg    = None if filter_pet == "All pets" else filter_pet
    status_arg = None if filter_status == "All" else (filter_status == "Completed")
    filtered   = scheduler_for_filter.filter_tasks(pet_name=pet_arg, completed=status_arg)

    if filtered:
        rows = [
            {
                "Pet": pet.name,
                "Task": task.name,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Category": task.category,
                "Frequency": task.frequency,
                "Done": "✓" if task.completed else "",
            }
            for pet, task in filtered
        ]
        st.table(rows)
    else:
        st.info("No tasks match that filter.")

# ---------------------------------------------------------------------------
# Section 5 — Generate schedule
# Uses Scheduler.generate_plan(), sort_by_time(), and detect_conflicts().
# ---------------------------------------------------------------------------
st.divider()
st.header("5. Generate Schedule")

if not owner.get_all_tasks():
    st.info("Add at least one task before generating a schedule.")
else:
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.text_input("Start time (HH:MM)", value="08:00")
    with col2:
        sort_by_time = st.checkbox("Sort display by start time", value=False)

    if st.button("Generate schedule"):
        scheduler = Scheduler(owner)
        plan = scheduler.generate_plan(date=str(date.today()), start_time=start_time)

        st.subheader(f"Today's plan — {plan.summary()}")

        # Conflict warnings — shown before the table so they're impossible to miss
        if plan.conflicts:
            for warning in plan.conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        # Schedule table — optionally sorted by start time
        if plan.slots:
            display_slots = scheduler.sort_by_time() if sort_by_time else plan.slots
            schedule_rows = [
                {
                    "Time": t,
                    "Pet": pet.name,
                    "Task": task.name,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                }
                for t, pet, task in display_slots
            ]
            st.table(schedule_rows)
        else:
            st.warning("No tasks could be scheduled within the available time.")

        # Skipped tasks
        if plan.skipped_tasks:
            with st.expander(f"Skipped tasks ({len(plan.skipped_tasks)} — not enough time)"):
                for pet, task in plan.skipped_tasks:
                    st.write(f"• {task.name} ({task.duration_minutes} min) [{task.priority}] → {pet.name}")

        # Reasoning
        with st.expander("Why this order?"):
            st.text(scheduler.explain_plan())
