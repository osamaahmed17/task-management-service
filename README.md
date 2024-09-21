<h1>Task Management API with Email Notifications</h1>
<p>This repository contains a simple Task Management API built with <strong>FastAPI</strong> and <strong>SQLite</strong>. The service allows users to perform &nbsp;CRUD operations (Create, Read, Update, Delete) on tasks, with email notifications upon task creation.</p>
<h2>Features</h2>
<ol>
    <li>
        <p><strong>CRUD Operations for Tasks</strong>:</p>
        <ul>
            <li><strong>Create a Task</strong>: Add a new task with a title, description, status, and due date.</li>
            <li><strong>Read Tasks</strong>: Retrieve all tasks or a specific task by its ID.</li>
            <li><strong>Update a Task</strong>: Modify a task&rsquo;s title, description, status, or due date.</li>
            <li><strong>Delete a Task</strong>: Remove a task by its ID.</li>
        </ul>
    </li>
    <li>
        <p><strong>Email Notifications</strong>:</p>
        <ul>
            <li>Upon task creation, an email is sent to the user with task details, such as title, description, and due date.</li>
        </ul>
    </li>
    <li>
        <p><strong>Task Filtering:</strong></p>
        <ul>
            <li>Filter tasks by their status (pending&quot;, &quot;completed&quot;, &quot;in_progress&quot;).</li>
        </ul>
    </li>
</ol>
<h2>Technology Stack</h2>
<ul>
    <li><strong>Backend Framework</strong>: FastAPI (Python)</li>
    <li><strong>Database</strong>: SQLite&nbsp;</li>
    <li><strong>Email Service</strong>: Integrated with Google OAuth2.0 and SMTP service for notifications</li>
    <li><strong>Docker</strong>: Dockerized application for easy setup and deployment</li>
</ul>
<h2>Requirements</h2>
<ul>
    <li>Python&nbsp;</li>
    <li>FastAPI</li>
    <li>SQLite3</li>
    <li>Redis&nbsp;</li>
</ul>
