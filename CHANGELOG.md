# Changelog

## 1.0.0 - 2026-08-24

Initial public version.

### Multi-student workflow

- Continue directly to another student in the same course after each accommodation.
- Switch between Classic and New Quizzes without restarting.
- Move to another Canvas course without re-entering the API token.
- Cache the selected course's quiz list during a run to reduce repetitive API reads.

### Features

- Beginner-friendly command-line workflow for macOS and Windows.
- Student lookup by Canvas login/email or name.
- Classic Quizzes support.
- New Quizzes support using Canvas's documented accommodations APIs.
- Multiplier accommodations such as 1.5× and 2×.
- Exact extra-minute accommodations.
- Automatic reading of actual quiz time limits.
- Correct multiplier calculation when quiz durations differ.
- Automatic per-quiz handling for mixed-duration Classic Quizzes.
- Automatic skipping of untimed Classic Quiz items.
- Preview of all planned changes before writing to Canvas.
- Explicit `YES` confirmation required before any accommodation is applied.
- No third-party Python dependencies.
