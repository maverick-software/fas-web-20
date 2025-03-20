# Project Requirements Document (PRD)

## 1. Project Overview

This project is an AI-powered real-time data visualization & manipulation tool built to simplify and speed up data analysis. The tool allows users to upload datasets (initially CSV and XLSX files) and automatically converts them into a structured format. It then cleans the data by identifying issues like missing values and duplicates, and provides one-click fixes. The core innovation lies in using natural language commands to drive data transformations, so even non-technical users can filter, sort, and create new data columns with ease. Moreover, dynamic visualizations update instantly, giving users immediate feedback on their changes.

The primary purpose is to empower financial analysts, business professionals, and similar users to derive insights from data without needing advanced technical skills. It’s being built to eliminate the friction commonly associated with traditional data processing tools by automating cleaning, manipulation, and visualization tasks. Success will be measured by reduced time from data upload to actionable insights, high user satisfaction via a clean and minimalist interface (including dark mode), and the system’s ability to process user commands in under two seconds with visual updates in less than one second.

## 2. In-Scope vs. Out-of-Scope

**In-Scope:**

*   Data upload from CSV and XLSX files using a drag-and-drop or file selection interface.
*   Automatic data preprocessing and cleaning (e.g., flagging missing values, duplicates, and mismatched data types).
*   Enable natural language input for data manipulation (filtering, sorting, column creation, aggregation).
*   Real-time, interactive data visualizations (bar charts, line graphs, scatter plots, histograms) with minimal lag.
*   A clean, minimalist user interface designed for local use with dark mode preferences.
*   API endpoints for data upload, command execution, data retrieval, and visualization rendering.
*   Use of a scalable backend (FastAPI) with necessary Python data processing libraries (Pandas, NumPy) and integration with an AI engine (OpenAI API or Llama model).

**Out-of-Scope:**

*   Multi-user collaboration features (such as real-time editing and conflict resolution) – these are planned for future enhancements.
*   Complex authentication or login systems; the tool is designed for local use without user security layers.
*   Support for additional file types beyond the core CSV/XLSX; however, the design should allow adding more file types later.
*   Advanced third-party integrations such as external cloud storage or analytics services, beyond the current use of CassandraDB.

## 3. User Flow

A typical user will launch the application locally in their web browser, which will open in dark mode and display a clear, minimalist interface. The first impression is a dedicated area for file upload and a prominently placed command input field. The user simply drags and drops the dataset (CSV or XLSX) or selects it via a file-picker interface. Once the dataset is uploaded, the system preprocesses the data, cleans inconsistencies such as missing values and duplicates, and immediately displays an updated table view alongside an initial visualization of the data.

After preprocessing, the user interacts with the dataset by entering simple natural language commands in the command input box. For instance, the user may type “Filter entries below $1000” or “Create a new column for total revenue.” The AI engine processes these commands, instantly updating both the table view and the visualization area with detailed and highlighted feedback in a minimalist notification panel. The interactive visualizations support actions like zooming, panning, and displaying tooltips for enhanced clarity. Finally, when satisfied with the analysis, the user easily exports the modified dataset or visualization in various formats like CSV, XLSX, PNG, or PDF.

## 4. Core Features

*   **Data Import & Cleaning**

    *   Support CSV and XLSX file uploads via a drag-and-drop or file-picker interface.
    *   Automatically preprocess and convert uploaded files into a structured format (like a Pandas DataFrame or JSON).
    *   Detect and flag data inconsistencies (missing values, duplicates, wrong data types) and provide one-click solutions.

*   **AI-Powered Data Manipulation**

    *   Accept natural language commands such as “Filter entries below $1000” or “Create a new column for total revenue.”
    *   Use an AI engine (e.g., OpenAI API or a fine-tuned Llama model) to parse and execute data operations.
    *   Handle operations including filtering, sorting, aggregation, column creation, and basic cleaning.
    *   Provide clear and minimalist error messages when commands are ambiguous or invalid.

*   **Interactive Data Visualization**

    *   Generate dynamic charts including bar graphs, line charts, scatter plots, and histograms.
    *   Enable interactive controls like zooming, panning, and tooltips.
    *   Update visualizations in real time (ideally within <1 second) as the dataset is modified.
    *   Allow customization of visual elements (colors, axis labels, titles) via direct commands or sidebar options.

