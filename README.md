# Comment Management Service Documentation

## Overview
This documentation provides an overview of the components, Docker configurations, and FastAPI endpoints implemented in the `comment_mgmt_service` for the BQP Assignment platform. The service is designed to manage comments efficiently, enabling users to post, view, update, and delete comments in a scalable manner.

## Directory Structure

    /comment_mgmt_service
    ├── /compose
    │   └── /local
    │       ├── Dockerfile             # Dockerfile to build the Docker image
    │       └── start                  # Startup script to launch the FastAPI server
    ├── /src
    │   ├── database.py                # Defines database models and configurations
    │   ├── main.py                    # FastAPI application entry point
    │   ├── requirements.txt           # Lists Python dependencies
    │   ├── utils.py                   # Contains utility classes for external interactions
    │   └── /config
    │       ├── .env                   # Stores environment variables
    │       └── constants.py           # (Optional) Stores constants used across the application
    └── local.yml                      # Docker Compose configuration for local development

## Components

### Docker Configuration
- **File**: `local.yml`
- **Description**: Configures the Docker environment for the comment management service, setting up the necessary service parameters, exposed ports, and volume mappings for development.

### Dockerfile
- **Location**: `compose/local/Dockerfile`
- **Purpose**: Builds the Docker image for the service, installing required Python packages and setting up the environment.

### Startup Script
- **File**: `compose/local/start`
- **Purpose**: Executes the FastAPI application using Uvicorn with specified host and port configurations. It ensures that the service reloads automatically during development when changes are detected.

## Source Code Files

### Main Application (FastAPI)
- **File**: `src/main.py`
- **Functionality**:
  - Entry point for the FastAPI application.
  - Defines routes for CRUD operations on comments.
  - Handles application middleware configurations.

### Database Configuration
- **File**: `src/database.py`
- **Functionality**:
  - Establishes database connections using SQLAlchemy.
  - Defines ORM models for the comments.
  - Manages database session creation and closure.

### Utility Functions
- **File**: `src/utils.py`
- **Functionality**:
  - `NotifierClient`: Manages asynchronous notification sending when comments are posted.
  - `UserProfileClient`: Fetches user profile information from an external authentication service.

### Python Requirements
- **File**: `src/requirements.txt`
- **Details**: Includes all necessary Python libraries such as FastAPI, Uvicorn, SQLAlchemy, and others required to run the comment management service.

## Configuration Files

### Environment Variables
- **File**: `src/config/.env`
- **Contains**:
  - Google client credentials for integration with Google services (if required).
  - Other sensitive keys and secrets required for the operation of the service.

### Constants
- **File**: `src/config/constants.py`
- **Description**: This file can store constant values used throughout the application, although it is optional and currently empty.

## Setup and Deployment
To deploy the comment management service locally using Docker:
1. Navigate to the service directory:
    ```bash
    cd /path/to/comment_mgmt_service
    ```
2. Build and run the Docker container:
    ```bash
    docker-compose -f local.yml up --build
    ```

This setup ensures that the comment management service is properly configured and ready for integration with other services or for standalone functionality as part of the BQP Assignment platform.
