.PHONY: build test package clean

build:
	poetry install

test:
	poetry run aw-watcher-afk-barrier --help  # Ensures that it at least starts
	make typecheck

typecheck:
	poetry run mypy aw_watcher_afk_barrier --ignore-missing-imports

package:
	pyinstaller aw-watcher-afk-barrier.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf aw_watcher_afk_barrier/__pycache__
