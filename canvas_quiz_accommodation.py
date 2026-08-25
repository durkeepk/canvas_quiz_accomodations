#!/usr/bin/env python3
"""
Canvas Quiz Accommodation Helper

Adds extra quiz time for one student across a Canvas course using Canvas's
official APIs.

Classic Quizzes:
- Reads each timed quiz's actual time limit.
- For multiplier accommodations (e.g. 1.5x or 2x), calculates the correct
  extra minutes for every quiz.
- If all timed quizzes need the same number of extra minutes, uses Canvas's
  course-level Quiz Extensions endpoint.
- If quizzes need different extra minutes, uses Canvas's quiz-level Quiz
  Extensions endpoint.
- Skips untimed quiz items.

New Quizzes:
- Supports Canvas's documented course-level and quiz-level accommodations APIs.
- Reads quiz_settings.session_time_limit_in_seconds when Canvas exposes it.
- Stops rather than guessing when a multiplier cannot be calculated safely.

No third-party Python packages are required.
"""

import getpass
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value if value else default


def parse_course_url(value):
    value = value.strip()
    match = re.match(r"^(https?://[^/]+)/courses/(\d+)", value)
    if not match:
        raise ValueError(
            "Please paste a full Canvas course URL, for example "
            "https://yourinstitution.instructure.com/courses/123456"
        )
    return match.group(1).rstrip("/"), int(match.group(2))


def parse_link_header(header):
    links = {}
    if not header:
        return links
    for part in header.split(","):
        match = re.match(r'\s*<([^>]+)>;\s*rel="([^"]+)"', part)
        if match:
            links[match.group(2)] = match.group(1)
    return links


class Canvas:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _request(self, url, method="GET", payload=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, method=method, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                raw = response.read().decode("utf-8")
                body = json.loads(raw) if raw else None
                return body, response.headers

        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"\nCanvas returned HTTP {exc.code}:\n{body}\n", file=sys.stderr)
            raise

    def get(self, path, params=None):
        url = self.base_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        body, _ = self._request(url)
        return body

    def get_all(self, path, params=None):
        params = dict(params or {})
        params.setdefault("per_page", 100)
        url = self.base_url + path + "?" + urllib.parse.urlencode(params, doseq=True)
        items = []

        while url:
            body, headers = self._request(url)
            if not isinstance(body, list):
                raise RuntimeError("Expected a list response from Canvas.")
            items.extend(body)
            url = parse_link_header(headers.get("Link")).get("next")

        return items

    def post_json(self, path, payload):
        body, _ = self._request(
            self.base_url + path,
            method="POST",
            payload=payload,
        )
        return body


def find_student(canvas, course_id, search):
    enrollments = canvas.get_all(
        f"/api/v1/courses/{course_id}/enrollments",
        {
            "type[]": "StudentEnrollment",
            "state[]": "active",
        },
    )

    needle = search.lower()
    matches = []
    seen_ids = set()

    for enrollment in enrollments:
        user = enrollment.get("user", {}) or {}
        uid = user.get("id")

        if uid in seen_ids:
            continue

        fields = [
            user.get("name"),
            user.get("sortable_name"),
            user.get("login_id"),
            user.get("sis_user_id"),
        ]

        if any(needle in str(field or "").lower() for field in fields):
            matches.append(user)
            seen_ids.add(uid)

    return matches


def round_extra(base_minutes, multiplier):
    # Canvas stores extra_time as integer minutes.
    # Round to nearest minute, with .5 rounded upward.
    raw = base_minutes * (multiplier - 1)
    return int(math.floor(raw + 0.5))


