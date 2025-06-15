#!/bin/bash

mkdir -p app/{api/v1,services,repositories,models,schemas,db}

touch app/__init__.py
touch app/main.py

# API
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/user_controller.py

# Services
touch app/services/__init__.py
touch app/services/user_service.py

# Repositories
touch app/repositories/__init__.py
touch app/repositories/user_repository.py

# Models
touch app/models/__init__.py
touch app/models/user_model.py

# Schemas
touch app/schemas/__init__.py
touch app/schemas/user_schema.py
touch app/schemas/response_schema.py

# Database
touch app/db/__init__.py
touch app/db/base.py
touch app/db/session.py

echo "✅ FastAPI folder structure created."
