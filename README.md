# editThatNextMaster
Script for RoboFont: makes switching glyph, space ord font windows super easy.

If you're editing masters or whatever and you want to switch to the same glyph in the other master
and you spend a lot of time moving glyph windows around or you've had to divide your
massive pixel real estate into small lots.

Add this script to RF and wire it to a key command and then woosh woosh woosh cycle between the masters.
* The script opens the window you're looking at, but for the next or previous font,
* Maintains window location and size.
* In glyph windows it preserves zoom and scroll position.
* In space windows it copies the preview text.

The other script, *editThatNextMaster.py* wooshes the other direction.
The order in which these scripts woosh through the fonts: alphabetically sorted filepath.

