FROM --platform=linux/amd64 python:3.11 as build

WORKDIR /app


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]



