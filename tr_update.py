#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
if sys.platform == 'win32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
    pybabel = 'pybabel'
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot cps')
os.system(pybabel + ' update -i messages.pot -d cps/translations')
os.unlink('messages.pot')