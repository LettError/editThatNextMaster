# coding: utf-8

import subprocess
import vanilla

"""
   Little window that shows a list of the currently selected glyphs,
   with different format options, with spaces, commas, slashes, or as unicode.
   v 1 April 17 2017 

    ǺÆÐØÞĐĦĲĿŁŊŒŦǻßæðøþđħĳŀłŋœŧ

    Aringacute AE Eth Oslash Thorn Dcroat Hbar IJ Ldot Lslash Eng OE Tbar aringacute germandbls ae eth oslash thorn dcroat hbar ij ldot lslash eng oe tbar

    Aringacute, AE, Eth, Oslash, Thorn, Dcroat, Hbar, IJ, Ldot, Lslash, Eng, OE, Tbar, aringacute, germandbls, ae, eth, oslash, thorn, dcroat, hbar, ij, ldot, lslash, eng, oe, tbar

    /Aringacute/AE/Eth/Oslash/Thorn/Dcroat/Hbar/IJ/Ldot/Lslash/Eng/OE/Tbar/aringacute/germandbls/ae/eth/oslash/thorn/dcroat/hbar/ij/ldot/lslash/eng/oe/tbar

"""


class NameCopier(object):
    maxTitleLength = 20
    def __init__(self):
        self.w = vanilla.Window((170, 240), "Copier")
        self.w.l = vanilla.List((0,0,0,-120), [])
        self.w.copyAsGlyphNames = vanilla.Button((2,-118,-2,20), "names", self.click, sizeStyle="small")
        self.w.copyAsGlyphNames.tag = "names"
        self.w.copyAsGlyphNamesComma = vanilla.Button((2,-96,-2,20), "names + comma", self.click, sizeStyle="small")
        self.w.copyAsGlyphNamesComma.tag = "comma"
        self.w.copyAsSlashedNames = vanilla.Button((2,-74,-2,20), "slash + name", self.click, sizeStyle="small")
        self.w.copyAsSlashedNames.tag = "slash"
        self.w.copyAsUnicode = vanilla.Button((2,-52,-2,20), "Unicode text", self.click, sizeStyle="small")
        self.w.copyAsUnicode.tag = "unicode"
        self.w.caption = vanilla.TextBox((2,-25,-2,20), "Copy selected names to clipboard", sizeStyle="mini")
        self.w.open()
        self.w.bind("became main", self.update)
        self.w.bind("became key", self.update)
        self.update()
    
    def update(self, sender=None):
        f = CurrentFont()
        names = f.selection
        self.w.l.set(names)
        if len(f.selection)==0:
            self.w.copyAsGlyphNames.setTitle("names")
            self.w.copyAsGlyphNamesComma.setTitle("names + comma")
            self.w.copyAsSlashedNames.setTitle("slash + name")
            self.w.copyAsUnicode.setTitle("Unicode text")
        else:
            self.w.copyAsGlyphNames.setTitle(" ".join(names)[:self.maxTitleLength]+u"…")
            self.w.copyAsGlyphNamesComma.setTitle(", ".join(names)[:self.maxTitleLength]+u"…")
            self.w.copyAsSlashedNames.setTitle("/"+"/".join(names)[:self.maxTitleLength]+u"…")
            self.w.copyAsUnicode.setTitle(self._namesToUnicode(f, names)[:self.maxTitleLength]+u"…")
    
    def _namesToUnicode(self, font, names):
        text = ""
        for n in names:
            if font[n].unicode is not None:
                text += unichr(font[n].unicode)
        if not text:
            return "[no unicodes]"
        return text
        
    def click(self, sender):
        t = sender.tag
        f = CurrentFont()
        names = f.selection
        copyable = ""
        if t == "names":
            copyable = " ".join(names)
        elif t == "comma":
            copyable = ", ".join(names)
        elif t == "slash":
            copyable = "/"+"/".join(names)
        elif t == "unicode":
            copyable = self._namesToUnicode(f, names)
        subprocess.Popen(['osascript', '-e', u'set the clipboard to ' + u'\"' + copyable + u'\"'])

if __name__ == "__main__":            
    n = NameCopier()
