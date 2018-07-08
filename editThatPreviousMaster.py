# menuTitle : Edit That Previous Master
# shortCut : command+shift+]

"""

    If you're editing masters or whatever
    and you want to switch to the same glyph in the other master
    and you spend a lot of time moving glyph windows around
    or you've had to divide your massive pixel real estate into small lots.

    Add this script to RF and wire it to a key command
    and then woosh woosh woosh cycle between the masters.
    The other script, "editThatNextMaster.py" wooshes the other direction.

    The order in which these scripts woosh through the fonts: alphabetically sorted filepath.

    With massive help from @typemytype
    @letterror
    20160930
    v6


"""

#from AppKit import *
import AppKit
from mojo.UI import *
from mojo.roboFont import CurrentFont, CurrentGlyph, AllFonts, OpenWindow, version

#import addSomeGlyphsWindow
#reload(addSomeGlyphsWindow)
#from addSomeGlyphsWindow import AddSomeGlyphsWindow

def copySelection(g):
    pointSelection = []
    compSelection = []
    for ci, c in enumerate(g.contours):
        for pi, p in enumerate(c.points):
            if p.selected:
                pointSelection.append((ci, pi))
    for compi, comp in enumerate(g.components):
        if comp.selected:
            compSelection.append(compi)
    return pointSelection, compSelection

def applySelection(g, pointSelection, compSelection):
    # reset current selected points
    for ci, c in enumerate(g.contours):
        c.selected = False
    for ci, c in enumerate(g.components):
        c.selected = False
    for ci, pi in pointSelection:
        if g.contours and len(g.contours) >= ci + 1:
            if len(g.contours[ci].points) >= pi + 1:
                g.contours[ci].points[pi].selected = True
    for ci in compSelection:
        if len(g.components) >= ci:
            g.components[ci].selected = True

def getCurrentFontAndWindowFlavor():
    """ Try to find what type the current window is and which font belongs to it."""
    windows = [w for w in AppKit.NSApp().orderedWindows() if w.isVisible()]
    skip = ["PreferencesWindow", "ScriptingWindow"]
    for window in windows:
        if hasattr(window, "windowName"):
            windowName = window.windowName()
            if windowName in skip:
                continue
            if hasattr(window, "document"):
                return window.document().font.path, windowName
    return None, None

def getGlyphWindowPosSize():
    w = CurrentGlyphWindow()
    if w is None:
        return
    x,y, width, height = w.window().getPosSize()
    settings = getGlyphViewDisplaySettings()
    view = w.getGlyphView()
    viewFrame = view.visibleRect()
    viewScale = w.getGlyphViewScale()
    return (x, y), (width, height), settings, viewFrame, viewScale

def setGlyphWindowPosSize(glyph, pos, size, animate=False, settings=None, viewFrame=None, viewScale=None, layerName=None):
    OpenGlyphWindow(glyph=glyph, newWindow=False)
    w = CurrentGlyphWindow()
    view = w.getGlyphView()
    w.window().setPosSize((pos[0], pos[1], size[0], size[1]), animate=animate)
    if viewScale is not None:
        w.setGlyphViewScale(viewScale)
    if viewFrame is not None:
        view.scrollRectToVisible_(viewFrame)
    if settings is not None:
        setGlyphViewDisplaySettings(settings)
    if layerName is not None:
        w.setLayer(layerName, toToolbar=True)

def setSpaceCenterWindowPosSize(font):
    w = CurrentSpaceCenterWindow()
    posSize = w.window().getPosSize()
    c = w.getSpaceCenter()
    rawText = c.getRaw()
    prefix = c.getPre()
    suffix = c.getAfter()
    size = c.getPointSize()
    w = OpenSpaceCenter(font, newWindow=False)
    new = CurrentSpaceCenterWindow()
    new.window().setPosSize(posSize)
    w.setRaw(rawText)
    w.setPre(prefix)
    w.setAfter(suffix)
    w.setPointSize(size)

