export const PLAN_PREVIEW = [
  {
    key: "starter",
    name: "Starter",
    price: "USD 15/mes",
    hook: "Ordena tu carga y deja de perder tiempo acomodando archivos.",
    bullets: [
      "Subes inventario y ventas con plantillas claras",
      "Soporte por tickets y onboarding guiado",
      "Ideal si hoy sigues resolviendo todo a punta de Excel",
    ],
  },
  {
    key: "pro",
    name: "Pro",
    price: "USD 40/mes",
    hook: "Mira qué te deja plata quieta y qué debes comprar sin adivinar.",
    bullets: [
      "Productos muertos, quiebres y compra sugerida",
      "Análisis con explicación en lenguaje de negocio",
      "El plan que más sentido tiene cuando ya quieres decisiones",
    ],
  },
  {
    key: "enterprise",
    name: "Enterprise",
    price: "USD 100/mes",
    hook: "Convierte el análisis en órdenes, correos y operación real.",
    bullets: [
      "Órdenes de compra listas para trabajar",
      "Más usuarios, más volumen y soporte prioritario",
      "Para negocios que ya no quieren improvisar compras",
    ],
  },
] as const;