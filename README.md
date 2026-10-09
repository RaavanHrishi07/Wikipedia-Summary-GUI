# Wikipedia Summary GUI

A Python desktop application built with Tkinter that retrieves and displays Wikipedia article summaries. It includes search suggestions, recent search history, and persistent history storage between sessions.

## Features

- **Wikipedia Search:** Retrieve article summaries by entering a topic.
- **Search Suggestions:** View matching Wikipedia article titles while typing.
- **Keyboard Support:** Press Enter to search and use the Down arrow to navigate suggestions.
- **Recent Search History:** View your 10 most recent successful searches.
- **Persistent History:** Automatically save and restore search history when reopening the application.
- **Duplicate Prevention:** Keep only one entry for each topic, moving repeated searches to the top.
- **Quick Re-search:** Double-click a suggestion or history item to retrieve its summary.
- **Clear History:** Remove saved search history whenever needed.
- **Scrollable Results:** Read long article summaries in the text area.
- **Input Validation:** Receive a warning when the search field is empty.
- **Error Handling:** Display an error message when an article cannot be retrieved.

## Requirements

- Python 3.8 or newer
- Tkinter support
- Internet connection
- The `pymediawiki` package

Tkinter is included with most standard Python installations.

## Installation

Clone the repository:

    git clone https://github.com/RaavanHrishi07/Wikipedia-Summary-GUI.git

Navigate to the project directory:

    cd Wikipedia-Summary-GUI

Install the required dependency:

    python -m pip install -r requirements.txt

## Run the Application

Start the application with:

    python main.py

## How to Use

1. Launch the application.
2. Enter a topic in the search field.
3. Select a suggested article title or press Enter to search.
4. Read the retrieved summary in the results area.
5. Double-click an item under Recent Searches to search for it again.
6. Select Clear History to remove all saved search entries.

## Search History

The application stores successful searches in `search_history.json`, located alongside the Python script.

- The latest successful search appears first.
- A maximum of 10 topics are retained.
- Duplicate topics are prevented without regard to letter case.
- Search history is restored when the application starts again.
- Clearing history also clears the saved history file.

The history file is generated automatically when a successful search is completed.

## Project Structure

    Wikipedia-Summary-GUI/
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── LICENSE
    ├── .gitignore
    └── search_history.json

The `search_history.json` file is created automatically at runtime and may not exist in a fresh checkout.

## Technologies Used

- Python
- Tkinter
- Pymediawiki
- JSON
- pathlib

## Troubleshooting

**The application cannot retrieve an article**

- Check your internet connection.
- Try a more specific topic or select one of the suggestions.
- Confirm that the required package is installed in the Python environment used to run the application.

**The application cannot save search history**

- Ensure the project directory is writable.
- Check whether another application is preventing access to `search_history.json`.

**The `mediawiki` module is missing**

Install the requirements using:

    python -m pip install -r requirements.txt

## Author

**Hrishikesh Sharma**

GitHub: https://github.com/RaavanHrishi07

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.