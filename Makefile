.DEFAULT_GOAL := help

.PHONY: init
init: ## Init the requirements
	$(info --- 🖥 Init dependencies ---)
	@pip install -r requirements.txt

.PHONY: format
format: ## Format the code
	$(info --- 🐍 Check Python format ---)
	@ruff . --fix
	@echo "👍"


.PHONY: prepare-data
prepare-data: ## Prepare data
	$(info --- 📍 Prepare data ---)
	@PYTHONPATH=. python data_preparation/prepare_delta_buddy.py
	@echo "👍"

.PHONY: launch-ui
launch-ui: ## Launch the UI
	$(info --- 🤖 Launch the UI ---)
	@PYTHONPATH=. chainlit run app/chainlit_main.py
	@echo "👍"


.PHONY: launch-api
launch-api: ## Launch the API
	$(info --- 🏭 Launch the API ---)
	@uvicorn app.main:app --reload
	@echo "👍"

.PHONY: help
help: ## List the rules
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'