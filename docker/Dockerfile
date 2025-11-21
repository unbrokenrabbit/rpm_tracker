# Dockerfile for nexus-populator service
FROM almalinux:8.10-20251117

# Set working directory
WORKDIR /app

# Install Python and system dependencies
RUN dnf install -y --setopt=tsflags=nodocs \
    python3 \
    python3-pip \
    && dnf clean all \
    && rm -rf /var/cache/dnf

# Copy requirements file (if exists)
# COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY project/main.py .
COPY docker/entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port if needed
# EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
