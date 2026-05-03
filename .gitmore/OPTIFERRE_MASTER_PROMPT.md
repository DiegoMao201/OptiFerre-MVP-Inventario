# OPTIFERRE MASTER PROMPT

## Rol esperado de cualquier IA o colaborador

Actúa como Staff Software Engineer, Product Architect, UX Architect y operador de una plataforma SaaS B2B de inventarios. Toda propuesta debe partir del estado real implementado hoy en este repositorio, no desde una idea antigua del MVP.

Este archivo es la fuente de verdad operativa del producto. Antes de proponer cambios, entiende primero qué ya existe, qué está funcionando, qué cambió recientemente y qué sigue pendiente.

## Identidad y posicionamiento actual

- Nombre operativo de la app: OptiFerre.
- Identidad comercial auxiliar: Nexus Pro.
- Tipo de producto: SaaS guiado para transformar archivos de inventario en decisiones de compra, reducción de caja atrapada y prevención de quiebres.
- Público objetivo real:
  - dueños y gerentes,
  - responsables de compras,
  - operaciones,
  - finanzas,
  - empresas con inventario físico.

La app ya no debe narrarse como una simple herramienta técnica. La intención actual es que se sienta como un consultor senior de inventarios que guía paso a paso.

## Stack y base técnica vigente

- Python 3.11.
- Streamlit como runtime principal de UI.
- SQLAlchemy 2.x.
- PostgreSQL externo en producción.
- Alembic para migraciones reales.
- Stripe Checkout + webhook base.
- SendGrid para correo transaccional.
- OpenRouter + DeepSeek para la capa de IA.

## Estado real implementado hoy

### Experiencia pública

Ya existe una landing pública pulida en `ui/pages/login.py` con:

- hero comercial,
- propuesta de valor,
- animaciones,
- FAQ,
- pricing público,
- acceso,
- registro,
- recuperación de contraseña,
- soporte público.

Restricción vigente: no tocar visualmente el login salvo necesidad crítica explícita.

### Autenticación y tenants

Ya existen:

- registro de tenant y owner,
- login persistente,
- hashing de contraseña,
- recuperación de contraseña con token y expiración,
- sesión de usuario en Streamlit,
- tenant branding básico en la experiencia autenticada.

### Billing y planes

Ya existen planes funcionales y visibles:

- Starter - 15 USD/mes - Concierge,
- Pro - 40 USD/mes - Analista de Inventarios,
- Enterprise - 100 USD/mes - Director de Operaciones (COO).

Se implementó:

- catálogo de planes centralizado en `core/plans.py`,
- checkout vía Stripe en `core/billing.py`,
- helper de RBAC y features en `core/access.py`,
- paywall elegante por función bloqueada,
- upgrade desde la pantalla de planes.

### Datos, análisis y operación

El sistema hoy ya hace:

- Smart Importer para mapear columnas comunes de ERP,
- carga de inventario,
- carga de ventas,
- carga de catálogo maestro,
- demo guiada,
- limpieza de datos,
- análisis ABC/XYZ,
- cálculo de stock de seguridad,
- punto de reorden,
- capital inmovilizado,
- costo de oportunidad,
- simulación por nivel de servicio,
- compra sugerida.

### Flujo autenticado actual

La navegación autenticada fue simplificada y hoy está orientada a este flujo:

1. `🏠 Inicio`
2. `1. Carga de Datos`
3. `2. Insights IA`
4. `3. Qué Comprar`
5. `🤖 Asistente IA`
6. `🆘 Soporte`
7. `💳 Planes y Suscripción`
8. `🎨 Marca (White-label)`

La intención es reducir la sensación de enredo y forzar un recorrido más comprensible.

### UX actual implementada

#### Dashboard / Inicio

La página `ui/pages/dashboard.py` ahora funciona como golpe de valor inicial:

- bienvenida con propuesta clara,
- KPIs inmediatos de impacto,
- dinero atrapado en stock,
- productos en riesgo de quiebre,
- pasos para el éxito,
- alertas y tareas prioritarias,
- guía hacia la compra sugerida.

#### Carga de datos

La página `ui/pages/upload.py` fue reestructurada como puerta de entrada real:

- plantillas oficiales integradas dentro del mismo flujo,
- explicación de qué problema resuelve la app,
- mensajes humanos de error en vez de errores técnicos crudos,
- carga separada de:
  - inventario maestro,
  - histórico de ventas,
  - catálogo maestro,
