import vtk
import os
import numpy as np
import sys

def getIsoValuePoint(edge, isoValue):
    """ Function to get the point with the target IsoValue."""
    p1,p2,v1,v2 = edge
    p1 = np.array(p1)
    p2 = np.array(p2)
    t = (isoValue - v1) / (v2 - v1)
    return tuple(p1 + t * (p2 - p1))

if __name__ == "__main__":
    # Checking for proper script usage.
    if(len(sys.argv)<4):
        print("Error: Incorrect usage.")
        print("Usage: python task1.py <inputFilePath> <outputFilePath> <isoValue>")
        sys.exit(1)

    # Defining the file paths.
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    isoValue = sys.argv[3]

    # Checking if the file exists.
    if (not os.path.exists(inputFilePath)):
        print(f"Input file not present in the expected path. Please move the input file to the following path: {inputFilePath}")
        print("Usage: python task1.py <inputFilePath> <outputFilePath> <isoValue>")
        sys.exit(1)

    # Checking if the isoValue is a valid float or integer.
    try:
        isoValue = float(isoValue)
    except ValueError:
        print(f"Error: {isoValue} is not a valid float or integer.")
        print("Usage: python task1.py <inputFilePath> <outputFilePath> <isoValue>")
        sys.exit(1)

    # Loading the file.
    print("Reading input VTI file...")
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(inputFilePath)
    reader.Update()
    data = reader.GetOutput()

    # Printing out some parameters.
    numPoints = data.GetNumberOfPoints()
    numCells = data.GetNumberOfCells()
    spacing = data.GetSpacing()
    extent = data.GetExtent()
    dimensions = (extent[1] - extent[0] + 1,
                extent[3] - extent[2] + 1,
                extent[5] - extent[4] + 1)

    print(f"Number of points in the data: {numPoints}")
    print(f"Number of cells in the data: {numCells}")
    print(f"Dimensions of the data: {dimensions}")
    print()

    # Getting the Pressure values.
    dataValues = data.GetPointData().GetArray("Pressure")

    # Initialising the required VTK objects.
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    # Looping through all the cells in the file.
    for cellNum in range(numCells):
        # Getting the point number of the cell points in counterclockwise order.
        cell = data.GetCell(cellNum)
        pointNum1 = cell.GetPointId(0)
        pointNum2 = cell.GetPointId(1)
        pointNum3 = cell.GetPointId(3)
        pointNum4 = cell.GetPointId(2)

        # Getting the values of the cell points.
        value1 = dataValues.GetTuple1(pointNum1)
        value2 = dataValues.GetTuple1(pointNum2)
        value3 = dataValues.GetTuple1(pointNum3)
        value4 = dataValues.GetTuple1(pointNum4)
        
        # Getting the coordinates of the points.
        pointId1 = data.GetPoint(pointNum1)
        pointId2 = data.GetPoint(pointNum2)
        pointId3 = data.GetPoint(pointNum3)
        pointId4 = data.GetPoint(pointNum4)

        # Creating an empty list to store the intersection points.
        intersectionPoints = []

        # Making the edges in counter clockwise order.
        edges = [(pointId1, pointId2, value1, value2),
                 (pointId2, pointId3, value2, value3),
                 (pointId3, pointId4, value3, value4),
                 (pointId4, pointId1, value4, value1)]
        
        # For each edge, check if the values at the ends have the same sign.
        # If not then find the intersection point on the edge and 
        # append the point onto the isoPoints list.
        for edge in edges:
            if ((edge[2]-isoValue)*(edge[3]-isoValue)<0):
                intersectionPoints.append(getIsoValuePoint(edge, isoValue))

        if(len(intersectionPoints)==2):
            # Inserting the two points onto the vtkPoints object.
            pid0 = points.InsertNextPoint(intersectionPoints[0])  
            pid1 = points.InsertNextPoint(intersectionPoints[1]) 

            # Create a line between two points.
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, pid0)
            line.GetPointIds().SetId(1, pid1)
            lines.InsertNextCell(line)  # Add line to vtkCellArray object.

        elif (len(intersectionPoints) == 4):
            # Inserting the four points onto the vtkPoints object.
            pid0 = points.InsertNextPoint(intersectionPoints[0])
            pid1 = points.InsertNextPoint(intersectionPoints[1])
            pid2 = points.InsertNextPoint(intersectionPoints[2])
            pid3 = points.InsertNextPoint(intersectionPoints[3])

            # Create a line between first two points.
            line1 = vtk.vtkLine()
            line1.GetPointIds().SetId(0, pid0)
            line1.GetPointIds().SetId(1, pid1)
            lines.InsertNextCell(line1) # Add line to vtkCellArray object.

            # Create a line between last two points.
            line2 = vtk.vtkLine()
            line2.GetPointIds().SetId(0, pid2)
            line2.GetPointIds().SetId(1, pid3)
            lines.InsertNextCell(line2) # Add line to vtkCellArray object.

    # Create vtkPolyData object
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetLines(lines)

    # Write the output to a .vtp file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outputFilePath)
    writer.SetInputData(polyData)
    writer.Write()

    print(f"Isocontour saved to {outputFilePath}")


