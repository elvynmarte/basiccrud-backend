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
