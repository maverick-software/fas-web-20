# Backend Structure Document

This document outlines the complete design, architecture, and components of the backend for our real-time AI-powered data visualization and manipulation tool. It is written in everyday language so that even non-technical readers can follow along with the overall setup.

## 1. Backend Architecture

- **Frameworks & Patterns:**
  - We are using FastAPI as our core web framework. FastAPI is known for its speed, asynchronous support, and overall simplicity which guarantees rapid responses even under load.
  - The pattern used borrows from a modular and loosely coupled design. This means each functionality (data upload, cleaning, command processing, and visualization) works as separate modules that communicate with each other in a predictable manner.
  - It incorporates ideas from the microservices approach though running as a single integrated service initially. This sets the stage for easy scalability and future separation if needed.

- **Scalability, Maintainability & Performance:**
  - The use of FastAPI and asynchronous operations means the system can handle multiple requests in parallel, ensuring quick responses.
  - Modules are designed to be independent and replaceable, enabling easy maintenance and upgrades.
  - Robust error handling and centralized logging further ensure that performance issues are quickly identified and resolved.

## 2. Database Management

- **Database Technology:**
  - We use CassandraDB as our database system. Cassandra is a NoSQL database that excels in handling flexible JSON storage while providing high scalability and availability.

- **Data Structure & Storage:**
  - The data from uploaded files (CSV, XLSX, etc.) is first converted into a structured format (for instance, a Pandas DataFrame) and then stored as JSON data.
  - This approach allows us to store complex datasets and easily retrieve them during operations such as cleaning and visualizations.
  - Data management practices include automatic flagging of inconsistencies and a record of cleaning actions performed on the dataset.

## 3. Database Schema

Since we are using CassandraDB, the schema is defined in terms of key spaces and column families rather than traditional tables. Here’s a human readable description along with an example layout:

- **Keyspace:** data_visualization_app

- **Column Families (Tables):**
  - **datasets**: 
    - Contains the dataset details after upload.
    - Fields include:
      - dataset_id: A unique identifier for each dataset
      - file_type: Type of upload (CSV, XLSX, etc.)
      - upload_time: Timestamp of when the dataset was uploaded
      - original_data: The raw JSON data
      - processed_data: The cleaned/processed JSON format after initial transformation
      - cleaning_log: A log recording the cleaning operations applied

  - **operations_log** (optional for tracking data modifications):
    - Contains a history log of natural language commands and modifications.
    - Fields include:
      - log_id: Unique operation identifier
      - dataset_id: Associated dataset
      - command: The natural language command provided
      - execution_time: Timestamp for the operation
      - result_summary: A brief summary of the changes

This design is flexible, allowing for additional fields if new features, such as voice commands or more intricate visual properties, need to be stored.

## 4. API Design and Endpoints

Our API follows RESTful design principles to facilitate smooth communication between the frontend and the backend. Key endpoints include:

- **POST /upload**
  - Purpose: Allow users to upload CSV or XLSX files.
  - Input: Multipart file upload.
  - Output: JSON response with dataset ID and details about the initial data structure.

- **POST /modify**
  - Purpose: Receives a dataset ID along with a natural language command. This lets our integrated AI engine (either using OpenAI API or a fine-tuned Llama model) modify the dataset.
  - Input: Dataset ID and user command in natural language.
  - Output: Updated dataset in JSON format along with a confirmation message.

- **GET /data**
  - Purpose: Retrieve the current state of the dataset.
  - Input: Dataset ID.
  - Output: The dataset in JSON format reflecting any modifications.

- **GET /visualize**
  - Purpose: Generate visualizations like bar charts, line graphs, or scatter plots based on the dataset.
  - Input: Dataset ID, desired chart type, and any optional visualization parameters.
  - Output: The rendered chart either as HTML (for embedding) or JSON (to be consumed by frontend libraries like Plotly).

## 5. Hosting Solutions

- **Hosting Environment:**
  - We plan to host the backend on a cloud provider that supports containerized applications (e.g., AWS, Google Cloud, or Azure). This makes scaling up straightforward as demand increases.

- **Benefits:**
  - **Reliability:** Cloud providers offer high uptime and robust infrastructure, ensuring the app is always available.
  - **Scalability:** Easy to add more resources like servers and load balancers on demand.
  - **Cost-Effectiveness:** We only pay for what we use, and serverless or managed container services reduce maintenance overhead.

## 6. Infrastructure Components

- **Load Balancers:**
  - To distribute incoming traffic evenly across multiple server instances. This prevents any single server from becoming a bottleneck.

- **Caching Mechanisms:**
  - A caching layer (using services like Redis or built-in caching mechanisms) can be used to store common queries or visualization templates, reducing load and speeding up responses.

- **Content Delivery Network (CDN):**
  - While the backend processes dynamic data, static assets like documentation, help pages, or even pre-rendered portions of the visualizations can be served via a CDN to reduce latency.

These components work in tandem to ensure high performance, smooth user experiences, and resilience against high traffic.

## 7. Security Measures

- **Authentication & Authorization:**
  - Given that the application is meant for local use without complex login requirements, we are not integrating heavy authentication. However, endpoints may implement basic checks to ensure correct data flow.

- **Data Encryption:**
  - Data in transit is encrypted using HTTPS to ensure that data uploaded or retrieved from our backend remains secure.
  - Sensitive data and logs (if any are stored) can be additionally encrypted at rest, especially within our cloud storage solutions.

- **Compliance:**
  - While the project currently does not have advanced user authentication, basic security measures ensure data integrity and privacy in line with modern web applications.

## 8. Monitoring and Maintenance

- **Monitoring Tools:**
  - Tools like Prometheus and Grafana can be integrated to constantly monitor system performance and health.
  - Logging will be centralised so that any issues can be reviewed and addressed promptly.
  - Regular audits and health checks are scheduled for the system to ensure stability, particularly as more features and modules get added.

- **Maintenance Strategies:**
  - Code updates, dependency management, and cloud infrastructure reviews are part of the routine maintenance.
  - Automated alerts for performance dips or failures help catch issues early and minimize downtime.

## 9. Conclusion and Overall Backend Summary

- The backend is built on FastAPI, leveraging its asynchronous capabilities and speed for a responsive user experience.
- Data is imported, cleaned, and managed in CassandraDB, with the use of flexible JSON storage supporting massive scalability.
- A simple, yet robust, API is set up to handle file uploads, natural language command processing, data retrieval, and visualization generation.
- Cloud hosting, along with infrastructure components like load balancers, CDNs, and caching, ensures the application performs well under load with improved reliability and scalability.
- Security measures ensure data privacy and integrity, while monitoring and maintenance practices keep the system running smoothly.

This setup not only meets the current project requirements but also positions the application for future enhancements such as additional file types, voice commands, collaborative features, and predictive insights. All these components work together to provide a seamless experience for non-technical users, making data analysis accessible and intuitive.

**Tech Stack Used in Backend:**
- FastAPI
- Pandas
- NumPy
- OpenAI API or fine-tuned Llama model
- CassandraDB

Overall, this backend structure is designed with simplicity, flexibility, and performance in mind, ensuring that the application meets both immediate and future needs.