TeXBriX
=======
A granular approach to LaTeX
----------------------------

Texbrix is a file standard that comes with useful tools for managing and exporting latex code

Installation
------------

Download it from PyPi:

```shell
pip install TeXBriX
```

TeXBriX uses Python 3.

What are TexBriX?
-----------------

TeXBriX are intended as both a note taking and a document writing system. A Brik is a small text document which can contain references to other briks.

### Intended Usecase
Instead of writing all of your notes in a subject into a long `.tex` file, like many people do, you instead write a Brik for each note, containing all relevant references. If the time comes to export a result in a paper (or many results in a book), you write a top-level Brik
referencing all results you want to include. TeXBriX then generates a `.tex` excerpt of your notes directory containing only the depencency tree of referenced Briks.


### Why not just use LaTeX' input?
Say document `a.tex` includes documents `b.tex` and `c.tex`, where the content of `d.tex` is a prerequisite for `c.tex`, as well as `b.tex`.
Since you want the content of `b.tex` and `c.tex` to be useable on their own, you incude `d.tex` in both of them. This results in the problem, that the content of `d.tex` is present twice in `a.tex`. TeXBriX makes all of those documents useable on their own while only importing prerequisites once, no matter whether they are used multiple times or not. (There is still a way to have content printed multiple times by explicitly placing it inside a document using \brikinsert).

Using TeXBriX, you would write the content of `a`, `b`, `c` and `d` in files `a.brik`, `b.brik`, `c.brik` and `d.brik`, respectively using the syntax stated below. If you want your final documents to have a special appearance, or make some makros a prerequisite of all BriKs in your project, you would write your own `template` file. You can then generate a LaTeX excerpt of your project containing only the content you specify with it's prerequisites by calling `texbrix`.

Usage
-----
### Command Line

To generate a LaTeX document from your TeXBriX structure use the command

```
texbrix <top TeXBriK>
```

This will by default use the `default_template` located in the src directory. If you would like to use another
template file instead (e.g. to define Math environments which should be expected to work in all BriX),
pass it via the optional `-template` Flag.

It is recommended to simplify the compilation process using Makefiles.

### Brik Structure
Currently there are two different types of Brix: Ordinary Brix and MathBrix
#### Ordinary Brix
Ordinary Brix are files with a `.brik` extension.
A TeXBriK has the following basic structure:
```LaTeX
\usepackage{<some LaTeX package required for this BriK's content>}
...
\usepackage{<more packages>}
\prerequisite{<some brik>}
...
\prerequisite{<some other brik>}
\begin{content}
This is ordinary \LaTeX.
\newline

...
\brikinsert{<yet another brik>}

...
\end{content}

```

Both the `\prerequisite{}` and the `\brikinsert{}` Commands take a file path relative to the BriK they are mentioned in, as well as absolute paths
(without the `.brik` or `.mbrik`-Postfix).
`\prerequisite{}` will make sure the mentioned BriK is included with all it's dependencies before the content, while
not generating any duplicates.
`\brikinsert{}` will insert the mentioned brik on the given position (with all not yet included dependencies) no matter whether
or not it has been previously used.

#### Mathbrix
Mathbrix are files with an `.mbrik` extension. They behave mostly like regular briks, with the exception that they can have multiple top-level `\begin{...} ... \end{...}` statements.
These are intended to be used for *theorem*, *proof*, *definition*, etc. Blocks.

In the future mathbriks will allow you to state theorems etc. without printing their proofs (e.g. for short excerpts).

### Template File
You can write the general structure of your final LaTeX document in a template file (passed to TeXBriX via the `-template` argument).
Here you should use the following placeholders:

| Placeholder | Meaning |
| ----------- | ------- |
| $packages   | In the place where you want the LaTeX imports to be inserted |
| $content    | Where you want the BriK's content to be |


Other tools
---------------------------
### VSCodium
Add to settings.json

```json
"files.associations": {
	"*.brik": "latex",
        "*.texbrik": "latex
}
```
If you use the `latex-workshop` extension:
```json
"latex-workshop.latex.tools":[
	{
		"name": "texbrix",
		"command": "texbrix",
		"args": [
			"%DOC%.brik"
		],
		"env": {}
	},
	{
		"name": "pdflatex",
		"command": "pdflatex",
		"args": [
			"-synctex=1",
			"-interaction=nonstopmode",
			"-file-line-error",
			"%DOC%.tex"
		],
		"env": {}
	}
]
"latex-workshop.latex.recipes":[
	{
		"name": "texbrix then pdflatex",
		"tools": [
			"texbrix",
			"pdflatex"
		]
	}
]

```
