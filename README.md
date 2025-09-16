# BeatStack

BeatStack is a web app dashboard that enables music producers to seamlessly publish their beats to YouTube.  
The backend is built with **FastAPI** and integrates **Google OAuth2** for secure authentication, while also providing endpoints for uploading audio + cover art and automatically converting them into video files for publishing.

---

## Features

- **Google OAuth2 Authentication**  
  - Secure sign-in and token exchange with Google APIs.  
  - Handles access token validation, refresh token persistence, and user identity verification.  

- **Media Upload & Processing**  
  - Upload audio and cover art files directly through the dashboard.  
  - Automatically combines audio + image into a publish-ready MP4 video.  
  - Uses async background tasks for processing and automatic cleanup of temporary files.  

- **REST API Design**  
  - FastAPI-powered endpoints for authentication and uploads.  
  - Structured error handling and extensibility for future integrations.  

---

## Tech Stack

- **Backend:** FastAPI (Python)  
- **Authentication:** OAuth2 (Google APIs)  
- **Video Conversion:** Custom media processing with background tasks library 
- **Deployment:** Docker-ready (customizable for cloud services)  

