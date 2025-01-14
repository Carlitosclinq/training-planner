# Documentation API

## Authentification

### POST /api/auth/login
Connexion avec les identifiants intervals.icu

**Request body:**
```json
{
    "intervals_athlete_id": "string",
    "intervals_api_key": "string"
}
```

**Response:**
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

## Objectifs

### GET /api/goals
Récupérer la liste des objectifs

**Response:**
```json
[
    {
        "id": "integer",
        "type": "string",
        "target_date": "date",
        "target_value": "number",
        "description": "string"
    }
]
```

### POST /api/goals
Créer un nouvel objectif

**Request body:**
```json
{
    "type": "string",
    "target_date": "date",
    "target_value": "number",
    "description": "string"
}
```

## Activités

### GET /api/activities
Récupérer les activités synchronisées

**Query parameters:**
- start_date (optional): Date de début (YYYY-MM-DD)
- end_date (optional): Date de fin (YYYY-MM-DD)

**Response:**
```json
[
    {
        "id": "string",
        "type": "string",
        "start_date": "datetime",
        "distance": "number",
        "duration": "number",
        "power": {
            "normalized": "number",
            "average": "number"
        }
    }
]
```

## Planification

### POST /api/training-plans
Générer un plan d'entraînement

**Request body:**
```json
{
    "goal_id": "integer",
    "start_date": "date",
    "end_date": "date",
    "preferences": {
        "weekly_hours": "number",
        "max_session_duration": "number"
    }
}
```

**Response:**
```json
{
    "id": "integer",
    "workouts": [
        {
            "date": "date",
            "type": "string",
            "duration": "number",
            "description": "string",
            "target_power": "number"
        }
    ]
}
```

## Prédictions

### GET /api/predictions/ftp
Prédire le FTP futur

**Query parameters:**
- target_date: Date cible (YYYY-MM-DD)

**Response:**
```json
{
    "current_ftp": "number",
    "predicted_ftp": "number",
    "confidence": "number"
}
```

### GET /api/predictions/race-time
Prédire un temps de course

**Query parameters:**
- distance: Distance en mètres
- elevation: Dénivelé en mètres

**Response:**
```json
{
    "predicted_time": "number",
    "predicted_power": "number",
    "confidence": "number"
}
```