def get_accommodation():
    print("\nHow is the accommodation stated?")
    print("  1 - Multiplier (for example, 1.5x or 2x)")
    print("  2 - Exact number of extra minutes")

    mode = ask("Choose 1 or 2")

    if mode == "1":
        multiplier = float(ask("Multiplier (for example 1.5 or 2)"))
        if multiplier <= 1:
            raise ValueError("Multiplier must be greater than 1.")
        return {"mode": "multiplier", "multiplier": multiplier}

    if mode == "2":
        extra = int(ask("Extra minutes to add"))
        if extra < 0:
            raise ValueError("Extra minutes cannot be negative.")
        return {"mode": "exact", "extra": extra}

    raise ValueError("Please choose 1 or 2.")



def new_quiz_time_limit_minutes(quiz):
    """
    Current Canvas New Quizzes commonly expose:
      quiz_settings.has_time_limit
      quiz_settings.session_time_limit_in_seconds

    A few deployments/versions may expose other fields, so we check those too.
    """
    settings = quiz.get("quiz_settings") or {}
    alt_settings = quiz.get("settings") or {}

    has_time_limit = settings.get("has_time_limit")
    seconds = settings.get("session_time_limit_in_seconds")

    if has_time_limit is False:
        return None

    if seconds is not None:
        try:
            seconds = int(seconds)
            if seconds > 0:
                return seconds / 60.0
        except (TypeError, ValueError):
            pass

    candidates_minutes = [
        quiz.get("time_limit"),
        settings.get("time_limit"),
        alt_settings.get("time_limit"),
    ]

    for value in candidates_minutes:
        if value is not None:
            try:
                value = float(value)
                if value > 0:
                    return value
            except (TypeError, ValueError):
                pass

    return None



