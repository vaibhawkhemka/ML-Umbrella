# Define colors
RED := \033[0;31m
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RESET := \033[0m

# Define environment name
ENV_NAME := py39upstash

help:
	@echo Usage: make [target]
	@echo ""
	@echo Available targets:
	@echo -------------------
	@echo "$(YELLOW)list$(RESET)		: List available targets with descriptions"
	@echo ""
	@echo "== Env =="
	@echo "$(GREEN)install$(RESET)		: Installs a new py39 env and sets-up poetry packages"
	@echo ""
	@echo "== Help =="
	@echo "$(RED)clean_vdb$(RESET)		: Removes all vectors from upstash vector db"
	@echo ""
	@echo "== Test =="
	@echo "$(YELLOW)test$(RESET)		: Runs unit-tests."
	@echo ""
	@echo "== Production =="
	@echo "$(GREEN)run_producers$(RESET)	: Starts the Kafka Producers"
	@echo "$(GREEN)run_pipeline$(RESET)		: Starts the bytewax pipeline"
	@echo "$(GREEN)run_ui$(RESET)		: Starts the bytewax pipeline"
	@echo ""
	@echo ""

list: help

install:
	@echo $(GREEN) [CONDA] Creating [$(ENV_NAME)] python env $(RESET)
	conda create --name $(ENV_NAME) python=3.12 -y
	@echo Activating the environment...
	@call conda activate $(ENV_NAME) && pip install poetry
	@echo Setting Poetry to use the current Python interpreter...
	@for /f "delims=" %%i in ('where python') do @call poetry env use %%i
	@echo Installing Packages
	@echo Changing to pyproject.toml location...
	set PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring && call conda activate $(ENV_NAME) && poetry install
	
test:
	@echo $(GREEN) [TESTING] Running UnitTests $(RESET)
	@call conda activate $(ENV_NAME) && poetry run pytest tests/

run_producers:
	@echo $(GREEN) [RUNNING] Producers $(RESET)
	@call conda activate $(ENV_NAME) && poetry run python -m src.producer

run_pipeline:
	@echo $(GREEN) [RUNNING] Bytewax Pipeline $(RESET)
	@call conda activate $(ENV_NAME) && set RUST_BACKTRACE=1 && poetry run python -m bytewax.run src/start:flow

clean_vdb:
	@echo $(RED) [CLEANING] Upstash Vector DB $(RESET)
	@call conda activate $(ENV_NAME) && poetry run python -m src.helpers clean_vectordb

run_ui:
	@echo $(GREEN) [RUNNING] Streamlit UI interface $(RESET)
	@call conda activate $(ENV_NAME) && poetry run streamlit run ui.py
