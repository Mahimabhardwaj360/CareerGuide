# ============================================================
#  Career Roadmap Generator — Flask Backend
#  app.py
#
#  Entry point for the web application. Handles routing,
#  form processing, validation, and rendering templates.
# ============================================================

from flask import Flask, render_template, request, redirect, url_for
from roadmap_generator import generate_roadmap

# ── App Initialisation ──────────────────────────────────────
app = Flask(__name__)
app.secret_key = "career-roadmap-secret-key"   # Required for session / flash messages


# ── Helper ──────────────────────────────────────────────────
def _collect_form_data(form) -> dict:
    """
    Pull every field from the submitted form and return a
    clean dictionary.  Skills, industries, and exams are
    comma-separated strings — we normalise them into lists
    so downstream code doesn't have to care.
    """
    def _split(value: str) -> list[str]:
        """Split a comma-separated string and strip whitespace."""
        return [item.strip() for item in value.split(",") if item.strip()]

    return {
        "education_level":        form.get("education_level", "").strip(),
        "career_goal":            form.get("career_goal", "").strip(),
        "current_year_or_class":  form.get("current_year_or_class", "").strip(),
        "skills":                 _split(form.get("skills", "")),
        "industries":             _split(form.get("industries", "")),
        "exams_certifications":   _split(form.get("exams_certifications", "")),
        "career_path_progression": form.get("career_path_progression", "").strip(),
    }


def _validate(data: dict) -> list[str]:
    """
    Return a list of human-readable error messages for any
    required fields that are empty or missing.
    An empty list means the form is valid.
    """
    errors = []

    required_fields = {
        "education_level":        "Education level",
        "career_goal":            "Career goal",
        "current_year_or_class":  "Current year / class",
        "career_path_progression": "Career path progression",
    }

    for field, label in required_fields.items():
        if not data.get(field):
            errors.append(f"'{label}' is required.")

    if not data.get("skills"):
        errors.append("Please enter at least one skill.")

    if not data.get("industries"):
        errors.append("Please enter at least one industry.")

    return errors


# ── Routes ──────────────────────────────────────────────────

@app.route("/")
def index():
    """
    GET /
    Renders the home page with the career-input form.
    """
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    POST /generate
    1. Reads and validates the submitted form data.
    2. Delegates roadmap creation to generate_roadmap().
    3. Renders result.html with the generated roadmap.

    On validation failure the user is redirected back to the
    form with a descriptive error message rather than a bare
    400 / 500 page — keeping the experience friendly.
    """
    # ── 1. Collect ────────────────────────────────────────
    user_data = _collect_form_data(request.form)
    print("DEBUG: Form data received:", user_data)

    # ── 2. Validate ───────────────────────────────────────
    errors = _validate(user_data)
    print("DEBUG: Validation errors:", errors)
    if errors:
        # Pass errors back to the form so the user can fix them
        print("DEBUG: Returning to form with errors")
        return render_template("index.html", errors=errors, form_data=user_data), 422

    # ── 3. Generate ───────────────────────────────────────
    try:
        roadmap = generate_roadmap(user_data)
        print("DEBUG: Roadmap generated successfully")
    except Exception as exc:                         # Catch any unexpected generator error
        app.logger.error("Roadmap generation failed: %s", exc)
        print("DEBUG: Roadmap generation failed:", exc)
        return render_template(
            "index.html",
            errors=["Something went wrong while generating your roadmap. Please try again."],
            form_data=user_data,
        ), 500

    # ── 4. Render ─────────────────────────────────────────
    print("DEBUG: Rendering result page")
    return render_template("result.html", roadmap=roadmap, user_data=user_data)


# ── Entry Point ─────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True auto-reloads on code changes during development.
    # Set debug=False (and use a proper WSGI server) in production.
    app.run(debug=True)