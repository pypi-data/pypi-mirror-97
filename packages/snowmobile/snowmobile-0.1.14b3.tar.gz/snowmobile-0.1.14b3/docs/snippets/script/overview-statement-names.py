"""
Instantiate `script` from 'overview.sql' and demonstrate 'nm' resolution.
../docs/snippets/script/overview-statement-names.py
"""

# Setup -----------------------------------------------------------------------
from pathlib import Path
paths = {p.name: p for p in Path.cwd().glob('**/*.sql')}
path = paths['overview.sql']

import snowmobile

sn = snowmobile.connect(delay=True)

# Example ---------------------------------------------------------------------

# ==== nm ====
script = snowmobile.Script(path=path, sn=sn)
script.dtl()

# Store statements 1 and 4 for inspection
s1, s4 = script(1), script(4)

print(s1.nm)      #> create table~s1
print(s4.nm)      #> select all~sample_table

print(s1.desc)    #> s1
print(s4.desc)    #> sample_table

print(s1.anchor)  #> create table
print(s4.anchor)  #> select all

print(sn.cfg.script.patterns.core.delimiter)  #> ~

# -- Block 2
print(s4.anchor_ge)  #> select data
print(s4.anchor_pr)  #> select all
print(s4.anchor)     #> select all

print(s4.desc_ge)    #> s4
print(s4.desc_pr)    #> sample_table
print(s4.desc)       #> sample_table

print(s4.nm_ge)      #> select data~s4
print(s4.nm_pr)      #> select all~sample_table
print(s4.nm)         #> select all~sample_table

# -- Definitions --

print(s1.nm)      #> create table~s1
print(s4.nm)      #> select all~sample_table

print(s1.desc)    #> s1
print(s4.desc)    #> sample_table

print(s1.anchor)  #> create table
print(s4.anchor)  #> select all

print(s1.kw)  #> create
print(s4.kw)  #> select
