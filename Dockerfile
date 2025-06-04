FROM python:3-alpine

WORKDIR /app

RUN apk add --no-cache curl

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only needed files explicitly
COPY entrypoint.sh scheduler.py notifier.py token_manager.py state_manager.py ./

RUN chmod +x entrypoint.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
