# Loading environment variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Usage in Docker File
ifeq ($(USE_DOCKER),1)
	EXEC_CMD := docker compose exec -ti web
else
	EXEC_CMD :=
endif

# Load All files
MAKE_DIR=./Makefiles
include $(wildcard $(MAKE_DIR)/*/*.mk)
include $(wildcard $(MAKE_DIR)/*.mk)

#
#.PHONY: sass
#sass:
#	$(EXEC_CMD) poetry run python manage.py compilescss
#	make collectstatic
#
#.PHONY: quality
#quality:
#	$(EXEC_CMD) ruff check .
#	$(EXEC_CMD) poetry run black --check --exclude=venv .
#
#.PHONY: fix
#fix:
#	$(EXEC_CMD) ruff check . --fix
#	$(EXEC_CMD) poetry run black --exclude=venv .
#
#.PHONY: index
#index:
#	$(EXEC_CMD) poetry run python manage.py update_index
#
#.PHONY: init
#init:
#	$(EXEC_CMD) poetry install --without dev
#	$(EXEC_CMD) poetry run python manage.py migrate
#	make collectstatic
#	$(EXEC_CMD) poetry run python manage.py set_config
#	$(EXEC_CMD) poetry run python manage.py import_dsfr_pictograms
#	$(EXEC_CMD) poetry run python manage.py create_starter_pages
#	$(EXEC_CMD) poetry run python manage.py import_page_templates
#	make index
#
#.PHONY: init-dev
#init-dev:
#	make init
#	$(EXEC_CMD) poetry install
#	$(EXEC_CMD) poetry run pre-commit install
#
#
#.PHONY: update
#update:
#	$(EXEC_CMD) poetry install --without dev
#	$(EXEC_CMD) poetry run python manage.py migrate
#	make collectstatic
#	$(EXEC_CMD) poetry run python manage.py import_dsfr_pictograms
#	$(EXEC_CMD) poetry run python manage.py import_page_templates
#	make index
#
#
#.PHONY: demo
#demo:
#	make init
#	$(EXEC_CMD) poetry run python manage.py create_demo_pages
#
#.PHONY: runserver
#runserver:
#	$(EXEC_CMD) poetry run python manage.py runserver $(HOST_URL):$(HOST_PORT)
#
#
#.PHONY: test
#test:
#	$(EXEC_CMD) poetry run python manage.py test --buffer --parallel
#
#.PHONY: test-unit ## test unit
#test-unit:
#	$(EXEC_CMD) poetry run python manage.py test --settings config.settings_test


.PHONY: clean
clean: ## Tidy up local environment
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete