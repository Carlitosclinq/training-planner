# Backend Training Planner

API FastAPI pour la gestion des entraînements.

## Structure

- `app/api/` : Routes de l'API
- `app/core/` : Configuration
- `app/models/` : Modèles SQLAlchemy
- `app/services/` : Services métier

## Installation

```bash
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sous Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```