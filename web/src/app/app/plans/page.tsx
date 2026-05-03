"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

export default function PlansPage() {
  const { data: plans } = useQuery({ queryKey: ["plans"], queryFn: api.plans });
  const { data: subscription } = useQuery({ queryKey: ["subscription"], queryFn: api.subscription });
  const checkout = useMutation({
    mutationFn: api.createCheckout,
    onSuccess: (res) => {
      if (res.url) {
        window.location.href = res.url;
      }
    },
  });

  return (
    <div className="space-y-8 max-w-7xl">
      <header className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="text-xs uppercase tracking-widest text-primary font-bold">Planes claros y comprables</div>
          <h1 className="text-3xl md:text-4xl font-black mt-1">Elige el plan según el momento real de tu negocio.</h1>
          <p className="text-muted-foreground mt-2 max-w-3xl">
            Aquí ves qué ganas con cada plan: ordenar tus archivos, encontrar plata quieta y comprar mejor sin volver a improvisar.
          </p>
        </div>
        <div className="card-glass px-5 py-4 min-w-72">
          <div className="text-xs uppercase tracking-widest text-primary font-bold">Tu estado actual</div>
          <div className="text-xl font-bold mt-1">{subscription?.subscription?.plan || "prueba gratis"}</div>
          <p className="text-sm text-muted-foreground mt-2">Estado: {subscription?.subscription?.status || "activa"}</p>
        </div>
      </header>

      <section className="grid gap-4 xl:grid-cols-3">
        {plans?.plans.map((plan) => (
          <article key={plan.key} className={`card-glass p-6 flex flex-col ${plan.key === "pro" ? "border-primary/40 shadow-primary/20" : ""}`}>
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-widest text-primary font-bold">{plan.tagline}</div>
                <h2 className="text-2xl font-black mt-1">{plan.name}</h2>
              </div>
              <div className="text-right">
                <div className="text-3xl font-black">USD {plan.price_monthly_usd}</div>
                <div className="text-xs text-muted-foreground">por mes</div>
              </div>
            </div>

            <p className="text-sm text-muted-foreground mt-4">{plan.summary}</p>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 mt-4 text-sm text-muted-foreground">
              {plan.sales_pitch}
            </div>

            <div className="mt-5 space-y-2 flex-1">
              {plan.features.map((feature) => (
                <div key={feature} className="text-sm text-muted-foreground">• {feature}</div>
              ))}
            </div>

            <div className="mt-6 space-y-3">
              {plan.key === "enterprise" ? (
                <Button asChild size="lg" className="w-full">
                  <a href={`mailto:${plan.sales_email}?subject=Quiero%20Enterprise%20en%20OptiFerre`}>Hablar con ventas</a>
                </Button>
              ) : (
                <Button size="lg" className="w-full" onClick={() => checkout.mutate(plan.key)} disabled={checkout.isPending}>
                  {checkout.isPending ? "Procesando..." : `Elegir ${plan.name}`}
                </Button>
              )}
              <p className="text-xs text-muted-foreground">
                {plan.upgrade_trigger}
              </p>
              {checkout.data?.message && checkout.variables === plan.key ? <p className="text-sm text-accent">{checkout.data.message}</p> : null}
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}