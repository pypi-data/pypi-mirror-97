<!--- Copyright (c) 2021 Valentin Weber

    This file is part of the software mendeley-watchdog.

    The software is licensed under the European Union Public License
    (EUPL) version 1.2 or later. You should have received a copy of
    the english license text with the software. For your rights and
    obligations under this license refer to the file LICENSE or visit
    https://joinup.ec.europa.eu/community/eupl/og_page/eupl to view
    official translations of the licence in another language of the EU.
--->

# Entry Point: Mendeley Watchdog

```
usage: mendeley-watchdog [-h] [--mendeley-bibtex] bibfile mirrored

watch *.bib file and mirror its contents after modification

positional arguments:
  bibfile             name of mendeley bib file to watch
  mirrored            path to file Mendeley bib file mirrored will be mirrored to

optional arguments:
  -h, --help          show this help message and exit
  --mendeley-bibtex   path to directory in which Mendeley stores BibTeX files

--mendeley-bibtex defaults to the value of the environment variable MENDELEY_BIBTEX_DIR.
If that isn't set and no value is provided the program will exit.
```

## Usage Examples
```
mendeley-watchdog "my_bib_file" "my-latex-project/references.bib"
```
In this case the Watchdog will look for a file called `my_bib_file` in the
directory returned by calling `os.getenv("MENDELEY_BIBTEX_DIR")`. Whenever a
change in the last modification date of the source file was noticed (it checks
every second) its contents are be written to the file `references.bib` in the
subdirectory `my-latex-project` of the current working directory. The target
directory must exist and the file must be writable. Otherwise the process will
exit.

**WARNING** Note that the source file has no file extension while the
            destination file does. The software appends the `.bib` extension to
            either of the provided filenames if a check determined that they
            have different one (or none at all). This behavior my be changed in
            future version so I recommend specifying the extension.

If the environment variable `MENDELEY_BIBTEX_DIR` isn't set or its value
doesn't point to a directory the application will also exit. This can be
avoided by calling like this:
```
mendeley-watchdog --mendeley-bibtex . "my_bib_file" "my-latex-project/references.bib"
```
By adding `--mendeley-bibtex .` the Watchdog now attempts to find the file in
the current working directory (`.` could have been a path to any existing
directory), everything else behaves the same as in the example above. Be aware
that calling this way will not use the value of `MENDELEY_BIBTEX_DIR` even if
it is set.

## Monitor a Bib File While Working on a Project in VS Code
**WARNING:**  I recommend using Version Control for the project to make sure any
              unintended changes can be reversed easily. I do not take 
              responsibility for any data loss when using this software.

When added to the `tasks` array in the `tasks.json` file as described in the
[VS Code Tasks Documentation][vscode-tasks] the following configuration launches
mendeley-watchdog (assuming it's exposed on PATH) as soon as the workspace is opened:
```
{
    "label": "Mirror hhn-it-systems",
    "type": "shell",
    "command": "mendeley-watchdog",
    "runOptions": {"runOn": "folderOpen"},
    "args": [
        "--mendeley-bibtex",
        "'R:\\Mendeley Library\\.bib'",
        "hhn-it-systems",
        "resources/references.bib"
    ]
}
```
The first time the workspace is opened VS Code will ask you whether you want
to allow the task to run automatically. The confirmation is only needed once.

The label can be changed to whatever string should be used as the task's name
by VS Code when displaying it.

The `args` array contains the arguments that should be used when executing the
specified `command` as introduced in the [Usage Examples][toc-usage-examples]
above. A special considerations must be made when using an argument that
contains spaces (which can easily happen when dealing with filepaths).

As per the [VS Code Custom Task Documentation][vscode-tasks-custom] arguments
that contain spaces need to be quoted just like on a regular command line, e.g.:
`"'R:\\Mendeley Library\\.bib'"`. 

Don't change `runOptions.runOn` unless the task should not run automatically as
soon as the workspace is opened. It can always be started manually.

[toc-usage-examples]: #usage-examples
[vscode-tasks]: https://code.visualstudio.com/docs/editor/tasks
[vscode-tasks-custom]: https://code.visualstudio.com/docs/editor/tasks#_custom-tasks
