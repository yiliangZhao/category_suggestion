#!/bin/bash
gunicorn --graceful-timeout 600 --timeout 600 -w 15 -b 0.0.0.0:32143 web_service_category_online:app
