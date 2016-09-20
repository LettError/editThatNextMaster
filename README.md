# editThatNextMaster
Script for RoboFont that makes switching glyph, space or font windows super easy.

If you're editing masters or whatever and you want to switch to the same glyph in the other master
and you spend a lot of time moving glyph windows around or you've had to divide your
massive pixel real estate into small lots.

Add these scripts to RF and wire them to a key command and then ⏩ or ⏪ cycle between the masters.

* *editThatNextMaster.py* wooshes one way.
* *editThatPreviousMaster.py* wooshes the other way.

RoboFont key commands can be added in the .py tab of the [Preferences window.](http://doc.robofont.com/documentation/workspace/preferences/python/) (link to RoboFont docs)

* The script opens the window you're looking at, but for the next or previous font,
* Maintains window location and size.
* Between glyph windows it preserves zoom and scroll position.
* Between space windows it copies the preview text and preview font size.
* Between font windows it maintains glyph selection, current sort query and smart group selection.

The order in which these scripts woosh through the fonts: alphabetically sorted filepaths.

Notes
-----

* Does not work in single window mode because single window mode.
* Script windows, vanilla windows, preference window etc. are excluded from all the wooshing fun.
