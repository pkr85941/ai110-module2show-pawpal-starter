# PawPal+ Project Reflection

## 1. System Design

**a. Core user actions**

The three core actions a user can perform in PawPal+ are:

1. **Enter pet and owner info** — The user provides their name, their pet's name and breed, and how much time they have available for the day. This gives the scheduler the constraints it needs before building a plan.

2. **Add and manage care tasks** — The user creates tasks such as a morning walk, feeding, medication, or grooming, specifying a duration and a priority level for each. These tasks are the raw material the scheduler works from; without them there is nothing to plan.

3. **Generate and view today's schedule** — The user triggers schedule generation and receives a time-ordered daily plan showing each task's start time, duration, and priority. The plan should also explain why tasks were ordered the way they were, so the owner understands and trusts the output.

**b. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
