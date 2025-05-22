# Contact Management Prototype

This is a basic prototype of a Contact Management module with a web-based UI and a Python Flask backend. It supports CRUD (Create, Read, Update, Delete) operations for contacts, with data stored in a JSON file.

## Prerequisites

*   **Python 3.x installed:** Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).
*   **Flask and Flask-CORS installed:** These Python packages are required for the backend server. You can install them using pip:
    ```bash
    pip install Flask Flask-CORS
    ```

## Project Files

The key files in this prototype are:

*   `server.py`: The Flask backend server that handles API requests and data storage.
*   `index.html`: The main frontend HTML file that provides the user interface.
*   `style.css`: CSS styles for the frontend.
*   `app.js`: JavaScript for frontend logic, including API interactions and UI updates.
*   `contacts.json`: The JSON file where contact data is stored. This file will be created automatically in the same directory as `server.py` if it doesn't exist when the server starts.

### Planning Documents (Contextual)
The following documents were created during the planning and specification phase of this prototype and provide additional context:
*   `Contact_Management_Prototype_Scope.md`: Defines the features and fields for this prototype.
*   `Contact_Management_Prototype_UI_Layout.md`: Describes the UI layout for the different views.
*   `Contact_Management_Prototype_Tech_Stack.md`: Outlines the technology choices for the prototype.

## Running the Prototype

Follow these steps to set up and run the application:

### Step 1: Start the Backend Server

1.  Open a terminal or command prompt.
2.  Navigate to the directory where the `server.py` file is located.
3.  Run the backend server using the following command:
    ```bash
    python server.py
    ```
4.  The server will start, and you should see output indicating it's running. By default, it will run on `http://localhost:5001`.
    *   Example output: `* Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)`

### Step 2: Access the Frontend

1.  Open your preferred web browser (e.g., Chrome, Firefox, Edge, Safari).
2.  Open the `index.html` file directly in your browser. You can usually do this by:
    *   Navigating to the project directory in your file explorer and double-clicking `index.html`.
    *   Dragging the `index.html` file from your file explorer into an open browser window.
    *   Using the browser's "File > Open" or "File > Open File..." menu and selecting `index.html`.

    The application should now be loaded and ready to use. The frontend will communicate with the backend server running at `http://localhost:5001`.

## How to Use

Once the frontend is loaded in your browser and the backend server is running:

*   **View Contacts:** The main page displays a list of contacts. If it's the first time running, this list will be empty.
*   **Add a Contact:** Click the "Add New Contact" button to open a form. Fill in the details and click "Save".
*   **Manage Contacts:** For each contact in the list, you will see action buttons:
    *   **View Details:** Click to see all information for that contact.
    *   **Edit:** Click to modify the contact's information.
    *   **Delete:** Click to remove the contact (a confirmation prompt will appear).

## Stopping the Application

*   **Backend Server:** To stop the Flask backend server, go to the terminal window where it is running and press `Ctrl+C`.
*   **Frontend:** Simply close the browser tab or window where `index.html` is open.

---

This README provides the necessary information to get the Contact Management prototype up and running. Enjoy testing the application!
