# This project was made by Lancelot

import VertexTable, Projectors
import sys,  pygame
import Button

#create display window
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("3D Wire Frame Renderer")

surface = pygame.image.load("./../Images/logo.png").convert_alpha()
pygame.display.set_icon(surface)

import DiyShape

screen.fill((33, 40, 48))
#load button images "C:\Users\lance\OneDrive\Documents\Python\3D_Renderer\Images\shape1.png"
nextShape = pygame.image.load("./../Images/NextShape.png").convert_alpha()
prevShape = pygame.image.load("./../Images/PrevShape.png").convert_alpha()
nextPoint = pygame.image.load("./../Images/NextPoint.png").convert_alpha()
prevPoint = pygame.image.load("./../Images/PrevPoint.png").convert_alpha()
CheckedBox = pygame.image.load("./../Images/PointToggleSelected.png").convert_alpha()
UncheckedBox = pygame.image.load("./../Images/PointToggleUnselected.png").convert_alpha()
CheckedTick = pygame.image.load("./../Images/CheckedBox.png").convert_alpha()
UncheckedTick = pygame.image.load("./../Images/UncheckedBox.png").convert_alpha()
SliderBar = pygame.image.load("./../Images/SliderBar.png").convert_alpha()
SliderNob = pygame.image.load("./../Images/SliderNob.png").convert_alpha()
CustomShapeUI = pygame.image.load("./../Images/CustomShapeUI.png").convert_alpha()
AddEdge = pygame.image.load("./../Images/AddEdge.png").convert_alpha()
UndoButton = pygame.image.load("./../Images/Undo.png").convert_alpha()
Save = pygame.image.load("./../Images/Save.png").convert_alpha()
Delete = pygame.image.load("./../Images/Delete.png").convert_alpha()
SaveDelete = pygame.image.load("./../Images/SaveDeleteRect.png").convert_alpha()
Settings = pygame.image.load("./../Images/Settings.png").convert_alpha()
NotSave = pygame.image.load("./../Images/NotSave.png").convert_alpha()


#create button instances
nextShapeButton = Button.Button(144, 14, nextShape, 1)
prevShapeButton = Button.Button(31, 14, prevShape, 1)
SizeSlider = Button.Slider(34, 277, SliderBar, SliderNob)
FOVSlider = Button.Slider(32, 337, SliderBar, SliderNob)
SensitivitySlider = Button.Slider(32, 530, SliderBar, SliderNob)
dragPad = Button.Tactile(256, 0, 768, 576)
nextVertex = Button.Button(144, 305, nextPoint, 1)
prevVertex = Button.Button(61, 305, prevPoint, 1)
AddEdge = Button.Button(35, 461, AddEdge, 1)
UndoButton = Button.Button(35, 513, UndoButton, 1)
CustomShapePointA = Button.RadioCheck(168, 376, UncheckedBox, CheckedBox, 1, True)
CustomShapePointB = Button.RadioCheck(168, 417, UncheckedBox, CheckedBox, 1)
Save = Button.Button(38, 175, Save, 1)
Delete = Button.Button(38, 127, Delete, 1)
ViewCenter = Button.Check(160, 411, UncheckedTick, CheckedTick, 1)
ViewVertices = Button.Check(160, 447, UncheckedTick, CheckedTick, 1)


