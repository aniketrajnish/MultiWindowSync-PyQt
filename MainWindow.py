import random
from fileinput import filename
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ImageWindow import ImageWindow

class MainWindow(QMainWindow):
    '''
    This class manages all the image windows and governs various settings, window count, and the image to be applied on the image windows.
    '''
    def __init__(self):
        '''
        Initialize the UI of the window, assign the default path of the images, and intialize an array to store all the image windows.
        '''
        super().__init__()        
        self.imageWindows = []        
        self.currentImagePath = 'Files/tess.gif'
        self.initUI()
        
    def initUI(self):
        '''
        Initialize the window settings, layout and the UI components.
        '''
        self.initWindow()        
        self.initLayout()
        self.initComponents()       
        
    def initWindow(self):
        '''
        The main window settings and properties are assigned here.
        The winow location is kept relative to the screen size and the size of the window is goverened by the layout itself.
        '''
        screen = QApplication.primaryScreen().size()
        self.screenWidth = screen.width()
        self.screenHeight = screen.height()
        
        self.move(self.screenWidth // 10, self.screenHeight // 10)
        
        self.setWindowIcon(QIcon('Files/logo.png'))
        self.setWindowTitle('Image Window Manager')
        
    def initLayout(self):
        '''
        The layouts that make up the window are intialized here. This includes:
        - Central Layout (Widget)
        - Left Side Layout (Controls)
        - Right Side Layout (Image Display)
        - Button Layout (Bottom Buttons)
        '''        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)

        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSizeConstraint(QLayout.SetFixedSize)
      
        self.rightLayout = QVBoxLayout()
        
        self.btnLayout = QHBoxLayout()
        self.btnLayout.addStretch(1)
    
    def initComponents(self):
        '''
        Initialize all the UI components that are defined below.
        '''
        self.initMenuBar()        
        self.initStatusBar()
        self.initToolBar()
        self.initScaleSlider()
        self.initCheckBoxes()
        self.initRadioBtns()
        self.initImageDisplay()
        self.initBottomButtons()
        
    def initMenuBar(self):
        '''
        Initializes a Menu Bar with options to load an image/gif and close all the windows that are open.
        '''
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        
        loadAction = QAction('&Open Image/GIF', self)
        loadAction.triggered.connect(self.openFileDialog)
        fileMenu.addAction(loadAction)
        
        closeAllAction = QAction('&Close All Windows', self)
        closeAllAction.triggered.connect(self.closeAllImageWindows)
        fileMenu.addAction(closeAllAction)
        
    def initStatusBar(self):
        '''
        Initalize a Status Bar to message about display different operations in the bottom of the screen.
        '''
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Open a new window!', 5000)
        
    def initToolBar(self):
        '''
        Initialize a Tool Bar with options to randomize the settings and open multiple windows based on the number of window specified.
        '''
        toolBar = QToolBar('Tool Bar', self)
        self.addToolBar(Qt.TopToolBarArea, toolBar)
        
        randomizeAction = QAction(QIcon('Files/randomize.png'), 'Randomize', self)
        randomizeAction.triggered.connect(self.randomizeSettings)
        toolBar.addAction(randomizeAction)
        
        self.numWindowsInput = QLineEdit(self)
        self.numWindowsInput.setValidator(QIntValidator(1, 99))
        self.numWindowsInput.setText('5')
        self.numWindowsInput.setFixedWidth(self.screenWidth // 50)  
        toolBar.addWidget(self.numWindowsInput)

        openWindowsBtn = QPushButton('Open Windows', self)
        openWindowsBtn.clicked.connect(self.openMultipleWindows)
        toolBar.addWidget(openWindowsBtn)
        
    def initScaleSlider(self):
        '''
        Initialize a Slider for scaling the image.
        The values are scaled 100 folds to enable fine control and each step for a slider is an integer.
        '''
        self.scaleLabel = QLabel('Scale Image')
        self.scaleSlider = QSlider(Qt.Horizontal)
        
        self.scaleSlider.setFixedSize(self.screenWidth // 15, self.screenHeight // 50)
        self.scaleSlider.setRange(25, 400) # Represents .25 to 4
        self.scaleSlider.setValue(100)  # Represents 1
        self.scaleSlider.valueChanged.connect(self.updateImageScale)
        
        self.leftLayout.addWidget(self.scaleLabel)
        self.leftLayout.addWidget(self.scaleSlider)
    
    def initCheckBoxes(self):
        '''
        Initilize checkboxes for Image Settings.
        '''
        self.imageSettLabel = QLabel('Image Settings')
        self.moveWWindowCb = QCheckBox('Move with window')
        self.keepCenteredCb = QCheckBox('Keep Centered')
        
        self.leftLayout.addWidget(self.imageSettLabel)
        self.leftLayout.addWidget(self.moveWWindowCb)
        self.leftLayout.addWidget(self.keepCenteredCb)   
        
        self.moveWWindowCb.clicked.connect(self.updateImageSettings)
        self.keepCenteredCb.clicked.connect(self.updateImageSettings)
        self.moveWWindowCb.setChecked(True) # Default
        
    def initRadioBtns(self):
        '''
        Initialize radio buttons to control the refresh rate of the update function of Image Windows.
        '''
        self.refreshRateLabel = QLabel('Refresh Rate')
        self.slowR = QRadioButton('Slow')
        self.medR = QRadioButton('Medium')
        self.fastR = QRadioButton('Fast')
        self.fastR.setChecked(True) # Default
        
        self.slowR.clicked.connect(self.updateTimeStep)
        self.medR.clicked.connect(self.updateTimeStep)
        self.fastR.clicked.connect(self.updateTimeStep)       

        self.leftLayout.addWidget(self.refreshRateLabel)
        self.leftLayout.addWidget(self.slowR)
        self.leftLayout.addWidget(self.medR)
        self.leftLayout.addWidget(self.fastR)
        
    def initImageDisplay(self):
        '''
        Initialize area for displaying image that will be diplayed in all the Image Windows.
        '''
        self.imgDisp = QLabel('Display the image here')
        self.imgDisp.setAlignment(Qt.AlignCenter)        
        self.rightLayout.addWidget(self.imgDisp)
    
    def initBottomButtons(self):
        '''
        Initialize buttons to open a new Image Window or Quit the application.
        '''
        self.newWindowBtn = QPushButton('Open Image Window')
        self.newWindowBtn.clicked.connect(self.openNewWindow)
        
        self.quitBtn = QPushButton('Quit')
        self.quitBtn.clicked.connect(self.confirmQuit)
        
        self.btnLayout.addWidget(self.newWindowBtn)
        self.btnLayout.addWidget(self.quitBtn)
        self.leftLayout.addStretch(1)
        
        self.mainLayout.addLayout(self.leftLayout, 1)
        self.mainLayout.addLayout(self.rightLayout, 1) 
        self.rightLayout.addLayout(self.btnLayout) 
        
    def openFileDialog(self):
        '''
        Opens File Explorer to choose image/GIF files.
        The selected image is displayed in Image Windows.
        '''
        self.statusBar.showMessage('Choosing a new Image/GIF', 5000)
        
        options = QFileDialog.Options()    
        fileName, i = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.jpg;*.jpeg;*.png;*.bmp;*.gif)', options=options)
        
        if fileName:
            self.currentImagePath = fileName
            
        self.updateAllWindows()

    def updateAllWindows(self):
        '''
        Updates image preview in the main window and loads the image in all image windows.
        '''
        self.displayImagePreview()
        
        for window in self.imageWindows:
            window.loadImage(self.currentImagePath, self.scaleSlider.value() / 100) # Scale = 1

    def openNewWindow(self):
        '''
        Opens a new image window as a child of the main window.
        Connects signals for image position and window closing.
        '''
        newWindow = ImageWindow(self)
        
        newWindow.imageMoved.connect(self.onImageMoved)
        newWindow.windowClosing.connect(self.removeImageWindow)
        
        newWindow.show()
        
        self.imageWindows.append(newWindow)
        
        newWindow.loadImage(self.currentImagePath, self.scaleSlider.value() / 100)
        
        self.statusBar.showMessage('Opened new window', 3000)
        
        for window in self.imageWindows: # Sync GIF
            window.restartGif()
            
        self.displayImagePreview()
        
        self.updateAllSettings()

    def onImageMoved(self, globalPos):
        '''
        Handles communication b/w windows on moving a window and updates the position of the images in other windows.
        '''
        senderWindow = self.sender()
        
        for window in self.imageWindows:
            if window is not senderWindow:
                localPos = window.mapFromGlobal(globalPos)
                window.imageLabel.move(localPos)
                window.update()  # Refresh
                window.isImageMoved = False    
    
    def displayImagePreview(self):
        '''
        Display current image in  image display area and scale the image to fit the display area while maintaining aspect ratio.
        '''
        pixmap = QPixmap(self.currentImagePath)
    
        if not pixmap.isNull():
            scaledPixmap = pixmap.scaled(self.imgDisp.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
            self.imgDisp.setPixmap(scaledPixmap)
            self.imgDisp.adjustSize() 
        else:
            self.statusBar.showMessage('Failed to load image.', 5000)
            
    def updateAllSettings(self):
        '''
        Single method to update all settings from the Main Window.
        '''
        self.updateImageScale()
        self.updateTimeStep()
        self.updateImageSettings() 
        
    def updateTimeStep(self):
        '''
        Update refresh rate of Update Function in the windows based on the radio button selected.
        '''
        timeStep = 0
        if self.fastR.isChecked():
            timeStep = 1
        elif self.medR.isChecked():
            timeStep = 100
        else:  
            timeStep = 2000
        
        for window in self.imageWindows:
            window.updateFunction(timeStep)
        
    def updateImageScale(self):
        '''
        Apply scale value from the slider to the all the image and their labels in the image window.
        '''
        scaleFactor = self.scaleSlider.value() / 100 # Scale = 1 
        
        for window in self.imageWindows:
            window.setScale(scaleFactor) 
            
        self.statusBar.showMessage('Scale Value Assigned', 5000)
            
    def updateImageSettings(self):
        '''
        Apply settings from the checkboxes. 
        Give message in the status bar about one of the bugs that we're currently facing.
        '''
        moveWithWindow = self.moveWWindowCb.isChecked()
        keepCentered = self.keepCenteredCb.isChecked()
        
        for window in self.imageWindows:
            window.setMoveWithWindow(moveWithWindow)
            window.setKeepCentered(keepCentered)
            
        if (moveWithWindow ==  False):
            self.statusBar.showMessage('Parent window still moves the image for ref to other windows', 5000) # To be fixed
            
    def randomizeSettings(self):
        '''
        Randomize all the Main Window Settings.
        '''
        self.scaleSlider.setValue(random.randint(25, 400))
        
        self.moveWWindowCb.setChecked(random.choice([True, False]))
        self.keepCenteredCb.setChecked(random.choice([True, False]))
        
        random.choice([self.slowR, self.medR, self.fastR]).setChecked(True)
        
        for i in range(random.randint(2, 10)):  
            self.openNewWindow()
        
        self.updateAllSettings()

    def openMultipleWindows(self):
        '''
        Open multiple mindows specified in the toolbar.
        '''
        numWindows = int(self.numWindowsInput.text())
        
        for i in range(numWindows):
            self.openNewWindow()
            
        self.statusBar.showMessage('Opened {} windows!'.format(numWindows), 5000)
              
    def closeAllImageWindows(self):
        '''
        Close all the windows and remove their reference in the Main Window.
        '''
        windowsToClose = self.imageWindows.copy()
        
        for window in windowsToClose:
            window.close()
            
        self.imageWindows.clear()
        
    def removeImageWindow(self, window):
        '''
        Remove closed window based on signals from the closing window.
        '''
        if window in self.imageWindows:
            self.imageWindows.remove(window)
        
    def confirmQuit(self):
        '''
        Quit Window. You can't see me :-]
        '''
        self.statusBar.showMessage('Quitting', 5000)
        reply = QMessageBox()
        reply.setWindowIcon(QIcon('Files/johnwacenwa.png'))
        reply.setIcon(QMessageBox.Question)
        reply.setText('Are you sure about that?')
        reply.setWindowTitle('Confirm Quit')
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnVal = reply.exec_()
        
        if returnVal == QMessageBox.Yes:
            QApplication.instance().quit()