#!/bin/bash
service nginx start
gunicorn app:app