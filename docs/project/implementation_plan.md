# Implementation plan

## Phase 1: Environment Setup

1.  Create the project root directory named `ai-data-tool` to house the entire project. (PRD: Project Goal)
2.  Within `ai-data-tool`, create two subdirectories: `/frontend` for the React application and `/backend` for the FastAPI server. (PRD: Technical Requirements – Frontend & Backend)
3.  Verify that Node.js v20.2.1 is installed on your system. If not, install Node.js v20.2.1. **Validation:** Run `node -v` and ensure the output is v20.2.1. (Tech Stack: Core Tools)
4.  Verify that Python 3.11.4 is installed. If it is not installed, install Python 3.11.4. **Validation:** Run `python --version` and ensure it shows 3.11.4. (Tech Stack: Core Tools)
5.  Set up a local CassandraDB instance for database operations. You can run CassandraDB via Docker using the appropriate image. (Tech Spec: Database)
6.  **Validation:** Connect to the CassandraDB instance (using cqlsh or a similar tool) to verify connectivity.

## Phase 2: Frontend Development

1.  Initialize a new React project in the `/frontend` directory. Use Create React App by running `npx create-react-app .` from within `/frontend`. (PRD: UI/UX)
2.  Install Plotly.js and the React wrapper (react-plotly.js) by running `npm install plotly.js react-plotly.js` in the `/frontend` directory. **Validation:** Check that these packages appear in `package.json`. (Tech Spec: Interactive Data Visualization)
3.  In `/frontend/src/components`, create a new file `FileUpload.jsx`. Implement a file upload component supporting both drag-and-drop and file-picker functionality to accept CSV and XLSX files. (Core Feature: Data Import & Cleaning)
4.  **Validation:** Launch the development server (`npm start`) and confirm that the file upload component allows sample CSV/XLSX file selection.
5.  In `/frontend/src/components`, create `CommandInput.jsx` to serve as the UI for inputting natural language commands (e.g., "Filter entries below $1000"). (Core Feature: AI-Powered Data Manipulation)
6.  **Validation:** Type a sample command into the CommandInput component and verify its capture via a console log or state update.
7.  In `/frontend/src/components`, create `ChartView.jsx` and `DataTable.jsx` to display interactive charts and data tables respectively. (Core Feature: Interactive Data Visualization)
8.  In `/frontend/src`, update `App.css` (or a dedicated CSS/SCSS file) to add styles for a minimalist layout with dark mode support. (Core Feature: User Interface – Dark Mode)
9.  **Validation:** Run the React app and manually toggle between dark and light mode to verify proper styling.

## Phase 3: Backend Development

1.  In the `/backend` directory, initialize a Python virtual environment. (Tech Stack: Core Tools)
2.  Activate the environment and install required packages: run `pip install fastapi uvicorn pandas numpy cassandra-driver openai` to add FastAPI (for the server), Uvicorn (for async running), Pandas and NumPy (for data handling), the Cassandra driver, and OpenAI API client. (Tech Spec: Backend)
3.  In `/backend`, create a new file `main.py` which will hold the FastAPI app initialization. (PRD: API Endpoints)
4.  In `main.py`, implement the `POST /upload` endpoint. This endpoint should accept CSV/XLSX uploads, process them with Pandas to a structured DataFrame, and return a JSON response containing a dataset ID. (API Endpoints: /upload)
5.  **Validation:** Run the FastAPI server with `uvicorn main:app --reload` and use Postman or curl to post a sample file to `/upload` and confirm receipt of a dataset ID.
6.  In `main.py`, implement the `POST /modify` endpoint. This endpoint should receive a dataset ID along with a natural language command, use the OpenAI API (or an alternative AI engine) to parse and execute the command, and return the updated dataset as JSON. (API Endpoints: /modify)
7.  **Validation:** Use curl to send a dummy command with a dataset ID to `/modify` and verify that the response returns the modified dataset.
8.  In `main.py`, implement the `GET /data` endpoint, which retrieves the current state of a dataset based on the dataset ID input. (API Endpoints: /data)
9.  **Validation:** Test the `/data` endpoint using Postman to ensure it returns the expected JSON structure.
10. In `main.py`, implement the `GET /visualize` endpoint. This endpoint should accept parameters (dataset ID, chart type, and additional options) and generate a visualization using Plotly (or Matplotlib/Seaborn) that is returned (or rendered) appropriately. (API Endpoints: /visualize)
11. **Validation:** Call `/visualize` with sample parameters, and verify the output image or JSON response representing the chart.
12. In the `/backend` directory, create a file `db.py` to handle the connection with CassandraDB. Implement functions to store and retrieve datasets in JSON format. (Tech Spec: Database)
13. **Validation:** Execute a simple CRUD operation from `db.py` to ensure data can be stored and fetched from CassandraDB.

