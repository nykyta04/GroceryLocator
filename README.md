# ITSC-4155-002-Team-9


## Team Members (Group 9):
Divine Mobote
Wending Fang
Giani Hill
Nykyta Fedchenko
Onyae' Stewart

---

## Description
This project is a full-stack web application that allows users to compare grocery prices across multiple stores, view item availability, build a grocery list, and sort stores by total price.
Built with Django REST Framework (backend) and React (Vite) (frontend).

This README covers how to set up, run, and understand the project structure.

---

## How to Run
Backend:
- cd backend/django_app
- Activate venv:

    python -m venv .venv
    .\.venv\Scripts\activate   (Windows)
    source .venv/bin/activate  (Mac/Linux)
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver


Frontend
- cd frontend/grocery-app
- npm install
- npm run dev

---

## Running test

- python manage.py test

The project includes:
- CRUD tests
- Search & sorting tests
- Store hours tests
- Distance & pgeocode tests
- Store-selection tests

All tests currently pass.

---

## Features

Backend (Django REST API):
- Store CRUD (with hours, distance, coordinates)
- Item & GroceryItem CRUD
- Search by item name or brand (case-insensitive, sorting included)
- “Sort List” endpoint calculates total grocery list price across stores
- Store selection confirmation (/by-store/:id)
- Distance sorting using ZIP code
- Full suite of automated API tests (31 tests)


Frontend (React):
- Search items
- Search by brand
- Filter search by dietary restrictions
- Add/remove items from list
- Calculate grocery items
- View cheapest store with items
- View all stores
- Display price results
- Clean component-based architecture

---

## Project Structure:
ITSC-4155-002-Team-9/
│
├── backend/
│   └── django_app/
│       ├── api/
│       │   ├── migrations/
│       │   │   └── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       │
│       ├── django_app/
│       │   ├── __init__.py
│       │   ├── asgi.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       │
│       ├── sql/
│       │   └── initialize_fullstack_db.sql
│       │
│       ├── manage.py
│       └── requirements.txt
│
├── frontend/
│   └── grocery-app/
│       ├── node_modules/
│       ├── public/
│       │   └── vite.svg
│       │
│       ├── src/
│       │   ├── assets/
│       │   │   ├── clock.png
│       │   │   ├── listview.png
│       │   │   ├── pin.png
│       │   │   ├── search.png
│       │   │   ├── storePin.png
│       │   │   └── Stores.png
│       │   │
│       │   ├── components/
│       │   │   ├── ListItem.jsx
│       │   │   ├── Navbar.jsx
│       │   │   ├── SearchItem.jsx
│       │   │   └── SearchResults.jsx
│       │   │
│       │   ├── context/
│       │   │   └── (context files)
│       │   │
│       │   ├── pages/
│       │   │   ├── Search.jsx
│       │   │   ├── StoreBreakdown.jsx
│       │   │   ├── Stores.jsx
│       │   │   ├── ViewList.jsx
│       │   │   └── ViewTotal.jsx
│       │   │
│       │   ├── styles/
│       │   │   └── index.css
│       │   │
│       │   ├── App.jsx
│       │   ├── items.js
│       │   └── main.jsx
│       │
│       ├── .env
│       ├── index.html
│       ├── package.json
│       ├── package-lock.json
│       ├── vite.config.js
│       ├── eslint.config.js
│       └── README.md
│
└── .gitignore

---

## API Endpoints Overview

Stores:
- GET /api/stores/
- GET /api/stores/<id>/
- GET /api/stores/nearest/?zip=xxxxx
- GET /api/stores/nearby/?zip=xxxxx&radius=x

Items:

- GET /api/items/
- POST /api/items/

Grocery Items:

- GET /api/grocery-items/
- GET /api/grocery-items/search/?q=milk&sort=brand
- GET /api/grocery-items/by-store/<store_id>/

Sort List:
- POST /api/sort-lists/

---

# Included
- Full backend and frontend source code
- SQL database export
- All migrations
- Complete API and unit tests

---
