.PHONY: poetry-update
#@@ Compile intermediate products only
#@ Compiles the intermediate products, such as .obj files and such.
poetry--update:
	$(EXEC_CMD) poetry update