def getOtherMaster(nextFont=True):
    cf = CurrentFont()
    orderedFonts = []
    fonts = {}
    for f in AllFonts():
        if f.path is None:
            fontSortKey = str(id(f))
        else:
            fontSortKey = f.path
        fonts[fontSortKey]=f
    sortedPaths = list(fonts.keys())
    sortedPaths.sort()

    for i in range(len(sortedPaths)):
        if cf.path == fonts[sortedPaths[i]].path:
            prev = fonts[sortedPaths[i-1]]
            nxt = fonts[sortedPaths[(i+1)%len(sortedPaths)]]
            if nextFont:
                return nxt
            else:
                return prev

def switch(direction=1):
    currentPath, windowType = getCurrentFontAndWindowFlavor()
    nextMaster = getOtherMaster(direction==1)
    f = CurrentFont()
    if windowType == "FontWindow":
        fontWindow = CurrentFontWindow()
        selectedGlyphs = f.selection
        currentFontWindowQuery =  fontWindow.getGlyphCollection().getQuery()
        print("currentFontWindowQuery", currentFontWindowQuery)
        selectedSmartList = fontWindow.fontOverview.views.smartList.getSelection()
        posSize = fontWindow.window().getPosSize()
        nextWindow = nextMaster.document().getMainWindow()
        nextMaster.selection = [s for s in selectedGlyphs if s in nextMaster]
        nextWindow.setPosSize(posSize)
        nextWindow.show()
        # set the selected smartlist
        fontWindow = CurrentFontWindow()
        try:
            fontWindow.fontOverview.views.smartList.setSelection(selectedSmartList)
            fontWindow.getGlyphCollection().setQuery(currentFontWindowQuery)    # sorts but does not fill it in the form
        except:
            pass
        #if f.path is not None and nextMaster.path is not None:
        #    hasOne = False
        #    OpenWindow(AddSomeGlyphsWindow, f, nextMaster)
    elif windowType == "SpaceCenter":
        setSpaceCenterWindowPosSize(nextMaster)
    elif windowType == "GlyphWindow":
        g = CurrentGlyph()
        selectedPoints, selectedComps = copySelection(g)
        currentMeasurements = g.naked().measurements
        if g is not None:
            # wrap possible UFO3 / fontparts objects
            if version[0] == '2':
                # RF 2.0
                currentLayerName = g.layer.name
            else:
                # RF 1.8.x
                currentLayerName = g.layerName
            if not g.name in nextMaster:
                #OpenWindow(AddSomeGlyphsWindow, f, nextMaster, g.name)
                NSBeep()
                return None
            nextGlyph = nextMaster[g.name]
            applySelection(nextGlyph, selectedPoints, selectedComps)
            nextGlyph.naked().measurements = currentMeasurements
            if nextGlyph is not None:
                rr = getGlyphWindowPosSize()
                if rr is not None:
                    p, s, settings, viewFrame, viewScale = rr
                    setGlyphWindowPosSize(nextGlyph, p, s, settings=settings, viewFrame=viewFrame, viewScale=viewScale, layerName=currentLayerName)
    elif windowType == "SingleFontWindow":
        print("SingleFontWindow!")
        fontWindow = CurrentFontWindow()
        selectedGlyphs = f.selection
        print("SingleFontWindow", fontWindow, selectedGlyphs)
        g = CurrentGlyph()
        if g is not None:
            selectedPoints, selectedComps = copySelection(g)
            currentMeasurements = g.naked().measurements
            print("SingleFontWindow", fontWindow, selectedGlyphs, g, selectedPoints, currentMeasurements)
        posSize = fontWindow.window().getPosSize()
        print("SingleFontWindow", posSize)
        nextWindow = nextMaster.document().getMainWindow()
        print("SingleFontWindow", nextWindow)
        nextWindow.setPosSize(posSize)
        nextWindow.show()

if __name__ == "__main__":
    switch(-1)
