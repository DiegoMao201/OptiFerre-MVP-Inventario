# Migración a SaaS profesional (FastAPI + Next.js 14)

Esta carpeta documenta el nuevo stack que reemplaza a Streamlit. La lógica de
negocio (`core/`, `services/`, `engine/`) se mantiene intacta y se reutiliza
desde el nuevo backend `api/`.

## Estructura final

```
api/                       # Backend FastAPI
├── main.py                # entrypoint (uvicorn api.main:app)
├── deps/security.py       # JWT + get_current_user
├── routes/                # endpoints REST
│   ├── auth.py            # /auth/login /auth/register /auth/me
│   ├── inventory.py       # /inventory/upload
│   ├── analysis.py        # /analysis/run
│   ├── dashboard.py       # /dashboard/summary
│   ├── products.py        # /products/dead /products/opportunities
│   └── purchase_orders.py # /purchase-orders /purchase-orders/generate
├── services/analysis_runner.py  # orquesta full_analysis sobre snapshots DB
└── schemas/               # contratos Pydantic

web/                       # Frontend Next.js 14 (App Router)
├── src/app/
│   ├── page.tsx           # landing pública (CRO ferretero)
│   ├── login/page.tsx
│   ├── register/page.tsx
│   └── app/               # área autenticada
│       ├── layout.tsx     # AuthGate + AppShell
│       ├── page.tsx       # dashboard (KPIs)
│       ├── dead-products/page.tsx
│       ├── opportunities/page.tsx
│       ├── upload/page.tsx
│       └── purchase-orders/page.tsx
├── src/components/        # UI base (shadcn-style)
├── src/lib/               # api client, auth storage, query provider
├── tailwind.config.ts
├── package.json
└── next.config.js

Dockerfile.api             # imagen FastAPI (uvicorn)
Dockerfile.web             # imagen Next.js (standalone)
docker-compose.yml         # api + web (+ legacy streamlit con profile=legacy)
```

## Cómo correrlo en local

### 1. Backend (FastAPI)

```bash
cd "/Users/diegogarcia/Aplicaciones IA/MVP INVENTARIOS"
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=sqlite:///optiferre.db
export APP_SECRET_KEY=cambia-esto-en-produccion
alembic upgrade head
uvicorn api.main:app --reload --port 8000
# Swagger en http://localhost:8000/docs
```

### 2. Frontend (Next.js)

```bash
cd web
cp .env.example .env.local   # ajusta NEXT_PUBLIC_API_URL si necesitas
npm install
npm run dev
# http://localhost:3000
```

## Cómo desplegarlo en Coolify (Docker Compose)

1. Apunta Coolify al repo y selecciona `docker-compose.yml`.
2. Define las variables de entorno (mínimo `DATABASE_URL`, `APP_SECRET_KEY`,
   `API_CORS_ORIGINS=https://app.tu-dominio.com`,
   `NEXT_PUBLIC_API_URL=https://api.tu-dominio.com`).
3. Coolify levantará dos servicios: `optiferre-api` (puerto 8000) y
   `optiferre-web` (puerto 3000). Apunta dos subdominios:
   - `api.tu-dominio.com` → `optiferre-api:8000`
   - `app.tu-dominio.com` → `optiferre-web:3000`
4. El servicio Streamlit antiguo queda bajo el profile `legacy`. Para correrlo
   durante la migración:
   ```bash
   docker compose --profile legacy up -d optiferre-streamlit
   ```
   Cuando ya no lo necesites, elimina ese servicio.

## Plan de migración por fases

| Fase | Qué se entrega | Estado |
| ---- | -------------- | ------ |
| 1    | API + Landing + Login/Register en Next.js | ✅ entregado |
| 2    | Dashboard ejecutivo + Productos muertos + Oportunidades | ✅ entregado |
| 3    | Upload, generación de OC y panel completo | ✅ entregado |
| 4    | Apagar Streamlit (eliminar `ui/`, `app.py`, `Dockerfile`) | pendiente decisión final |

## Mapeo Streamlit → nueva app

| Streamlit (`ui/pages/*.py`) | Equivalente nuevo |
| --------------------------- | ----------------- |
| `login.py` (público + login) | `web/src/app/page.tsx` + `/login` + `/register` + `api/routes/auth.py` |
| `dashboard.py`               | `web/src/app/app/page.tsx` + `api/routes/dashboard.py` |
| `analysis.py`                | `api/routes/analysis.py` + `api/services/analysis_runner.py` |
| `upload.py`                  | `web/src/app/app/upload/page.tsx` + `api/routes/inventory.py` |
| `purchase_orders.py`         | `web/src/app/app/purchase-orders/page.tsx` + `api/routes/purchase_orders.py` |

## Endpoints disponibles

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| POST   | `/auth/register` | Crea tenant + usuario + trial 14 días, devuelve JWT |
| POST   | `/auth/login` | Login, devuelve JWT |
| GET    | `/auth/me` | Datos del usuario autenticado |
| POST   | `/inventory/upload` | Sube `inventory` (CSV/XLSX) y opcionalmente `sales` |
| POST   | `/analysis/run` | Ejecuta `full_analysis` y persiste sugerencias |
| GET    | `/dashboard/summary` | KPIs: dinero atrapado, muertos, estrellas, quiebre |
| GET    | `/products/dead` | Productos muertos (sobrestock / sin demanda) |
| GET    | `/products/opportunities` | Productos a comprar |
| GET    | `/products/all` | Listado completo |
| GET    | `/purchase-orders` | Listado de órdenes |
| POST   | `/purchase-orders/generate` | Crea OC desde sugerencias activas |
| GET    | `/purchase-orders/{id}/export.xlsx` | Descarga la OC en Excel |

Toda llamada (excepto `/auth/login` y `/auth/register`) requiere
`Authorization: Bearer <token>`.
