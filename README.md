# ElectraMind AI

An AI-powered Electrical Machines Question Answering Platform built using Django, MySQL, and Groq AI.

The application allows users to register, log in securely, ask questions related to electrical machines, receive AI-generated answers, and maintain a history of previous questions and responses.

---

## Project Overview

ElectraMind AI is designed to assist students, engineers, and learners in understanding electrical machine concepts through an intelligent question-answering system.

The platform combines:

- Secure user authentication
- AI-powered answer generation
- Question history tracking
- Database persistence
- Modern responsive user interface

---

## Features

### User Management

- User Registration
- User Login
- User Logout
- Session Management
- Protected Routes

### AI Question Answering

- Ask questions related to:
  - Transformers
  - Motors
  - Generators
  - Alternators
  - Electrical Machines
- AI-generated responses using Groq LLM
- Structured answer formatting

### History Management

- Stores user questions
- Stores AI-generated answers
- View previous questions
- Search through question history

### Database Integration

- MySQL database
- Persistent storage of:
  - Users
  - Questions
  - Answers
  - Timestamps

### User Interface

- Modern dark theme
- Responsive design
- Professional dashboard layout
- Clean answer presentation

---

## Tech Stack

### Backend

- Python
- Django

### Database

- MySQL

### AI Integration

- Groq API
- Llama Model

### Frontend

- HTML5
- CSS3
- Bootstrap

### Authentication

- Django Authentication System

---

## Project Structure

```text
electrical-machines-qa/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│
├── qa/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── groq_service.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── ask_question.html
│   ├── history.html
│
├── requirements.txt
├── manage.py
└── README.md
```

---

## Workflow

1. User registers an account.
2. User logs into the system.
3. User submits an electrical machines question.
4. Question is sent to Groq AI.
5. AI generates a response.
6. Question and answer are stored in MySQL.
7. User can review previous interactions in the History page.

---

## Key Functionalities Implemented

- Secure Authentication
- AI Integration using Groq
- Question Storage
- Answer Storage
- Question History
- Search Functionality
- Responsive UI Design
- MySQL Connectivity

---

## Future Enhancements

- PDF Notes Generation
- Export Question History
- Voice-based Question Input
- Admin Dashboard
- Bookmark Important Answers
- Topic-wise Categorization
- Advanced Search and Filtering

---

## Status

Completed and fully functional.
