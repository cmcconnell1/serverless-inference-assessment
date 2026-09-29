# Changelog

All notable changes to this project.

## [0.1.0] - 2026-09-29

### Added
- Initial release: assessment docs 00 to 06, a short brief (`brief/`), probe and summary scripts, source check, and two PDF builds from one pipeline: the brief and the full report (`build_report.sh --variant`).
- PDF design: embedded IBM Plex Sans and Mono (SIL OFL 1.1), navy cover with author, evidence window, build date, and version; contents with page numbers (`scripts/report/toc_pages.py`); navy table headers with zebra rows; Key insights callouts in docs 00; Mermaid diagrams on the same palette (white background, shared `upstream`, `vendor`, `compute`, `flag`, `akamai` classes).
