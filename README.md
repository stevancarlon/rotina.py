# rotina.py
#### Video Demo:  https://www.youtube.com/watch?v=t9wl4OSXVKE
#### Description: This was my final project for the **Harvard University's CS50 Course: Introduction to Computer Science**.
#
>This application developed using PyQt5 modules is a routine scheduler. The user will add tasks with a specified hour and the application will pop desktop notifications and a voice alarm. The user can also save routines as well as load past routines. If minimized, the app will hide to the Windows task tray while still notifying the user's tasks.

## Features

- Add/remove tasks including a title, a brief description and a specified time;
- Receive desktop notifications;
- Voice alarm announces the name of the task;
- Start/stop notifications from running;
- Save and load routines;
- Hide application to the Windows system tray.

![This is an image](https://i.ibb.co/3WmwKgG/rotina.jpg)

#
## Explaining the code
Some libraries that made this application possible are:
- `PyQt5` for the GUI;
- `pyttsx3` for the voice alarm;
- `plyer` for the desktop notifications;
- `systemtray` for the interface hiding function;
- `win32gui` to reopen the GUI from the systemtray.

The `class MainWindow` is responsible for loading the user interface with `self.ui = uic.loadUi('ui_main.ui', self)`. After that, it connects the functions that will be defined a bit further to the buttons and initialize some lists, dictionaries and variables such as `tasks` and `thread`. Still inside the `class MainWindow`, 8 functions are defined:

- `add_task` - Gets the user input and store into the dictionary `tasks`;
- `add_widget` - Creates a `QFrame` with 3 `QLabel` texts and a close button using the info provided by the user;
- `handle_delete_clicked` - Deletes the frame and all the widgets inside it;
- `start_routine` - This function will set the variable `notifications = on` and start a `QThread` that will run a `while` loop and keep checking if the `current_time` is in the dicionary `tasks`;
- `stop_routine` - Stops the `QThread` from running;
- `save_routine` - Saves the routine `tasks` to a file;
- `load_routine` - Loads a saved routine;
- `hide_win` - Enables the user to hide the program to the Windows system tray by clicking the yellow button and open it again by clicking the app icon.

The `class ThreadClass` is responsible for checking  if the `current_time` is into the dictionary `tasks` with a `while` loop. In Python, you have to use multiprocessing resources if you want to use while loop to check conditions, otherwise your application will crash. 

A bit of what's happening inside the ThreadClass:

```python

for row in win.tasks:
                if row['hour'] == current_time and row['check'] == False:
                    row['check'] = True
                    notification.notify(
                                        title=f"{row['title']}",
                                        message=f"{row['description']}",
                                        app_icon="icons/bell.ico",
                                        timeout=10,
                                        toast=False
                                        )

```

#
## How to use it

To execute the application you must have installed in your system [Python3](https://www.python.org/downloads/) and have `pip` to install some dependencies.

Execute `pip install systemtray` to install the tray library. To open the program, execute the bat file `rotina.py` inside the folder.

![This is an image](https://i.ibb.co/Tw6tGLK/rotina2.jpg)

If the system has `cx_freeze` installed, it's possible to create a fully executable file using the command `python .\setup.py build`.

![This is an image](https://i.ibb.co/7Yz6tdL/ezgif-4-0ff91f3d10.gif)

Add tasks, run notifications, save/load routines and hide the interface to the Windows by clicking the yellow button.

#

## About Harvard University's CS50 Course: Introduction to Computer Science
An entry-level course taught by David J. Malan, CS50x teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, software engineering, and web development. Languages include C, Python, SQL, and JavaScript plus CSS and HTML. Problem sets inspired by real-world domains of biology, cryptography, finance, forensics, and gaming. The on-campus version of CS50x , CS50, is Harvard's largest course.

[LinkedIn: Stevan Carlon](https://www.linkedin.com/in/stevancarlon/)