"use client";

import Link from "next/link";
import { ArrowRight, AlertTriangle, PackageX, ShoppingCart, Wallet } from "lucide-react";
import { Button } from "@/components/ui/button";

const demoMetrics = [
  { label: "Plata quieta detectada", value: "$12.000.000", hint: "capital atrapado en 22 productos muertos", icon: Wallet },
  { label: "Productos muertos", value: "22", hint: "referencias que no debían volver a comprarse", icon: PackageX },
  { label: "Urgencias de compra", value: "9", hint: "productos que sí estaban poniendo en riesgo ventas", icon: AlertTriangle },
  { label: "Compra sugerida", value: "$3.400.000", hint: "pedido más fino en vez de comprar a ojo", icon: ShoppingCart },
];

const decisions = [
  "Frenar recompra de 22 referencias lentas hasta vender lo que ya estaba quieto.",
  "Priorizar 9 productos que ya estaban a punto de acabarse y sí empujaban ventas.",
  "Usar 2 semanas de seguimiento para ajustar compras y dejar de inmovilizar caja.",
];

export default function DemoPage() {
  return (
    <div className="min-h-screen container py-10 space-y-10">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div className="max-w-3xl">
          <div className="text-xs uppercase tracking-widest text-primary font-bold">Ver ejemplo real</div>
          <h1 className="text-4xl md:text-5xl font-black mt-2 leading-tight">
            Así se ve una ferretería cuando la app le muestra dónde tiene la plata quieta.
          </h1>
          <p className="text-muted-foreground mt-3 text-lg">
            Caso piloto de referencia en Pereira: se cargó el inventario, se vio la plata quieta y en dos semanas ya se estaba comprando con más cabeza.
          </p>
        </div>
        <div className="flex gap-3">
          <Button asChild variant="outline" size="lg">
            <Link href="/">Volver al landing</Link>
          </Button>
          <Button asChild size="lg">
            <Link href="/register">Quiero mi prueba gratis <ArrowRight className="h-4 w-4" /></Link>
          </Button>
        </div>
      </header>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {demoMetrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <article key={metric.label} className="card-glass p-6">
              <div className="h-11 w-11 rounded-2xl bg-primary/15 text-primary grid place-content-center mb-4">
                <Icon className="h-5 w-5" />
              </div>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">{metric.label}</div>
              <div className="text-3xl font-black mt-2">{metric.value}</div>
              <p className="text-sm text-muted-foreground mt-2">{metric.hint}</p>
            </article>
          );
        })}
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="card-glass p-6 md:p-8">
          <div className="text-xs uppercase tracking-widest text-primary font-bold">Ejemplo real</div>
          <h2 className="text-3xl font-black mt-2">Menos adivinanza, más claridad para comprar y vender.</h2>
          <div className="grid md:grid-cols-2 gap-4 mt-6">
            <DemoPanel title="Lo urgente" tone="danger" items={[
              "22 productos muertos drenando caja",
              "9 productos a punto de agotarse",
              "$12.000.000 quietos en bodega",
            ]} />
            <DemoPanel title="Lo que harías hoy" tone="primary" items={decisions} />
          </div>
        </div>

        <div className="card-glass p-6 md:p-8 space-y-5">
          <div>
            <div className="text-xs uppercase tracking-widest text-primary font-bold">Caso piloto</div>
            <h2 className="text-2xl font-black mt-2">Ferretería en Pereira</h2>
            <p className="text-muted-foreground mt-3">
              En el piloto la app ayudó a separar lo que estaba quieto de lo que sí se movía, y eso cambió la conversación de compras en menos de dos semanas.
            </p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-5 text-sm text-muted-foreground">
            "No necesitábamos otro software gigante. Necesitábamos ver rápido dónde estaba enterrada la plata y qué sí valía la pena pedir." 
          </div>
          <Button asChild size="lg" className="w-full">
            <Link href="/register">Quiero ver esto con mi propio Excel</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}

function DemoPanel({ title, items, tone }: { title: string; items: string[]; tone: "danger" | "primary" }) {
  const toneClass = tone === "danger" ? "border-destructive/30 bg-destructive/10" : "border-primary/30 bg-primary/10";

  return (
    <div className={`rounded-2xl border p-5 ${toneClass}`}>
      <div className="font-bold text-lg">{title}</div>
      <div className="space-y-3 mt-4">
        {items.map((item) => (
          <div key={item} className="text-sm text-foreground">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}