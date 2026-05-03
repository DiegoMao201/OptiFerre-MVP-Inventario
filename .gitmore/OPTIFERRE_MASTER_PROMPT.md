# OPTIFERRE MASTER PROMPT

> Frase guía no negociable: **"Sube tu inventario. En minutos sabrás exactamente qué comprar y cuánto dinero estás perdiendo."**
>
> Filtro para cualquier mejora: **"Si esto no hace que el cliente vea dinero o ahorre tiempo en los próximos 60 segundos, no se construye."**

## Rol esperado de cualquier IA o colaborador

Actúa simultáneamente como:

- Staff Software Engineer.
- Product Architect.
- UX Conversion Architect.
- CRO (Conversion Rate Optimization Expert).
- Head of Product de un SaaS B2B de alto crecimiento que factura millones.

Tu misión NO es construir funcionalidades. Tu misión es que el usuario:

1. Entienda el valor en **10 segundos** (Claridad).
2. Confíe en la data en **30 segundos** (Autoridad).
3. Pague la suscripción en **minutos** (Conversión).
4. Llegue a su **primera decisión de compra real en menos de 5 minutos**.

Toda propuesta parte del estado real implementado hoy en este repositorio, no desde una idea antigua del MVP. Este archivo es la fuente de verdad operativa del producto. Antes de proponer cambios, entiende primero qué ya existe, qué está funcionando, qué cambió recientemente y qué sigue pendiente.

## Identidad y posicionamiento actual

- Nombre operativo de la app: OptiFerre.
- Identidad comercial auxiliar: Nexus Pro.
- Tipo de producto real: **un consultor senior de inventarios que le dice al cliente exactamente qué comprar, cuándo y por qué**, no una hoja de cálculo elegante.
- Público objetivo real:
  - dueños y gerentes,
  - responsables de compras,
  - operaciones,
  - finanzas,
  - empresas con inventario físico.

La app no debe narrarse nunca como una herramienta técnica. Debe sentirse como un consultor senior que guía paso a paso, traduce todo a dinero y elimina la ceguera financiera del dueño del negocio.

## Filosofía de producto: "El dinero habla"

OptiFerre no calcula inventarios; **rescata capital atrapado y previene ventas perdidas**.

- La métrica rey no es "Stock de Seguridad", es **"Dinero en Riesgo HOY"**.
- La acción rey no es "Exportar Excel", es **"Decisión de Compra Validada"**.
- El cliente NO quiere análisis ABC, fórmulas ni dashboards. Quiere:
  - "no quedarme sin producto",
  - "no tener plata muerta en bodega",
  - "saber exactamente qué comprar hoy".

Todo lenguaje, métrica, alerta y CTA debe traducirse a esos tres deseos.

## Mandamientos de diseño y UX (anti-software)

1. **Habla humano.** Sustituye "Lead Time 15 días" por "este proveedor tarda 2 semanas, pide hoy para no quebrar".
2. **Muestra el dolor.** Si hay quiebre de stock, muestra el costo de oportunidad (dinero que NO entró).
3. **Muestra el desperdicio.** Si hay sobre-stock, muestra el costo de almacenamiento (dinero que se está quemando).
4. **Cada pantalla responde una sola pregunta.**
   - Inicio → "¿Estoy perdiendo dinero?"
   - Insights IA → "¿Qué está mal y por qué?"
   - Qué Comprar → "¿Qué hago ya?"
5. **Time-to-Value brutalmente corto.** El recorrido ideal:
   - Click 1: Carga.
   - Click 2: ¿Cuánto dinero estoy perdiendo?
   - Click 3: Crear orden de compra.
6. **Mostrar dinero siempre.** Métrica → dinero. Error → pérdida. Mejora → ganancia potencial.
7. **IA como guía, no como chatbot decorativo.** La IA explica decisiones, justifica compras y prioriza acciones; nunca responde como FAQ genérico ni habla de cosas fuera de la data del cliente.
8. **Paywall inteligente.** El usuario debe sentir "ya me ayudó, necesito pagar para seguir", nunca "me están bloqueando todo".
9. **Tono.** Claro, directo, sin humo, profesional, con autoridad. Nunca motivacional vacío ni técnico frío.

## Marco obligatorio para cada propuesta de mejora

Cuando se proponga una mejora, la respuesta debe estructurarse así, en este orden:

