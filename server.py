import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CONTACTS_FILE = 'contacts.json'

# --- Helper Functions for Data Storage ---

def read_contacts_from_file():
    """Reads the contacts list from the JSON file."""
    if not os.path.exists(CONTACTS_FILE):
        return []
    try:
        with open(CONTACTS_FILE, 'r') as f:
            data = f.read()
            if not data: # Handle empty file
                return []
            return jsonify(data).get_json() # Use jsonify to correctly parse the string from file
    except Exception as e:
        print(f"Error reading contacts file: {e}")
        return []

def write_contacts_to_file(contacts):
    """Writes the contacts list to the JSON file."""
    try:
        with open(CONTACTS_FILE, 'w') as f:
            f.write(jsonify(contacts).get_data(as_text=True)) # Use jsonify to correctly format as JSON string
    except Exception as e:
        print(f"Error writing contacts file: {e}")

def initialize_contacts_file():
    """Initializes the contacts.json file with an empty list if it doesn't exist or is empty."""
    if not os.path.exists(CONTACTS_FILE) or os.path.getsize(CONTACTS_FILE) == 0:
        write_contacts_to_file([])

# --- Contact ID Generation ---
def generate_contact_id():
    """Generates a unique contact ID."""
    return uuid.uuid4().hex

# --- Flask Routes (API Endpoints) ---

@app.route('/contacts', methods=['GET'])
def get_contacts():
    """Reads all contacts and returns them as JSON."""
    contacts = read_contacts_from_file()
    return jsonify(contacts), 200

@app.route('/contacts', methods=['POST'])
def create_contact():
    """Creates a new contact."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    contacts = read_contacts_from_file()

    new_contact = {
        "ContactID": generate_contact_id(),
        "FirstName": data.get('FirstName'),
        "LastName": data.get('LastName'),
        "Email": data.get('Email'),
        "Phone": data.get('Phone'),
        "Company": data.get('Company'),
        "CreatedAt": datetime.datetime.utcnow().isoformat() + 'Z',
        "UpdatedAt": datetime.datetime.utcnow().isoformat() + 'Z'
    }

    # Basic validation
    if not new_contact['FirstName'] or not new_contact['LastName'] or not new_contact['Email']:
        return jsonify({"error": "FirstName, LastName, and Email are required"}), 400
    
    # Check for duplicate email
    if any(c['Email'] == new_contact['Email'] for c in contacts):
        return jsonify({"error": "Email already exists"}), 400


    contacts.append(new_contact)
    write_contacts_to_file(contacts)
    return jsonify(new_contact), 201

@app.route('/contacts/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Reads a single contact by its ID."""
    contacts = read_contacts_from_file()
    contact = next((c for c in contacts if c['ContactID'] == contact_id), None)
    if contact:
        return jsonify(contact), 200
    return jsonify({"error": "Contact not found"}), 404

@app.route('/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Updates an existing contact."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    contacts = read_contacts_from_file()
    contact_index = -1
    for i, c in enumerate(contacts):
        if c['ContactID'] == contact_id:
            contact_index = i
            break
    
    if contact_index == -1:
        return jsonify({"error": "Contact not found"}), 404

    # Check for duplicate email if email is being changed
    new_email = data.get('Email')
    if new_email and new_email != contacts[contact_index]['Email']:
        if any(c['Email'] == new_email and c['ContactID'] != contact_id for c in contacts):
            return jsonify({"error": "Email already exists for another contact"}), 400


    # Update fields
    contacts[contact_index]['FirstName'] = data.get('FirstName', contacts[contact_index]['FirstName'])
    contacts[contact_index]['LastName'] = data.get('LastName', contacts[contact_index]['LastName'])
    contacts[contact_index]['Email'] = data.get('Email', contacts[contact_index]['Email'])
    contacts[contact_index]['Phone'] = data.get('Phone', contacts[contact_index]['Phone'])
    contacts[contact_index]['Company'] = data.get('Company', contacts[contact_index]['Company'])
    contacts[contact_index]['UpdatedAt'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    # Basic validation for updated fields
    if not contacts[contact_index]['FirstName'] or not contacts[contact_index]['LastName'] or not contacts[contact_index]['Email']:
        return jsonify({"error": "FirstName, LastName, and Email are required"}), 400

    write_contacts_to_file(contacts)
    return jsonify(contacts[contact_index]), 200

@app.route('/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Deletes a contact."""
    contacts = read_contacts_from_file()
    original_length = len(contacts)
    contacts = [c for c in contacts if c['ContactID'] != contact_id]

    if len(contacts) == original_length:
        return jsonify({"error": "Contact not found"}), 404

    write_contacts_to_file(contacts)
    return jsonify({"message": "Contact deleted"}), 200 # Changed to 200 with message for easier frontend handling than 204

if __name__ == '__main__':
    initialize_contacts_file()
    app.run(debug=True, port=5001) # Running on a different port than default 5000