*   **User Interface & Experience**

    *   Web-based application with a clean, minimalist layout and responsive design optimized for dark mode.
    *   Dedicated panels for data upload, command entry, table view, visualization area, and highlighted feedback.
    *   A beginner-friendly design focusing on minimal steps, clear icons, and straightforward instructions.

*   **API Integration and Technical Architecture**

    *   A set of API endpoints for file uploads, natural language command processing, data retrieval, and visualization rendering.
    *   Modular architecture that allows for easy addition of new file types and future functionalities.

## 5. Tech Stack & Tools

*   **Frontend:**

    *   Frameworks: Streamlit (for rapid prototyping) or React with Plotly for advanced interactivity.
    *   Visualization Libraries: Plotly for interactive visualizations and Matplotlib/Seaborn for static exports.
    *   UI Preferences: Dark mode design with minimalist, responsive layout.

*   **Backend:**

    *   API Framework: FastAPI (preferred for speed and asynchronous support) or Flask (for simplicity).
    *   Data Processing: Python libraries such as Pandas, NumPy for data manipulation.
    *   AI Integration: OpenAI API for natural language processing or optionally a fine-tuned Llama model.

*   **Database:**

    *   Primary Data Storage: CassandraDB for handling flexible JSON storage and future scalability.

*   **Development Tools:**

    *   IDE Integration: Cursor (for advanced AI-powered coding with real-time suggestions).

## 6. Non-Functional Requirements

*   **Performance:**

    *   AI command processing should execute under 2 seconds (95th percentile).
    *   Visualization updates must occur in less than 1 second after data changes.
    *   Maintain 100% accuracy in applying user-requested data transformations.

*   **Security & Compliance:**

    *   Data encryption at rest (AES-256) and in transit (TLS 1.3) for secure handling.
    *   Minimal authentication as the application is intended for local use without login requirements.
    *   Rate limiting may be considered in future versions once multi-user scenarios are introduced.

*   **Usability:**

    *   The interface should be intuitive, requiring minimal training for non-technical users.
    *   Provide clear, highlighted, and minimalist feedback messages for both successful operations and errors.

*   **Scalability:**

    *   Handle future integration of larger datasets and additional file formats with minimal changes to the core architecture.

## 7. Constraints & Assumptions

*   The application will start locally and be accessible through a web browser, eliminating the need for complex authentication.
*   The initial file formats supported are CSV and XLSX; the system is built to allow easy addition of other file types in the future.
*   We assume that the AI engine (using OpenAI API or a fine-tuned Llama model) is readily available and performs at the expected response times.
*   CassandraDB is used from the start; adjustments might be required if scaling or additional integrations are pursued.
*   The tool is aimed at non-technical users, so natural language processing must remain simple and forgiving.

## 8. Known Issues & Potential Pitfalls

*   **AI Misinterpretation:** There is a risk that the natural language commands might be misinterpreted. To mitigate this, clear and immediate feedback should be provided, with suggestions for correction where ambiguity is detected.
*   **Performance Degradation:** While performance goals are set (AI commands under 2 seconds, visualization updates under 1 second), extremely large datasets (e.g., millions of rows) may affect speed. Early performance testing and optimization, such as lazy loading and batch processing, will be essential.
*   **Browser Compatibility:** Although the tool is designed for modern browsers (Chrome, Firefox, Safari), minor compatibility issues may arise with new browser versions, necessitating ongoing testing.
*   **Extensibility:** Adding support for additional file types later might require adjustments in the preprocessing logic and data parsing modules. Designing a modular file handler from the start will help streamline this.
*   **Local Deployment Constraints:** Since the application is intended for local use, network-related constraints (e.g., API call limitations) are minimized. However, any future move to a cloud environment would require revisiting the security and scalability mechanisms.

This document provides a detailed and unambiguous reference for the AI-powered data visualization tool’s project requirements. All subsequent documents (Tech Stack Document, Frontend Guidelines, Backend Structure, etc.) should refer to this PRD as the single source of truth.
