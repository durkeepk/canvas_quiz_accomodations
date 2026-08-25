# Canvas Quiz Accommodation Helper

A small, beginner-friendly Python tool for applying extended-time quiz accommodations to a student across an entire Canvas course.

Instead of opening every quiz and using **Moderate This Quiz** one at a time, this script:

- connects to Canvas using your own personal Canvas access token;
- finds the student in the course;
- reads the actual time limit of each timed quiz;
- calculates the correct extra time for accommodations such as **1.5×** or **2×**;
- handles courses where quizzes have **different time limits**;
- skips untimed Classic Quiz items automatically;
- shows you exactly what it plans to change;
- requires you to type `YES` before it changes anything.

> **Important scope:** The Classic Quizzes workflow has been tested in a live Canvas course. The New Quizzes workflow uses Canvas's documented accommodations API, but you should verify the first change manually in your own Canvas environment before relying on it broadly.

---

## Table of contents

1. [What you need](#1-what-you-need)
2. [Download the script](#2-download-the-script)
3. [Install or check Python](#3-install-or-check-python)
4. [Create a Canvas access token](#4-create-a-canvas-access-token)
5. [Run the script on macOS](#5-run-the-script-on-macos)
6. [Run the script on Windows](#6-run-the-script-on-windows)
7. [Use the script for a student](#7-use-the-script-for-a-student)
8. [How the extra-time calculation works](#8-how-the-extra-time-calculation-works)
9. [Classic Quizzes vs. New Quizzes](#9-classic-quizzes-vs-new-quizzes)
10. [Always verify the first change](#10-always-verify-the-first-change)
11. [Common problems](#11-common-problems)
12. [Privacy and safe use](#12-privacy-and-safe-use)
13. [What the script actually does](#13-what-the-script-actually-does)
14. [Limitations](#14-limitations)
15. [Canvas API references](#15-canvas-api-references)

---

## 1. What you need

You need:

- instructor-level access to the Canvas course;
- permission from your institution to create a personal Canvas access token;
  - Fresno State currently allows faculty to create these from Canvas Account Settings;
- Python 3 on your computer;
- the file [`canvas_quiz_accommodation.py`](canvas_quiz_accommodation.py);
- the student's Canvas login/email or name;
- the student's approved accommodation, such as **1.5× time** or **2× time**.

The script uses only Python's built-in standard library. You do **not** need to install any Python packages.

If you have never used Python, Terminal, PowerShell, or an API before, that is fine. The steps below assume no prior experience.

---

## 2. Download the script

### Option A: Download only the Python file

1. On this GitHub page, click [`canvas_quiz_accommodation.py`](canvas_quiz_accommodation.py).
2. Click the **Download raw file** button near the upper-right corner of the file view.
3. Save the file to your **Downloads** folder.

Do not open the file in Word or rename it to `.txt`. The filename should remain:

```text
canvas_quiz_accommodation.py
```

### Option B: Download the whole repository

1. Click the green **Code** button near the top of the repository.
2. Choose **Download ZIP**.
3. Open the downloaded ZIP file.
4. Inside the extracted folder you will find `canvas_quiz_accommodation.py`.

For a first-time user, Option A is usually simpler.

---

## 3. Install or check Python

### macOS

#### Step 1: Open Terminal

1. Press **Command + Space** to open Spotlight.
2. Type `Terminal`.
3. Press **Return**.

A window with a text prompt will open. You do not need to know any Terminal commands beyond the ones shown in this guide.

#### Step 2: Check whether Python 3 is available

Copy and paste this command into Terminal:

```bash
python3 --version
```

Then press **Return**.

If you see something like:

```text
Python 3.11.9
```

or another Python 3 version, you are ready.

If Terminal says that `python3` is not found, install Python 3 from:

https://www.python.org/downloads/

After installing it, close Terminal, reopen Terminal, and run:

```bash
python3 --version
```

again.

---

### Windows

The easiest command-line program to use is **PowerShell**.

#### Step 1: Open PowerShell

1. Open the **Start** menu.
2. Type `PowerShell`.
3. Open **Windows PowerShell** or **PowerShell**.

#### Step 2: Check whether Python is available

Run:

```powershell
py --version
```

If that does not work, try:

```powershell
python --version
```

If either command reports Python 3, you are ready.

If Python is not installed, download it from:

https://www.python.org/downloads/windows/

During installation, if the installer gives you an option such as **Add python.exe to PATH**, select it.

Then reopen PowerShell and run:

```powershell
py --version
```

again.

---

## 4. Create a Canvas access token

The script needs a personal access token so Canvas knows that the API request is coming from you and should have the same permissions you have as an instructor.

### In Canvas

1. Sign in to Canvas.
2. Open **Account**.
3. Open **Settings**.
4. Find **Approved Integrations**, **Access Tokens**, or similar wording.
5. Choose **New Access Token** or **+ New Access Token**.
6. Give it a clear purpose, such as:

   ```text
   Quiz accommodation helper
   ```

7. Set an expiration date.
   - End of the semester is a reasonable choice.
   - That way the token still works if a student receives an accommodation later in the semester.
8. Create the token.
9. Copy the token when Canvas displays it.

Canvas generally shows the full token only when it is first created.

### Security warning

**Treat your Canvas access token like a password.**

Do not:

- email it to anyone;
- paste it into a shared Google Doc;
- put it in a GitHub repository;
- hard-code it into the Python script;
- send it in a support ticket or GitHub Issue.

The script asks you to paste the token **locally on your own computer**. The token is hidden while you paste/type it.

If you believe your token has been exposed, revoke it in Canvas and create a new one.

---

## 5. Run the script on macOS

These instructions assume you saved `canvas_quiz_accommodation.py` in your **Downloads** folder.

### Step 1: Open Terminal

Press **Command + Space**, type `Terminal`, and press **Return**.

### Step 2: Run the script

Copy and paste:

```bash
python3 ~/Downloads/canvas_quiz_accommodation.py
```

Press **Return**.

The script should begin with:

```text
Canvas Quiz Accommodation Helper
================================
```

If you saved the file on your Desktop instead, run:

```bash
python3 ~/Desktop/canvas_quiz_accommodation.py
```

### If the filename contains `(1)` or another suffix

Your browser may rename a second download to something like:

```text
canvas_quiz_accommodation (1).py
```

Either rename it back to `canvas_quiz_accommodation.py`, or place the full path in quotation marks.

For example:

```bash
python3 "~/Downloads/canvas_quiz_accommodation (1).py"
```

---

## 6. Run the script on Windows

These instructions assume you saved `canvas_quiz_accommodation.py` in your **Downloads** folder.

### Step 1: Open PowerShell

Open the Start menu, type `PowerShell`, and open PowerShell.

### Step 2: Run the script

Try:

```powershell
py "$HOME\Downloads\canvas_quiz_accommodation.py"
```

If `py` is not recognized but `python` worked when you checked your Python version, use:

```powershell
python "$HOME\Downloads\canvas_quiz_accommodation.py"
```

The script should begin with:

```text
Canvas Quiz Accommodation Helper
================================
```

If the file is on your Desktop instead, use:

```powershell
py "$HOME\Desktop\canvas_quiz_accommodation.py"
```

### If PowerShell says it cannot find the file

The most common cause is that the file was saved somewhere else.

In File Explorer:

1. Find `canvas_quiz_accommodation.py`.
2. Right-click it and choose **Copy as path** if that option is available.
3. In PowerShell type `py `, including the trailing space.
4. Paste the path.

For example:

```powershell
py "C:\Users\YourName\Downloads\canvas_quiz_accommodation.py"
```

---

## 7. Use the script for a student

The script walks you through the process one question at a time.

### 7.1 Canvas course URL

It first asks:

```text
Paste the Canvas course URL:
```

Open the course in your browser and copy its main Canvas URL.

For example:

```text
https://yourinstitution.instructure.com/courses/123456
```

The script extracts both the Canvas server and the course ID from the URL.

If you are at Fresno State, a typical URL looks like:

```text
https://fresnostate.instructure.com/courses/123456
```

### 7.2 Canvas access token

The script asks:

```text
Paste your Canvas access token (hidden):
```

Paste the token you created in Canvas and press **Return**.

Nothing may appear on the screen while you paste it. That is intentional.

### 7.3 Student

The script asks for:

```text
Enter the student's Canvas login/email or full name:
```

The student's Canvas login/email is safest because two students can have similar names.

The script searches only active student enrollments in the course.

If more than one student matches, it stops and asks you to rerun it using a more exact login/email. It will not guess which student you meant.

### 7.4 Accommodation

The script asks whether the accommodation is:

1. a multiplier, such as `1.5` or `2`; or
2. an exact number of extra minutes.

For a typical SSD/DS accommodation stated as "time and a half," choose the multiplier option and enter:

```text
1.5
```

For double time, enter:

```text
2
```

### 7.5 Quiz engine

The script asks whether the course uses:

```text
1 - Classic Quizzes
2 - New Quizzes
```

If you are unsure, open one of your quizzes in Canvas.

A **Classic Quiz** normally has the traditional Canvas quiz editor and a **Moderate This Quiz** page. A **New Quiz** opens in Canvas's newer quiz-building interface and may be labeled "New Quizzes."

### 7.6 Preview before anything changes

The script reads the quizzes and prints a proposed change.

For example:

```text
PROPOSED CHANGE
---------------
Accommodation: 1.5x time

Quiz 1: 20 min -> +10 -> 30 min
Quiz 2: 30 min -> +15 -> 45 min
Exam Quiz: 60 min -> +30 -> 90 min
```

This is the point to check the calculation.

Nothing has changed yet.

The script will ask:

```text
Type YES to apply this accommodation:
```

It changes Canvas only if you type exactly:

```text
YES
```

Anything else cancels the operation.

---

## 8. How the extra-time calculation works

Canvas stores quiz accommodations as **extra minutes**, not directly as a percentage multiplier.

The script therefore reads each quiz's existing time limit and converts the multiplier into the appropriate number of extra minutes.

Examples:

| Standard quiz | Accommodation | Extra minutes | Student total |
|---:|---:|---:|---:|
| 20 min | 1.5× | +10 | 30 min |
| 30 min | 1.5× | +15 | 45 min |
| 30 min | 2× | +30 | 60 min |
| 60 min | 1.5× | +30 | 90 min |
| 60 min | 2× | +60 | 120 min |

### Courses with different quiz lengths

This is an important feature of the script.

Suppose a course contains:

- a 20-minute quiz;
- a 30-minute quiz; and
- a 60-minute exam.

A fixed `+15 minutes` would **not** produce 1.5× time for all three.

Instead, for a 1.5× accommodation, this script calculates:

```text
20 min -> +10 -> 30 min
30 min -> +15 -> 45 min
60 min -> +30 -> 90 min
```

For Classic Quizzes:

- if every timed quiz needs the same number of extra minutes, the script can use Canvas's efficient course-level Quiz Extensions endpoint;
- if different quizzes need different extra minutes, the script automatically uses Canvas's quiz-level extension endpoint and applies the correct value to each quiz separately.

You do not have to calculate the extra minutes yourself.

### Rounding

Canvas stores `extra_time` in whole minutes.

If a multiplier produces a fractional minute, the script rounds to the nearest whole minute, with `.5` rounded upward.

Always review the proposed change before typing `YES`.

### Untimed quizzes

For Classic Quizzes, items without a time limit are skipped automatically.

There is no timed accommodation to calculate for an untimed quiz.

---

## 9. Classic Quizzes vs. New Quizzes

### Classic Quizzes

This is the workflow that has been tested in a live Canvas course.

The script:

1. lists the course's Classic Quizzes;
2. reads each quiz's time limit;
3. skips untimed quiz items;
4. calculates the appropriate extra time;
5. uses the course-level Quiz Extensions API when one fixed value works for all timed quizzes;
6. otherwise uses the quiz-level Quiz Extensions API to apply the correct extra minutes quiz-by-quiz.

### New Quizzes

Canvas also documents both course-level and quiz-level accommodations APIs for New Quizzes.

The script supports those documented endpoints.

For multiplier accommodations, it attempts to read each New Quiz's configured time limit. Current Canvas API responses typically expose this in the quiz settings as a session time limit in seconds. The script converts that to minutes and calculates the multiplier.

Because institutional Canvas configurations and New Quizzes behavior can vary, **verify your first New Quizzes accommodation manually before using the workflow broadly**.

If the API does not expose a usable time limit, the script stops rather than guessing.

### A course containing both Classic and New Quizzes

Run the script once for the Classic Quizzes and again for the New Quizzes.

The script intentionally asks which engine to modify so you can review each operation separately.

---

## 10. Always verify the first change

Even though the API is performing the same kind of update you would make manually in Canvas, keep a human verification step.

After the script reports success:

1. Open one quiz in Canvas.
2. Open the quiz moderation/accommodation view.
3. Find the student.
4. Confirm the extra time is correct.

For a 30-minute quiz with a 1.5× accommodation, you should see the equivalent of:

```text
+15 minutes
```

or a 45-minute total, depending on the Canvas interface.

If the course has different quiz lengths, verify at least:

- one shorter quiz; and
- one longer quiz.

Only after that first verification should you rely on the same workflow for additional students in that course.

---

## 11. Common problems

| Problem | What to check |
|---|---|
| `401 Unauthorized` | The token may be invalid, expired, copied incorrectly, or associated with a different Canvas server. |
| `403 Forbidden` | Your Canvas role may not have permission to modify quiz accommodations in that course. |
| `400 Bad Request` | Canvas rejected the request format or a value. Copy the error message, but **remove student information and never share your token** before asking for help. |
| No student found | Use the student's exact Canvas login/email and confirm the student is actively enrolled. |
| More than one student matched | Rerun with the exact Canvas login/email rather than a partial name. |
| No timed Classic Quizzes found | Confirm the course actually uses Classic Quizzes and that the quizzes have time limits. |
| New Quiz time limit could not be read | The institution's New Quizzes API response may not expose the necessary setting. Do not guess; set the accommodation manually or use an exact-minute accommodation if appropriate. |
| `python3: command not found` on Mac | Install Python 3 from python.org, then reopen Terminal. |
| `py` is not recognized on Windows | Try `python` instead; otherwise install Python 3 and make sure it is available in PATH. |
| File not found | Confirm where `canvas_quiz_accommodation.py` was downloaded and use that path. |

---

## 12. Privacy and safe use

This script handles student information, so use it carefully.

### Do

- enter student information only into the local script prompt;
- verify the student's identity before confirming;
- use the minimum information needed to identify the student;
- keep your access token private;
- revoke and replace a token if you think it was exposed;
- verify the first accommodation manually in Canvas.

### Do not

- put student names, IDs, or email addresses into the shared Python file;
- commit student information to GitHub;
- put your Canvas access token into this repository;
- paste a token into a GitHub Issue;
- email your token to another instructor;
- type `YES` without reviewing the proposed changes.

A Canvas API call acts with **your Canvas permissions**. The API is not a separate account.

---

## 13. What the script actually does

You do not need to understand this section to use the tool.

At a high level, the script uses Canvas's official REST API:

1. It reads the course from the URL you provide.
2. It uses your access token to authenticate as you.
3. It searches active student enrollments.
4. It retrieves the course's quizzes.
5. It reads the quiz time limits.
6. It calculates the accommodation.
7. It prints a preview.
8. It waits for an explicit `YES`.
9. It submits the accommodation to Canvas.

### Classic Quizzes

For a single shared extra-time value, the script can use:

```text
POST /api/v1/courses/:course_id/quiz_extensions
```

When different quizzes require different values, it uses:

```text
POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions
```

### New Quizzes

At the course level:

```text
POST /api/quiz/v1/courses/:course_id/accommodations
```

At the individual quiz level:

```text
POST /api/quiz/v1/courses/:course_id/quizzes/:assignment_id/accommodations
```

The script sends only the information needed for the accommodation.

---

## 14. Limitations

- Your institution must permit personal Canvas API tokens.
- Your Canvas role must have permission to modify quiz accommodations.
- Canvas's API accepts extra time in integer minutes, so some multipliers require rounding.
- Classic Quizzes and New Quizzes use different Canvas APIs.
- The Classic Quizzes workflow has been field-tested; New Quizzes should be verified carefully in your own environment.
- This tool does not interpret an accommodation letter for you. Enter only the accommodation that has already been approved by your institution's disability/accessibility office.
- This tool does not change assignment due dates, availability windows, or attempts unless the code is explicitly extended to do so.
- A successful API response is not a substitute for verifying the first accommodation in Canvas.

---

## 15. Canvas API references

Official Instructure documentation:

- **Quiz Extensions API — Classic Quizzes**  
  https://canvas.instructure.com/doc/api/quiz_extensions.html

- **Course Quiz Extensions API — Classic Quizzes**  
  https://canvas.instructure.com/doc/api/all_resources.html

- **New Quizzes Accommodations API**  
  https://canvas.instructure.com/doc/api/new_quizzes_accommodations.html

- **New Quizzes API**  
  https://canvas.instructure.com/doc/api/new_quizzes.html

- **Canvas OAuth / access tokens**  
  https://canvas.instructure.com/doc/api/file.oauth.html

---

## Recommended practice

Use the API to eliminate repetitive clicking, not human review.

The safest workflow is:

```text
identify student
      ↓
read actual quiz durations
      ↓
preview exact changes
      ↓
type YES
      ↓
verify in Canvas
```

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

## Contributing

Bug reports and improvements are welcome. Before posting an issue, remove all student-identifying information and **never include a Canvas access token**. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).
