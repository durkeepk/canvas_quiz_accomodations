# Security and privacy

This project works with Canvas LMS using a personal access token and may be used with student information. Treat both carefully.

## Canvas access tokens

A Canvas access token should be treated like a password.

Never:

- commit an access token to this repository;
- paste an access token into a GitHub Issue or Discussion;
- email your token to another person;
- hard-code your token into `canvas_quiz_accommodation.py`;
- include a token in a screenshot.

The script requests the token interactively and does not save it to disk.

If a token may have been exposed, revoke it in Canvas immediately and create a new one.

## Student information

Do not post real student names, email addresses, Canvas IDs, SIS IDs, accommodation letters, or other student-identifying information in public issues or pull requests.

If you need help troubleshooting:

1. remove the access token;
2. replace student names/emails/IDs with placeholders;
3. remove any other institutional or student information that is not necessary to reproduce the problem.

## Reporting a security issue

If you identify a problem that could expose access tokens or student information, do not publish sensitive details in a public issue. Report the problem privately to the repository maintainer.

## Institutional policy

This project does not override your institution's rules regarding accessibility accommodations, student records, FERPA, Canvas API access, or personal access tokens. Use the tool only when you are authorized to make the same accommodation manually in Canvas.
