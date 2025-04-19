# Usage: python task.py <inputFilePath> <outputFilePath> <seed_x> <seed_y> <seed_z>
# e.g. python task.py tornado3d_vector.vti 0_0_7.vtp 0 0 7
import vtk
import numpy as np
import os
import sys

def in_bounds(next_point, bounds):
    '''
    Function to check if the next_point is within bounds.
    '''
    return (bounds[0] <= next_point[0] <= bounds[1] and # Checks X axis bounds.
            bounds[2] <= next_point[1] <= bounds[3] and # Checks Y axis bounds.
            bounds[4] <= next_point[2] <= bounds[5])    # Checks Z axis bounds.

def get_vector(data, point):
    '''
    Function to interpolate the vector at a point in the field using VTKProbeFilter.
    '''
    # Converting the given point to a vtkPoints object and then to a vtkPolyData object.
    pt = vtk.vtkPoints()
    pt.InsertNextPoint(point)
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(pt)

    # Creating a VTK Probe Filter.
    vtk_probe = vtk.vtkProbeFilter()
    vtk_probe.SetSourceData(data) # Adding the flow field.
    vtk_probe.SetInputData(polyData) # Adding the point at which to get the vector.
    vtk_probe.Update() 

    # Retrieving the vector from the probe output.
    probed_data = vtk_probe.GetOutput() 
    vector = probed_data.GetPointData().GetArray("vectors") # Name of the array was given in the assignment pdf.

    # Converting the vector to a numpy array and returning it.
    return np.array(vector.GetTuple(0), dtype=np.float64)

def RK4_integration(data, current_point, step_size):
    '''
    Function to perform one RK4 integration step.
    '''
    # Calculating the intemediate values, using the step_size and current_point.
    a = step_size * get_vector(data, current_point)
    b = step_size * get_vector(data, current_point + a/2)
    c = step_size * get_vector(data, current_point + b/2)
    d = step_size * get_vector(data, current_point + c)

    # Calculating the next_point.
    next_point = current_point + (a + 2*b + 2*c + d)/6

    # Return the next_point as an numpy array.
    return np.array(next_point, dtype=np.float64)

def particle_trace(data, seed, step_size, max_steps, bounds):
    '''
    Function used to trace the streamline of the particle.
    Direction of trace depends on the sign of step_size.
    Positive step_size = Forward trace.
    Negative step_size = Backward trace.
    '''
    trace_points = [] # A list to store the traced points.
    
    # Since we are starting the trace from the seed point, it is the initial current point.
    current_point = np.array(seed, dtype=np.float64)

    '''The following loop iterates untill the "max_steps" number of points have been 
       traced, or aslong as the next_point is within the bounds of the vector field.
    '''
    for _ in range(max_steps):
        # Finds the next point using RK4 Integration.
        next_point = RK4_integration(data, current_point, step_size)

        # Check if the next_point is with the bounds or not.
        if(not in_bounds(next_point, bounds)):
            break                 # Stop tracing of the streamline if the point is out of bounds.
        else:
            trace_points.append(next_point.copy()) # Store the next_point in the trace_points list.
            current_point = next_point             # The next_point in this iteration is the current_point in the next iteration.

    return trace_points # Return the traced points.

if __name__ == "__main__":
    "Checking for proper script usage."
    if(len(sys.argv)!=6):
        print("Error: Incorrect usage.")
        print("Usage: python task.py <inputFilePath> <outputFilePath> <seed_x> <seed_y> <seed_z>")
        sys.exit(1)

    # Defining the file paths.
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    
    # Checking if the seed values are valid floats or ints.
    seed = None
    try:
        seed = [float(arg) for arg in sys.argv[3:]]
        seed = np.array(seed, dtype=np.float64)  # Converts seed to a numpy array.
    except ValueError:
        print("Error: All seed coordinates must be numeric (float).")
        sys.exit(1)

    # Checking if the file exists.
    if (not os.path.exists(inputFilePath)):
        print(f"Input file not present in the expected path. Please move the input file to the following path: {inputFilePath}")
        print("Usage: python task.py <inputFilePath> <outputFilePath> <seed_x> <seed_y> <seed_z>")
        sys.exit(1)

    # Loading the file.
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(inputFilePath)
    reader.Update()
    data = reader.GetOutput()

    # Get the bounds of the vector field.
    bounds = data.GetBounds()

    # Set the step size and max steps as given in assignment pdf.
    step_size = 0.05 
    max_steps = 1000

    # Tracing the particle in the forward direction.
    forward_trace = particle_trace(data, seed, step_size, max_steps, bounds)
    # Tracing the particle in the backward direction can be done by negating the step size.
    backward_trace = particle_trace(data, seed, -step_size, max_steps, bounds)

    # Combining the traces. Since we are tracing from the seed position 
    # and going backwards, we need to reverse the points in the backward trace.
    # Total trace = reverse(backward_trace) + seed + forward_trace
    streamline_points = list(reversed(backward_trace)) + [seed] + forward_trace

    # Initialising the required VTK objects.
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    # Iterates through each point in the streamline_points and adds it to the vtkPoints object.
    for point in streamline_points:
        points.InsertNextPoint(point)

    # Defining the vtkPolyLine object to store the connectivity info of a line of multiple connected points.
    polyLine = vtk.vtkPolyLine()
    # Set the number of points in the polyLine as the number of points in the streamline.
    polyLine.GetPointIds().SetNumberOfIds(len(streamline_points))

    # Add each point in the streamline to the polyLine.
    for i in range(len(streamline_points)):
        polyLine.GetPointIds().SetId(i, i) 

    # Add the polyLine to the "lines" vtkCellArray object.
    lines.InsertNextCell(polyLine)

    # Create vtkPolyData object
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)  # Adds the "points" vtkPoints object.
    polyData.SetLines(lines)    # Adds the "lines" vtkCellArray object.

    # Write the output to a .vtp file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outputFilePath)
    writer.SetInputData(polyData)
    writer.Write()


