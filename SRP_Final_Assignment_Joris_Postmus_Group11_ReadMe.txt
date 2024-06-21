# How to Run the Program with AlphaMini Robot

This guide will help you run the `SRP_Final_Assignment_Joris_Postmus_Group11.py` Python script with an AlphaMini robot.

## Prerequisites

- Python 3.6 or higher installed on your system.
- The `autobahn.twisted` library installed. You can install it using pip:
  ```
  pip install autobahn[twisted]
  ```
- An AlphaMini robot with the necessary sensors for touch, sound, and face detection.
- Ensure that the AlphaMini robot is turned on and connected to it's respective hub.
- Ensure that the realm in the `SRP_Final_Assignment_Joris_Postmus_Group11.py`file at line 169 is correctly set to the realm of the robot.

## Steps to Run the Program

1. Open a terminal or command prompt.

2. Navigate to the directory containing the `SRP_Final_Assignment_Joris_Postmus_Group11.py` file. You can do this with the `cd` command. For example:
   ```
   cd path/to/directory
   ```
   Replace `path/to/directory` with the path to the directory that contains the `SRP_Final_Assignment_Joris_Postmus_Group11.py` file.

3. Run the Python script with the following command:
   ```
   python SRP_Final_Assignment_Joris_Postmus_Group11.py
   ```
   If you have multiple versions of Python installed on your system, you may need to use `python3` instead of `python`.

The program should now run, and you will see output in your terminal or command prompt as the program executes.

## Interacting with the Program

The program is designed to interact with an AlphaMini robot. It plays guitar notes and quizzes the user to identify them. The listener can interact with the program using verbal interaction (speech recognition).

- **Face Detection**: The robot uses face detection to initiate interaction. It starts the game after recognizing the user's face.
- **Audio Recognition**: The robot plays guitar notes and asks the user to identify the notes by listening to them. The user responds verbally to the robot's questions. The robot processes these responses to determine if the answers are correct or incorrect.

Please note that you will need the appropriate hardware (an AlphaMini robot with the necessary sensors) to fully interact with this program.

## Important notes for testing

- Some sensors may not work equally well depending on the robot used for testing. 
- Specifically, the face recognition does not always work equally well and so I have provided instructions in the code (and they will be printed in-console), in case the robot appears to freeze.
- Furthermore, if the speech recognition does not appear to be picking up the right answers, please switch from robot as some have better microphones than others.