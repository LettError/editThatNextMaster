from mojo.UI import *
from mojo.roboFont import CurrentFont, CurrentGlyph, AllFonts, OpenWindow

def smartSetToSpaceCenter(f, direction=1):
    # make a guess which smartset is currently on display
    # based on the contents of the currentspace center
    # If we find one, take the next smartset
    # and set the space center to those names
    currentSC = CurrentSpaceCenter()
    if currentSC is None:
        OpenSpaceCenter(f, newWindow=False)
        currentSC = CurrentSpaceCenter()
    currentSpaceCenterContents = currentSC.get()
    smartSets = getSmartSets()
    foundOne = False
    for i in range(len(smartSets)):
        thisSet = smartSets[i]
        if thisSet.glyphNames == currentSpaceCenterContents:
            if direction > 0:
                idx = (i+1)%len(smartSets)
            else:
                idx = i-1
                if idx < 0:
                    idx = len(smartSets)-1
            nextSet = smartSets[idx]
            #print 'look at \"%s\"'%(nextSet.name)
            newNames = nextSet.glyphNames
            if newNames:
                currentSC.set(newNames)
                foundOne = True
                break

    if not foundOne:
        currentSC.set(smartSets[0].glyphNames)

def seeNextSet():
    f = CurrentFont()
    if f is not None:
        smartSetToSpaceCenter(f, 1)
    
def seePreviousSet():
    f = CurrentFont()
    if f is not None:
        smartSetToSpaceCenter(f, -1)

if __name__ == "__main__":
    seeNextSet()