# Deployment Guide: legal_doc_ai

## Local Docker

```bash
cd docker
docker-compose up --build
```

## Production Checklist

- [ ] Set `SECRET_KEY` and database credentials in environment
- [ ] Run database migrations
- [ ] Use a managed PostgreSQL instance
- [ ] Enable HTTPS
- [ ] Configure CORS origins
