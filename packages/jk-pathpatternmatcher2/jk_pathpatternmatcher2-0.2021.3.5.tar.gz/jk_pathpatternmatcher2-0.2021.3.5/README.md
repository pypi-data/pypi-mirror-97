jk_pathpatternmatcher2
==========

Introduction
------------

This python module perform pattern matching tasks on paths.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-pathpatternmatcher2)
* [pypi.python.org](https://pypi.python.org/pypi/jk_pathpatternmatcher2)

Why this module?
----------------

In various applications it is mandatory to scan for files in directory trees. Then often some files found need to be included in a selection, other files need to be excluded from a selection.

For example such path matching is performed if you provide a file such as `.gitignore`. As you very likely will now this file is part of the `git` version control system. You specify paths in this file to exclude specific files and directories.

This module `jk_pathpatternmatcher2` now mimiks this behavior. It is intended to be used in conjunction with recursive file and directory iteration processes.

How this module works
---------------------

This module achieves path matching by compiling a pattern to a regular expression. Then this regular expression is used to check paths specified to the matcher.

Limitations of this module
--------------------------

For the moment this module is only capable of patterns applying to a normal path. By doing so only the path is in focus of any matching. Unlike in a `.gitignore` file this module does not distinguish between files or directories. Though such a feature might be implemented here in this module one day right now no distinction is made between files and directories per se: This module only knows one thing - paths - and therefore only matches paths (and not file paths or directory paths in particular).

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_pathpatternmatcher2
```

### Compile a pattern

Now a pattern can be compiled like this:

```python
PATTERN = "src/**/*.py"

pm = jk_pathpatternmatcher2.compilePattern(PATTERN)
```

### Use the matcher to check paths

After having compiled a pattern you can match paths. Example:

```python
PATH_TO_MATCH = "src/foo/bar.py"

if pm.match(PATH_TO_MATCH):
	print("We have a match!")
else:
	print("No match!")
```

### (Recursively) walking through directory trees

This module provides a function named `walk(..)` that will traverse directory trees.

In doing so `walk(..)` distinguishes between various directory entry types such as *files*, *directories*, *links* and *errors*. While files and directories do not need any further explanations, other aspects do:
* By default instead of failing with an exception an *error* is returned if a directory is not readable. Sometimes you just want to ignore such entries. (To control that behavior you can modify option `emitErrorEntries` accordingly.)
* By default soft links are recognized as links and returned as a *link*. This is imporant in directory traversals as you only want to follow "physical" members of a directory tree, not links. (Otherwise you might even end up in an endless loop if links are set inconveniently.)

But `walk(..)` has more features:
* `walk(..)` can return the root directory as an own directory entry if desired. In some applications this is very convenient therefore this can be configured by setting `emitBaseDirs` to `True`.
* The files returned can automatically be sorted by name.
* Without additional configuration `walk(..)` will return objects of type `Entry`. But you can derive from `Entry` and specify your own class: This way `walk(..)` will generate instances of your own type with all the methods you have defined in your class. So instead of getting `Entry` instances and maybe then in addition creating your own instances `walk(..)` will immediately provide *your* instances, therefore avoiding unnecessary loss of performance.

Here is an example of how a simple traversal can be performed:

```python
for e in walk(
		"/my/github/project",
		ignoreDirPathPatterns = [
			".git",
			".vscode",
		],
		emitDirs = False,
		emitBaseDirs = False,
	):
	print(e)
```

To learn more about the arguments for `walk(..)` see below in the API section.

API
------------------

### walk()

The function `walk(..)` will traverse directory trees. It is a *generatore* that will provide instances of `Entry` (or your own class). This function expectes the following arguments:

* `*dirPaths` : (required) Provide one or more (!) directories here to traverse.
* `str[] acceptDirPathPatterns` : (optional) If specfied these are patterns of directories to accept. Patterns are relative to the base directory traversed. If not specified all directories are accepted by default.
* `str[] acceptFilePathPatterns` : (optional) If specfied these are patterns of files to accept. Patterns are relative to the base directory traversed. If not specified all files are accepted by default.
* `str[] acceptLinkPathPatterns` : (optional) If specfied these are patterns of links to accept. Patterns are relative to the base directory traversed. If not specified all links are accepted by default.
* `str[] ignorePathPatterns` : (optional) If specfied these are patterns of files/directories/links to ignore. Patterns are relative to the base directory traversed.
* `str[] ignoreDirPathPatterns` : (optional) If specfied these are patterns of directories to ignore. Patterns are relative to the base directory traversed.
* `str[] ignoreFilePathPatterns` : (optional) If specfied these are patterns of files to ignore. Patterns are relative to the base directory traversed.
* `str[] ignoreLinkPathPatterns` : (optional) If specfied these are patterns of links to ignore. Patterns are relative to the base directory traversed.
* `bool emitDirs` : (optional) If `True` function `walk(..)` will emit directory entries. (This option is `True` by default.)
* `bool emitFiles` : (optional) If `True` function `walk(..)` will emit file entries. (This option is `True` by default.)
* `bool emitLinks` : (optional) If `True` function `walk(..)` will emit link entries. (This option is `True` by default.)
* `bool emitBaseDirs` : (optional) If `True` function `walk(..)` will emit traversal root directory entries. (This option is `True` by default.)
* `bool recursive` : (optional) If `True` function `walk(..)` will traverse recursively through the specified directory tree. (This option is `True` by default.)
* `bool sort` : (optional) If `True` function `walk(..)` will sort all entries returns by name. (This option is `True` by default.)
* `bool emitErrorEntries` : (optional) If `True` function `walk(..)` will emit error entries. If `false` exceptions are raised. (This option is `True` by default.)
* `type clazz` : (optional) If a class is specified here instances of *this* class are instantiated instead of `Entry`.

### Entry

Instances of `Entry` are returned by function `walk(..)`. Entries provide the following variables and/or properties:

* `str baseDirPath` : The (absolute) base directory path of the current traversal
* `str relPath` : The relative path of this file, directory or link
* `str typeID` : A type identifier:
	* "d" for directory
	* "f" for file
	* "l" for symbolic link
	* "e" for error in reading a directory
* `float mtime` : The last modification time of the file or link.
* `int uid` : The owning user
* `int gid` : The owning group
* `int size` : The size of the file.
* `Exception exception` : An exception object (if this is entry represents an error).
* `str dirPath` : This is the directory the current entry resides in, An absolute path is returned here.
* `str name` : The name of this entry
* `str linkText` : Returns the link text stored at the link if this is a link. If this entry is not a link `None` is returned.
* `str fullPath` : This is the absolute path of this entry.
* `bool isBaseDir` : `True` if this is a base directory (and base directory only).
* `bool isError` : `True` if this is an error entry.
* `str group` : The name of the owning group
* `str user` : The name of the owning user

Additionally `Entry` will provide the following methods:

* `void dump(str prefix = None, printFunc = None)` : Invoke `dump()` in order to quickly write the contents of this object so STDOUT.
* `str __repr__()`
* `str __str__()`

If you want `walk(..)` to provide instances of your own class instead of `Entry`, inherit from `Entry`. If you need to overwrite the constructor method your code will need to be prepared for those arguments:

* `str baseDirPath` : The (absolute) base directory path of the current traversal
* `str relPath` : The relative path of this file, directory or link
* `str typeID` : A type identifier:
	* "d" for directory
	* "f" for file
	* "l" for symbolic link
	* "e" for error in reading a directory
* `float mtime` : The last modification time of the file or link.
* `int uid` : The owning user
* `int gid` : The owning group
* `int size` : The size of the file.
* `Exception exception` : An exception object (if this is entry represents an error).


Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