## Phase 4: Integration

1.  In `/frontend/src/services`, create `apiService.js` which will encapsulate API calls. Add an axios POST call from the file upload component to the `/upload` endpoint. (API Endpoints: /upload)
2.  **Validation:** Use browser developer tools to inspect the network request when a file is uploaded, ensuring proper communication with the backend.
3.  In `apiService.js`, add an axios POST method that connects the CommandInput component with the `/modify` endpoint. (API Endpoints: /modify)
4.  **Validation:** Trigger a natural language command from the UI and verify that the backend response is received correctly.
5.  In `apiService.js`, implement GET request methods that fetch updated data from `/data` and visualizations from `/visualize`, integrating them with the DataTable and ChartView components. (API Endpoints: /data, /visualize)
6.  **Validation:** Confirm that both data and visualizations update interactively in the UI after backend processing.
7.  Implement error handling logic in the frontend components so that any errors returned (with clear, minimalist messages) are displayed in the feedback panel. (Core Feature: AI-Powered Data Manipulation, UI/UX)
8.  **Validation:** Simulate an error scenario (e.g., incorrect file format or command) and verify that the UI shows a user-friendly error message.

## Phase 5: Deployment

1.  In `/backend`, create a run script (e.g., `run.sh`) that starts the FastAPI server using Uvicorn with the command: `uvicorn main:app --host 0.0.0.0 --port 8000`. (Deployment: Local Setup)
2.  In `/frontend`, update the `package.json` scripts to include a start command (`npm start`) for the React application. (Deployment: Local Setup)
3.  In the project root `ai-data-tool`, create a `README.md` file that documents installation, running instructions for both frontend and backend, and outlines the plan for future improvements. (PRD: Project Goal)
4.  (Optional/Future) Create Dockerfiles in both `/frontend` and `/backend` for containerized deployments. (Note: This step is for future microservice integration.)
5.  **Validation:** Run the backend with the run script and the frontend with `npm start`, then access the application via a web browser to verify overall functionality.
6.  In the project root, create a CI/CD configuration file (e.g., `.github/workflows/ci-cd.yaml`) that runs tests and builds on commits using a service like GitHub Actions. (Deployment: CI/CD Pipeline)
7.  **Validation:** Push a commit to trigger the CI/CD pipeline and check that all tests pass in the pipeline logs.

## Additional Testing and Documentation

1.  Write automated performance tests (using a tool like pytest for backend endpoints and Jest for frontend components) to ensure the AI processing time is less than 2 seconds (95th percentile) and visualization updates are processed within 1 second. (Non-Functional Requirements: Performance)
2.  **Validation:** Run the performance tests to confirm response times meet the requirements.
3.  Develop unit tests for backend data transformation functions to guarantee 100% transformation accuracy. (Non-Functional Requirements: Data Accuracy)
4.  **Validation:** Execute the tests (using pytest) and ensure all tests pass without any errors.
5.  Update the project documentation to list out-of-scope features (e.g., multi-user collaboration, complex authentication) and future enhancement ideas. (PRD: Out of Scope)
6.  **Validation:** Review the documentation with the team to confirm it accurately reflects the current scope and future plans.
7.  Conduct an end-to-end manual test: upload a sample data file, apply a natural language command, and render a visualization to verify the complete flow from frontend to backend. (PRD: Project Goal, Core Features)

End of Implementation Plan.
