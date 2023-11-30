#!/bin/bash
# Requires the database to be up
FLASK_ENV=development DATABASE_URI=postgresql://postgres:martinez@localhost:5432/BBDDFLASK python manage.py