- guía explícita del siguiente paso tras cargar archivos.

#### Qué Comprar

La página `ui/pages/purchase_orders.py` se convirtió en el centro de decisión:

- muestra sugerencias persistidas,
- cruza catálogo maestro cuando existe,
- muestra proveedor, marca y línea,
- permite editar cantidades finales,
- permite marcar qué entra en la orden,
- guarda cambios,
- genera orden de compra,
- exporta Excel en Enterprise,
- muestra historial de órdenes,
- explica cómo usar la pantalla sin asumir conocimiento técnico.

#### Asistente IA

La página `ui/pages/assistant.py` ya existe y funciona por plan:

- Starter: Concierge,
- Pro: Analista de Inventarios,
- Enterprise: COO con function calling.

El contexto de IA hoy incluye:

- sugerencias persistidas,
- KPIs principales,
- y ahora también contexto de catálogo maestro si fue cargado.

#### Insights IA

La página `ui/pages/analysis.py` ya no debe interpretarse como una tabla técnica cruda. Hoy ya quedó orientada a:

- explicar el problema antes de comprar,
- mostrar KPIs de impacto rápidos,
- enriquecer la lectura con proveedor, marca y línea si existe catálogo,
- guiar al usuario desde insight hacia compra sugerida.

#### Soporte y Marca

Las páginas `ui/pages/support_page.py` y `ui/pages/settings_page.py` ya incluyen más contexto de uso, más guía explícita y mejor narrativa para un usuario no técnico.

## Arquitectura funcional vigente

### Archivos y módulos importantes

- `app.py`
  - entrypoint,
  - routing,
  - sidebar,
  - aplicación de branding,
  - experiencia pública vs autenticada.

- `core/auth.py`
  - registro,
  - login,
  - sesión,
  - password reset.

- `core/config.py`
  - carga central de env vars,
  - Stripe,
  - SendGrid,
  - OpenRouter / DeepSeek.

- `core/plans.py`
  - catálogo de planes,
  - jerarquía,
  - features por plan.

- `core/access.py`
  - `effective_plan`,
  - `require_feature`,
  - control visual y funcional de acceso.

- `core/models.py`
  - tenants,
  - users,
  - subscriptions,
  - analysis runs,
  - audit logs,
  - tickets,
  - password reset tokens,
  - inventory snapshots,
  - sales snapshots,
  - purchase suggestions,
  - purchase orders,
  - AI conversations,
  - AI messages,
  - AI action logs.

- `services/inventory_store.py`
  - snapshots persistentes,
  - UPSERT de sugerencias,
  - edición de sugerencias,
  - log de acciones IA.

- `services/purchase_orders.py`
  - creación de órdenes,
  - exportación Excel,
  - listado de órdenes.

- `services/ai_factory.py`
  - clientes IA por plan,
  - retries,
  - fallback simulado,
  - tools Enterprise.

- `engine/cleaning.py`
  - limpieza de inventario,
  - limpieza de ventas,
  - mapeo inteligente,
  - limpieza de catálogo maestro.

- `engine/optimization.py`
  - pipeline de análisis,
  - ABC/XYZ,
  - SS,
  - ROP,
  - capital inmovilizado,
  - estados operativos,
  - sugerencia de compra.

- `ui/theme.py`
  - sistema visual global,
  - modo público dark impactante,
  - modo autenticado light,
  - contraste reforzado en campos, radios, selectores, uploaders y data editors.

## Datos que hoy sí se pueden cargar

Las plantillas oficiales vigentes son:

1. Inventario maestro.
2. Histórico de ventas.
3. Catálogo maestro.

Nota importante:

- hoy sí existe carga real para catálogo maestro en la app autenticada;
- el catálogo se usa para enriquecer contexto comercial y contexto del asistente IA;
- aún no está explotado al máximo dentro del motor analítico ni en toda la UI.

## Persistencia y base de datos

### Ya implementado

- PostgreSQL externo como fuente principal en producción.
- normalización de `DATABASE_URL`.
- migraciones Alembic reales.
- migración 0004 para IA, snapshots y operación accionable.

### Migraciones vigentes conocidas

- baseline schema,
- soporte,
- password reset,
- AI + snapshots + purchase orders.

## Comportamiento por plan

### Starter

- soporte de onboarding,
- carga básica,
- Concierge IA,
- sin análisis profundo explicado por IA,
- experiencia más simple y más limpia.

### Pro

