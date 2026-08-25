# Contributing

Contributions that improve reliability, documentation, accessibility, or compatibility with Canvas are welcome.

## Before opening an issue

Please check that the problem is reproducible and include:

- operating system (macOS or Windows);
- Python version (`python3 --version`, `py --version`, or `python --version`);
- whether the course uses Classic Quizzes or New Quizzes;
- the Canvas HTTP error code and error message, if one appeared.

## Protect student information

Before posting anything publicly:

- remove all student names;
- remove student email/login information;
- remove Canvas/SIS student IDs;
- remove accommodation letters or disability-related information;
- remove your Canvas access token.

Use placeholders such as `STUDENT_NAME`, `STUDENT_ID`, and `TOKEN`.

## Pull requests

For code changes:

1. keep the script dependency-free unless there is a strong reason to add a package;
2. preserve the preview-and-confirm workflow;
3. do not add logging that writes tokens or student information to disk;
4. prefer stopping with a clear error over guessing;
5. update the README when behavior changes.

## Testing

The Classic Quizzes workflow has been field-tested in a live Canvas course. Changes affecting New Quizzes should be tested carefully against current Canvas documentation and verified manually in Canvas.
