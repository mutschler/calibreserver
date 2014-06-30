#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
if sys.platform == 'win32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
    pybabel = 'pybabel'
os.system(pybabel + ' compile -d cps/translations')