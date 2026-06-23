FROM python:3.12-slim

WORKDIR /app

# -------------------------
# 1. System dependencies
# -------------------------
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    apt-transport-https \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# 2. Microsoft ODBC Driver (SQL Server)
# -------------------------
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && mv microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && curl -sSL https://packages.microsoft.com/config/debian/12/prod.list \
    > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# 3. Python dependencies
# -------------------------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# -------------------------
# 4. App code
# -------------------------
COPY . .

# -------------------------
# 5. Runtime config
# -------------------------
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]