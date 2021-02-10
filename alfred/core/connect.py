""" Internal connection module.
"""
import sqlite3

# TODO: Move to show configuration
__WGIT_DATABASE = "/software/config/alfred/wgid.db"

wgit = sqlite3.connect(__WGIT_DATABASE)
cursor = wgit.cursor()

del __WGIT_DATABASE
