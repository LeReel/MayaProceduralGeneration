import random, math, sys, os
from maya import cmds
from PySide2 import QtCore, QtGui, QtWidgets

class myRangeSlider(QtWidgets.QWidget):
    def __init__(self, parent=None, labelText="", min=0, max=10):
        super().__init__(parent)

        self.sliderLayout = QtWidgets.QVBoxLayout(self)

        self.sliderLayout.addWidget(QtWidgets.QLabel(labelText))

        self.minSlider = mySliderLayout()
        self.minSlider.getSlider().setMinimum(min)
        self.minSlider.getSlider().setMaximum(max)
        self.sliderLayout.addLayout(self.minSlider)

        self.maxSlider = mySliderLayout()
        self.maxSlider.getSlider().setMinimum(min)
        self.maxSlider.getSlider().setMaximum(max)
        self.sliderLayout.addLayout(self.maxSlider)

        self.minSlider.getSlider().valueChanged.connect(self.calibrateMaxWithMin)
        self.maxSlider.getSlider().valueChanged.connect(self.calibrateMinWithMax)

        self.setLayout(self.sliderLayout)
    
    def calibrateMaxWithMin(self):
        if self.minSlider.getValue() > self.maxSlider.getValue():
            self.maxSlider.getSlider().setValue(self.minSlider.getValue())
    
    def calibrateMinWithMax(self):
        if self.maxSlider.getValue() < self.minSlider.getValue():
            self.minSlider.getSlider().setValue(self.maxSlider.getValue())
    
    def getValues(self):
        return [self.minSlider.getValue(), self.maxSlider.getValue()]

class mySliderLayout(QtWidgets.QHBoxLayout):
    def __init__(self, labelText="", min=1, max=10):
        super().__init__()

        self.label = QtWidgets.QLabel(labelText)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.valueChanged.connect(self.update_ui)

        self.value = QtWidgets.QLineEdit(str(self.slider.value()))
        self.value.setFixedSize(50,25)
        self.value.textChanged.connect(self.updateSlider)
        
        self.addWidget(self.label)
        self.addWidget(self.slider)
        self.addWidget(self.value)

    def update_ui(self):
        self.value.setText(str(self.slider.value()))
    
    def updateSlider(self):
        self.slider.setValue(int(self.value.text()))

    def getValue(self):
        return self.slider.value()
    
    def getSlider(self):
        return self.slider

