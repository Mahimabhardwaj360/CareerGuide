# ============================================================
#  Career Roadmap Generator — Core Logic
#  roadmap_generator.py
#
#  Generates a structured, personalised 5-phase career roadmap
#  from user-provided data.  The function is intentionally
#  self-contained so it can be dropped into any Flask/FastAPI
#  app or later replaced with an LLM API call.
# ============================================================

from __future__ import annotations


# ── Internal helpers ─────────────────────────────────────────

def _fmt_list(items: list[str], bullet: str = "  •") -> str:
    """Render a Python list as a bulleted multi-line string."""
    return "\n".join(f"{bullet} {item}" for item in items) if items else f"{bullet} N/A"


def _join(items: list[str], fallback: str = "your field") -> str:
    """Join a list naturally, falling back to a default string."""
    return ", ".join(items) if items else fallback


def _phase_header(number: int, emoji: str, title: str, duration: str) -> str:
    """Return a formatted phase header block."""
    bar = "─" * 55
    return (
        f"\n{bar}\n"
        f" {emoji}  PHASE {number}: {title.upper()}\n"
        f"     ⏱  Duration: {duration}\n"
        f"{bar}"
    )


# ── Phase builders ───────────────────────────────────────────

def _phase_foundation(data: dict) -> str:
    """
    Phase 1 — Foundation
    Helps the user understand where they stand and set
    a clear direction aligned with their career goal.
    """
    education   = data.get("education_level", "your current level")
    goal        = data.get("career_goal", "your target role")
    current     = data.get("current_year_or_class", "your current year")
    skills      = data.get("skills", [])
    industries  = data.get("industries", [])

    steps = [
        f"📌 Audit your current position: you are at {education}, {current} — identify the gap between now and '{goal}'.",
        f"🗺️  Research the {_join(industries)} industry deeply: study job descriptions, salary benchmarks, and required qualifications on LinkedIn Jobs & Glassdoor.",
        f"📚 Build a strong base in your existing skills ({_join(skills, 'your core areas')}) using structured resources like MIT OpenCourseWare, Khan Academy, or NPTEL.",
        "🧠 Define your personal 'North Star' metric — one measurable outcome (e.g., land an internship, clear an exam, publish a project) to chase in the next 6 months.",
        "🗓️  Set up a weekly study tracker using Notion or Google Sheets — consistency at this stage beats intensity.",
    ]

    return (
        _phase_header(1, "🧱", "Foundation", "0 – 3 Months")
        + "\n\n"
        + _fmt_list(steps)
        + "\n\n"
        + "  💡 Key platforms: LinkedIn, Glassdoor, NPTEL, Khan Academy, Notion"
    )


def _phase_skill_building(data: dict) -> str:
    """
    Phase 2 — Skill Building
    Targeted upskilling based on the user's declared skills,
    exams, and industry focus.
    """
    skills      = data.get("skills", [])
    exams       = data.get("exams_certifications", [])
    goal        = data.get("career_goal", "your target role")
    industries  = data.get("industries", [])

    cert_line = (
        f"Enrol in prep courses for {_join(exams)} on Coursera, Udemy, or the official exam portal."
        if exams else
        "Research the top 2–3 certifications respected in your industry and start the most entry-friendly one."
    )

    steps = [
        f"🎯 Double down on the skills most demanded for '{goal}': {_join(skills, 'core technical skills')}.",
        f"📖 {cert_line}",
        f"🏗️  Apply every concept immediately — build small weekend projects tied to the {_join(industries)} industry so learning sticks.",
        "🤝 Join relevant communities: subreddits, Discord servers, or LinkedIn groups in your niche — passive learning accelerates here.",
        "🔁 Follow a 70/30 rule: 70% hands-on practice, 30% theory. Avoid tutorial hell.",
    ]

    return (
        _phase_header(2, "🛠️", "Skill Building", "2 – 6 Months")
        + "\n\n"
        + _fmt_list(steps)
        + "\n\n"
        + "  💡 Key platforms: Coursera, Udemy, freeCodeCamp, LeetCode, HackerRank, YouTube"
    )


def _phase_practical_experience(data: dict) -> str:
    """
    Phase 3 — Practical Experience
    Converts knowledge into a visible, shareable portfolio.
    """
    goal        = data.get("career_goal", "your target role")
    skills      = data.get("skills", [])
    industries  = data.get("industries", [])

    steps = [
        f"🚀 Build 2–3 portfolio projects that directly demonstrate value for '{goal}' — host them publicly on GitHub or a personal site.",
        f"🏢 Seek internships, part-time roles, or freelance gigs in the {_join(industries)} sector via Internshala, LinkedIn, Wellfound (AngelList), or Upwork.",
        f"🤖 Contribute to open-source projects that use {_join(skills, 'your core skills')} — even small PRs signal initiative to recruiters.",
        "📝 Document every project with a clear README, demo video, and results — treat each project like a mini case study.",
        "🌐 Publish 1–2 technical articles or case studies on Medium, Hashnode, or LinkedIn to start building a public presence.",
    ]

    return (
        _phase_header(3, "🚀", "Practical Experience", "4 – 9 Months")
        + "\n\n"
        + _fmt_list(steps)
        + "\n\n"
        + "  💡 Key platforms: GitHub, Internshala, Upwork, Kaggle, Medium, Hashnode, Wellfound"
    )


