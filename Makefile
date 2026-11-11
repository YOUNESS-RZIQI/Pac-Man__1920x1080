CONFIG = config.json
install:

	    pip install uv || true
		uv sync
		@clear

run:

		@clear
		@uv run python3 src/pac-man.py $(CONFIG)

debug:

# s: step into function
# n: Step Over
# r: Step Out
# l: list source code
# p: print
# q: quit

		@clear
		@uv run python -m pdb src/pac-man.py $(CONFIG)

package:
		rm -rf dist build Pacman.spec	
		uv run pyinstaller --name Pacman --onefile \
    	--collect-all mlx \
    	--add-data "Images:Images" \
    	--add-data "songs:songs" \
    	src/pac-man.py


clean:
		@rm -rf src/__pycache__ __pycache__ .mypy_cache 
		@clear

fclean: clean
		rm -rf build dist .venv


lint:
		@clear
		uv run flake8 src/

		uv run mypy src/ \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
