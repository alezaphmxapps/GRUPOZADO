document.addEventListener('DOMContentLoaded', () => {
    // Views
    const contactListView = document.getElementById('contactListView');
    const contactFormView = document.getElementById('contactFormView');
    const contactDetailView = document.getElementById('contactDetailView');

    // Buttons
    const addNewContactBtn = document.getElementById('addNewContactBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const backToListBtn = document.getElementById('backToListBtn');
    const editContactDetailBtn = document.getElementById('editContactBtn');
    const deleteContactDetailBtn = document.getElementById('deleteContactBtn');

    // Forms & Tables
    const contactForm = document.getElementById('contactForm');
    const contactsTableBody = document.querySelector('#contactsTable tbody');
    const formTitle = document.getElementById('formTitle');
    const contactIdInput = document.getElementById('contactId'); // Hidden input for contact ID

    // Detail View Elements
    const detailName = document.getElementById('detailName');
    const detailEmail = document.getElementById('detailEmail');
    const detailPhone = document.getElementById('detailPhone');
    const detailCompany = document.getElementById('detailCompany');
    const detailCreatedAt = document.getElementById('detailCreatedAt');
    const detailUpdatedAt = document.getElementById('detailUpdatedAt');
    const detailViewTitle = document.getElementById('detailViewTitle');

    const API_BASE_URL = 'http://localhost:5001'; // Base URL for the Flask API

    // --- Helper function for API calls ---
    async function fetchAPI(endpoint, options = {}) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Request failed with status ' + response.status }));
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            if (response.status === 204) { // No Content
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            alert(`Error: ${error.message}`);
            throw error; // Re-throw to handle in calling function if needed
        }
    }

    // --- View Navigation ---
    function showListView() {
        contactListView.style.display = 'block';
        contactFormView.style.display = 'none';
        contactDetailView.style.display = 'none';
        loadAndRenderContacts();
    }

    function showFormView(contact = null) {
        contactListView.style.display = 'none';
        contactFormView.style.display = 'block';
        contactDetailView.style.display = 'none';

        if (contact) {
            formTitle.textContent = 'Edit Contact';
            contactIdInput.value = contact.ContactID; // Store ID in hidden field
            document.getElementById('firstName').value = contact.FirstName;
            document.getElementById('lastName').value = contact.LastName;
            document.getElementById('email').value = contact.Email;
            document.getElementById('phone').value = contact.Phone || '';
            document.getElementById('company').value = contact.Company || '';
        } else {
            formTitle.textContent = 'Add New Contact';
            contactForm.reset();
            contactIdInput.value = ''; // Clear ID for new contact
        }
    }

    async function showDetailView(contactId) {
        try {
            const contact = await fetchAPI(`/contacts/${contactId}`);
            if (contact) {
                contactListView.style.display = 'none';
                contactFormView.style.display = 'none';
                contactDetailView.style.display = 'block';
                populateDetailView(contact);
            }
        } catch (error) {
            // Error already handled by fetchAPI
            showListView(); // Go back to list view if contact fetch fails
        }
    }

    // --- Load and Render Contact List ---
    async function loadAndRenderContacts() {
        try {
            const contacts = await fetchAPI('/contacts');
            renderContactList(contacts);
        } catch (error) {
            // Error already handled by fetchAPI, table will show no contacts or error message
            contactsTableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Failed to load contacts.</td></tr>';
        }
    }

    function renderContactList(contacts) {
        contactsTableBody.innerHTML = ''; // Clear existing rows
        if (!contacts || contacts.length === 0) {
            const row = contactsTableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 4;
            cell.textContent = 'No contacts found. Add a new contact to get started.';
            cell.style.textAlign = 'center';
            return;
        }

        contacts.forEach(contact => {
            const row = contactsTableBody.insertRow();
            row.insertCell().textContent = `${contact.FirstName} ${contact.LastName}`;
            row.insertCell().textContent = contact.Email;
            row.insertCell().textContent = contact.Company;

            const actionsCell = row.insertCell();
            const viewBtn = document.createElement('button');
            viewBtn.textContent = 'View';
            viewBtn.dataset.id = contact.ContactID;
            viewBtn.classList.add('view-btn');
            actionsCell.appendChild(viewBtn);

            const editBtn = document.createElement('button');
            editBtn.textContent = 'Edit';
            editBtn.dataset.id = contact.ContactID;
            editBtn.classList.add('edit-btn');
            actionsCell.appendChild(editBtn);

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.dataset.id = contact.ContactID;
            deleteBtn.classList.add('delete-btn');
            actionsCell.appendChild(deleteBtn);
        });
    }

    // --- Populate Detail View ---
    function populateDetailView(contact) {
        detailViewTitle.textContent = `Contact Details: ${contact.FirstName} ${contact.LastName}`;
        detailName.textContent = `${contact.FirstName} ${contact.LastName}`;
        detailEmail.textContent = contact.Email;
        detailPhone.textContent = contact.Phone || 'N/A';
        detailCompany.textContent = contact.Company || 'N/A';
        detailCreatedAt.textContent = contact.CreatedAt ? new Date(contact.CreatedAt).toLocaleString() : 'N/A';
        detailUpdatedAt.textContent = contact.UpdatedAt ? new Date(contact.UpdatedAt).toLocaleString() : 'N/A';
        // Store current contact ID in the detail view buttons for easy access
        editContactDetailBtn.dataset.id = contact.ContactID;
        deleteContactDetailBtn.dataset.id = contact.ContactID;
    }


    // --- Event Listeners ---
    addNewContactBtn.addEventListener('click', () => showFormView());
    cancelBtn.addEventListener('click', showListView);
    backToListBtn.addEventListener('click', showListView);

    contactForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const id = contactIdInput.value; // Get ID from hidden input
        const contactData = {
            FirstName: document.getElementById('firstName').value,
            LastName: document.getElementById('lastName').value,
            Email: document.getElementById('email').value,
            Phone: document.getElementById('phone').value,
            Company: document.getElementById('company').value,
        };

        try {
            if (id) { // Editing existing contact
                await fetchAPI(`/contacts/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(contactData)
                });
            } else { // Adding new contact
                await fetchAPI('/contacts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(contactData)
                });
            }
            contactForm.reset();
            showListView(); // Reload list after successful save/update
        } catch (error) {
            // Error already handled by fetchAPI
            // Optionally, keep the form open or give specific feedback
        }
    });

    contactsTableBody.addEventListener('click', async (event) => {
        const target = event.target;
        const id = target.dataset.id;
        if (!id) return;

        if (target.classList.contains('view-btn')) {
            showDetailView(id);
        } else if (target.classList.contains('edit-btn')) {
            try {
                const contact = await fetchAPI(`/contacts/${id}`);
                if (contact) {
                    showFormView(contact);
                }
            } catch (error) {
                // Error already handled by fetchAPI
            }
        } else if (target.classList.contains('delete-btn')) {
            try {
                const contact = await fetchAPI(`/contacts/${id}`); // Fetch to get name for confirmation
                if (contact && confirm(`Are you sure you want to delete ${contact.FirstName} ${contact.LastName}?`)) {
                    await fetchAPI(`/contacts/${id}`, { method: 'DELETE' });
                    loadAndRenderContacts(); // Re-render the list
                }
            } catch (error) {
                // Error already handled by fetchAPI
            }
        }
    });
    
    editContactDetailBtn.addEventListener('click', async (event) => {
        const id = event.target.dataset.id;
        try {
            const contact = await fetchAPI(`/contacts/${id}`);
            if (contact) {
                showFormView(contact);
            }
        } catch (error) {
            // Error already handled by fetchAPI
        }
    });

    deleteContactDetailBtn.addEventListener('click', async (event) => {
        const id = event.target.dataset.id;
        try {
            const contact = await fetchAPI(`/contacts/${id}`); // Fetch to get name for confirmation
            if (contact && confirm(`Are you sure you want to delete ${contact.FirstName} ${contact.LastName}?`)) {
                await fetchAPI(`/contacts/${id}`, { method: 'DELETE' });
                showListView();
            }
        } catch (error) {
            // Error already handled by fetchAPI
        }
    });

    // --- Initial Load ---
    showListView(); // Load contacts from backend on page load
});
