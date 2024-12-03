# Clinic Management System

## Overview
The Clinic Management System is a software application designed to manage patient records, appointments (to be added soon in the future), and other clinic-related activities. It provides both a Command-Line Interface (CLI) and a Graphical User Interface (GUI) for ease of use.

## Prerequisites
- Python 3.8 or higher

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/isaac-preyser/seng-265/tree/d992e192656e13d7af1f6fd67820e1f9532c517f/a5
    ```
2. Navigate to the project directory:
    ```sh
    cd a5
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration
- Ensure that any necessary environment variables are set up.

## Usage
You can run the application in either CLI or GUI mode.

### Command-Line Interface (CLI)
To start the CLI, run:
```sh
python -m clinic cli
```

### Graphical User Interface (GUI)
To start the GUI, run:
```sh
python -m clinic gui
```

#### Patients List
The patients list contains a list of all patients in the database, which may be searched by either name or PHN, using the search bar above the list. 

To add a patient to the database, click the '+' button below the list, and navigate to the [Patient Data Tab](#patient-data-tab) to enter relevant patient data.

Likewise, the '-' button will remove the current patient from the database. 

#### Notes Tab
The notes tab contains the "meat and potatoes" of the system- where patient notes may be read, updated, searched for, and stored. 

To view notes, select a patient in the patients list, and select a note in the note list. To add a new note, click the '+' at the bottom of the notes list. 

Above the notes list, there is a search bar, which performs multiple functions: 

1. Searches for (and retrieves) matching note content to the given search term. 
2. Given numeric input, retrieves notes with a code matching the given search term. 
3. If the above fail to return any notes, the search term will be considered to be a date, returning notes with a matching date/time. 

#### Patient Data Tab
The Patient Data Tab is the central hub for reading and managing patient data. The fields will be automatically populated with loaded patient data from the database, and may be edited by selecting the desired field, and inputting new data to be updated. 

To push the updated data to the database, click the 'Save' button. 

The 'Reset' button will undo any edits made, and restore the fields with the currently stored data from the database. 

The 'Discard' button will begin the delete patient prompt, similar to the '-' button in the [Patients List](#patients-list). 

#### System Tab
The System Tab contains a few 'extraneous' functions that didn't quite fit in with the other tabs. Right now, the Log Out and List Patient Record functions are housed there. 

## Features
- Manage patient records
- Add, update, and delete patient notes
- Search for patients and notes
- User authentication
- Autosave functionality

## Running Tests
To run the tests, use:
```sh
python -m unittest discover tests
```

## Debugging
You can use the provided VSCode launch configurations to debug the application.

1. Open the project in VSCode.
2. Go to the Run and Debug view.
3. Select either "Clinic (CLI)" or "Clinic (GUI)" and start debugging.

## File Structure
- `clinic/`: Contains the main application code.
- `tests/`: Contains the test cases.
- `.vscode/`: Contains VSCode configuration files.

## Known Issues
- The content on the System and Patient Data tabs does not scale "nicely" upon window resizing. 
- Exception handling needs to be refactored on  the client end, as many thrown exceptions from the database will lead to crashes. 

Please submit any other bugs or suggestions on the [issue tracker](https://github.com/isaac-preyser/seng-265/issues). 

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.



## Contact
For any questions or feedback, please contact [preyser@uvic.ca](mailto:preyser@uvic.ca)