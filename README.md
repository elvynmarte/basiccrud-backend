# BasicCRUD - Backend 🐍

**Python back-end API for the BasicCRUD React project.**

This repository provides the backend API service to handle basic CRUD (Create, Read, Update, Delete) operations, designed to be consumed by a separate frontend application, such as the associated BasicCRUD React project.

---

## 🚀 Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following software installed:

* **Python 3.x**
* **Git** (optional, for cloning)
* A virtual environment tool (**venv** or **conda** is recommended)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/elvynmarte/basiccrud-backend.git](https://github.com/elvynmarte/basiccrud-backend.git)
    cd basiccrud-backend
    ```

2.  **Create and activate a virtual environment (Recommended):**

    * **On Unix/macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows (Command Prompt):**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To start the API server:

```bash
python app.py
```
The API should then be accessible at http://localhost:5000/ (or the configured host/port).

1 **✨ Features:**
* **2RESTful API endpoints for standard CRUD operations.**
* **3Python-based server4 (utilizing a lightweight framework like Flask).**
* **Designed for easy integration with a separate frontend client (e.g., React, Vue, Angular).**
*
**🛠️ Tech Stack:**
* **Language:** PythonWeb
* **Framework:** Flask (Implicitly used based on common Python web services and file structure)
* **Dependencies:** As listed in requirements.txt.
  
**🗺️ API Endpoints**
The following are the typical RESTful endpoints provided by this backend. The resource name (/resources) may vary depending on the data model defined in app.py

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| POST | /get-login | email, passw | Authenticate user to log in. |
| GET | /get-users | N/D | Get all users data. |
| POST | /iu-user | name,email, passw, active, id | Insert / Update user. |
| POST | /reset-pass | passw, npassw, cpassw, id | Reset current password for user loged. |
| POST | /del-user | id | Delete a user by its ID. |
| GET | /get-items | N/D | Get all items. |
| POST | /iu-item | name, type,price,quantity,id | Insert / Update Item. |
| POST | /del-item | id | Delete a item by its ID. |
| GET | /get-types | N/D | Get all types. |
| POST | /iu-type | description,active, id | Insert / Update type. |
| POST | /del-type | id | Delete a type by its ID. |

**⚙️ Configuration**

* Review app.py for settings related to host/port, debug mode, and database connection strings.
* For production deployment, ensure debug mode is disabled and use a proper WSGI server (like Gunicorn or uWSGI) instead of running python app.py directly.
* Manage sensitive configurations (like database credentials) using environment variables.

