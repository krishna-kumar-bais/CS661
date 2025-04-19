import vtk
import os
import sys
 
if __name__ == '__main__':
    # Checking for proper script usage.
    if(len(sys.argv)<2):
        print("Error: Incorrect usage.")
        print("Usage: python task2.py <inputFilePath>")
        sys.exit(1)

    # Defining the file path.
    filePath = sys.argv[1]

    # Checking if the file exists.
    if (not os.path.exists(filePath)):
        print(f"Input file not present in the expected path. Please move the input file to the following path: {filePath}")
        print("Usage: python task2.py <inputFilePath>")
        sys.exit(1)

    # Asking the user wheather to use Phong Shading or not.
    print("Would you like to use VTK’s Phong Shading feature?")
    phong = input("Please answer (Y/N). Any other input will be interpreted as Y.")
    if phong in ('N','n'):
        phong = False
        print("Phong shading disabled.")
    else:
        phong = True
        print("Phong shading enabled.")

    # Loading the input file.
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(filePath)
    reader.Update()

    # Setting up the vtkColorTransferFunction.
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
    colorTransferFunction.AddRGBPoint(-1873.90, 0.0, 0.0, 0.5)
    colorTransferFunction.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
    colorTransferFunction.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

    # Setting up the vtkPiecewiseFunction(Opacity transfer function).
    opacityTransferFunction = vtk.vtkPiecewiseFunction() 
    opacityTransferFunction.AddPoint(-4931.54, 1.0)
    opacityTransferFunction.AddPoint(101.815, 0.002)
    opacityTransferFunction.AddPoint(2594.97, 0.0)

    # Setting up the vtkVolumeProperty.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetInterpolationTypeToLinear()
    
    # Use Phong shading as per user input.
    if phong:
        volumeProperty.ShadeOn()
        volumeProperty.SetAmbient(0.5)
        volumeProperty.SetDiffuse(0.5)
        volumeProperty.SetSpecular(0.5)

    # Setting up the vtkSmartVolumeMapper.
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    # Setting up the vtkOutlineFilter.
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())
    
    # Setting up the vtkActor.
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(0, 0, 0) # Change color to black.

    # Setting up the vtkVolume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # Setting up the vtkRenderer.
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.AddActor(outlineActor)
    renderer.SetBackground(1, 1, 1)

    # Setting up the vtkRenderWindow.
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1000, 1000)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName('Hurricane Volume Rendering')

    # Setting up the vtkRenderWindowInteractor.
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # Starting the rendering.
    renderWindow.Render()
    interactor.Start()

