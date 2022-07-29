import hou
import os

class StartFlipbook():
    def __init__(self):
        frameRange = hou.playbar.frameRange()
        self._startFrame = frameRange[0]
        self._endFrame = frameRange[1]
        self._version = 'v001'
        self._fileName = '$HIPNAME'
        self._directory = '$HIP/video'
        self._outputPath = '{0}/{1}/{2}.$F4.jpg'.format(self._directory, self._version, self._fileName)


    def begin(self):
        desktop = hou.ui.curDesktop()
        scene = desktop.paneTabOfType(hou.paneTabType.SceneViewer)

        flipbook_options = scene.flipbookSettings().stash()

        flipbook_options.frameRange((self._startFrame, self._endFrame))
        flipbook_options.output(self._outputPath)
        # flipbook_options.useResolution(False)

        scene.flipbook(scene.curViewport(), flipbook_options)



    @property
    def startFrame(self):
        return self._startFrame

    @property
    def endFrame(self):
        return self._endFrame
    @property
    def fileName(self):
        return self._fileName

    @property
    def version(self):
        return self._version

    @property
    def outputPath(self):
        return self._outputPath

    @property
    def directory(self):
        return self._directory

    @startFrame.setter
    def startFrame(self, startFrame):
        self._startFrame = startFrame

    @endFrame.setter
    def endFrame(self, endFrame):
        self._endFrame = endFrame

    @fileName.setter
    def fileName(self, fileName):
        self._fileName = fileName

    @version.setter
    def version(self, version):
        self._version = version

    @directory.setter
    def directory(self, directory):
        self._directory = directory
        self._outputPath = '{0}/{1}.$F4.jpg'.format(self._directory, self._fileName)




