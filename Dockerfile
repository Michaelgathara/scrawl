# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN pip install uv
RUN uv pip install --system

# Copy the application files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port for API or testing (optional)
EXPOSE 8000

# Default command
CMD ["uv", "run", "pytest", "-v"]

