# PresenceIQ

**PresenceIQ** is an AI-powered attendance automation system that combines real-time facial recognition with intelligent workflows to streamline employee tracking, minimize manual HR work, and provide actionable insights to management.

---

## Features

- **Facial Recognition Check-In/Out**: Detects and logs employee presence using the webcam and DeepFace.
- **Automated Attendance Logging**: Updates a connected PostgreSQL database with daily records via n8n workflows.
- **Absence & Late Tracking**: Identifies employees who are absent or late and tracks violation patterns.
- **Warning & Escalation System**: Automatically emails warnings and escalates frequent violations to admins.
- **Weekly AI-Generated Reports**: Uses Groq’s LLaMA3 model to summarize weekly attendance trends for HR.

---

## Tech Stack

- **Python** – Real-time face recognition (`DeepFace`, `OpenCV`)
- **n8n** – Workflow automation and logic handling
- **PostgreSQL** (via Neon) – Cloud-hosted attendance database
- **Groq LLM** – Weekly report generation using LLaMA3-70B
- **Gmail API** – Automated warning and summary emails

---

## Files

- **n8n Workflow.json**: The exported workflow from n8n platform.
- **employee_pics**: Sample images of employees & weights for the facial recognition model
- **face_id.py**: Script for detection of employee and triggerring workflow activation
