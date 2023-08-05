(script)=
# Script
<hr class="sn-grey">

```{div} sn-dedent-v-b-h
{class}`snowmobile.Script` provides lightweight enhancements to how raw sql 
scripts are interacted with through Python; its purpose is to deliver a
composition of objects and data that can be further leveraged
based on the use case.
```

````{admonition} Note
:class: note, toggle, toggle-shown, sn-code-pad

 ```{div} sn-unset-code-margins
 **The easiest way to simply execute a sql file is with the 
 {xref}`execute_stream() method` 
 of the {xref}`snowflake.connector2`**, the API for which can be accessed 
 directly off 
 <a class="fixture-sn" href="../index.html#fixture-sn"></a> with: 
 ```
 ```{code-block} python
 :emphasize-lines: 3,3
 from codecs import open
 with open(sqlfile, 'r', encoding='utf-8') as f:
    for cur in sn.con.execute_stream(f):
        for ret in cur:
            print(ret)
 ```

````

+++

<a
    class="sphinx-bs badge badge-secondary badge-pill text-white reference external"
    href="../autoapi/snowmobile/core/script/index.html"
    title="Documentation parsed from docstrings">
    <span>API Docs: snowmobile.core.script</span>
</a>

<hr class="sn-grey">
<hr class="sn-spacer-thick">

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

(script/overview/fixture1)=
## Overview

```{div} sn-dedent-list
- [](#statements)
    - [Quick Intro](script/statements/quick-intro)
    - [Statement Names](script/statements/statement-names)
- [](#markup)
    - [](#tags)
        - [Single-Line](#single-line-tags)
        - [Multi-Line](#multi-line-tags)
    - [](#markers)
    - [](#patterns)
```

<hr class="sn-spacer-thick2">

