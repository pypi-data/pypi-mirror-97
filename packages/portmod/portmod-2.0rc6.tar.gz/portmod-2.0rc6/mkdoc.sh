#!/bin/bash

rm -r apidoc
sphinx-apidoc -o apidoc . test setup.py -e --ext-autodoc --ext-todo --ext-viewcode --extensions sphinx.ext.napoleon --extensions sphinx_autodoc_typehints --extensions sphinx.ext.intersphinx --extensions sphinx_rtd_theme --full -H Portmod -A "Portmod Authors" -V "`./bin/portmod --version`"
cd apidoc
echo -e "\nhtml_theme = \"sphinx_rtd_theme\"" >> conf.py
echo "always_document_param_types = True" >> conf.py
PYTHONPATH=.. make html
RESULT=$?
cd ..
exit $RESULT