def fmt_minutes(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def print_classic_plan(plan, accommodation):
    print("\nPROPOSED CHANGE")
    print("---------------")

    if accommodation["mode"] == "multiplier":
        print(f"Accommodation: {accommodation['multiplier']:g}x time")
    else:
        print(f"Accommodation: +{accommodation['extra']} minutes")

    for item in plan:
        print(
            f"  {item['title']}: "
            f"{fmt_minutes(item['base'])} min -> "
            f"+{item['extra']} -> "
            f"{fmt_minutes(item['total'])} min"
        )


def print_new_plan(plan, accommodation):
    print("\nPROPOSED CHANGE")
    print("---------------")

    if accommodation["mode"] == "multiplier":
        print(f"Accommodation: {accommodation['multiplier']:g}x time")
    else:
        print(f"Accommodation: +{accommodation['extra']} minutes")

    if plan["strategy"] == "course" and "plan" not in plan:
        print(f"  New Quizzes course-level extra time: +{plan['extra']} minutes")
        return

    for item in plan.get("plan", []):
        print(
            f"  {item['title']}: "
            f"{fmt_minutes(item['base'])} min -> "
            f"+{item['extra']} -> "
            f"{fmt_minutes(item['total'])} min"
        )

    if plan["strategy"] == "course":
        print(
            f"\nAll timed New Quizzes require the same +{plan['extra']} minutes, "
            "so the script can use the course-level accommodation endpoint."
        )


def apply_classic(canvas, course_id, student_id, plan):
    unique_extras = sorted({item["extra"] for item in plan})

    if len(unique_extras) == 1:
        payload = {
            "quiz_extensions": [
                {
                    "user_id": student_id,
                    "extra_time": unique_extras[0],
                }
            ]
        }

        return [
            canvas.post_json(
                f"/api/v1/courses/{course_id}/quiz_extensions",
                payload,
            )
        ]

    results = []

    for item in plan:
        payload = {
            "quiz_extensions": [
                {
                    "user_id": student_id,
                    "extra_time": item["extra"],
                }
            ]
        }

        results.append(
            canvas.post_json(
                f"/api/v1/courses/{course_id}/quizzes/"
                f"{item['quiz_id']}/extensions",
                payload,
            )
        )

    return results


def apply_new_quizzes(canvas, course_id, student_id, plan):
    if plan["strategy"] == "course":
        payload = [
            {
                "user_id": student_id,
                "extra_time": plan["extra"],
                "apply_to_in_progress_quiz_sessions": True,
            }
        ]

        return [
            canvas.post_json(
                f"/api/quiz/v1/courses/{course_id}/accommodations",
                payload,
            )
        ]

    results = []

    for item in plan["plan"]:
        payload = [
            {
                "user_id": student_id,
                "extra_time": item["extra"],
            }
        ]

        results.append(
            canvas.post_json(
                f"/api/quiz/v1/courses/{course_id}/quizzes/"
                f"{item['assignment_id']}/accommodations",
                payload,
            )
        )

    return results


def choose_engine():
    print("\nWhich quiz engine do you want to modify?")
    print("  1 - Classic Quizzes")
    print("  2 - New Quizzes")

    quiz_mode = ask("Choose 1 or 2")

    if quiz_mode == "1":
        return "classic"
    if quiz_mode == "2":
        return "new"

    raise ValueError("Please choose 1 or 2.")


def prepare_course(canvas, course_id, engine):
    course = canvas.get(f"/api/v1/courses/{course_id}")

    if engine == "classic":
        quizzes = canvas.get_all(f"/api/v1/courses/{course_id}/quizzes")
        return course, quizzes

    quizzes = canvas.get_all(f"/api/quiz/v1/courses/{course_id}/quizzes")
    return course, quizzes


def classic_plan_from_quizzes(quizzes, accommodation):
    timed = []
    untimed = []

    for quiz in quizzes:
        limit = quiz.get("time_limit")

        if limit is None:
            untimed.append(quiz)
            continue

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            untimed.append(quiz)
            continue

        if limit <= 0:
            untimed.append(quiz)
            continue

        if accommodation["mode"] == "multiplier":
            extra = round_extra(limit, accommodation["multiplier"])
        else:
            extra = accommodation["extra"]

        timed.append(
            {
                "quiz_id": quiz["id"],
                "title": quiz.get("title", f"Quiz {quiz['id']}"),
                "base": limit,
                "extra": extra,
                "total": limit + extra,
            }
        )

    if not timed:
        raise RuntimeError("No timed Classic Quizzes were found in this course.")

    return timed, untimed


def new_quiz_plan_from_quizzes(quizzes, accommodation):
    if not quizzes:
        raise RuntimeError("No New Quizzes were found in this course.")

    if accommodation["mode"] == "exact":
        return {
            "strategy": "course",
            "extra": accommodation["extra"],
            "quizzes": quizzes,
        }

    plan = []
    missing_limits = []

    for quiz in quizzes:
        base = new_quiz_time_limit_minutes(quiz)

        if base is None:
            missing_limits.append(quiz)
            continue

        extra = round_extra(base, accommodation["multiplier"])

        plan.append(
            {
                "assignment_id": quiz.get("id"),
                "title": quiz.get("title", f"New Quiz {quiz.get('id')}"),
                "base": base,
                "extra": extra,
                "total": base + extra,
            }
        )

    if missing_limits:
        names = ", ".join(
            str(q.get("title", q.get("id")))
            for q in missing_limits[:5]
        )
        more = "..." if len(missing_limits) > 5 else ""

        raise RuntimeError(
            "Canvas did not expose a readable time limit for one or more "
            f"New Quizzes ({names}{more}). The script will not guess a "
            "multiplier. Set those accommodations manually or use an exact "
            "extra-minute accommodation if that matches the approved accommodation."
        )

    if not plan:
        raise RuntimeError("No timed New Quizzes with readable time limits were found.")

    unique_extras = sorted({item["extra"] for item in plan})

    if len(unique_extras) == 1:
        return {
            "strategy": "course",
            "extra": unique_extras[0],
            "plan": plan,
            "quizzes": quizzes,
        }

    return {
        "strategy": "per_quiz",
        "plan": plan,
        "quizzes": quizzes,
    }


def process_student(canvas, course, course_id, engine, cached_quizzes):
    student_search = ask(
        "\nEnter the student's Canvas login/email or full name "
        "(email/login is best)"
    )

    matches = find_student(canvas, course_id, student_search)

    if len(matches) == 0:
        print("\nNo matching active student was found in this course.")
        return

    if len(matches) > 1:
        print("\nMore than one student matched:")
        for user in matches:
            print(f"  {user.get('name')} | login: {user.get('login_id')}")
        print(
            "\nNo change was made. Try this student again using the exact "
            "Canvas login/email."
        )
        return

    student = matches[0]
    student_id = student["id"]

    print(f"\nStudent found: {student.get('name')} (Canvas ID {student_id})")

    accommodation = get_accommodation()

    if engine == "classic":
        plan, untimed = classic_plan_from_quizzes(cached_quizzes, accommodation)

        print(
            f"\nCanvas found {len(plan)} timed Classic Quizzes and "
            f"{len(untimed)} untimed quiz item(s)."
        )

        if untimed:
            print("Untimed items will be skipped automatically.")

        print_classic_plan(plan, accommodation)

    else:
        plan = new_quiz_plan_from_quizzes(cached_quizzes, accommodation)
        print_new_plan(plan, accommodation)

    print(f"\nCourse: {course.get('name')} (ID {course_id})")
    print(f"Student: {student.get('name')}")

    confirm = input("\nType YES to apply this accommodation: ").strip()

    if confirm != "YES":
        print("\nCancelled. Nothing was changed.")
        return

    if engine == "classic":
        results = apply_classic(canvas, course_id, student_id, plan)
    else:
        results = apply_new_quizzes(canvas, course_id, student_id, plan)

    print(f"\nCanvas accepted {len(results)} accommodation request(s).")

    if engine == "classic":
        extras = sorted({item["extra"] for item in plan})
        if len(extras) > 1:
            print(
                "Because quiz durations differed, Canvas was updated quiz-by-quiz "
                "with the appropriate extra time."
            )
    elif plan["strategy"] == "per_quiz":
        print(
            "Because New Quiz durations required different extra time, Canvas was "
            "updated quiz-by-quiz."
        )

    print(
        "\nVERIFY: Open at least one quiz in Canvas and confirm the student's "
        "moderation/accommodation. If quiz durations differ, verify at least one "
        "short quiz and one long quiz."
    )


def main():
    print("\nCanvas Quiz Accommodation Helper")
    print("================================\n")

    token = None

    while True:
        course_url = ask("Paste the Canvas course URL")
        base_url, course_id = parse_course_url(course_url)

        if token is None:
            token = getpass.getpass(
                "Paste your Canvas access token (hidden): "
            ).strip()
            if not token:
                raise RuntimeError("No access token was entered.")

        canvas = Canvas(base_url, token)
        engine = choose_engine()
        course, cached_quizzes = prepare_course(canvas, course_id, engine)

        print(f"\nCourse found: {course.get('name')} (ID {course_id})")

        while True:
            process_student(
                canvas=canvas,
                course=course,
                course_id=course_id,
                engine=engine,
                cached_quizzes=cached_quizzes,
            )

            print("\nWhat would you like to do next?")
            print("  1 - Add an accommodation for another student in this same course")
            print("  2 - Switch quiz engine in this same course")
            print("  3 - Choose a different course")
            print("  4 - Exit")

            choice = ask("Choose 1, 2, 3, or 4")

            if choice == "1":
                continue

            if choice == "2":
                engine = choose_engine()
                course, cached_quizzes = prepare_course(
                    canvas,
                    course_id,
                    engine,
                )
                continue

            if choice == "3":
                print("\nReturning to course selection...\n")
                break

            if choice == "4":
                print("\nDone.")
                return

            print("\nPlease choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, urllib.error.HTTPError) as exc:
        print(f"\nSTOPPED: {exc}", file=sys.stderr)
        sys.exit(1)
