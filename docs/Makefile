# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

PACKAGE = django_aai_eduhr

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

apidoc:
	sphinx-apidoc -e -o $(SOURCEDIR)/api $(SOURCEDIR)/../$(PACKAGE) \
	    $(SOURCEDIR)/../$(PACKAGE)/management \
	    $(SOURCEDIR)/../$(PACKAGE)/migrations \
	    $(SOURCEDIR)/../$(PACKAGE)/aai_attribute_map.py \
	    $(SOURCEDIR)/../$(PACKAGE)/tests.py \
	    $(SOURCEDIR)/../$(PACKAGE)/urls.py
