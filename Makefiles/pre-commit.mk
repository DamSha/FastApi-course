.PHONY: pre-commit-run
#@@ pre-commit run -a
pc--run:
	$(EXEC_CMD) pre-commit run -a

.PHONY: pre-commit-install
#@@ pre-commit install
pc--install:
	$(EXEC_CMD) pre-commit install

.PHONY: pre-commit-autoupdate
#@@ pre-commit autoupdate
pc--up:
	$(EXEC_CMD) pre-commit autoupdate

.PHONY: pre-commit-uninstall
#@@ pre-commit uninstall
pc--uninstall:
	$(EXEC_CMD) pre-commit uninstall