# Launch the projection
def launchWindow():
    
    # Temp
    prevZoom = 0
    prevDragX = 0
    prevDragY = 0
    sensitivity = 0.5
        
    # Set offset
    offset = (640, 288)
    
    vertexTable = VertexTable.Vertices(VertexTable.vertexTable, 0)
    projection = Projectors.Projectors(vertexTable, 250, vertexTable.EdgeTable, offset)
    pygame.draw.rect(screen, (69, 74, 79), pygame.Rect(0, 0, 256, 576))
    diyShape = DiyShape.DiyShape(vertexTable)
    
    # Main loop
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                sys.exit
                
        # Earase previous frame
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(256, 0, 768, 576))
        pygame.draw.rect(screen, (69, 74, 79), pygame.Rect(0, 0, 256, 576))
        
        # Choose propper UI for cuur state
        if vertexTable.CurrShape == vertexTable.ShapeNumber:
            makeYourOwnShape = True
        else:
            makeYourOwnShape = False
        
        # If designing a new shape, open UI
        if makeYourOwnShape:
            vertexTable.EdgeTable = diyShape.edgeTable
            # Draw the UI
            screen.blit(CustomShapeUI, (20, 247))
            # Select the point
            if CustomShapePointA.draw(screen):
                CustomShapePointA.state = True
                CustomShapePointB.state = False
                diyShape.currPoint = 0
            if CustomShapePointB.draw(screen):
                CustomShapePointA.state = False
                diyShape.currPoint = 1
            # Move the point
            if prevVertex.draw(screen):
                if diyShape.currPoint == 0:
                    diyShape.SelectedA -= 1
                    if diyShape.SelectedA < 0:
                        diyShape.SelectedA = len(VertexTable.vertexTable) -1
                else:
                    diyShape.SelectedB -= 1
                    if diyShape.SelectedB < 0:
                        diyShape.SelectedB = len(VertexTable.vertexTable) -1
            if nextVertex.draw(screen):
                if diyShape.currPoint == 0:
                    diyShape.SelectedA += 1
                    if diyShape.SelectedA > len(VertexTable.vertexTable) -1:
                        diyShape.SelectedA = 0
                else:
                    diyShape.SelectedB += 1
                    if diyShape.SelectedB > len(VertexTable.vertexTable) -1:
                        diyShape.SelectedB = 0
            if AddEdge.draw(screen):
                diyShape.AddEdge()
            if UndoButton.draw(screen):
                if len(projection.EdgeTable) != 0:
                    projection.EdgeTable.pop()
            # Draw buttons on window, check if clicked
            screen.blit(SaveDelete, (22, 114))
            if Save.draw(screen):
                diyShape.SaveShape("./../EdgeTables/EdgeTables.txt")
                vertexTable.ShapeNumber += 1
        else:
            screen.blit(Settings, (23, 240))
            if ViewVertices.draw(screen):
                projection.DrawPoints(projection.projectedPoints, screen, (255, 255, 255))
            if ViewCenter.draw(screen):
                projection.DrawCenter(screen, (255, 0, 0))
            
            # Update sliders
            if SizeSlider.draw(screen):
                if (SizeSlider.value - 0.5) != prevZoom:
                    vertexTable.BetterZoom(2*((SizeSlider.value - 0.5) - prevZoom))
                    prevZoom = (SizeSlider.value - 0.5)
            if FOVSlider.draw(screen):
                projection.focalLen = (projection.minFocalLen * (1 - FOVSlider.value)) + (projection.maxFocalLen * FOVSlider.value)
            if SensitivitySlider.draw(screen):
                sensitivity = SensitivitySlider.value
            # Draw buttons on window, check if clicked
            screen.blit(SaveDelete, (22, 114))
            screen.blit(NotSave, (38, 175))
            
        
        if Delete.draw(screen):
            if diyShape.DeleteShape("./../EdgeTables/EdgeTables.txt", vertexTable.CurrShape):
                vertexTable.ShapeNumber -= 1
            projection.EdgeTable = vertexTable.GetEdgeTable()
            

        
        if nextShapeButton.draw(screen):
            vertexTable.CurrShape += 1
            if (vertexTable.CurrShape > vertexTable.ShapeNumber):
                vertexTable.CurrShape = 0
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        if prevShapeButton.draw(screen):
            vertexTable.CurrShape -= 1
            if (vertexTable.CurrShape < 0):
                vertexTable.CurrShape = vertexTable.ShapeNumber
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        
        
        
        # If screen drag, rotate shape
        if dragPad.updatePad():
            if dragPad.valueX != prevDragX:
                vertexTable.RotateVertexTableY(sensitivity * 10 * (dragPad.valueX - prevDragX))
                prevDragX = dragPad.valueX
        else:
            prevDragX = 0
        if dragPad.updatePad():
            if dragPad.valueY != prevDragY:
                vertexTable.RotateVertexTableX(sensitivity * 10 * (dragPad.valueY - prevDragY))
                prevDragY = dragPad.valueY
        else:
            prevDragY = 0
        
        # Rotate alog Z axis to keepshape centered on the Y axis
        deltaX = projection.projectedPoints[4][0] - projection.projectedPoints[22][0]
        deltaY = projection.projectedPoints[4][1] - projection.projectedPoints[22][1]
        if deltaY > 0:
            side = 1
        else:
            side = -1
        if deltaX < -1 or 1 < deltaX:
            if deltaX > 0:
                vertexTable.RotateVertexTableZ(side * deltaX/(2*vertexTable.size))
            if deltaX < 0:
                vertexTable.RotateVertexTableZ(side * deltaX/(2*vertexTable.size))
        
        # Update the projection
        projection = Projectors.Projectors(vertexTable, projection.focalLen , vertexTable.EdgeTable, offset)
        
        # Draw new frame
        projection.DrawShape((71, 225, 12), screen)
        
        # Draw points
        if makeYourOwnShape:
            diyShape.ShowVertices(screen, projection.projectedPoints)
        
        # Update the canvas
        pygame.display.update()
        pygame.time.Clock().tick(30)
    
    pygame.quit

launchWindow()