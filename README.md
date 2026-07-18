# Plannery Backend

API REST construida con FastAPI para la aplicación Plannery — una plataforma donde los usuarios guardan lugares para visitar y un agente de IA les recomienda planes personalizados en Bogotá.

## Tecnologías

- **FastAPI** — framework web para construir la API
- **Uvicorn** — servidor ASGI para correr FastAPI
- **Firebase Admin SDK** — conexión con Firestore para guardar planes
- **httpx** — cliente HTTP async para llamar a Google Places API
- **Groq** — modelo de IA para el chat de recomendaciones
- **python-dotenv** — manejo de variables de entorno

## Estructura del proyecto

```
plannery-backend/
├── app/
│   ├── main.py                  # Punto de entrada — configura CORS, Firebase y rutas
│   ├── routes/
│   │   ├── places.py            # POST /places/search
│   │   ├── plans.py             # POST, GET, DELETE /plans
│   │   └── chat.py              # POST /chat
│   ├── models/
│   │   ├── places.py            # PlaceSearchRequest, PlaceResult
│   │   ├── plans.py             # PlanCreate, PlanResponse
│   │   └── chat.py              # ChatRequest, ChatResponse
│   └── services/
│       ├── firebase_service.py  # Inicialización de Firebase
│       ├── places_service.py    # Lógica de Google Places API + descripciones con Groq
│       ├── plans_service.py     # CRUD de planes en Firestore
│       └── chat_service.py      # Agente de IA con Groq
├── serviceAccount.json          # Credenciales Firebase (no incluido en el repo)
├── .env                         # Variables de entorno (no incluido en el repo)
├── .gitignore
└── requirements.txt
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Verifica que el servidor está activo |
| POST | `/places/search` | Busca lugares en Bogotá usando Google Places API |
| POST | `/plans/` | Guarda un lugar como plan en Firestore |
| GET | `/plans/{userId}` | Devuelve todos los planes de un usuario |
| GET | `/plans/{userId}/count` | Devuelve el total de planes de un usuario |
| DELETE | `/plans/{planId}` | Elimina un plan por ID |
| POST | `/chat/` | Envía un mensaje al agente de IA Plannery |

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con estas variables:

```env
GOOGLE_PLACES_API_KEY=tu_api_key_de_google
FIREBASE_CREDENTIALS=serviceAccount.json
GROQ_API_KEY=tu_api_key_de_groq
```

En producción (Render), configura estas mismas variables en el dashboard de Environment. Para `FIREBASE_CREDENTIALS`, pega el contenido completo del JSON en vez de la ruta del archivo.

## Instalación y uso local

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/plannery-backend.git
cd plannery-backend

# 2. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env con las variables indicadas arriba

# 5. Correr el servidor
uvicorn app.main:app --reload
```

El servidor corre en `http://localhost:8000`.
La documentación interactiva está disponible en `http://localhost:8000/docs`.

## Despliegue

El backend está desplegado en **Render**.

El frontend está desplegado en **Vercel**: [clone-plannery.vercel.app](https://clone-plannery.vercel.app)

## Funcionalidades principales

**Búsqueda de lugares**
Recibe un texto de búsqueda y devuelve lugares reales en Bogotá con nombre, dirección, coordenadas, rating, foto, categoría y una descripción generada por IA.

**Gestión de planes**
Los usuarios pueden guardar, consultar y eliminar lugares en su lista de planes, almacenados en Firestore.

**Chat con IA**
Un agente de IA llamado Plannery recibe el mensaje del usuario junto con su lista de planes guardados y genera recomendaciones personalizadas en español basadas en su conocimiento de Bogotá.