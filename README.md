# OptiFerre SaaS

Plataforma SaaS B2B para análisis y optimización masiva de inventarios ferreteros e industriales. El producto está diseñado para operar en modo multitenant, cobrar suscripciones con Stripe, soportar marca blanca por cliente y entregar decisiones accionables de abastecimiento con lógica de ingeniería de inventarios.

Frontend productivo previsto: https://optiferre.datovatenexuspro.com

## Resumen ejecutivo

OptiFerre SaaS resuelve cuatro problemas operativos críticos:

1. Detecta capital atrapado en inventario inmovilizado.
2. Calcula niveles de reposición para evitar quiebres.
3. Estandariza cargas desde Excel, CSV y ERPs heterogéneos.
4. Convierte el análisis en un SaaS cobrable por suscripción, con servicios de integración aparte.

## Qué hace la aplicación

- Multitenancy con aislamiento por empresa.
- Registro e inicio de sesión con trial automático de 14 días.
- Landing pública rediseñada con propuesta de valor, prueba guiada, FAQ y mensajes de confianza.
- Smart Importer con aliases y fuzzy matching para columnas ERP heterogéneas.
- Demo Mode con dataset industrial precargado para reducir time-to-value comercial.
- Paywall por suscripción activa.
- Descarga de plantillas oficiales de Inventario, Ventas y Catálogo.
- Validación estructural al subir archivos.
- Popovers y guías contextuales para resolver dudas dentro del flujo.
- Limpieza financiera de datos de ERP.
- Clasificación ABC/XYZ.
- Stock de seguridad dinámico.
- Punto de reorden.
- Simulador de nivel de servicio y sensibilidad de compra.
- KPI de costo de oportunidad y alertas accionables priorizadas.
- Redondeo de compra al empaque mínimo con `math.ceil`.
- Sugerencia de catalizadores para químicos industriales.
- Dashboard ejecutivo y vista analítica exportable a CSV/Excel.
- Resumen ejecutivo con health score, prioridades gerenciales y lectura comercial del riesgo.
- White-label por tenant: color, logo y modo dark/light.
- Logging estructurado JSON con `tenant_id` y `user_id`.
- Ruta inicial de migraciones con Alembic.

## Reglas de negocio implementadas

### Clasificación ABC/XYZ

- ABC clasifica por valor acumulado del inventario según Pareto.
- XYZ clasifica por previsibilidad usando el coeficiente de variación de la demanda.
- La clase final es combinada: `AX`, `BY`, `CZ`, etc.

### Stock de Seguridad

Se calcula con la fórmula:

`SS = Z * sigma_d * sqrt(LeadTime)`

Si no hay suficiente histórico, el sistema usa una heurística conservadora basada en el 20% de la demanda promedio diaria.

### Punto de Reorden

`ROP = demanda_promedio_diaria * lead_time + stock_seguridad`

### Limpieza financiera

- Las notas crédito y devoluciones restan demanda.
- Las fechas y numéricos se normalizan.
- El Smart Importer sugiere y corrige aliases comunes como `Existencias`, `Qty`, `Codigo`, `Descripcion`.
- Se corrigen columnas mínimas para que el motor no falle por formatos erráticos.

### KPI financiero ampliado

- El sistema estima `capital_inmovilizado` cuando hay demanda nula o cobertura excesiva.
- Sobre ese capital se calcula costo de oportunidad anual y mensual.
- El dashboard expone este costo como proxy directo de caja atrapada.

### Simulación operativa

- El nivel de servicio sigue siendo configurable globalmente.
- La app ahora compara escenarios y muestra cómo cambia la sugerencia total de compra al mover el service level.
- Esto permite discutir trade-offs entre fill rate, caja y riesgo de quiebre.

### Seguridad de tenancy

- Se añadió `tenant_session_scope()` para abrir sesiones con contexto explícito de tenant.
- Se añadió `tenant_select()` para forzar filtros por `tenant_id` en modelos tenant-scoped.
- Se añadió logging estructurado para que errores y eventos puedan rastrearse por tenant y usuario.
- Se añadió `AuditLog` para registrar ejecuciones clave como corridas de análisis.
- El contexto de logging se limpia al cerrar cada sesión de persistencia para evitar contaminación cruzada entre requests.
- El `logout()` limpia también estado de demo, configuraciones de análisis y firma de auditoría en memoria de sesión.

