.PHONY: help evidence summarize check-sources report rebuild-report all clean

BRIEF      := dist/serverless-inference-assessment-brief-chris-mcconnell.pdf
REPORT     := dist/serverless-inference-assessment-full-report-chris-mcconnell.pdf
# Inputs both PDFs share: cover date range, version, build tooling, fonts.
COMMON_SRC := evidence/manual/browser-checked-urls.tsv evidence/derived/source-check.md \
              $(wildcard evidence/probes/*/*.meta) \
              CHANGELOG.md scripts/build_report.sh \
              $(filter-out %/__pycache__,$(wildcard scripts/report/*)) \
              $(wildcard scripts/report/fonts/*)
BRIEF_SRC  := $(wildcard brief/*.md) $(COMMON_SRC)
REPORT_SRC := $(wildcard docs/*.md) $(wildcard evidence/derived/*.md) $(COMMON_SRC)

help:
	@echo "make evidence   Capture probes and regenerate derived tables (network, about 90 seconds)"
	@echo "make summarize  Regenerate evidence/derived/*.md from existing captures (offline)"
	@echo "make check-sources  Check cited URLs and key quotes against live pages (network)"
	@echo "make report     Build the brief and the full report, each only if its inputs changed"
	@echo "                  $(BRIEF)"
	@echo "                  $(REPORT)"
	@echo "make rebuild-report  Build both PDFs unconditionally"
	@echo "make all        summarize, then report"
	@echo "make clean      Remove dist/"

evidence:
	./scripts/probe_providers.sh -v
	python3 scripts/summarize_probes.py

summarize:
	python3 scripts/summarize_probes.py

check-sources:
	python3 scripts/check_sources.py

# Each PDF is a build artifact of its chapters plus the shared tooling.
# Editing an input leaves it stale, so each is a real file target with those
# prerequisites rather than a .PHONY command.
$(BRIEF): $(BRIEF_SRC)
	./scripts/build_report.sh -v --variant brief

$(REPORT): $(REPORT_SRC)
	./scripts/build_report.sh -v --variant full

report: $(BRIEF) $(REPORT)
	@echo "$(BRIEF) and $(REPORT) are up to date with their inputs"

rebuild-report:
	./scripts/build_report.sh -v --variant brief
	./scripts/build_report.sh -v --variant full

all: summarize report

clean:
	rm -rf dist
