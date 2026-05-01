# Journezy Frontend

This is the Next.js frontend for the Journezy Trip Planner.

## Prerequisites

- Node.js 18+ installed on your machine.
- Python 3.10+ (for the backend).

## Setup Instructions

1.  **Install Dependencies**:
    Open a terminal in this `frontend` directory and run:

    ```bash
    npm install
    # or
    yarn install
    # or
    pnpm install
    ```

2.  **Start the Backend**:
    In a separate terminal (in the root `journezy-trip-planner-main` directory), start the Python backend:

    ```bash
    uvicorn main:app --reload
    ```
    Ensure the backend is running on `http://127.0.0.1:8000`.

3.  **Start the Frontend**:
    In the `frontend` terminal, run:

    ```bash
    npm run dev
    ```

4.  **Open the App**:
    Open your browser and navigate to `http://localhost:3000`.

## Features

- **Home Page**: Beautiful animated landing page.
- **Planner**: Comprehensive form to collect trip details.
- **Itinerary**: Dashboard to view the AI-generated trip plan, flights, hotels, and places.
- **PDF Export**: Download your itinerary as a PDF.