def _phase_job_exam_prep(data: dict) -> str:
    """
    Phase 4 — Job / Exam Preparation
    Targeted preparation for landing a role or clearing key exams.
    """
    goal        = data.get("career_goal", "your target role")
    exams       = data.get("exams_certifications", [])
    industries  = data.get("industries", [])
    progression = data.get("career_path_progression", "a structured career path")

    exam_step = (
        f"📋 Begin full-length mock tests for {_join(exams)} — target at least 3 timed mock exams per week and review every mistake."
        if exams else
        "📋 Research the most respected entry-level certifications in your domain and schedule your first exam date."
    )

    steps = [
        f"🎯 Tailor your résumé and LinkedIn profile specifically for '{goal}' roles in {_join(industries)} — use keywords from real job postings.",
        exam_step,
        "🗣️  Practise mock interviews weekly using Pramp, Interviewing.io, or recorded self-sessions — focus on both technical and behavioural rounds.",
        f"🔗 Network intentionally: send 5 personalised connection requests per week to professionals following the '{progression}' path you want.",
        "📬 Apply consistently — aim for 5–10 quality applications per week, track them in a spreadsheet, and follow up after 7 days.",
    ]

    return (
        _phase_header(4, "🎯", "Job / Exam Preparation", "8 – 14 Months")
        + "\n\n"
        + _fmt_list(steps)
        + "\n\n"
        + "  💡 Key platforms: LinkedIn Jobs, Naukri, Pramp, Interviewing.io, Glassdoor, AmbitionBox"
    )


def _phase_career_growth(data: dict) -> str:
    """
    Phase 5 — Career Growth
    Long-term compounding: mentorship, advanced skills, and trajectory.
    """
    goal        = data.get("career_goal", "your target role")
    progression = data.get("career_path_progression", "a senior-level trajectory")
    industries  = data.get("industries", [])

    steps = [
        "📈 Once in the role, set a 90-day onboarding goal — become the person who ships first and asks smart questions.",
        f"🏆 Pursue advanced certifications or a specialisation that accelerates the '{progression}' path in the {_join(industries)} industry.",
        "🧑‍🏫 Find a mentor (via ADPList, LinkedIn, or your organisation) — one good mentor compresses years of trial and error.",
        f"🌱 Revisit your skills inventory every 6 months; the industry evolves, and so should your edge as a '{goal}'.",
        "📣 Give back — speak at local meetups, mentor juniors, or publish insights. Visibility compounds into opportunities.",
    ]

    return (
        _phase_header(5, "📈", "Career Growth", "12 Months & Beyond")
        + "\n\n"
        + _fmt_list(steps)
        + "\n\n"
        + "  💡 Key platforms: ADPList, LinkedIn Learning, Coursera (Advanced), industry conferences & meetups"
    )


# ── Public API ───────────────────────────────────────────────

def generate_roadmap(data: dict) -> str:
    """
    Generate a structured, personalised 5-phase career roadmap.

    Parameters
    ----------
    data : dict
        Expected keys:
          education_level          (str)
          career_goal              (str)
          current_year_or_class    (str)
          skills                   (list[str])
          industries               (list[str])
          exams_certifications     (list[str])
          career_path_progression  (str)

    Returns
    -------
    str
        A fully formatted, emoji-decorated multi-line roadmap
        ready to be displayed in a web template or terminal.

    Notes
    -----
    The function is intentionally free of external dependencies
    so it can be hot-swapped for an LLM API call (OpenAI,
    Anthropic, Gemini, etc.) without changing app.py at all.
    """

    # ── Friendly defaults ────────────────────────────────────
    goal        = data.get("career_goal", "your target role")
    education   = data.get("education_level", "your current level")
    current     = data.get("current_year_or_class", "your current stage")

    # ── Document header ──────────────────────────────────────
    header = (
        "╔══════════════════════════════════════════════════════╗\n"
        "║        🗺️   YOUR PERSONALISED CAREER ROADMAP         ║\n"
        "╚══════════════════════════════════════════════════════╝\n"
        f"\n  🎯 Goal       : {goal}"
        f"\n  🎓 Education  : {education}"
        f"\n  📅 Right Now  : {current}"
        f"\n  🏭 Industries : {_join(data.get('industries', []))}"
        f"\n  🔧 Key Skills : {_join(data.get('skills', []))}"
    )

    # ── Motivational opener ───────────────────────────────────
    opener = (
        "\n\n"
        "  ✨ Every expert was once a beginner. This roadmap turns your ambition\n"
        "     into a concrete, week-by-week action plan. Trust the process.\n"
    )

    # ── Five phases ───────────────────────────────────────────
    phases = "\n".join([
        _phase_foundation(data),
        _phase_skill_building(data),
        _phase_practical_experience(data),
        _phase_job_exam_prep(data),
        _phase_career_growth(data),
    ])

    # ── Closing note ─────────────────────────────────────────
    footer = (
        "\n\n"
        + "─" * 55 + "\n"
        + "  🏁  FINAL NOTE\n"
        + "─" * 55 + "\n"
        + "  Roadmaps are guides, not guarantees. Review this plan\n"
        + "  every 60 days, adjust based on what you learn, and\n"
        + "  keep moving. Progress > Perfection. You've got this! 💪\n"
        + "─" * 55
    )

    # ── Assemble & return ─────────────────────────────────────
    return header + opener + phases + footer