class myVector3Layout_Range(QtWidgets.QWidget):
    def __init__(self, parent=None, min=0, max=10):
        super().__init__(parent)

        self.setFixedHeight(100)

        self.vectorLayout = QtWidgets.QHBoxLayout(self)

        self.lockButtonsLayout = QtWidgets.QVBoxLayout(self)

        self.lockButtonsLayout.addSpacing(20)

        self.lockButton_Min = QtWidgets.QCheckBox("Lock")
        self.lockButtonsLayout.addWidget(self.lockButton_Min)

        self.lockButton_Max = QtWidgets.QCheckBox("Lock")
        self.lockButtonsLayout.addWidget(self.lockButton_Max)

        self.vectorLayout.addLayout(self.lockButtonsLayout)

        self.xRangeLayout = myRangeSlider(self, "X", min, max)
        self.vectorLayout.addWidget(self.xRangeLayout)
        self.yRangeLayout = myRangeSlider(self, "Y", min, max)
        self.vectorLayout.addWidget(self.yRangeLayout)
        self.zRangeLayout = myRangeSlider(self, "Z", min, max)
        self.vectorLayout.addWidget(self.zRangeLayout)

        self.xRangeLayout.minSlider.getSlider().valueChanged.connect(self.lockBehaviour_MinX)
        self.yRangeLayout.minSlider.getSlider().valueChanged.connect(self.lockBehaviour_MinY)
        self.zRangeLayout.minSlider.getSlider().valueChanged.connect(self.lockBehaviour_MinZ)

        self.xRangeLayout.maxSlider.getSlider().valueChanged.connect(self.lockBehaviour_MaxX)
        self.yRangeLayout.maxSlider.getSlider().valueChanged.connect(self.lockBehaviour_MaxY)
        self.zRangeLayout.maxSlider.getSlider().valueChanged.connect(self.lockBehaviour_MaxZ)
    
    def getVectorValues_Min(self):
        return [self.xRangeLayout.getValues()[0], self.yRangeLayout.getValues()[0], self.zRangeLayout.getValues()[0]]
    
    def getVectorValues_Max(self):
        return [self.xRangeLayout.getValues()[1], self.yRangeLayout.getValues()[1], self.zRangeLayout.getValues()[1]]

    def lockBehaviour_MinX(self):
        self.lockBehaviourMin(self.xRangeLayout.minSlider.getSlider(),
                           self.yRangeLayout.minSlider.getSlider(),
                           self.zRangeLayout.minSlider.getSlider())

    def lockBehaviour_MinY(self):
        self.lockBehaviourMin(self.yRangeLayout.minSlider.getSlider(),
                           self.xRangeLayout.minSlider.getSlider(),
                           self.zRangeLayout.minSlider.getSlider())

    def lockBehaviour_MinZ(self):
        self.lockBehaviourMin(self.zRangeLayout.minSlider.getSlider(),
                           self.yRangeLayout.minSlider.getSlider(),
                           self.xRangeLayout.minSlider.getSlider())

    def lockBehaviour_MaxX(self):
        self.lockBehaviourMax(self.xRangeLayout.maxSlider.getSlider(),
                           self.yRangeLayout.maxSlider.getSlider(),
                           self.zRangeLayout.maxSlider.getSlider())

    def lockBehaviour_MaxY(self):
        self.lockBehaviourMax(self.yRangeLayout.maxSlider.getSlider(),
                           self.xRangeLayout.maxSlider.getSlider(),
                           self.zRangeLayout.maxSlider.getSlider())

    def lockBehaviour_MaxZ(self):
        self.lockBehaviourMax(self.zRangeLayout.maxSlider.getSlider(),
                           self.yRangeLayout.maxSlider.getSlider(),
                           self.xRangeLayout.maxSlider.getSlider())

    def lockBehaviourMin(self, slider1, slider2, slider3):
        if not self.lockButton_Min.isChecked():
            return
        slider2.setValue(slider1.value())
        slider3.setValue(slider1.value())

    def lockBehaviourMax(self, slider1, slider2, slider3):
        if not self.lockButton_Max.isChecked():
            return
        slider2.setValue(slider1.value())
        slider3.setValue(slider1.value())


class ToolWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)


