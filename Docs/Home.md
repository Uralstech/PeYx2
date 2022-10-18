# PeYx2 Wiki

## User's guide
### Toolbar
- **File menu**
    - New: Closes current file and clears window
    - Open: Opens existing file
    - Save: Saves current file to disk
    - Save-as: Copies contents of current file to new file
    - Quit: Closes PeYx2
- **Edit menu**
    - Cut: Cuts and copies selected text
    - Copy: Copies selected text
    - Paste: Pastes text at cursor position
    - Undo: Un-does last action
    - Redo: Re-does last un-done action
- **Theme menu**
    - Change theme: Opens popup to change editor theme
- **IDE menu**
    - Run: Executes command given in langConfig file for current file's type
    - List all langConfigs: Opens popup which displays all available langConfig files
- **Help**
    - PeYx2 wiki: Opens PeYx2 wiki page in browser
    - PeYx2 code: Opens PeYx2 GitHub page in browser
    - PeYx2 ReadMe: Opens PeYx2 README file
    - PeYx2 License: Opens PeYx2 LICENSE file

### Shortcuts
- **Ctrl+n: Create new file**
- **Ctrl+o: Open file**
- **Ctrl+s: Save file**
- **Ctrl+a+s: Save-as file**
- **Ctrl+z: Undo action**
- **Ctrl+y: Redo action**
- **F1: Open link to PeYx2 wiki**
- **F5: Run *any* file with a langConfig**

## Language extension guide
### How does a language extension work?
A language extension for PeYx2 (>1.1.0) is a JSON file with the command to execute to 'Run' the file and the syntax regex patterns.
Each extension's name is the file extension of the language it is for (eg: Python = .py.json, ezr = .ezr.json, C = .c.json) - But this may change in the future.
All extension JSONs must be stored under the 'configs' folder, which can be found where PeYx2 is installed.

Here's the structure of the JSON file; Remove the comments and try it yourself!
```
{
    // Version of JSON file
    // It isn't used anywhere now, but that may change in the future
    "version":"1.0.0",

    // Command to execute when 'Run' is called by user
    // When run, PeYx2 replaces ___FILE___ with the path to the current open file and
    // ___FOLDER___ with the path to the folder of the current open file
    "command":"echo Current file: ___FILE___, current dir: ___FOLDER___",

    // Syntaxe classes, from least to most priority
    "syntaxes":
        [
            {
                // Name for highlight tag, can be anything but should be unique
                "name":"number",

                // Regex expression
                "regex":"\\b[1234567890]*\\b",

                // Color of highlight
                "color":"#b9c0ff"
            },
            
            // The below class will override the one above, if there's a match
            {
                "name":"comment",
                "regex":"(COMMENT).*(ENDCOMMENT)",
                "color":"#008000"
            },
            
            // The below class will override all the above, if there's a match
            {
                "name":"string",
                "regex":"([\"'])((\\\\{2})*|(.*?[^\\\\](\\\\{2})*))\\1",
                "color":"#ffa264",

                // NEW for v1.3.0! Sub-syntaxes are applied to any of the main syntax classes!
                // For example, when PeYx2 finds text in the above 'string' syntax category,
                // it will check for the below sub-syntax 'string-escape' IN the 'string' text!
                // If found, PeYx2 will apply the below color and tag to the text
                "sub-syntaxes":
                [
                    {
                        "name":"string-escape",
                        "regex":"(\\\\'|\\\\\"|\\\\{2})",
                        "color":"#ff8000"

                        // NEW for v1.4.0! Sub-syntaxes can now have sub-sub-syntaxes! Check out
                        // .test.json to see how crazy it can get!
                    }

                    // Note: There can be more than one sub-syntax category, even though only one is shown here
                ]
            }
        ]
}
```