### Ruta de migración

- El proyecto ya incluye `alembic.ini`, `alembic/env.py` y una baseline `20260502_0001`.
- La baseline crea `tenants`, `users`, `subscriptions`, `analysis_runs`, `audit_logs` y `alembic_version`.
- Se validó con `alembic upgrade head` sobre una base SQLite vacía.

### Guardarraíl industrial

- Toda sugerencia de compra se redondea al empaque mínimo con `math.ceil`.
- Si el producto contiene `PINTUCOAT`, se sugiere catalizador `13227`.
- Si el producto contiene `INTERTHANE`, se sugiere catalizador `PHA046`.

## Arquitectura del proyecto

```text
.
├── app.py
├── Dockerfile
├── alembic.ini
├── docker-compose.yml
├── core/
│   ├── auth.py
│   ├── billing.py
│   ├── config.py
│   ├── database.py
│   ├── logging_config.py
│   ├── models.py
│   ├── tenancy.py
│   └── templates.py
├── engine/
│   ├── cleaning.py
│   ├── demo_data.py
│   └── optimization.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── ui/
│   ├── components.py
│   ├── theme.py
│   └── pages/
├── assets/templates/
├── tests/
└── requirements.txt
```

## Guía para clientes y equipos comerciales

### Flujo de uso del cliente final

1. Crear cuenta e iniciar trial.
2. Revisar FAQ, confianza y alcance directamente desde la portada pública.
3. Descargar las plantillas oficiales.
4. Completar las columnas obligatorias.
5. Cargar Inventario y Ventas con ayuda contextual en pantalla.
6. Si quiere validar rápido, activar Demo Mode con dataset industrial precargado.
7. Ir a Dashboard para ver capital inmovilizado, costo de oportunidad, alertas y tareas prioritarias.
8. Ir a Análisis para revisar SS, ROP, sugerencia de compra y sensibilidad por nivel de servicio.
9. Exportar resultados y ejecutar compras o acciones correctivas.

### Qué ve ahora un decisor en el dashboard

- Diagnóstico ejecutivo resumido como `riesgo alto`, `riesgo controlable` o `salud estable`.
- Health score sintético para lectura rápida en comité o reunión comercial.
- Foco principal de caja atrapada.
- Riesgo de quiebre en horizonte de 7 días.
- Presión concentrada en SKUs clase A.
- Escenario de service level más liviano en caja dentro del simulador.

### Qué debe cargar el cliente

#### Inventario Maestro

Columnas mínimas:

- `sku`
- `nombre_comercial`
- `stock_actual`
- `costo_unitario`
- `lead_time_dias`
- `categoria`
- `unidad_empaque_minimo`

#### Histórico de Ventas

Columnas mínimas:

- `fecha`
- `sku`
- `cantidad_vendida`
- `tipo_documento`

#### Catálogo Maestro

Columnas mínimas:

- `sku`
- `nombre_comercial`
- `marca`
- `proveedor`
- `linea`
- `es_quimico`

### Qué ve el cliente en el dashboard

- Capital total invertido.
- Capital inmovilizado.
- Costo de oportunidad mensual.
- SKUs en quiebre.
- SKUs por reponer.
- Sobrestock.
- Distribución por clase ABC/XYZ.
- Matriz bubble ABC/XYZ según capital atrapado.
- Escenarios de nivel de servicio.
- Lista de tareas priorizadas para compras y desinversión.

### Qué significa cada estado

- `QUIEBRE`: no hay stock.
- `REPONER`: el stock actual ya está por debajo del punto de reorden.
- `SOBRESTOCK`: demasiados días de cobertura o demanda nula.
- `OK`: inventario controlado dentro de parámetros sanos.

## Transparencia y confianza para el cliente

La aplicación ya incorpora un enfoque explícito de confianza para ayudar a conversión y adopción:

- portada pública rediseñada sin sidebar distractor,
- hero ejecutivo con propuesta de valor clara,
- bloque de capacidad del producto y planes,
- preguntas frecuentes en ventanas emergentes,
- explicación del uso de la información cargada,
- aclaración de que la integración ERP no es obligatoria al inicio,
- guía contextual en la sección de carga de archivos,
- demo industrial para acortar onboarding,
- separación comercial entre suscripción SaaS e integración premium.

Preguntas que la app responde directamente:

