# snowmobile

```{include} /description.md
```

```{eval-rst}

.. toctree::
    :maxdepth: 1
    :hidden:

    ./setup.md

.. toctree::
    :caption: Core
    :maxdepth: 1
    :hidden:

    ./usage/snowmobile.md
    ./usage/table.md
    ./usage/script.md
    ./usage/sql.ipynb
    ./usage/snowmobile_toml.md

.. toctree::
    :caption: Technical Resources
    :maxdepth: 1
    :hidden:

    ./autoapi/snowmobile/core/index
    ./snippets.md
    ./usage/advanced.md

.. toctree::
    :caption: Other
    :maxdepth: 1
    :hidden:

    ./acknowledgements.md
    ./changelog.md
    ./authors.md
    ./license.md
```
+++
## Overview
- *[Connecting](#connecting)*
- *[Query Execution](#query-execution)*
- *[Information API](#information-api)*
- *[Loading Data](#loading-data)*
- *[Working with SQL Scripts](#working-with-sql-scripts)*

<br>

```{div} sn-phantom
&nbsp;
```
### *Connecting*

````{admonition} *Connecting*
:class: toggle, sn-gradient-header, sn-indent-h-cell-right-m, sn-toggle-expand

```{div} sn-dedent-v-b-h, sn-dedent-v-t-container-neg
{func}`snowmobile.connect()` returns a [Snowmobile](./usage/snowmobile.md#snowmobile) whose purpose is to:
```
1.  Locate, instantiate, and store [snowmobile.toml](./usage/snowmobile_toml.md#snowmobiletoml)
    as a {class}`~snowmobile.Configuration` object ({class}`sn.cfg`)
1.  Establish a connection to {xref}`snowflake` and store the {xref}`SnowflakeConnection` ({class}`sn.con`)
1.  Serve as the primary entry point to the {xref}`SnowflakeConnection` and {xref}`snowmobile` APIs
+++
```{div} sn-dedent-v-t-h
  The first time it's invoked, [Snowmobile](./usage/snowmobile.md) will find [snowmobile.toml](./usage/snowmobile_toml) and cache its location;
  this step isn't repeated unless the file is moved, the cache is manually cleared, or a new version of {xref}`snowmobile` is installed.
```
+++
**With all arguments omitted, it will authenticate with the default credentials and connection arguments specified in** [**snowmobile.toml**](./usage/snowmobile_toml).

<hr class="sn-blue">

```{div} sn-link-container
{link-badge}`./usage/snowmobile.html,cls=badge-primary badge text-white,Usage: Snowmobile,tooltip=Intro & usage documentation for snowmobile.Snowmobile`
{link-badge}`./autoapi/snowmobile/core/connection/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.connection,tooltip=Documentation parsed from docstrings`
```

````

```{div} sn-pre-code
Establishing a connection from configured defaults is done with:
```

```{div} sn-pre-code, sn-post-code
`sn` is a [](./usage/snowmobile) with the following attributes:
```

```{div} sn-pre-code, sn-post-code
(fixture-sn)=
Different connection arguments are accessed by assigned alias:
```

<br>

`````{admonition} **sn**
:class: sn-fixture, sn-fixture-global

````{div} sn-dedent-v-b-h, sn-dedent-v-t-container-neg
The variable `sn` represents a generic instance of [](./usage/snowmobile) roughly
equivalent to that created with the snippet below; it is referred to as {fa}`fixture sn`
throughout the documentation, and applicable examples make use of
it as a fixture without recreating it each time.
````

```{code-block} python
:emphasize-lines: 3, 3

import snowmobile

sn = snowmobile.connect()
```

<hr class="sn-spacer">

`````

<hr class="sn-spacer">

% -----------------------------------------------------------------------------

```{div} sn-phantom
<br>
```
### *Query Execution*

`````{admonition} *Query Execution*
:class: toggle, sn-gradient-header, sn-indent-h-cell-right-m, sn-toggle-expand

```{div} sn-dedent-v-b-h, sn-dedent-v-container-neg
  There are three convenience methods for executing raw SQL directly off [{fa}`fixture sn`](fixture-sn):
```

```{div} sn-left-pad
{meth}`~snowmobile.Snowmobile.query()` implements {meth}`pandas.read_sql()` for querying results into a {class}`~pandas.DataFrame`

{meth}`~snowmobile.Snowmobile.ex()` implements {meth}`SnowflakeConnection.cursor().execute()` for executing commands within a {xref}`SnowflakeCursor`

{meth}`~snowmobile.Snowmobile.exd()` implements {meth}`SnowflakeConnection.cursor(DictCursor).execute()` for executing commands within a {xref}`DictCursor`
```

<hr class="sn-blue">

```{div} sn-link-container
{link-badge}`./usage/snowmobile.html#executing-raw-sql,cls=badge-primary badge text-white,Usage: Executing Raw SQL,tooltip=Usage documentation for Executing Raw SQL`
{link-badge}`./autoapi/snowmobile/core/connection/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.connection,tooltip=Documentation parsed from docstrings`
```

`````

````{admonition} Setup
:class: is-setup, sn-clear-title, sn-indent-h-cell-m, sn-indent-h-sub-cell-right, sn-inline-block-container, sn-dedent-v-b-container

(sn)=
The next two sections make use\
of a **sample_table** containing:
```{div} sn-dedent-v-b-container
|   COL1 |   COL2 |
|-------:|-------:|
|      1 |      1 |
|      2 |      4 |
|      4 |      9 |
```
````

<hr class="sn-spacer">

```{div} sn-pre-code
Into a {class}`~pandas.DataFrame`:
```

```{div} sn-pre-code
Into a {xref}`SnowflakeCursor`:
```

```{div} sn-pre-code
Into a {xref}`DictCursor`:
```

```{div} sn-pre-code
Or to get a single value:
```

% -----------------------------------------------------------------------------

```{div} sn-phantom
<br>
```
### *Information API*

`````{admonition} *Information API*
:class: toggle, sn-gradient-header, sn-indent-h-cell-right-m, sn-toggle-expand

```{div} sn-dedent-v-container-neg
  [**snowmobile.SQL**](./sql.md) generates and executes raw SQL from inputs; it comes free as the {attr}`~snowmobile.Snowmobile.sql`
  attribute of [{fa}`fixture sn`](fixture-sn), and its purpose is to provide a bare bones Python API to query metadata and execute
  administrative commands against {xref}`snowflake`.
```

<hr class="sn-blue">

```{div} sn-link-container
{link-badge}`./autoapi/snowmobile/core/sql/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.sql,tooltip=Documentation parsed from docstrings`
```

`````

<p class="sn-indent-cell"></p>

```{div} sn-pre-code
Check existence of tables/views:
```

```{div} sn-pre-code, sn-post-code
Sample records from a table:
```

```{div} sn-pre-code
Query depth:
```

```{div} sn-pre-code, sn-post-code
Submit basic administrative commands:
```

```{div} sn-pre-code, sn-post-code
Query DDL:
```

```{div} sn-pre-code
Provide `run=False` to get the raw sql
```

```{div} sn-pre-code
Drop objects:
```

```{div} sn-phantom
<br>
```
### *Loading Data*

(intro/loading-data)=
`````{admonition} *Loading Data*
:class: toggle, sn-gradient-header, sn-indent-h-cell-right-m, sn-toggle-expand, sn-incl-tabbed-shadow-b-blue

<hr class="sn-spacer">

````{tabbed} Context
  {class}`~snowmobile.Table` is a loading solution that at minimum accepts a `df` ({class}`~pandas.DataFrame`)
  and a `table` name ({class}`str`) in addition to [{fa}`fixture sn`](fixture-sn).
+++
  In the same way that [**Snowmobile**](./usage/snowmobile) handles its keyword arguments,
  {class}`~snowmobile.Table` will adhere to any arguments explicitly provided and defer
  to the values configured in [snowmobile.toml](./usage/snowmobile_toml) otherwise.
````

````{tabbed} +
  ```{div} sn-dedent-v-t
  *The behavior outlined below reflects those within the
  [default snowmobile.toml file](./usage/snowmobile_toml.md#file-contents)*, meaning that `t1` will:
  ```
  1. Check if *sample_table* exists in the schema associated with {attr}`sn.con`
  2. If *sample_table* **does** exist, it will validate `df` against *sample_table* and throw an error
     if their dimensions are not identical
  3. If *sample_table* does **not** exist (as is the case here), it will generate DDL from `df` and execute it as part of the loading process
````

```{div} sn-link-container
{link-badge}`./usage/table.html,cls=badge-primary badge text-white,Usage: snowmobile.Table,tooltip=Intro & usage documentation for snowmobile.Table`
{link-badge}`./autoapi/snowmobile/core/table/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.table,tooltip=Documentation parsed from docstrings`
```

``````

`````{admonition} Setup
:class: is-setup, sn-clear-title, sn-block-container, sn-indent-h-cell-m, sn-indent-h-sub-cell-right

````{panels}

The `df` used below is created with:

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(
    data = {'COL1': [1, 2, 3], 'COL2': [1, 4, 9]}
)
print(df.shape)  #> (3, 2)
```

---

|   COL1 |   COL2 |
|-------:|-------:|
|      1 |      1 |
|      2 |      4 |
|      3 |      9 |

````

`````

<hr class="sn-spacer">

```{div} sn-pre-code, sn-indent-v-t-container
Given a `df` ({class}`~pandas.DataFrame`) and a `table` ({class}`str`) to load into, a [**Table**](./usage/table) can be created with:
```

```{div} sn-pre-code, sn-post-code
With [](./usage/snowmobile_toml) defaults, `t1` has pre-inspected some things like:
```

```{div} sn-pre-code
We can create *sample_table* and load `df` into with:
```

```{div} sn-pre-code
Here are two ways to verify `t1.load()` did its job:
```

```{div} sn-indent-h-cell
<hr class="sn-green-medium" style="margin-top: 1.4rem; margin-bottom: 0.5rem;">
```

```{div} sn-pre-code
In instances where the {class}`~pandas.DataFrame` and table have different dimensions:
```

```{div} sn-pre-code
Here's what `t2` knows about `df` and *sample_table*:
```

```{div} sn-pre-code, sn-post-code
`t2` also checked the columns of `df2` and deduped them by appending a suffix to the second set:
```

```{div} sn-pre-code
Loading in the same way we did `t1` will throw an error with the default [snowmobile.toml](./usage/snowmobile_toml):
```

```{div} sn-pre-code, sn-post-code
Explicit arguments take precedent over configurations in [snowmobile.toml](./usage/snowmobile_toml), so `df2` can still be loaded with:
```

<br>
<hr class="sn-spacer">

```{div} sn-phantom
&nbsp;
```
### *Working with SQL Scripts*

(intro/working-with-sql-scripts)=
`````{admonition} *Working with SQL Scripts*
:class: toggle, sn-gradient-header, sn-indent-h-cell-right-m, sn-toggle-expand, sn-incl-tabbed-shadow-b-blue

<hr class="sn-spacer">

````{tabbed} Context
  [**snowmobile.Script**](./usage/script.md) accepts a full `path` to a .sql file
  in addition to [{fa}`fixture sn`](fixture-sn); the contents of the .sql file are parsed based on the
  patterns specified in the [snowmobile.toml](./usage/snowmobile_toml) file that [{fa}`fixture sn`](fixture-sn)
  was instantiated with.
+++
  At a minimum, the file is split into individual statements, each of which is
  checked for decorated information in the form of a string directly preceding it
  wrapped in an opening (`/*-`) and closing (`-*/`) pattern, the simplest form of
  which is a single-line string that can be used as an accessor to the statement
  it precedes.
+++
  When no information is provided, [Script](./usage/script.ipynb) generates a
  generic name for the statement based on the literal first SQL keyword
  it contains and its index position.
````

````{tabbed} +
  Line **27** within *sample_table.sql* represents the minimum markup required to associate a
  name with an individual statement; consistency in tag structure has obvious benefits, but
  this is a freeform string that can be anything.
+++
  Line **19** is an example of a special tag; the leading `qa-empty` tells
  [**Script**](./usage/script.ipynb) to run assertion that its results are
  null (0 records) before continuing execution of the script.
+++
  The tags for statements beginning on lines **1**, **6**, and **17** were generated by
  [**Script**](./usage/script.ipynb) based their contents and relative positions within the script.
````

```{div} sn-link-container
{link-badge}`./usage/script.html,cls=badge-primary badge text-white,Usage: snowmobile.Script,tooltip=Intro & usage documentation for snowmobile.Script`
{link-badge}`./autoapi/snowmobile/core/script/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.script,tooltip=Documentation parsed from docstrings`
```

`````

````{admonition} Setup
:class: is-setup, sn-clear-title, sn-block-container, sn-indent-h-cell-m

```{div} sn-dedent-v-t-h, hanging
`path` is a full path ({class}`pathlib.Path` or {class}`str`) to a file,
*sample_table.sql*, containing 5 standard sql statements:
```

```{literalinclude}  ./snippets/overview/sample_table.sql
:language: sql
:lines: 2-37
:lineno-start: 1
:emphasize-lines: 1, 6, 17, 20, 28
```

````

```{div} sn-pre-code
Given a `path` to *sample_table.sql*, a [Script](./usage/script) can be created with:
```

```{div} sn-pre-code, sn-post-code
  Any [Statement](/autoapi/snowmobile/core/statement/index) can be accessed by
  their {attr}`~snowmobile.core.Name.nm` or index position:
```

```{div} sn-pre-code, sn-post-code
  Statements can be accessed by their index position or name ({attr}`~snowmobile.core.Name.nm`):
```

```{div} sn-pre-code, sn-post-code
Each [Statement](/autoapi/snowmobile/core/statement/index) has its own set of attributes:
```

```{div} sn-pre-code, sn-post-code
Based on statement attributes, `script` can be subsetted and ran within that context:
```

```{div} sn-pre-code, sn-post-code
Based on statement attributes, `script` can be filtered and used within that context:
```

```{div} sn-pre-code, sn-post-code
Spans of statements are directly executable by index boundaries:
```

```{div} sn-pre-code, sn-post-code
And their results accessible retroactively:
```

```{div} sn-pre-code, sn-post-code
Generated SQL can be added directly to `script`:
```

```{div} sn-pre-code, sn-post-code
And descriptive statements can be skipped instead of commented out:
```

<hr class="sn-spacer">

```{div} sn-pre-code
See [Usage: Script](./usage/script.md) for more in-depth use of [snowmobile.Script](./usage/script).
```

<br>

### *Wrap-Up*
<hr class="sn-green-thick sn-indent-h-cell-right-m">

`````{admonition} Note
:class: note

 ```{div} sn-dedent-v-b-h
 By instantiating `t1` and `script` with the same instance of [{fa}`fixture sn`](fixture-sn),
 **the same instance of {xref}`SnowflakeConnection` and [Configuration](./usage/snowmobile_toml)
 is shared amongst:**
 ```
 - {class}`sn:` {class}`~snowmobile.Snowmobile`
 - {class}`t1:` {class}`~snowmobile.Table`
 - {class}`script:` {class}`~snowmobile.Script`

`````

<style>
.md-typeset h1, .md-typeset h2 {
    margin-top: -0.5rem;
}

.md-typeset h3 {
    margin-top: -0.5rem;
    margin-bottom: 0.2rem;
    font-size: 140%;
}

<!-- .md-typeset .admonition.is-setup { -->
<!--     border-left-color: #11838e; -->
<!--     margin: -0.15rem 1.5rem .7rem 0.85rem; -->
<!--     display: block; -->
}
</style>