`````{admonition} **script**
 :class: toggle, toggle-shown, sn-fixture, sn-fixture-local, sn-unset-margins, sn-block, sn-code-pad

 
 ```{div} sn-pre-code
 This section performs operations on an instance of [](#script), referred to
 as {fa}`fixture script` and instantiated with: 
 ```
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 18-18
 ```
 
 <div class="sn-indent-h-cell-m sn-dedent-v-t-container-neg"> 
 
 Where:
 - `sn` is <a class="fixture-sn" href="../index.html#fixture-sn"></a>
 - `path` is a full path ({class}`pathlib.Path` or {class}`str`) to [overview.sql](script/overview/fixture1)
 
 <hr class="sn-spacer-thin">
 <hr class="sn-blue sn-top-margin-hr-thick">
 
 The 7 generic sql statements within 
 [overview.sql](script/overview/fixture1) are arbitrary and chosen based only 
 on the loose criteria of:
 ```{div} sn-bold-list
 1.  Encompassing a sufficient variety of [Statements](#statements) and [](#markup) 
     to demonstrate the fundamentals of how [](#script) parses a sql file
 1.  Can be executed from top to bottom without requiring additional setup
 ```
 
 </div>
 
 <hr class="sn-spacer-thick">
 
 ```{div} sn-snippet-h, sn-indent-h-cell
 [{fa}`file-code-o` overview.sql](../snippets.md#overviewsql)
 ```
 ````{div} sn-indent-h-cell
 ```{literalinclude} ../snippets/script/overview.sql
 :language: sql
 :lines: 3-34
 :emphasize-lines: 1, 6, 17, 20, 22, 24, 32
 ```
 ````
`````

<hr class="sn-spacer-thick">

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

<body>
<div class="sn-section-parent">

 (script/statements/quick-intro)=
 ### Statements
 ---

 <div class="sn-section-connector">&nbsp;</div>
 <div class="sn-section">

 #### **Quick Intro**
 ----

 ```{div} sn-pre-code-s
 When a sql file is parsed by {class}`~snowmobile.Script`, each statement is
 identified and stored as its own
 {class}`~snowmobile.core.statement.Statement`; {meth}`~snowmobile.Script.dtl()`
 is a helper method to inspect a 
 [{fa}`fixture script scripts`](script/overview/fixture1) contents:
 ```
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 19-19
 ```
 ````{div} sn-output
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 22-30
 ```  
 ````
 
 <hr class="sn-grey-dotted sn-top-pad-hr-thick">
  
 ```{div} sn-pre-code-s
 Accessing the first and last statements of 
 [{fa}`fixture script`](script/overview/fixture1)
 and inspecting a few of their attributes can be done with:
 ``` 
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 34-43
 ```
 
 ```{div} sn-pre-code-s, sn-post-code
 A {class}`~snowmobile.core.Statement` can be interacted with through the [](#script) 
 from which it was instantiated or stored and interacted with independently; for 
 example, here are two ways that the first statement in 
 [overview.sql](script/overview/fixture1) can be executed: 
 ```
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 46-47
 ```

 <hr class="sn-grey-dotted sn-top-pad-hr-thick">

 Those above are several amongst a set of {class}`~snowmobile.core.Statement` 
 attributes that can be used to alter the scope of a 
 [](#script).

 For example, the following snippet filters out `drop` and `select` statements 
 based on their {attr}`~snowmobile.core.name.Name.kw` attribute
 and returns a modified [{fa}`fixture script`](script/overview/fixture1), `s`, 
 that can be operated on within that context:
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 50-59
 ```
 ````{div} sn-output
 ```{literalinclude} ../snippets/script/overview-statement-intro.py
 :language: python
 :lines: 62-67
 ```
 ````  
 ```{div} sn-snippet, sn-indent-to-output
 [{fa}`file-code-o` overview-statement-intro.py](../snippets.md#overview-statement-intropy)
 ```
 
 (script/statements/statement-names)= 
 The following section outlines how these components are constructed.
 
 <hr class="sn-green sn-bottom-margin-hr-thick">
 <hr class="sn-spacer-thin">

 #### **Statement Names**
 ----
 
 ```{div} sn-dedent-v-b-h-m
 *The intent of the following taxonomy is to define a standard such that the 
 name for a given statement is:*
 ```
 ```{div} sn-bold-list
 1. Constructed from attributes that can be unambiguously parsed from 
    a piece of raw sql
 1. Structured such that user *provided* names can be easily
    implemented and loosely parsed into the same set of attributes 
    as those *generated* from (**1**)
 ```
 
 <hr class="sn-grey-dotted sn-top-pad-hr">
 
 Every statement has a {class}`~snowmobile.core.name.Name` with a set of
 underlying properties that are used by the rest of the API; for each property, 
 there is a *generated* (**_ge**) and *provided* (**_pr**) attribute from 
 which its final value is sourced.

 (script/note1)=
 *Generated* attributes are populated for all statements, whereas only those
 with a name specified in a [tag](#tags) have populated *provided* attributes;
 consequently, a *provided* value takes precedent over its *generated* counterpart. 
 
 ````{admonition} Example: **nm**
 :class: sn-example
 ```{div} sn-pre-code-s
 The {class}`~snowmobile.core.name.Name.nm` value for a given statement will 
 be equivalent to its {attr}`~snowmobile.core.name.Name.nm_pr` if present and 
 its {attr}`~snowmobile.core.name.Name.nm_ge` otherwise.
 ```
 ````

 (script/statement/nm)=
 This resolution order is repeated across the underlying 
 components of {class}`~snowmobile.core.name.Name.nm`, documented in the
 following sections.

 <hr class="sn-grey-dotted">
 <hr class="sn-spacer-thick2">
 
 `````{admonition} **s1** & **s4**
 :class: toggle, toggle-shown, sn-fixture, sn-fixture-local, sn-block, sn-increase-margin-v-container, sn-code-pad
 
 The below statements, `s1` and `s4`, from 
 [{fa}`fixture script`](script/overview/fixture1) are used throughout the 
 remaining examples in [this section](#statement-names). 
 ```{literalinclude} ../snippets/script/overview-statement-names.py
 :language: python
 :lines: 21-22
 :emphasize-lines: 4-5
 ```
 `````

 <hr class="sn-spacer-thick2">

 % (nm)
 ##### ***nm***
 
 ````{div} sn-def, sn-dedent-v-t-container, sn-linear-gradient-background, sn-thin-left-border-g
 
 <hr class="sn-blue-dotted">
 
  ```{div} sn-block-indented-h
  >{anchor}{delimiter}{desc}
  ```
  {attr}`~snowmobile.core.name.Name.anchor`\
  *what operation is a statement performing*<br>
  <p class="sn-def-p"><em>on what kind of object is it operating</em></p>
    
  {attr}`~snowmobile.core.cfg.script.Core.delimiter`
  ```{div} sn-multiline-def
  *a* <a class="sn-conf" href="./snowmobile_toml.html#script-patterns-core">
   <span>configured value</span>
  </a>
  *with which to delimit the {attr}`~snowmobile.core.name.Name.anchor` and
  {attr}`~snowmobile.core.name.Name.desc`*
  ```
    
  {attr}`~snowmobile.core.name.Name.desc`\
  *A free-form piece of text associated with the statement*
  
  <hr class="sn-blue-dotted sn-dedent-v-t-h-container">
  ````

% (-)
 ``````{tabbed} -
 :class-content: sn-light-shadow
 
 {attr}`~snowmobile.core.name.Name.nm` is the highest-level accessor
 for a {class}`~snowmobile.core.statement.Statement`.
 
 Its values for <a class="sn-local-fixture" href="./script.html#script-statement-nm">
  <span>s1 & s4</span>
 </a> (for example) can be inspected with:
 ```{literalinclude} ../snippets/script/overview-statement-names.py
 :language: python
 :lines: 24-25
 ```
 ``````
 
 ``````{tabbed} nm_pr
 :class-content: sn-light-shadow
 :class-label: sn-rm-background
 
 In determining the {attr}`~snowmobile.core.name.Name.nm` 
 for <a class="sn-local-fixture" href="./script.html#script-statement-nm">
  <span>s1</span> </a> specifically, [{fa}`fixture script`](script/overview/fixture1) 
 is considering the following two lines of [overview.sql](script/overview/fixture1):
  
 ```{literalinclude} ../snippets/script/overview.sql
 :language: sql
 :lines: 21-22
 ```
 
 ```{div} sn-post-code
 Each of these is the respective source for *provided* and *generated* 
 information about the statement called out 
 in <a class="sn-example" href="./script.html#script-note1">
 <span>Example: **nm**</span>
 </a>, the underlying values for which can be inspected in the same way:
 ```
 ```{literalinclude} ../snippets/script/overview-statement-names.py
 :language: python
 :lines: 36-46
 ```
 ``````
 

 <hr class="sn-spacer-thick2">
 
 % (anchor =======================================================)
 ##### ***anchor***
 
 ````{div} sn-def, sn-dedent-v-t-container, sn-linear-gradient-background
 
 <hr class="sn-blue-dotted">
 
 ```{div} sn-block-indented-h
 >{kw} {obj}
 ```
 {attr}`~snowmobile.core.name.Name.kw`\
 *the literal first sql keyword the statement contains*
 
 {attr}`~snowmobile.core.name.Name.obj`\
 *the in-warehouse object found in the first line of the statement* 
 
 <hr class="sn-blue-dotted sn-dedent-v-t-h-container">
 ````

 {attr}`~snowmobile.core.name.Name.anchor` represents all text to the left of
 the first {attr}`~snowmobile.core.cfg.script.Core.delimiter` and when 
 [*generated*](#statement-names) will fit the above structure to a varying
 degree depending on the sql being parsed and configurations in
 [](./snowmobile_toml.md). 

 ```{div} sn-pre-code-s
 For <a class="sn-local-fixture" href="./script.html#script-statement-nm">
  <span>s1 & s4</span>
 </a>:
 ```
 ```{literalinclude} ../snippets/script/overview-statement-names.py
 :language: python
 :lines: 30-31
 ```

 <hr class="sn-spacer-thick3">
 
 % (kw ===========================================================)
 (script-kw)=
 ##### ***kw***

 ``````{tabbed} -
 :class-content: sn-light-shadow

 {attr}`~snowmobile.core.name.Name.kw` is the literal first *keyword* 
 within the [command](https://docs.snowflake.com/en/sql-reference/sql-all.html)
 being executed by a statement's sql, determined by post-processing the tokens 
 returned from the {xref}`sqlparse.parse()` method.
 
 For <a class="sn-local-fixture" href="./script.html#script-statement-nm">
  <span>s1 & s4</span></a>:
 ```{literalinclude} ../snippets/script/overview-statement-names.py
 :language: python
 :lines: 59-60
 ```
 
 ``````

 ``````{tabbed} keyword-exceptions
 :class-content: sn-light-shadow
 
 The {ref}`keyword-exceptions <keyword-exceptions>` block in the
 {ref}`[sql] <sql.root>` section of 
 {ref}`snowmobile_ext.toml <file-contents-snowmobile-ext-toml>`
 enables
 specifying an alternate keyword for an identified keyword to use as its 
 {attr}`~snowmobile.core.name.Name.kw`:
 ```toml
    [sql.keyword-exceptions]
        "with" = "select"
 ```
 The default included above is the reason that the
 {attr}`~snowmobile.core.name.Name.kw` for both the following statements
 is `select` as opposed to `select` and `with` respectively:
 ```{literalinclude} ../snippets/script/keyword_exceptions.sql
 :language: sql
 :lines: 3-10
 ```
 ``````

 <hr class="sn-spacer-thick2">
 
 % (obj ==========================================================)
 (script-obj)=
 ##### ***obj***


 ``````{tabbed} -
 :class-content: sn-light-shadow

 {attr}`~snowmobile.core.name.Name.obj` is determined by a case-insensitive, 
 full ('word-boundaried') search through the **first** line of a statement's
 sql for a match within a pre-defined set of values.
 
 ``````

 ``````{tabbed} named-objects
 :class-content: sn-light-shadow
 
 The values for which a match is checked are configurable in the 
 {ref}`named-objects <named-objects>` block within the {ref}`[sql] <sql.root>` 
 section of [snowmobile_ext.toml](./snowmobile_toml.md#snowmobile_ext.toml),
 included below.
 
 Matching is peformed against values in the **literal** order as they are 
 configured in [snowmobile_ext.toml](./snowmobile_ext_toml) until a 
 match is found or the list is exhausted, enforcing that the object
 found cannot be equal to the {attr}`~snowmobile.core.name.Name.kw`
 for the statement.
 
 ```{code-block} toml
    named-objects = [
        # 'grant' statements
        "select",
        "all",
        "drop",

        # base objects
        "temp table",
        "transient table",
        "table",
        "view",
        "schema",
        "warehouse",
        "file format",

        # plural bases
        "tables",
        "views",
        "schemas",
    ]
 ```
 ````{admonition} Note
 :class: note, toggle, toggle-shown, sn-rm-t-m-code, sn-increase-margin-v-container

 The above order is as such so that table qualifiers for the following three 
 (types of) statements are reflected in the
 {attr}`~snowmobile.core.name.Name.obj` for each.
 
 <hr class="sn-spacer-thick">
 
 ```sql
 -- obj = 'table'
 create table any_table as 
 select 1 as any_col;
 
 -- obj = 'transient table'
 create transient table any_table2 as 
 select 1 as any_col;
 
 -- obj = 'temp table'
 create temp table any_table3 as 
 select 1 as any_col;
 ``` 

 ````
 ``````

 ``````{tabbed} generic-anchors
 :class-content: sn-light-shadow
 
 ```{admonition} TODO - MISSING
 :class: error
 Content goes here
 ```
 
 ``````

 <hr class="sn-spacer3">
 <hr class="sn-spacer2">
  
 % (delimiter ====================================================)
 (script-delimiter)=
 ##### ***delimiter***
 
 {attr}`~snowmobile.core.cfg.script.Core.delimiter` is a constant specified
 in the `description-delimiter` field within the
 {ref}`[script.patterns.core] section of snowmobile.toml<script.patterns.core>`,
 the value for which is accessible directly off
 <a class="fixture-sn" href="../index.html#fixture-sn"></a>: 
 
 ```{literalinclude} ../snippets/script/overview-statement-names.py
 :language: python
 :lines: 33-33
 ```
 
 <hr class="sn-spacer-thick2">
 
 % (desc =========================================================)
 (script-desc)=
 ##### ***desc***
  
 ````{tabbed} -
 Missing content
 ````

 </div>  
</div>
</body>

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

```{admonition} TODO - UNFINISHED DOCS - ALL CONTENT BELOW THIS POINT SHOULD NOT BE REFERENCED
 :class: error
 The below content is in a sandbox state and should not be referenced for usage details of [](#script).
```

### Tags
<hr class="sn-green-thick-g">

``````{div} sn-tabbed-section

 `````{tabbed} &nbsp;
 A tag contains an abitrary amount of information wrapped in a pre-defined opening/closing pattern.
 It can be associated with a {class}`~snowmobile.core.statement.Statement`, identified by its literal
 position relative to the statement's sql, or with a {class}`~snowmobile.core.cfg.script.Marker`,
 identified by its contents.

 The default pattern, highlighted in the below snippet from [snowmobile.toml](./snowmobile_toml.md),
 mirrors that of a standard sql block comment with an additional dash (`-`) on the inside of each component:
 ```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
 :class: sn-dedent-v-b-container-neg
 :language: toml
 :lineno-start: 64
 :lines: 64-66
 :emphasize-lines: 2-3
 ```
 `````

```````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

### Markers
<hr class="sn-green-thick-g">

``````{div} sn-tabbed-section

 `````{tabbed} Overview
 ```{admonition} TODO
 :class: error
 Missing
 ```
 `````

 `````{tabbed} +-
 MORE CONTENT GOES HERE
 `````

```````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

### Markup
<hr class="sn-green-thick-g">

``````{div} sn-tabbed-section

 `````{tabbed} &nbsp;

 ```{div} sn-hanging-p
 Using markup within a script enables:
 ```
 - Defining accessors for individual statements
 - Adding descriptive information to individual statements or to the script itself
 - Finer-grained control of the script's execution
 - Generating documentation and cleansed sql files from the working version of a script

 ```{div} sn-dedent-v-b-h
 {xref}`snowmobile` introduces two sql-compliant forms of adding markup to a sql file:
 ```
 1. [Tags](#tags) enable constructing collections of attributes amidst sql statements, including
 those directly associated with a particular statement
 2. [Markers](#markers) are a collection of attributes that are **not** associated with a
 particular statement

 The following sections outline the different ways that [](#tags) and [](#markers) are
 implemented and utilized.

 `````

```````

+++
<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

##### Single-Line Tags
<hr class="sn-green-thin-g">

``````{div} sn-tabbed-section

 `````{tabbed} Overview
 Single-line tags are the simplest form of [markup](#markup) and can be used to succinctly
 denote a name for a given statement.

 When a single-line string directly precedes a statement and is wrapped in [a valid open/close pattern](#tags),
 it will be recognized as the *provided* name ({attr}`~snowmobile.core.name.Name.nm_pr`) and used as
 the statement's name ({attr}`~snowmobile.core.name.Name.nm`) as opposed to its *generated*
 name  ({attr}`~snowmobile.core.name.Name.nm_ge`).
 `````

`````{tabbed} +

 Consider the sql file, *tags_single-line.sql*, containing two statements, the first and second of which have valid and invalid
 single-line tags respectively:
 ````{div} sn-inline-flex-container
 ```{literalinclude} ../snippets/script/tags_single-line.sql
 :language: sql
 :lines: 1-8
 ```
 ````

 Given a `path` to *tags_single-line.sql* and [{fa}`fixture sn`](../index.ipynb#fixture-sn), the following `script` can be created:
 ```python
 # Instantiate a Script from sql file
 script = snowmobile.Script(path=path, sn=sn)

 # Store individual statements for inspection
 s1, s2 = script(1), script(2)

 print(s1)        #> Statement('I am a tag')
 print(s1.nm_ge)  #> select data~s1
 print(s1.nm_pr)  #> I am a tag
 print(s1.nm)     #> I am a tag

 print(s2)        #> Statement('select data~s2')
 print(s2.nm_ge)  #> select data~s2
 print(s2.nm_pr)  #> ''
 print(s2.nm)     #> select data~s2
 ```

 ````{div} sn-indent-h-cell
  ```{admonition} Note
  :class: note, toggle, toggle-shown, sn-dedent-v-b-h-container

  The first statement has a valid tag directly preceding it, so its  name
  ({attr}`~snowmobile.core.name.Name.nm`) is populated by the *provided* name within
  the tag ({attr}`~snowmobile.core.name.Name.nm_pr`) as opposed to the name that was
  *generated* for the statement ({attr}`~snowmobile.core.name.Name.nm_ge`).

  The second statement does **not** have a valid tag directly preceding it, so
  its generated name, `select data~s2`, is used and the line
  `/*-I am a tag that isn't positioned correctly-*/` is ignored.
  ```
 ````
`````

``````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

##### Multi-Line Tags
<hr class="sn-green-thin-g">

```````{div} sn-tabbed-section

`````{tabbed} Overview
```{div} sn-hanging-p
 Multi-line tags provide a method of associating multiple attributes with
 a {class}`~snowmobile.core.statement.Statement` according to the following syntax:
- Attribute **names** must:
   1. Start at the beginning of a new line
   1. Have leading double underscores (`__`)
   1. End with a single colon (`:`)
- Attribute **values** have no restrictions except for several reserved attributes documented
  in the *reserved attributes* (LINK NEEDED) section below
```
`````

``````{tabbed} +
 In practice, this looks something like the following:
 ```{literalinclude} ../snippets/script/tags_multi-line.sql
 :language: sql
 :lines: 1-13
 ```

 `````{div} sn-dedent-v-t-container
  ````{admonition} Tip
  :class: tip, toggle, toggle-shown

  Trailing wildcards can be appended to attribute **names** to denote how information
  will be rendered in generated documentation; this is covered in [Patterns - Wildcards](#wildcards) below.
  ````
 `````
``````

```````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

#### Patterns
<hr class="sn-green-thick-g">

``````{div} sn-tabbed-section

 `````{tabbed} &nbsp;
 ```{admonition} TODO
 :class: error
 Missing
 ```
 `````

 `````{tabbed} +-
 MORE CONTENT GOES HERE
 `````

```````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

##### Core
<hr class="sn-green-thin-g">

``````{div} sn-tabbed-section

 `````{tabbed} Overview
 ```{admonition} TODO
 :class: error
 Missing
 ```
 `````

 `````{tabbed} +-
 MORE CONTENT GOES HERE
 `````

```````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">

##### Wildcards
<hr class="sn-green-thin-g">

``````{div} sn-tabbed-section

 `````{tabbed} Overview
 ```{admonition} TODO
 :class: error
 Missing
 ```
 `````

 `````{tabbed} +-
 MORE CONTENT GOES HERE
 `````

```````

<hr class="sn-green-rounded-g">
<hr class="sn-spacer-thick">


<style>
div.md-sidebar.md-sidebar--secondary :not(label.md-nav__title) {
    font-weight: 300;
}
</style>
