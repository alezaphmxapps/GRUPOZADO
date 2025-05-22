# Contact Management Prototype - UI Layout Description

This document provides a textual description of the basic user interface (UI) layout for the Contact Management prototype. It aims to guide developers in building a simple, functional UI.

## 1. Contact List View

*   **Purpose:** To display all contacts in a summarized format and provide access to actions for each contact.
*   **Layout:**
    *   **Page Title:**
        *   Text: "Contacts"
        *   Position: Typically at the top left or center of the page.
    *   **"Add New Contact" Button:**
        *   Text: "Add New Contact" or "+ New Contact"
        *   Position: Prominently placed, e.g., top right of the page, above the contact table.
        *   Action: Navigates to the "Contact Creation/Edit Form View" in "create" mode.
    *   **Table Displaying Contacts:**
        *   A standard HTML table structure.
        *   If no contacts exist, display a message like "No contacts found. Add a new contact to get started."

*   **Table Columns:**
    1.  **`FirstName`:**
        *   Header: "First Name"
        *   Content: Displays the `FirstName` of the contact.
    2.  **`LastName`:**
        *   Header: "Last Name"
        *   Content: Displays the `LastName` of the contact.
    3.  **`Email`:**
        *   Header: "Email"
        *   Content: Displays the `Email` of the contact.
    4.  **`Company`:**
        *   Header: "Company"
        *   Content: Displays the `Company` name associated with the contact.
    5.  **`Actions`:**
        *   Header: "Actions"
        *   Content: This column will contain buttons/links for each contact row.

*   **Actions Column (per row):**
    *   **"View Details" Button/Link:**
        *   Text: "View" or "Details"
        *   Action: Navigates to the "Contact Detail View" for the specific contact in that row.
    *   **"Edit" Button/Link:**
        *   Text: "Edit"
        *   Action: Navigates to the "Contact Creation/Edit Form View" for the specific contact in that row, pre-filled with the contact's data.
    *   **"Delete" Button:**
        *   Text: "Delete"
        *   Action: Initiates the delete process for the specific contact. A confirmation dialog (e.g., "Are you sure you want to delete [FirstName] [LastName]?") should be displayed before actual deletion.

*   **Navigation (Potential Feature):**
    *   If the list of contacts is extensive, basic pagination controls (e.g., "Previous," "Next," page numbers) should be placed below the table. For the minimal prototype, this can be omitted if the number of contacts is expected to be small.

## 2. Contact Creation/Edit Form View

*   **Purpose:** To allow users to add a new contact or edit the details of an existing one.
*   **Layout:**
    *   **Page Title:**
        *   Dynamic Text:
            *   For new contacts: "Add New Contact"
            *   For editing existing contacts: "Edit Contact: [FirstName] [LastName]" (e.g., "Edit Contact: John Doe")
        *   Position: Top left or center of the page.
    *   **Form:**
        *   A standard HTML form structure.
        *   Input fields should be clearly labeled.

*   **Form Fields:**
    *   **`FirstName`:**
        *   Label: "First Name:"
        *   Input Type: Text input (`<input type="text">`)
        *   Required: Yes
    *   **`LastName`:**
        *   Label: "Last Name:"
        *   Input Type: Text input (`<input type="text">`)
        *   Required: Yes
    *   **`Email`:**
        *   Label: "Email:"
        *   Input Type: Email input (`<input type="email">`)
        *   Required: Yes
    *   **`Phone`:**
        *   Label: "Phone:"
        *   Input Type: Telephone input (`<input type="tel">`)
        *   Required: No
    *   **`Company`:**
        *   Label: "Company:"
        *   Input Type: Text input (`<input type="text">`)
        *   Required: No
    *   *(Note: `ContactID`, `CreatedAt`, and `UpdatedAt` are system-managed and typically not directly editable. `ContactID` might be displayed in a read-only format in "Edit" mode for reference if deemed useful, but not as an input field.)*

*   **Action Buttons:**
    *   **"Save" Button:**
        *   Text: "Save" or "Save Contact"
        *   Action: Submits the form data. Upon successful save:
            *   If creating: Navigates to the "Contact Detail View" of the newly created contact or back to the "Contact List View".
            *   If editing: Navigates to the "Contact Detail View" of the edited contact or back to the "Contact List View".
        *   Position: Typically at the bottom of the form.
    *   **"Cancel" Button:**
        *   Text: "Cancel"
        *   Action: Discards any changes and navigates the user back:
            *   If creating: To the "Contact List View".
            *   If editing: To the "Contact Detail View" of the contact being edited, or to the "Contact List View".
        *   Position: Typically next to the "Save" button.

## 3. Contact Detail View

*   **Purpose:** To display all stored information for a single selected contact in a read-only format.
*   **Layout:**
    *   **Page Title:**
        *   Dynamic Text: "Contact Details: [FirstName] [LastName]" (e.g., "Contact Details: Jane Smith")
        *   Position: Top left or center of the page.
    *   **Display Area:**
        *   A clear presentation of contact information. Each field should have a label and its corresponding value.
        *   **`FirstName`:**
            *   Label: "First Name:"
            *   Value: [Contact's First Name]
        *   **`LastName`:**
            *   Label: "Last Name:"
            *   Value: [Contact's Last Name]
        *   **`Email`:**
            *   Label: "Email:"
            *   Value: [Contact's Email]
        *   **`Phone`:**
            *   Label: "Phone:"
            *   Value: [Contact's Phone Number]
        *   **`Company`:**
            *   Label: "Company:"
            *   Value: [Contact's Company Name]
        *   **`CreatedAt`:**
            *   Label: "Date Added:"
            *   Value: [Formatted timestamp of contact creation, e.g., "YYYY-MM-DD HH:MM"]
        *   **`UpdatedAt`:**
            *   Label: "Last Updated:"
            *   Value: [Formatted timestamp of last update, e.g., "YYYY-MM-DD HH:MM"]
        *   *(Note: `ContactID` can also be displayed here if useful for reference, e.g., Label: "Contact ID:", Value: [Contact's ID])*

*   **Action Buttons:**
    *   **"Edit" Button:**
        *   Text: "Edit" or "Edit Contact"
        *   Action: Navigates to the "Contact Creation/Edit Form View" for this contact, with fields pre-populated.
        *   Position: Typically grouped together, e.g., top right of the detail display area or at the bottom.
    *   **"Delete" Button:**
        *   Text: "Delete" or "Delete Contact"
        *   Action: Initiates the delete process. A confirmation dialog (e.g., "Are you sure you want to delete this contact?") must be displayed before actual deletion. Upon confirmation, the contact is removed, and the user is navigated to the "Contact List View".
        *   Position: Typically near the "Edit" button.
    *   **"Back to List" Button/Link:**
        *   Text: "Back to List" or "‹ All Contacts"
        *   Action: Navigates the user back to the "Contact List View".
        *   Position: Can be at the top or bottom of the view, clearly indicating navigation away from the details.

This textual layout description should provide a solid foundation for developing the UI for the Contact Management prototype. Focus should be on functionality and clarity over complex styling for this initial phase.
