---
code: RD09
title: Communicating in the Software Development Lifecycle
date: 2026-01-23
due: 2026-01-27
type:  reading
threads: ["System / APIs", "Design / Communication"]
authors: [Kris Jordan]
---

# 1. Communication in the Software Development Lifecycle

Effective communication is critical throughout the software development life cycle (SDLC). Whether a client is requesting a feature or multiple teams are collaborating on a project, intentional communication strategies help ensure that everyone remains on the same page. Poor communication, on the other hand, can lead to misunderstandings, delays, and even project failure.

## How Communication Enables Collective Success
One of the most remarkable aspects of the SDLC is how groups of people with very different backgrounds and roles band together to achieve a goal bigger than anyone could take on individually. A successful project relies on shared understanding—each person must know enough to contribute meaningfully, even if their expertise lies in a specific area. Everyone, from the client to the project manager, to the engineers and designers, needs to clearly understand the goals and desired outcomes of the project.

Good communication helps:

- **Clarify Goals**: Ensuring everyone has a unified understanding of what success looks like.
- **Distribute Knowledge**: Allowing team members to understand the context they need to make informed decisions.
- **Align Efforts**: Making sure that all work, no matter how specialized, contributes to the same broader goal.

## Intentional Communication Strategies

Some high-level strategies and concerns are pervasive in software development. We will explore these in more depth as the course goes on, but it is worth highlighting a few now:

1. **Using Shared _Resources_ (e.g. artifacts like files and documents)**
    - Architectural Design Records, Design documents, technical specifications, and wireframes help clarify ideas.
    - These artifacts act as shared _resources_, ensuring all stakeholders are able to rally around the same ideas _before_ they are built. This idea is not new to software development, think of blue prints and artistic renderings of buildings and spaces in the construction industry as a predecessor.

2. **Choosing the Right Medium for the Message**
    - **Synchronous Communication**: Lessons, video calls, or real-time collaboration are great for brainstorming or addressing urgent issues.
    - **Asynchronous Communication**: Emails, project management tools, and documentation are better for detailed updates and tracking progress.

3. **Adjusting Formality Based on Context**
    - Formal communication, such as signed contracts or requirements documents, cement guarantees and expectations. This is especially important between two disparate parties or firms.
    - Informal discussions, like Slack chats or quick hallway conversations, can promote collaboration and generate ideas. These are more useful internally, within a team or organization.

4. **Tightening Feedback Loops**
    - Regular check-ins, code reviews, and demos ensure that misunderstandings are caught early.
    - Feedback helps teams refine their work, aligning closer to the original intent.

## Communication Across Roles

Each role in the SDLC brings unique perspectives and needs, making effective communication even more important.

- **Client to Project Manager**: Clients communicate high-level goals, such as desired features or outcomes. A project manager translates these goals into actionable tasks for the development team. Without clarity, the team may deliver something that doesn’t meet the client’s expectations.

- **Designers to Software Engineers**: User interface (UI) designers create wireframes or mockups that software engineers implement. Miscommunication about design elements, like color schemes or interaction behaviors, can result in poor user experiences.

- **Software Engineers to Site Reliability Engineers**: Software engineers rely on site reliability engineers (SREs) to deploy software to production environments. Poorly communicated deployment requirements can lead to configuration errors, downtime, or failed releases.

As a foreshadowing, we will soon turn our attention toward communication between different _layers_ of a software system, such as front-end and back-end. One hand-waiving analogy of a system layer is like a different role in a team: it has its own concerns and jobs different from the others yet it still needs to work in coordination with the others. Sometimes these layers are implemented in different programming languages and we will need to pay careful attention to how communication between these layers ensures no information is lost in translation.

## What Happens When Communication Breaks Down

Poor communication can have serious consequences at every stage of development:

- **Client Dissatisfaction**: Vague requirements or misaligned priorities lead to deliverables that don’t meet the client’s needs.
- **Missed Deadlines**: Unclear expectations create confusion about what tasks need to be completed and when.
- **Team Frustration**: Miscommunication fosters blame and reduces morale, impacting productivity.
- **Technical Debt**: Lack of clarity around implementation can result in rushed, poorly designed solutions that need to be fixed later.

## Benefits of Good Communication

When communication is intentional and well-structured, it:

- **Clarifies Goals and Outcomes**: Ensures everyone knows what they’re working toward and why it matters.
- **Prevents Scope Creep**: Clear requirements help avoid last-minute changes that derail timelines.
- **Improves Collaboration**: Shared understanding across teams reduces friction and promotes teamwork.
- **Minimizes Rework**: Aligned expectations mean less time spent correcting misunderstandings.
- **Builds Trust**: Transparent communication fosters trust between clients and development teams.


!!! quote "Fred Brooks on Communication"
    "The hardest single part of building a software system is deciding precisely what to build. No other part of the conceptual work is so difficult as establishing the detailed technical requirements, including all the interfaces to people, to machines, and to other software systems. No other part of the work so cripples the resulting system if done wrong. No other part is more difficult to rectify later." 
    
    — Fred Brooks, ["No Silver Bullet: Essence and Accidents of Software Engineering," 1986](https://www.cs.unc.edu/techreports/86-020.pdf)
