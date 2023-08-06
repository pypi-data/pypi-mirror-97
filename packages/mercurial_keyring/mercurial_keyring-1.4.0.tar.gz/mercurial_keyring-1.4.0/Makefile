# This makefile is used only for running pytype checks.
#
# To prepare:
#     sudo apt install ninja
#     pip install pytype
#
# To run checks:
#     make pytype
#
# Usually you will set
#      HGPATH - to Mercurial sources directory
#      MEUPATH - to mercurial_extension_utils directory
# unless defaults below are OK

PYTHON = python
PYTYPE = pytype
PYTHON_VERSION = $(shell $(PYTHON) -c 'import sys; print("{0.major}.{0.minor}".format(sys.version_info))')

HGPATH  ?= ../../mercurial_tracked/hg-stable
MEUPATH ?= ../extension_utils

ifneq ($(HGPATH),)
export PYTHONPATH := $(realpath $(HGPATH)):$(PYTHONPATH)
endif
ifneq ($(MEUPATH),)
export PYTHONPATH := $(realpath $(MEUPATH)):$(PYTHONPATH)
endif


.PHONY: help
help:
	@echo 'Commonly used make targets:'
	@echo '  pytype       - run pytype checks on the source tree'

.PHONY: pytype
pytype:
	@ # [ -n "$(HGPATH)" ] || { echo "HGPATH not specified"; false; }
	@ # [ -d "$(HGPATH)" ] || { echo "HGPATH not found: $(HGPATH)"; false; }
	$(PYTYPE) -P ".:$(HGPATH):$(MEUPATH)" -V "$(PYTHON_VERSION)" -j auto \
		--config pytype.cfg
	@echo 'pytype crashed while generating the following type stubs:'
	find .pytype/pyi -name '*.pyi' | xargs grep -l '# Caught error' | sort

.PHONY: clean
clean:
	$(PYTHON) setup.py clean
	$(RM) -R .pytype
