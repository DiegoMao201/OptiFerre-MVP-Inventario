export const PLAN_PREVIEW = [
  {
    key: "starter",
    name: "Starter",
    price: "USD 15/mes",
    hook: "Empieza sin enredos y sube bien tus archivos desde el primer intento.",
    bullets: [
      "Subes inventario y ventas con plantillas claras",
      "Te acompaña para arrancar sin perder tiempo",
      "Ideal si hoy todavía manejas todo en Excel",
    ],
  },
  {
    key: "pro",
    name: "Pro",
    price: "USD 40/mes",
    hook: "Mira qué te está dejando plata quieta y qué sí vale la pena volver a pedir.",
    bullets: [
      "Productos muertos, quiebres y compra sugerida",
      "Te explica el problema en palabras simples",
      "El plan más lógico cuando ya quieres comprar con más cabeza",
    ],
  },
  {
    key: "enterprise",
    name: "Enterprise",
    price: "USD 100/mes",
    hook: "Pasa de ver el problema a dejar listas compras y mensajes para proveedores.",
    bullets: [
      "Órdenes de compra listas para trabajar",
      "Más usuarios, más volumen y soporte prioritario",
      "Para negocios que ya no quieren seguir improvisando compras",
    ],
  },
] as const;