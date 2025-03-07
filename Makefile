install:
	uv sync

run:
	export ENV_FOR_DYNACONF=dev; uv run app

lint:
	uv run pre-commit run --all

run_prod: install
	export ENV_FOR_DYNACONF=prod; uv run app