class ProceduralTool(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Dialog)
        self.setWindowTitle("Procedural tool")

        self.createdIndex = 0
        self.selectedIndex_Generated=0
        self.importedAssetsAmnt = 0

        self.draw()
        self.bind()

        self.updatePreviewLayouts()
        self.updateGenerateLayouts()
        self.updateImportParamLayoutsVisibility()

        self.generatePreview()
        self.updateAreaPreviewVisibility()

    def closeEvent(self, event):
        super().closeEvent(event)
        cmds.lockNode('preview*', lock=False)
        cmds.delete('preview*')

    def addWidgetToLayout(self, _layout, _widget, _text=""):
        _widget.setText(_text)
        _layout.addWidget(_widget)

    def draw(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        
#=============================================IMPORT WIDGET=====================================#
        self.importWidget = QtWidgets.QWidget()
        self.importLayout = QtWidgets.QVBoxLayout(self.importWidget)

        self.importButton = QtWidgets.QPushButton(self)
        self.addWidgetToLayout(self.importLayout, self.importButton, "Import")

        self.deleteImportBaseButton = QtWidgets.QPushButton(self)
        self.addWidgetToLayout(self.importLayout, self.deleteImportBaseButton, "Delete import base")

        self.importWidget.setLayout(self.importLayout)
        self.mainLayout.addWidget(self.importWidget)
#=============================================================================================#

#==========================================PREVIEW WIDGET=====================================#
        self.previewWidget = QtWidgets.QWidget()
        self.previewLayout = QtWidgets.QVBoxLayout(self.previewWidget)

        self.previewLayout.addWidget(QtWidgets.QLabel("Spawning area type"))

        self.typeBox_preview = QtWidgets.QComboBox()
        self.typeBox_preview.addItem("Sphere")
        self.typeBox_preview.addItem("Plane")
        self.typeBox_preview.addItem("Disc")
        self.previewLayout.addWidget(self.typeBox_preview)

        self.togglePreview_Area = QtWidgets.QCheckBox("Preview spawning area")
        self.previewLayout.addWidget(self.togglePreview_Area)
    #-------------------------------------------------------------------------------
        # Sphere Preview
        self.previewParamWidget_Sphere = QtWidgets.QWidget()
        self.previewParamLayout_Sphere = QtWidgets.QVBoxLayout(self.previewWidget)

        self.previewRadiusLayout_Sphere = mySliderLayout("Radius", 1, 50)
        self.previewParamLayout_Sphere.addLayout(self.previewRadiusLayout_Sphere)

        self.previewParamWidget_Sphere.setLayout(self.previewParamLayout_Sphere)
        self.previewLayout.addWidget(self.previewParamWidget_Sphere)
        
        # Plane Preview
        self.previewParamWidget_Plane = QtWidgets.QWidget()
        self.previewParamLayout_Plane = QtWidgets.QVBoxLayout(self.previewParamWidget_Plane)
        
        self.previewXLayout_Plane = mySliderLayout("Width (X)", 1, 25)
        self.previewParamLayout_Plane.addLayout(self.previewXLayout_Plane)
        self.previewZLayout_Plane = mySliderLayout("Height (Z)", 1, 25)
        self.previewParamLayout_Plane.addLayout(self.previewZLayout_Plane)

        self.previewParamWidget_Plane.setLayout(self.previewParamLayout_Plane)
        self.previewLayout.addWidget(self.previewParamWidget_Plane)

        # Disc Preview
        self.previewParamWidget_Disc = QtWidgets.QWidget()
        self.previewParamLayout_Disc = QtWidgets.QVBoxLayout(self.previewParamWidget_Disc)
        
        self.previewRadiusLayout_Disc = mySliderLayout("Radius", 1, 25)
        self.previewParamLayout_Disc.addLayout(self.previewRadiusLayout_Disc)

        self.previewParamWidget_Disc.setLayout(self.previewParamLayout_Disc)
        self.previewLayout.addWidget(self.previewParamWidget_Disc)
    #-------------------------------------------------------------------------------
        
        self.previewWidget.setLayout(self.previewLayout)
        self.mainLayout.addWidget(self.previewWidget)
#==============================================================================================#

        self.mainLayout.addSpacing(5)

#===========================================GENERATING PART====================================#
        self.generateWidget = QtWidgets.QWidget()
        self.generateLayout = QtWidgets.QVBoxLayout(self.generateWidget)

        self.generateLayout.addWidget(QtWidgets.QLabel("Generated object"))
        
        self.typeBox_generated = QtWidgets.QComboBox()
        self.generateLayout.addWidget(self.typeBox_generated)
        
        self.togglePreview_Import = QtWidgets.QCheckBox()
        self.addWidgetToLayout(self.generateLayout, self.togglePreview_Import, "Preview generated object")
        self.togglePreview_Import.setEnabled(False)

        self.generateLayout.addSpacing(5)

        self.isOutsideButton = QtWidgets.QCheckBox()
        self.addWidgetToLayout(self.generateLayout, self.isOutsideButton, "Spawn outside only")

        self.amntLayout = mySliderLayout("Amount", 1, 100)
        self.generateLayout.addLayout(self.amntLayout)

    #-------------------------------------------------------------------------------
        # Imported Parameters Layout
        self.generateParamWidget_Imported = QtWidgets.QWidget()
        self.generateParamLayout_Imported = QtWidgets.QVBoxLayout(self.generateParamWidget_Imported)

    # Random rotation 
        self.randomRotationButton = QtWidgets.QCheckBox()
        self.addWidgetToLayout(self.generateParamLayout_Imported, self.randomRotationButton, "Is random rotation")
        self.generateRotationParam_Imported = myVector3Layout_Range(min=-360, max=360)
        self.generateParamLayout_Imported.addWidget(self.generateRotationParam_Imported)

        self.generateParamLayout_Imported.addSpacing(25)
        
    # Random scale 
        self.randomScaleButton = QtWidgets.QCheckBox()
        self.addWidgetToLayout(self.generateParamLayout_Imported, self.randomScaleButton, "Is random scale")

        self.scaleDivisionGroup = QtWidgets.QButtonGroup(self.generateParamWidget_Imported)
        self.scaleDivisionLayout = QtWidgets.QHBoxLayout()

        self.divideBy1Button = QtWidgets.QRadioButton()
        self.divideBy10Button = QtWidgets.QRadioButton()
        self.divideBy100Button = QtWidgets.QRadioButton()
        self.divideBy1000Button = QtWidgets.QRadioButton()
        self.scaleDivisionGroup.addButton(self.divideBy1Button, 1)
        self.scaleDivisionGroup.addButton(self.divideBy10Button, 10)
        self.scaleDivisionGroup.addButton(self.divideBy100Button, 100)
        self.scaleDivisionGroup.addButton(self.divideBy1000Button, 1000)
        self.addWidgetToLayout(self.scaleDivisionLayout, self.divideBy1Button, "1")
        self.addWidgetToLayout(self.scaleDivisionLayout, self.divideBy10Button, "10")
        self.addWidgetToLayout(self.scaleDivisionLayout, self.divideBy100Button, "100")
        self.addWidgetToLayout(self.scaleDivisionLayout, self.divideBy1000Button, "1000")
        self.divideBy1Button.setChecked(True)

        self.generateParamLayout_Imported.addLayout(self.scaleDivisionLayout)

        self.generateScaleParam_Imported = myVector3Layout_Range(min=1, max=10000)
        self.generateParamLayout_Imported.addWidget(self.generateScaleParam_Imported)

        self.generateLayout.addWidget(self.generateParamWidget_Imported)
    #-------------------------------------------------------------------------------

        self.generateWidget.setLayout(self.generateLayout)
        self.mainLayout.addWidget(self.generateWidget)
#==============================================================================================#
        
        self.mainLayout.addSpacing(25)

#=============================================BUTTONS PART=====================================#
        self.buttonsWidget = QtWidgets.QWidget()
        self.buttonsLayout = QtWidgets.QVBoxLayout(self.buttonsWidget)

        self.generate_btn = QtWidgets.QPushButton("Generate")
        self.buttonsLayout.addWidget(self.generate_btn)
        self.regenerate_btn = QtWidgets.QPushButton("Re-Generate")
        self.buttonsLayout.addWidget(self.regenerate_btn)
        self.deleteSel_btn = QtWidgets.QPushButton("Delete selected")
        self.buttonsLayout.addWidget(self.deleteSel_btn)
        self.deleteAllOfType_btn = QtWidgets.QPushButton("Delete all of type")
        self.buttonsLayout.addWidget(self.deleteAllOfType_btn)
        self.deleteAll_btn = QtWidgets.QPushButton("Delete all")
        self.buttonsLayout.addWidget(self.deleteAll_btn)

        self.buttonsWidget.setLayout(self.buttonsLayout)
        self.mainLayout.addWidget(self.buttonsWidget)
#==============================================================================================#

    def bind(self):
        self.importButton.clicked.connect(self.importNewObject)
        self.deleteImportBaseButton.clicked.connect(self.deleteImportBase)
        self.togglePreview_Import.clicked.connect(self.updateImportPreviewVisibility)

        self.togglePreview_Area.clicked.connect(self.updateAreaPreviewVisibility)

        self.typeBox_preview.currentIndexChanged.connect(self.updatePreviewLayouts)
        self.typeBox_preview.currentIndexChanged.connect(self.generatePreview)

        self.typeBox_generated.currentIndexChanged.connect(self.updateGenerateLayouts)

        self.randomRotationButton.clicked.connect(self.updateImportParamLayoutsVisibility)
        self.randomScaleButton.clicked.connect(self.updateImportParamLayoutsVisibility)

        self.previewRadiusLayout_Sphere.getSlider().valueChanged.connect(self.updatePreview)
        self.previewXLayout_Plane.getSlider().valueChanged.connect(self.updatePreview)
        self.previewZLayout_Plane.getSlider().valueChanged.connect(self.updatePreview)
        self.previewRadiusLayout_Disc.getSlider().valueChanged.connect(self.updatePreview)

        self.generate_btn.clicked.connect(self.generate)
        self.regenerate_btn.clicked.connect(self.regenerate)
        self.deleteSel_btn.clicked.connect(self.deleteSelected)
        self.deleteAllOfType_btn.clicked.connect(self.deleteAllOfType)
        self.deleteAll_btn.clicked.connect(self.deleteAll)

    def updatePreviewLayouts(self):
        self.previewParamWidget_Sphere.setVisible(self.typeBox_preview.currentText() == "Sphere")
        self.previewParamWidget_Plane.setVisible(self.typeBox_preview.currentText() == "Plane")
        self.previewParamWidget_Disc.setVisible(self.typeBox_preview.currentText() == "Disc")
        self.isOutsideButton.setEnabled(self.typeBox_preview.currentText() != "Plane")

    def updateGenerateLayouts(self):
        self.selectedIndex_Generated=self.typeBox_generated.currentIndex()
        self.updateImportPreviewVisibility()

    def updateImportParamLayoutsVisibility(self):
        self.generateRotationParam_Imported.setEnabled(self.randomRotationButton.isChecked())
        self.generateScaleParam_Imported.setEnabled(self.randomScaleButton.isChecked())
        self.updateScaleDivisionButtons(self.randomScaleButton.isChecked())

    def updateScaleDivisionButtons(self, isEnabled):
        for button in self.scaleDivisionGroup.buttons():
            button.setEnabled(isEnabled)

    def createPreviewMaterial(self):
        _color = [1, 0, 0]
        _material = cmds.shadingNode("lambert", name="previewMaterial", asShader=True)
        _sg = cmds.sets(name="previewMaterialSG", empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr(f"{_material}.outColor", f"{_sg}.surfaceShader")
        cmds.setAttr(_material + ".color", _color[0], _color[1], _color[2], type="double3")
        cmds.setAttr(_material + ".transparency", .8, .8, .8, type="double3")
        cmds.sets(f"preview{self.typeBox_preview.currentText()}", forceElement=_sg)

    def updateImportPreviewVisibility(self):
        if not cmds.objExists(f"{self.typeBox_generated.currentText()}_Base"):
            return
        cmds.setAttr(f"{self.typeBox_generated.currentText()}_Base" + ".visibility", 
                     self.togglePreview_Import.isChecked())
        cmds.lockNode(f'{self.typeBox_generated.currentText()}_Base', 
                      lock=self.togglePreview_Import.isChecked())

    def updateAreaPreviewVisibility(self):
        if cmds.objExists(f"preview{self.typeBox_preview.currentText()}*"):
            cmds.setAttr(f"preview{self.typeBox_preview.currentText()}.visibility", 
                     self.togglePreview_Area.isChecked())

    def updatePreview(self):
        self.editPreview()
        if(self.togglePreview_Area.isChecked() == False):
            self.togglePreview_Area.setChecked(True)
            self.updateAreaPreviewVisibility()

    def generatePreview(self):
        if cmds.objExists('preview*'):
            cmds.lockNode('preview*', lock=False)
            cmds.delete('preview*')

        if self.typeBox_preview.currentText() == "Sphere":
            cmds.polySphere(n='previewSphere',
                            r=self.previewRadiusLayout_Sphere.getValue())

        elif self.typeBox_preview.currentText() == "Plane":
            cmds.polyPlane(n='previewPlane',
                           w=self.previewXLayout_Plane.getValue(),
                           h=self.previewZLayout_Plane.getValue())

        elif self.typeBox_preview.currentText() == "Disc":
            cmds.circle(n='previewDisc', r=self.previewRadiusLayout_Disc.getValue())
            cmds.setAttr('previewDisc.rotateX', 90)
        
        cmds.lockNode(f'preview{self.typeBox_preview.currentText()}', lock=True)
        if not self.typeBox_preview.currentText() == "Disc":
            self.createPreviewMaterial()
        
        self.updateAreaPreviewVisibility()

    def editPreview(self):
        if self.typeBox_preview.currentText() == "Sphere":
            cmds.polySphere('previewSphere', e=True,
                            r=self.previewRadiusLayout_Sphere.getValue())
            
        elif self.typeBox_preview.currentText() == "Plane":
            cmds.polyPlane('previewPlane', e=True,
                           w=self.previewXLayout_Plane.getValue(),
                           h=self.previewZLayout_Plane.getValue())
            
        elif self.typeBox_preview.currentText() == "Disc":
            cmds.circle('previewDisc', e=True, r=self.previewRadiusLayout_Disc.getValue())

    def importNewObject(self):
        _filePaths = cmds.fileDialog2(fm=4)
        for filePath in _filePaths:
            #Forbiden: & ' ( - ) ~ # { [ ^ @ ] } + ^ $ ! ,
            objectName = os.path.split(filePath)[1].split('.')[0].replace(" ", "_")

            _importedObjects = cmds.file(filePath, i=True, rnn=True)
            _transforms = cmds.ls(_importedObjects, type='transform')

            for i, object in enumerate(_transforms):
                _newName = f"Imported{objectName}_Base"
                cmds.lockNode(object, lock=False)
                cmds.rename(object, _newName)
                cmds.setAttr(_newName + ".visibility", False)
            
            self.typeBox_generated.addItem(f"Imported{objectName}")
            self.typeBox_generated.setCurrentText(f"Imported{objectName}")
            self.importedAssetsAmnt += 1
        self.togglePreview_Import.setEnabled(True)

    def generate(self):
    #--------------------------Spawning points (base) definition---------------------------#
        _x=_y=_z=0

        if self.typeBox_preview.currentText() == "Sphere":
            _x=_y=_z=self.previewRadiusLayout_Sphere.getValue()

        elif self.typeBox_preview.currentText() == "Plane":
            _x=self.previewXLayout_Plane.getValue() / 2
            _z=self.previewZLayout_Plane.getValue() / 2
        
        elif self.typeBox_preview.currentText() == "Disc":
            _x=_z=self.previewRadiusLayout_Disc.getValue()
    #-------------------------------------------------------------------------------------#
        
    #------------------------Spawning points (random) definition--------------------------#
        for x in range(self.amntLayout.getValue()):
            _randX = random.uniform(-_x, _x)
            _randY = random.uniform(-_y, _y)
            _randZ = random.uniform(-_z, _z)

            if self.typeBox_preview.currentText() == "Sphere" or "Disc":
                _randHoriAngle = math.radians(random.uniform(0, 360))
                _randVertiAngle = math.radians(random.uniform(0, 360))

                if self.isOutsideButton.isChecked():
                    if self.typeBox_preview.currentText() == "Sphere":
                        _point = self.getPointOnSphere(self.previewRadiusLayout_Sphere.getValue(), 
                                                       _randHoriAngle, 
                                                       _randVertiAngle)
                        _randX = _point[0]
                        _randY = _point[1]
                        _randZ = _point[2]
                    
                    elif self.typeBox_preview.currentText() == "Disc":
                        _point = self.getPointOnDisc(self.previewRadiusLayout_Disc.getValue(), 
                                                       _randHoriAngle)
                        _randX = _point[0] 
                        _randY = 0
                        _randZ = _point[2]
                else:
                    if self.typeBox_preview.currentText() == "Sphere":
                        _point = self.getPointOnSphere(self.previewRadiusLayout_Sphere.getValue(), 
                                                       _randHoriAngle, 
                                                       _randVertiAngle)
                        _randX = random.uniform(0, _point[0])
                        _randY = random.uniform(0, _point[1])
                        _randZ = random.uniform(0, _point[2])
                    
                    elif self.typeBox_preview.currentText() == "Disc":
                        _point = self.getPointOnDisc(self.previewRadiusLayout_Disc.getValue(), 
                                                       _randHoriAngle)
                        _randX = random.uniform(0, _point[0])
                        _randY = 0
                        _randZ = random.uniform(0, _point[2])

    #-------------------------------------------------------------------------------------#

    #-------------------------------------Generating--------------------------------------#
            _duplicateName = f"tool{self.typeBox_generated.currentText()}_Duplicate{self.createdIndex}"
            cmds.duplicate(f"{self.typeBox_generated.currentText()}_Base*",
                           n=_duplicateName)
            cmds.setAttr(_duplicateName + ".visibility", True)
            cmds.select(_duplicateName)
    #-------------------------------------------------------------------------------------#

    #---------------------------------------Moving----------------------------------------#
            cmds.move(
                cmds.getAttr(f'preview{self.typeBox_preview.currentText()}.translateX') + _randX,
                cmds.getAttr(f'preview{self.typeBox_preview.currentText()}.translateY') + _randY,
                cmds.getAttr(f'preview{self.typeBox_preview.currentText()}.translateZ') + _randZ)
    #-------------------------------------------------------------------------------------#
    
    #--------------------------------------Rotating---------------------------------------#
            if self.randomRotationButton.isChecked():
                _rot = self.getRandomVector(self.generateRotationParam_Imported.getVectorValues_Min(),
                                            self.generateRotationParam_Imported.getVectorValues_Max())
                cmds.rotate(_rot[0], _rot[1], _rot[2])
    #-------------------------------------------------------------------------------------#

    #--------------------------------------Scaling----------------------------------------#
            if self.randomScaleButton.isChecked():
                _scale = self.getRandomVector(self.generateScaleParam_Imported.getVectorValues_Min(),
                                              self.generateScaleParam_Imported.getVectorValues_Max())
                cmds.scale(_scale[0]/self.scaleDivisionGroup.checkedId(), 
                           _scale[1]/self.scaleDivisionGroup.checkedId(), 
                           _scale[2]/self.scaleDivisionGroup.checkedId())
    #-------------------------------------------------------------------------------------#
            self.createdIndex += 1

    def regenerate(self):
        self.deleteAllOfType()
        self.generate()

    def getPointOnSphere(self, radius, horiAngle, vertiAngle):
        x=radius * math.cos(horiAngle) * math.sin(vertiAngle)
        y=radius * math.sin(horiAngle) * math.sin(vertiAngle)
        z=radius * math.cos(vertiAngle)
        return [x,y,z]
    
    def getPointOnDisc(self, radius, horiAngle):
        x=radius * math.sin(horiAngle)
        y=0
        z=radius * math.cos(horiAngle)
        return [x,y,z]

    def getRandomVector(self, minVector, maxVector):
        _x=_y=_z=0

        if minVector[0] == maxVector[0]:
            _x=minVector[0]
        else:
            _x = random.randrange(minVector[0], maxVector[0])

        if minVector[1] == maxVector[1]:
            _y=minVector[1]
        else:
            _y = random.randrange(minVector[1], maxVector[1])

        if minVector[2] == maxVector[2]:
            _z=minVector[2]
        else:
            _z = random.randrange(minVector[2], maxVector[2])

        return [_x, _y, _z]

    def deleteSelected(self):
        selectedSet = cmds.ls(f'tool{self.typeBox_generated.currentText()}*', sl = True)
        selectedAmnt = len(selectedSet)
        self.createdIndex -= selectedAmnt
        cmds.delete()

    def deleteAllOfType(self):
        cmds.delete(f'tool{self.typeBox_generated.currentText()}*')
        self.createdIndex = 0
        if self.createdIndex < 0:
            self.createdIndex = 0
    
    def deleteImportBase(self):
        _baseName = f'{self.typeBox_generated.currentText()}_Base'
        if cmds.objExists(_baseName):
            cmds.lockNode(_baseName, lock=False)
            cmds.delete(_baseName)
            self.typeBox_generated.removeItem(self.selectedIndex_Generated)
            self.importedAssetsAmnt-=1
            if self.importedAssetsAmnt <= 0:
                self.togglePreview_Import.setEnabled(False)

    def deleteAll(self):
        cmds.delete(f'tool*')
        self.createdIndex = 0


# 'dump' window that lets widget be always on top
mainWindow = ToolWindow()
widget1 = ProceduralTool(mainWindow)
widget1.setFixedSize(800, 1000)
widget1.show()

#TODO:
#- overlap checking
#- subscribe updateGeneratedTypeList() on importPreviewDeleted
#- check if an imported object hasn't already been imported