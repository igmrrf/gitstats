
FROM python:3.13-slim

RUN apt update && apt install -y make && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set execute permissions for the entrypoint script
RUN chmod +x entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["/src/entrypoint.sh"]

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

