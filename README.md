<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <p align="center">
    <img src="task-management-service.png" width="350" alt="accessibility text">
    </p>
    <h1>Task Management API with Email Notifications</h1>
    <p>This repository contains a simple Task Management API built with <strong>FastAPI</strong> and <strong>SQLite</strong>. The service allows users to perform CRUD operations (Create, Read, Update, Delete) on tasks, with email notifications upon task creation.</p>
    <h2>Features</h2>
    <ol>
        <li>
            <p><strong>CRUD Operations for Tasks</strong>:</p>
            <ul>
                <li><strong>Create a Task</strong>: Add a new task with a title, description, status, and due date.</li>
                <li><strong>Read Tasks</strong>: Retrieve all tasks or a specific task by its ID.</li>
                <li><strong>Update a Task</strong>: Modify a task’s title, description, status, or due date.</li>
                <li><strong>Delete a Task</strong>: Remove a task by its ID.</li>
            </ul>
        </li>
        <li>
            <p><strong>Email Notifications</strong>:</p>
            <ul>
                <li>Upon task creation, an email is sent to the user with task details such as title, description, and due date.</li>
            </ul>
        </li>
        <li>
            <p><strong>Task Filtering:</strong></p>
            <ul>
                <li>Filter tasks by their status ("pending", "completed", "in_progress")</li>
            </ul>
        </li>
    </ol>
    <h2>Technology Stack</h2>
    <ul>
        <li><strong>Backend Framework</strong>: FastAPI (Python)</li>
        <li><strong>Database</strong>: SQLite</li>
        <li><strong>Email Notification</strong>: Integrated with Google OAuth 2.0 and SMTP service for email notifications</li>
        <li><strong>Docker</strong>: Dockerized application for easy setup and deployment</li>
    </ul>
    <h2>Requirements</h2>
    <ul>
        <li>Python</li>
        <li>FastAPI</li>
        <li>SQLite3</li>
        <li>Redis</li>
    </ul>
    <h2>Installation and Configuration Guide</h2>
    <h3>1. Clone the Repository</h3>
    <p>Start by cloning the repository to your local machine:</p>
    <pre><code>git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api
    </code></pre>
    <h3>2. Set Up a Virtual Environment</h3>
    <p>It's a good practice to create a virtual environment to manage dependencies.</p>
    <p><strong>On macOS/Linux:</strong></p>
    <pre><code>python3 -m venv venv
source venv/bin/activate
    </code></pre>
    <p><strong>On Windows:</strong></p>
    <pre><code>python -m venv venv
venv\Scripts\activate
    </code></pre>
    <h3>3. Install Dependencies</h3>
    <p>Install the necessary Python packages listed in the <code>requirements.txt</code> file:</p>
    <pre><code>pip install -r requirements.txt
    </code></pre>
    <h3>4. Set Up Environment Variables</h3>
    <p>Create a <code>.env</code> file in the project root to store your environment variables, such as Redis host, email configurations, etc.</p>
    <pre><code>REDIS_HOST=localhost
REDIS_PORT=6379
EMAIL_HOST=smtp.your-email-service.com
EMAIL_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-email-password
    </code></pre>
    <h3>5. Run the Application Locally</h3>
    <p>Run the FastAPI application locally using Uvicorn:</p>
    <pre><code>uvicorn src.main:app --reload --env-file .env --host 0.0.0.0 --port 8000
    </code></pre>
    <p>The API should now be running at <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>.</p>
    <p>Access the API documentation at:</p>
    <ul>
        <li><strong>Swagger UI:</strong> <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></li>
        <li><strong>ReDoc:</strong> <a href="http://localhost:8000/redoc" target="_blank">http://localhost:8000/redoc</a></li>
    </ul>
    <h3>6. Configure Email Notifications</h3>
    <p>Ensure your email SMTP service is properly configured. The API will use this service to send task creation notifications. Add the SMTP settings in the <code>.env</code> file.</p>
    <h3>7. Database Configuration</h3>
    <p>The application uses <strong>SQLite</strong> by default. Make sure SQLite is installed on your system (it should come bundled with Python). The tasks are stored in an SQLite database.</p>
    <h3>8. Run the Application Using Docker</h3>
    <h4>Ensure Docker is Installed</h4>
    <p>Make sure Docker is installed on your machine. You can download it from <a href="https://www.docker.com/get-started" target="_blank">Docker’s official website</a>.</p>
    <h4>Build and Run with Docker Compose</h4>
    <p>Use the provided <code>docker-compose.yml</code> to build and run the app and Redis together:</p>
    <pre><code>docker-compose up --build
    </code></pre>
    <p>Once the containers are running, access the FastAPI app at <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>.</p>
    <h4>Stopping the Containers</h4>
    <p>To stop the Docker containers, run:</p>
    <pre><code>docker-compose down
    </code></pre>
    <h3>Troubleshooting</h3>
    <ul>
        <li><strong>Port Issues:</strong> If you encounter port binding issues (e.g., <code>port already in use</code>), ensure no other services are running on port 8000 (for FastAPI) or 6379 (for Redis).</li>
        <li><strong>Redis Connection Error:</strong> Ensure Redis is running and <code>REDIS_HOST</code> is correctly set.</li>
        <li><strong>Email Notifications:</strong> Ensure your SMTP email service is correctly configured with valid credentials.</li>
    </ul>
</body>
</html>