- qué hace exactamente,
- cómo se suben y procesan los archivos,
- dónde se guarda la información,
- quién puede ver los datos,
- qué seguridad ofrece,
- qué pasa después de la prueba.

## Guía de despliegue en Coolify

La app queda lista para desplegar en Coolify con Docker Compose.

### Archivos ya preparados

- `Dockerfile`
- `docker-compose.yml`
- `docker-compose.yaml`
- `.dockerignore`
- `alembic.ini`
- `alembic/env.py`
- `alembic/versions/20260502_0001_baseline_schema.py`

### Configuración en Coolify

Usa exactamente estos valores:

1. Repository: tu repo GitHub.
2. Branch: `main`.
3. Build Pack: `Docker Compose`.
4. Base Directory: `/`.
5. Docker Compose Location: `/docker-compose.yml`.
6. Dominio público recomendado: `https://optiferre.datovatenexuspro.com`.

### Variables de entorno en Coolify

No subas secretos reales al repositorio. Deben ir en la sección de Environment Variables de Coolify.

Variables mínimas:

- `APP_NAME=OptiFerre SaaS`
- `APP_ENV=production`
- `APP_SECRET_KEY=<clave-larga-y-segura>`
- `APP_BASE_URL=https://optiferre.datovatenexuspro.com`
- `DATABASE_URL=<tu-postgresql+psycopg2://...>`
- `STRIPE_SECRET_KEY=<tu-clave>`
- `STRIPE_PUBLISHABLE_KEY=<tu-clave>`
- `STRIPE_WEBHOOK_SECRET=<tu-clave>`
- `STRIPE_PRICE_STARTER=<price_id>`
- `STRIPE_PRICE_PRO=<price_id>`
- `STRIPE_PRICE_ENTERPRISE=<price_id>`
- `SALES_CONTACT_EMAIL=ventas@optiferre.com`
- `SALES_CONTACT_PHONE=+57 300 000 0000`

### Qué falta para que el despliegue salga bien

1. Hacer push del repositorio a GitHub.
2. Conectar ese repositorio en Coolify.
3. Cargar las variables reales en Coolify.
4. Lanzar el primer deploy.
5. Verificar que la URL pública abra la pantalla de login.

### Qué ya quedó resuelto para producción

- Docker Compose creado.
- Dockerfile creado.
- PostgreSQL normalizado para SQLAlchemy aunque el proveedor entregue `postgres://`.
- Dependencia `psycopg2-binary` añadida.
- Healthcheck de contenedor configurado.

## Desarrollo local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Pruebas

```bash
pytest -q
```

```bash
alembic upgrade head
```

Validación reciente del slice crítico:

- `pytest -q tests/test_engine.py` -> `10 passed`
- `pytest -q` -> `10 passed`
- smoke import de `app.py` -> OK
- `streamlit run app.py` -> superficie HTTP respondió `200`
- `alembic upgrade head` sobre SQLite temporal -> OK

## Seguridad y buenas prácticas

- `.env.example` debe contener placeholders, no secretos reales.
- Las credenciales reales deben vivir en Coolify, no en Git.
- PostgreSQL es la opción recomendada para producción.
- SQLite solo debe usarse para demos locales o pruebas rápidas.
- Las consultas tenant-scoped deben pasar por helpers con filtro obligatorio por `tenant_id`.
- Los logs deben conservar `tenant_id` y `user_id` para auditoría y soporte.
- Alembic queda preparado como ruta de migración evolutiva para salir de `create_all()` sin ruptura.

## Modelo comercial

### Ingreso recurrente

- Plan Starter.
- Plan Pro.
- Plan Enterprise.

### Servicios de alto margen

- Integración a ERP.
- Automatizaciones de abastecimiento.
- Modelos de reposición multi-bodega.
- Personalización white-label avanzada.
- Acompañamiento operativo y consultoría.

## Estado actual del proyecto

El MVP ya está listo para:

- subirse a GitHub,
- desplegarse en Coolify,
- conectarse a PostgreSQL,
- operar con Stripe,
- y presentarse comercialmente a clientes con una guía clara de uso.

## Siguiente paso operativo

1. Añadir el remoto de GitHub.
2. Hacer push a `main`.
3. Completar variables en Coolify.
4. Desplegar.
5. Probar login, trial, carga de datos y checkout.
