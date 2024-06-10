# How to Run the Program with AlphaMini Robot

This guide will help you run the `assignment2.py` Python script with an AlphaMini robot.

## Prerequisites

- Python 3.6 or higher installed on your system.
- The `autobahn.twisted` library installed. You can install it using pip:
  ```
  pip install autobahn[twisted]
  ```
- An AlphaMini robot

## Steps to Run the Program

1. Open a terminal or command prompt.

2. Navigate to the directory containing the `project-code-group11.py` file. You can do this with the `cd` command. For example:
   ```
   cd path/to/directory
   ```
   Replace `path/to/directory` with the path to the directory that contains your `assignment2.py` file.

3. Run the Python script with the following command:
   ```
   python assignment2.py
   ```
   If you have multiple versions of Python installed on your system, you may need to use `python3` instead of `python`.

The program should now run, and you will see output in your terminal or command prompt as the program executes.

## Interacting with the Program

The program is designed to interact with an AlphaMini robot. Here you may list the different behavior that relies on the various sensors that produce certain behavior

- **Touch**: The robot responds by doing x when touched on the fore/middle/back part of his head-sensor
- **Aruco cards**: The robot responds to seeing an Aruco card. These are used to provide multiple-choice answers to a question asked by the robot.
- **Faces**: The robot responds to seeing faces. The robot only starts telling a story after it sees a listener's face.

Please note that you will need the appropriate hardware (an AlphaMini robot with the necessary sensors) to fully interact with this program.