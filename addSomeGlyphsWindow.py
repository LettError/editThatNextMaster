# coding=utf-8
# menuTitle : Add Some Glyphs

import os
import vanilla
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.roboFont import CurrentFont, CurrentGlyph, AllFonts, OpenWindow
from mojo.UI import *

"""

    Suppose we hop from one font to the next and there is one or more glyphs missing.
    Show this window to make them quickly.
"""

checkSymbol = u"✔️"

class AddSomeGlyphsWindow(BaseWindowController):
    _windowName = u"Want some glyphs?"
    def __init__(self, src, dst, glyphName=None):
        self.src = src
        self.dst = dst
        self.glyphName = glyphName
        self.candidates = []
        if glyphName is None:
            # we're switching between fonts, let's see what we need
            srcNames = set(self.src.keys())
            dstNames = set(self.dst.keys())
            missing = srcNames-dstNames
            for name in list(missing):
                comps = ""
                if len(self.src[name].components) > 0:
                    comps = checkSymbol
                uniValue = ''
                if self.src[name].unicode is not None:
                    uniValue = '%2X'%self.src[name].unicode
                self.addGlyph(glyphName=name, width = self.src[name].width, hasComponents=comps, unicodeValue=uniValue)
        else:
            if glyphName in src and glyphName in dst:
                # we're good
                return
            if glyphName not in dst:
                comps = ""
                if len(self.src[glyphName].components) > 0:
                    comps = checkSymbol
                unicodeValue = self.src[glyphName].unicode
                self.addGlyph(glyphName=glyphName, width = self.src[glyphName].width, hasComponents=comps, unicodeValue=unicodeValue)
        if len(self.candidates)==0:
            # no need to make this window
            #print "no glyphs missing"
            return
        self.w = vanilla.Window((500, 300), self._windowName)
        columnDescriptions = [
            {'title': 'Glyphname', 'key': 'glyphName', 'width':200},
            {'title': 'Unicode', 'key': 'unicodeValue', 'width':80},
            {'title': 'Width', 'key': 'width', 'width':100},
            {'title': 'Components', 'key': 'components', 'width':100},
            ]
        self.candidates.sort()
        self.w.l = vanilla.List((0,29,-0,-100), self.candidates, columnDescriptions=columnDescriptions)
        self.w.l.setSelection(range(len(self.candidates)))
        
        dstName = srcName = "Untitled"
        if self.src.path is not None:
            srcName = os.path.basename(self.src.path)
        if self.dst.path is not None:
            dstName = os.path.basename(self.dst.path)
        self.w.c = vanilla.TextBox((5, 5, -5, 20), "These glyphs are in %s but not in %s"%(srcName, dstName))
        
        self.w.copyCompsCheck = vanilla.CheckBox((10, -60, 200, 20), "Copy the glyph", value=True, callback=self.updateButtonTitle)
        
        self.w.makeButton = vanilla.Button((10, -30, -10, 20), "", callback=self.callbackMakeSelected)
        self.w.setDefaultButton(self.w.makeButton)
        self.updateButtonTitle()
        self.setUpBaseWindowBehavior()
        self.w.open()
    
    def updateButtonTitle(self, sender=None):
        title = "Make the missing glyphs"
        if self.w.copyCompsCheck.get():
            title += " and copy the glyph."
        self.w.makeButton.setTitle(title)
        
    def addGlyph(self, glyphName, width, hasComponents, unicodeValue):
        self.candidates.append(dict(glyphName=glyphName, width=width, components=hasComponents, unicodeValue=unicodeValue))
    
    def callbackMakeSelected(self, sender):
        # make these glyphs, close window
        copyComps = self.w.copyCompsCheck.get()
        selectNames = []
        for index in self.w.l.getSelection():
            glyphName = self.candidates[index]['glyphName']
            selectNames.append(glyphName)
            self.dst.newGlyph(glyphName)
            g = self.dst[glyphName]
            bg = g.getLayer("background")
            g.appendGlyph(self.src[glyphName])
            bg.appendGlyph(self.src[glyphName])
            self.dst[glyphName].unicode = self.src[glyphName].unicode
            self.dst[glyphName].width = self.guessWidth(glyphName)
        self.w.close()
    
    def guessWidth(self, glyphName):
        """ A tiny bit of speculative programming here:
            Suppose that we're about to copy a glyph
            and it has components
            and its width is the same as one of the components,
            then we can make the new glyph also the same width
        """
        possible = []
        for c in self.src[glyphName].components:
            if not c.baseGlyph in self.src:
                continue
            w = self.src[c.baseGlyph].width
            if w == self.src[glyphName].width:
                possible.append(c.baseGlyph)
        if possible:
            guess = self.dst[possible[0]].width
            # we're guessing this is good
            return guess
        # return the original width
        return self.src[glyphName].width
    
if __name__ == "__main__":
    fonts = AllFonts()
    fonts.reverse()
    if len(fonts)==2:
        if fonts[0].path is not None and fonts[1].path is not None:
            OpenWindow(AddSomeGlyphsWindow, fonts[0], fonts[1])

