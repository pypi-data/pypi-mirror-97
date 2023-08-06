# -*- coding: utf-8 -*-
"""pyramid_decoy setup module."""
from setuptools import setup


setup(
    entry_points="""
      [paste.app_factory]
      decoy = pyramid_decoy.app:main
    """,
)
