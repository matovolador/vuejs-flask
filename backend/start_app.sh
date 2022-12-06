#!/bin/bash
alembic upgrade head || exit 1
# coverage run tests.py || exit 1
# coverage xml
# coverage lcov
# coverage html
# genbadge coverage -i - < /app/coverage/coverage.xml -o /app/coverage/coverage-badge.svg
cron && tail -f /var/log/cron.log &
gunicorn --workers 3 --bind 0.0.0.0:5050 --timeout 50 app:app