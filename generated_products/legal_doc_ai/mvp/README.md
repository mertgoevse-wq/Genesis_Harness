# MVP: Legal Doc AI

Generated autonomously by Genesis OS MVP Builder.

## Local Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## Run Tests

```bash
cd backend
pytest
```

## Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md).
