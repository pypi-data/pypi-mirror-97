# vroParse 
## vRO XML Package Parser

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Support These Projects](#support-these-projects)

## Overview
`vroParse` is created by `Jim Sadlek`.

`vroParse` is an addendum to the vRealize Build Tools and Developer Tools, and is a Python package with two executable commands, `parsevro` and `updatevro`. 

This project parses code embedded in scriptable tasks from out of Workflow XML, saves them as discrete files for editing and SCC, and imports the edits back into XML for inclusion in vRO Package updates.
## Setup

```console
pip install vroParse
```

The package is hosted on **PyPi**.  If you do not have external access to the Internet, 
you will need to do a local install on your system.

To do that, obtain a clone of this repo to your local system. then, make sure
to run the `setup.py` file, so you can install any dependencies you may need. To
run the `setup.py` file, run the following command in your terminal.

`python(3) setup.py install --record files`

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the `parsevro` and `updatevro` commands.

To manually remove this package run `rm $(cat files)`

## Usage

Here is a simple example of using the `vroParse` package to parse vRO XML package files for Scriptable Tasks' element code, and then update XML with edited code, from within Visual Studio Code or some other code editor outside of vRO.

After performing a `mvn vro:pull` operation, run this from the root folder:
`parsevro`

After performing a `mvn vrealize:push` operation, run this from the root folder:
`updatevro`

## Other Projects

**vRealize Build Tools:**
[vRealize Build Tools](https://flings.vmware.com/vrealize-build-tools) is a Vmware Fling that provides tools to development and release teams implementing solutions based on vRealize Automation (vRA) and vRealize Orchestrator (vRO).

**vRealize Developer Tools:**
[vRealize Developer Tools](https://github.com/vmware/vrealize-developer-tools) is a Visual Studio Code Extension available on GitHub that provides code intelligence features and enables a more developer-friendly experience when creating vRealize content.
