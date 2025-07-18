# Use a minimal base image with Python 3.11
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies required for compiling packages
#    - gcc: Compiler for building Python packages
#    - libmysqlclient: Required for MySQL/MariaDB integration
#    - pkg-config: Helps detect and configure packages
#    - netcat-openbsd: Needed for wait-for-db.sh to check database readiness
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && apt-get clean

# Copy and install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#  Copy the entire project into the container
COPY . .

#  Add and make the wait-for-db script executable
#     This ensures Django doesn't start until the database is ready
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Start the Django server after confirming the DB is available
CMD ["/wait-for-db.sh", "db", "python3", "news_project/manage.py", "runserver", "0.0.0.0:8000"]
