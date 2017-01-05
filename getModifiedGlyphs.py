import os
import subprocess
import xml.etree.ElementTree as ET

"""
    
    For UFOs that are in a git repository, this RF script
    will find which glyphs have been modified.

"""

def getModifiedGlyphNames(f):
    cwd = os.getcwd()
    names = []
    if f.path is not None:
        glyphsPath = os.path.join(f.path, "glyphs") 
        print glyphsPath
        os.chdir(glyphsPath)
        p = subprocess.check_output(["git", "diff", "--name-only", glyphsPath])
        for path in p.split("\n"):
            glifPath = os.path.join(glyphsPath, os.path.basename(path))
            if os.path.isdir(glifPath):
                continue
            tree = ET.parse(glifPath)
            root = tree.getroot()
            name = root.attrib.get('name')
            if name is not None:
                names.append(name)
    os.chdir(cwd)
    return names

if __name__ == "__main__":
    # add your own hooks here.
    f = CurrentFont()
    modified = getModifiedGlyphNames(f)
    for name in modified:
        f[name].mark = 1, 0,0,0.25
    f.selection = modified