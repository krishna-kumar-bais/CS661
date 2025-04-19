Assignment 3 - CS661
Group No.: 76
Krishna Kumar Bais (241110038)
Milan Roy (241110042)


# Task: Particle Tracing in Steady Flow Field 
---------------------------------------------
1. Ensure that `VTK` and `NumPy` are installed before running the script.
2. If executing the script via Command Prompt (Windows) or Terminal (Linux), make sure you are in the
   same directory as the Python script to properly utilize relative file paths.
3. The input file should also be located in the same directory as the script when using relative paths.
4. If running the script in an IDE such as VS Code or PyCharm, use the built-in terminal.
5. To execute the script, use the following command:
   python task.py <inputFilePath> <outputFilePath> <seed_x> <seed_y> <seed_z>
   e.g. python task.py tornado3d_vector.vti 0_0_7.vtp 0 0 7
6. The created streamline will be saved to <outputFilePath>.


## Notes:  
- The input file (`tornado3d_vector.vti`) must be accessible by the script (use absolute or relative paths).  
- The output `.vtp` file will be saved to the path specified in `<outputFilePath>`.  
- Ensure seed coordinates are numeric (e.g., `0 0 7`).  

