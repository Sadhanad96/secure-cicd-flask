#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:8000 app:app --workers 2 --threads 2