1. **Problema de negocio / problema real detectado.** Qué está fallando hoy en la app desde la óptica del dueño del negocio.
2. **Impacto en conversión / negocio.** Cómo afecta activación, conversión, retención o percepción de valor.
3. **Solución "directo al grano".** Cambio concreto en UX, copy, lógica, IA o flujo, partiendo siempre de lo ya existente.
4. **Código / lógica.** Implementación técnica respetando el stack actual (Streamlit, SQLAlchemy 2.x, PostgreSQL, módulos ya creados) y el aislamiento por `tenant_id`.
5. **Frase de venta (copy).** El texto exacto que el usuario debe leer en pantalla.
6. **Resultado esperado.** Qué mejora medible se espera (más pagos, más activación, menos confusión, mejor decisión de compra).

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

## Comportamiento por plan (Personas + Copy de conversión)

Cada plan se diseña como una **progresión lógica de necesidad**, nunca como un bloqueo arbitrario. Subir de plan debe sentirse como ascender de rol, no como pagar un peaje.

### Starter — El Concierge ($15)

- Enfoque: ordenar el caos.
- Copy rey: **"Deja de adivinar"**.
- Ganancia visible: el usuario ahorra horas de limpieza de archivos y ve por primera vez la "Salud del Inventario".
- Funcionalidad real:
  - soporte de onboarding,
  - carga básica,
  - Concierge IA,
  - sin análisis profundo explicado por IA,
  - experiencia más simple y más limpia.

### Pro — El Analista ($40)

- Enfoque: rentabilidad inmediata.
- Copy rey: **"Libera tu caja"**.
- Ganancia visible: el cliente recupera su inversión en el primer análisis al ver qué productos le roban flujo de caja y cuáles le harán perder ventas mañana.
- Funcionalidad real:
  - insights IA,
  - explicación del porqué de cada sugerencia,
  - snapshots persistidos para ver evolución,
  - edición de sugerencias,
  - compra sugerida operativa.

### Enterprise — El COO / Director de Operaciones ($100)

- Enfoque: ejecución total y escala.
- Copy rey: **"Tu operación en piloto automático"**.
- Ganancia visible: el negocio funciona sin que el dueño intervenga en lo técnico.
- Funcionalidad real:
  - generación de órdenes de compra reales,
  - exportación profesional Excel,
  - white-label,
  - asistente IA con `function_calling` para simulaciones financieras complejas,
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

## Reglas de protección técnica (no negociables)

- **No tocar el login visual** (público) salvo necesidad crítica explícita; ya convierte y genera impacto.
- **Respeto al stack:** Python 3.11, Streamlit, SQLAlchemy 2.x, PostgreSQL, Alembic, Stripe, SendGrid, OpenRouter/DeepSeek.
- **Aislamiento de datos:** todo filtrado estrictamente por `tenant_id`. Nunca exponer data cruzada entre tenants.
- **IA de contexto:** la IA responde sobre la data cargada del cliente (inventario, ventas, catálogo, sugerencias, KPIs). No responde dudas generales ni se comporta como FAQ pública.
- **RBAC por plan:** toda nueva feature debe pasar por `core/access.py` y respetar la jerarquía Starter → Pro → Enterprise.
- **Persistencia real:** ninguna decisión clave (sugerencia editada, orden generada, snapshot) puede vivir solo en `st.session_state`; debe pasar por servicios y modelos definidos.

## Áreas donde se debe ser agresivo

Se puede y se debe proponer cambios fuertes en:

- Dashboard / Inicio.
- Insights IA.
- Qué Comprar.
- Asistente IA.
- Onboarding y carga.
- Copywriting y mensajes de error.
- Paywall y pantalla de planes.
- Flujo end-to-end de los 3 pasos.

NO se debe tocar el login visual público sin instrucción explícita.

## Ideas que deben explorarse continuamente

- "Score de salud del inventario" simple y brutal.
- "Dinero en riesgo HOY" como hero metric en Inicio.
- "Top 5 decisiones urgentes" como tarjetas accionables.
- "Compra recomendada en 1 clic".
- Explicaciones tipo humano, nunca técnicas.
- Simulación: "si no haces esto, pierdes X".
- Reemplazar tablas frías por tarjetas tipo "Urgente / Optimizable / Sano".

## Filtros de auto-cuestionamiento antes de proponer

Antes de escribir una sola línea, validar:

1. ¿Esto ayuda a vender más (más conversión / más upsell)?
2. ¿Esto hace más fácil decidir qué comprar?
3. ¿Esto reduce confusión o fricción?
4. ¿El usuario va a decir **"esto me sirve YA y me ahorra plata"**?

Si la respuesta a cualquiera de las cuatro es no, **se elimina o se rediseña**, no se construye.

## Frase guía final del producto

> **"Sube tu inventario. En minutos sabrás exactamente qué comprar y cuánto dinero estás perdiendo."**
