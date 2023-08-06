#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 19:56:52 2020

@author: corkep
"""

from spatialmath import *
from sympy import symbols

theta = symbols('theta')

a = base.rotx(theta)
print(a)

a = SO3.Rx(theta)
print(a)

a = SO3.Rx(0.3)
print(repr(a))