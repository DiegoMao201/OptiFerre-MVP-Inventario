# OptiFerre SaaS

Plataforma SaaS B2B para análisis y optimización masiva de inventarios ferreteros e industriales. El producto está diseñado para operar en modo multitenant, cobrar suscripciones con Stripe, soportar marca blanca por cliente y entregar decisiones accionables de abastecimiento con lógica de ingeniería de inventarios.

Frontend productivo previsto: https://optiferredatovatenexuspro.com

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
- Paywall por suscripción activa.
- Descarga de plantillas oficiales de Inventario, Ventas y Catálogo.
- Validación estructural al subir archivos.
- Popovers y guías contextuales para resolver dudas dentro del flujo.
- Limpieza financiera de datos de ERP.
- Clasificación ABC/XYZ.
- Stock de seguridad dinámico.
- Punto de reorden.
- Redondeo de compra al empaque mínimo con `math.ceil`.
- Sugerencia de catalizadores para químicos industriales.
- Dashboard ejecutivo y vista analítica exportable a CSV/Excel.
- White-label por tenant: color, logo y modo dark/light.

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
- Se corrigen columnas mínimas para que el motor no falle por formatos erráticos.

### Guardarraíl industrial

- Toda sugerencia de compra se redondea al empaque mínimo con `math.ceil`.
- Si el producto contiene `PINTUCOAT`, se sugiere catalizador `13227`.
- Si el producto contiene `INTERTHANE`, se sugiere catalizador `PHA046`.

## Arquitectura del proyecto

```text
.
├── app.py
├── Dockerfile
├── docker-compose.yml
├── core/
│   ├── auth.py
│   ├── billing.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── tenancy.py
│   └── templates.py
├── engine/
│   ├── cleaning.py
│   └── optimization.py
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
6. Ir a Dashboard para ver capital inmovilizado y alertas.
7. Ir a Análisis para revisar SS, ROP y sugerencia de compra.
8. Exportar resultados y ejecutar compras o acciones correctivas.

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
- SKUs en quiebre.
- SKUs por reponer.
- Sobrestock.
- Distribución por clase ABC/XYZ.

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
- `.dockerignore`

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

## Seguridad y buenas prácticas

- `.env.example` debe contener placeholders, no secretos reales.
- Las credenciales reales deben vivir en Coolify, no en Git.
- PostgreSQL es la opción recomendada para producción.
- SQLite solo debe usarse para demos locales o pruebas rápidas.

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