- insights IA,
- explicación del porqué de cada sugerencia,
- snapshots persistidos,
- edición de sugerencias,
- compra sugerida operativa.

### Enterprise

- generación de órdenes,
- exportación Excel,
- herramientas ejecutivas vía IA,
- paso hacia automatización operativa.

## Qué ya fue mejorado recientemente

### UX y claridad

- simplificación del menú autenticado,
- guía por pasos,
- mensajes de valor en Inicio,
- compra sugerida como centro operativo,
- billing más persuasivo,
- errores de carga más humanos,
- catálogo maestro integrado al flujo real,
- catálogo maestro visible también en insights y compra sugerida,
- contraste reforzado en la app logueada.

### UX adicional ya cerrada

- `Insights IA` simplificado para leerse como explicación y no como hoja técnica,
- `Qué Comprar` enriquecido con proveedor, marca y línea,
- `Soporte` más guiado para clientes sin contexto técnico,
- `Marca` más alineada con valor y confianza comercial.

### IA y operación accionable

- capas por persona y plan,
- paywalls visuales por feature,
- sugerencias editables persistentes,
- órdenes de compra con historial,
- contexto de negocio para el asistente.

## Limitaciones reales y trabajo pendiente

### Pendientes funcionales de alta prioridad

1. El webhook Stripe aún necesita un endpoint HTTP público y productivo fuera de Streamlit.
2. Los recordatorios automáticos de billing y trial requieren ejecución programada real en Coolify o cron.
3. El catálogo maestro aún no alimenta todas las pantallas ni todo el motor; hoy enriquece contexto, pero no domina la experiencia completa.
4. La guía dentro de `2. Insights IA` y `🤖 Asistente IA` mejoró, pero aún puede volverse más conversacional e interactiva.
5. Falta una experiencia más madura de helpdesk / bandeja operativa.
6. No existe verificación de correo al alta.
7. La autenticación sigue basada en sesión de Streamlit, no en backend desacoplado.
8. No hay workers asíncronos dedicados.

### Pendientes de producto / UX

1. Seguir reduciendo fricción en análisis detallado para que no se sienta técnico.
2. Unificar del todo naming y narrativa entre Nexus Pro y OptiFerre.
3. Añadir más señales de confianza honestas y no infladas en la experiencia autenticada.
4. Conectar mejor catálogo maestro con proveedores, marcas y priorización de compra.
5. Afinar white-label y consistencia visual en todos los componentes internos restantes.

## Variables de entorno importantes ya contempladas

### Base

- `DATABASE_URL`
- `APP_NAME`
- `APP_ENV`
- `APP_SECRET_KEY`
- `APP_BASE_URL`

### Mail / soporte

- `MAIL_PROVIDER`
- `MAIL_FROM_NAME`
- `MAIL_FROM_EMAIL`
- `MAIL_REPLY_TO`
- `SENDGRID_API_KEY`
- `SUPPORT_CONTACT_EMAIL`
- `SALES_CONTACT_EMAIL`
- `SALES_CONTACT_PHONE`

### Stripe

- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_STARTER`
- `STRIPE_PRICE_PRO`
- `STRIPE_PRICE_ENTERPRISE`

### IA

- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- `OPENROUTER_DEEPSEEK_MODEL`
- `AI_REQUEST_TIMEOUT_SECONDS`
- `AI_MAX_RETRIES`

## Reglas para futuras IAs

1. No asumir que la app está vacía. Ya tiene autenticación, billing, IA, snapshots, sugerencias persistentes y órdenes de compra.
2. No romper ni rediseñar arbitrariamente el login público sin instrucción explícita.
3. Tratar la app autenticada como producto guiado, no como herramienta técnica desnuda.
4. Priorizar claridad, contraste, confianza y reducción de pasos.
5. Si una propuesta agrega datos o plantillas nuevas, también debe agregar el punto de carga real correspondiente.
6. Si una mejora visual usa fondos claros, validar el contraste de textos, captions, radios, tabs, inputs y data editors.
7. Toda nueva funcionalidad debe respetar tenant isolation y RBAC por plan.

## Objetivo estratégico actual

La app debe sentirse cada vez menos como una hoja de cálculo complicada y cada vez más como un consultor senior de inventarios que:

- guía,
- explica,
- prioriza,
- y lleva al usuario a la decisión de compra con la menor fricción posible.

Ese es el criterio principal para evaluar cualquier siguiente cambio.
