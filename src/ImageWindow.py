import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ImageWindow(QMainWindow):
    '''
    Each window instance is used to display images and GIFs.
    '''
    imageMoved = pyqtSignal(QPoint)  # Signals b/w windows when an image is moved
    windowClosing = pyqtSignal(object)  # Signals b/w windows when any window closes

    def __init__(self, parent=None, imagePath=None):
        '''
        The settings and window is intialized as well the path of the image to be shown is assigned.
        '''
        super().__init__(parent)
        self.initUI()
        self.initSettings(imagePath)
        
    def setMoveWithWindow(self, state):
        self.moveWithWindow = state    

    def setKeepCentered(self, state):
        self.keepCentered = state        
    
    def initUI(self):
        '''
        The window is initialized randomly in a bounding box that's relative to the screen.
        The Image Label to hold the image is given the same size as the window.
        '''
        screen = QApplication.primaryScreen().size()
        screenWidth = screen.width()
        screenHeight = screen.height()
        
        self.setGeometry(random.randint(screenWidth//4, screenWidth//2),
                         random.randint(0, screenHeight//2),
                         int(screenWidth//2.5), int(screenHeight//2))
        
        self.setWindowIcon(QIcon('Files/logo.png'))
        self.setWindowTitle('Image Window')
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(self.rect())
    
    def initSettings(self, imagePath):
        '''
        The image path is assigned to the window as well as the update function to update the image position is initialized.
        The settings from the main window are initialized as well.
        '''
        self.currentImagePath = imagePath
        self.movie = None
        
        self.moveWithWindow = False
        self.keepCentered = False
        
        if imagePath:
            self.loadImage(imagePath, 1)        
        self.updateFunction(1)
        
    def updateFunction(self, timeStep):
        '''
        A timer to keep track and update the image's position until the window is moved.
        timeStep determines how often the update function is called and can be controlled by radio buttons in the main window.
        '''
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateImagePosition)
        self.timer.start(timeStep)    
        self.isImageMoved = False # Flag to check if the image window has been moved

    def moveEvent(self, event):
        '''
        Override the default move event to communicate the positon between different windows when an Image window is moved.
        It ensures that image remains at a consistent position relative to the other windows.
        '''
        if not self.moveWithWindow: # Return if 'Move With Window' has not been checked in the main window
            return
        super().moveEvent(event)
        if self.currentImagePath:
            globalPos = self.mapToGlobal(self.imageLabel.pos())
            self.imageMoved.emit(globalPos)  # Communicate the image position to different windows
            self.isImageMoved = True # Indicated that window has been moved manually

    def loadImage(self, imagePath, scaleFactor):
        '''
        Load the Image/GIF into the window and apply the scaleFactor.
        Decides between QMovie and QPixmap based on the type of image.
        If .gif it uses QMovie, else QPixmap.
        '''
        self.currentImagePath = imagePath
        if imagePath.lower().endswith('.gif'): 
            self.movie = QMovie(imagePath)
            self.movie.setScaledSize(self.imageLabel.size() * scaleFactor)             
            self.imageLabel.setMovie(self.movie)
            self.movie.start()  
            self.initScale = self.imageLabel.size() # Storing intial scale
        else:
            self.movie = None
            pixmap = QPixmap(imagePath)
            if not pixmap.isNull(): 
                scaledPixmap = pixmap.scaled(self.size() * scaleFactor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.imageLabel.setPixmap(scaledPixmap)
            self.initScale = self.size() # Storing initial scale

    def centerImage(self):
        '''
        Move the image/GIF to the center of the window.
        '''
        if self.movie: 
            rect = QRect(0, 0, self.movie.scaledSize().width(), self.movie.scaledSize().height())
        elif self.imageLabel.pixmap() and not self.imageLabel.pixmap().isNull():
            pixmap = self.imageLabel.pixmap()
            rect = pixmap.rect()
        else:
            return 

        rect.moveCenter(self.rect().center())
        self.imageLabel.setGeometry(rect)
    
    def updateImagePosition(self): 
        '''
        Used to update the position of image ensuring that the image remains  at a consistent position relative to the other windows.
        If the user has "Keep Centered" checked it aligns the images of the active window to the center and aligns images of other windows around it. 
        '''
        if self.isImageMoved: # Skip if window was moved, then moveEvent governs the image position            
            return

        if self.currentImagePath:
            activeWindow = QApplication.activeWindow()

            if self == activeWindow and self.keepCentered:
                self.centerImage()
                return

            if self.parent().imageWindows:
                if isinstance(activeWindow, ImageWindow) and self.keepCentered: 
                    refWindow = activeWindow #  Active window is the one that's selected and it governs the image positions
                else:
                    refWindow = self.parent().imageWindows[0] # If no window has been selected the first one governs the image positions
                globalPos = refWindow.mapToGlobal(refWindow.imageLabel.pos())
                localPos = self.mapFromGlobal(globalPos)
                self.imageLabel.move(localPos)
                self.update()
        
                
    def restartGif(self):
        '''Used to sync the GIF animation across all windows.'''
        if self.currentImagePath and self.currentImagePath.lower().endswith('.gif'):
            if self.movie:
                self.movie.stop()
                self.movie.start()
                
    def setScale(self, scaleFactor):
        '''
        Scale the image and its label based on the user input by using the scale slider.
        '''
        if self.movie and self.initScale:
            newSize = self.initScale * scaleFactor
            self.movie.setScaledSize(newSize)
        elif self.imageLabel.pixmap() and not self.imageLabel.pixmap().isNull() and self.initScale:
            newSize = self.initScale * scaleFactor
            scaledPixmap = QPixmap(self.currentImagePath).scaled(newSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imageLabel.setPixmap(scaledPixmap)
        self.imageLabel.setFixedSize(newSize)
        self.imageLabel.adjustSize()
        
    def closeEvent(self, event):
        '''
        Communicate to the main window that one image has been closed to remove it from the list of the imageWindows.
        '''
        self.windowClosing.emit(self) 
        super().closeEvent(event)