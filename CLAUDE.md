# Repository instructions

- Treat this file as the highest-priority repository-specific guidance.
- Do not edit `index.html` directly. It is a generated file.
- Make application and task-data changes in `build/build.py` (and, when map bounds change, `build/map_configs.json`).
- Regenerate the site from the repository root with `python build/build.py`.
- Review the generated `index.html` diff before committing.
- Do not commit or push unrelated files or changes.
