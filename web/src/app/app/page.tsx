"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Wallet, PackageX, Sparkles, AlertTriangle, RefreshCcw } from "lucide-react";
import { api } from "@/lib/api";
import { formatCurrency, formatNumber } from "@/lib/utils";
import { KpiCard } from "@/components/kpi-card";
import { Button } from "@/components/ui/button";
import { UpgradeLadder } from "@/components/upgrade-ladder";

export default function DashboardPage() {
  const qc = useQueryClient();
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: api.dashboardSummary
  });
  const { data: subscription } = useQuery({
    queryKey: ["subscription"],
    queryFn: api.subscription,
  });
  const { data: plans } = useQuery({
    queryKey: ["plans"],
    queryFn: api.plans,
  });

  const runAnalysis = useMutation({
    mutationFn: api.runAnalysis,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["dashboard-summary"] })
  });

  return (
    <div className="space-y-8 max-w-6xl">
      <header className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="text-xs uppercase tracking-widest text-primary font-bold">Tu negocio en números</div>
          <h1 className="text-3xl md:text-4xl font-black mt-1">¿Cuánta plata tienes atrapada?</h1>
          <p className="text-muted-foreground mt-2 max-w-xl">
            Esto es lo que pasa hoy en tu bodega. Sin corazonadas, en pesos.
          </p>
        </div>
        <Button onClick={() => runAnalysis.mutate()} variant="outline" disabled={runAnalysis.isPending}>
          <RefreshCcw className="h-4 w-4" />
          {runAnalysis.isPending ? "Analizando..." : "Volver a analizar"}
        </Button>
      </header>

      {isLoading ? (
        <div className="text-muted-foreground">Cargando tu negocio...</div>
      ) : isError ? (
        <div className="text-destructive">No pudimos cargar tus datos. <button className="underline" onClick={() => refetch()}>Reintentar</button></div>
      ) : !data?.has_data ? (
        <EmptyState />
      ) : (
        <>
          <section className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <KpiCard
              label="💰 Dinero atrapado"
              value={formatCurrency(data.dinero_atrapado)}
              hint={`Te cuesta ~${formatCurrency(data.dinero_atrapado_mensual)}/mes en oportunidad`}
              tone="danger"
              icon={<Wallet className="h-5 w-5" />}
            />
            <KpiCard
              label="🔴 Productos muertos"
              value={formatNumber(data.productos_muertos)}
              hint={`${formatCurrency(data.productos_muertos_valor)} congelados en bodega`}
              tone="danger"
              icon={<PackageX className="h-5 w-5" />}
            />
            <KpiCard
              label="🟢 Productos estrella"
              value={formatNumber(data.productos_estrella)}
              hint="Los que sí rotan y no puedes dejar morir"
              tone="success"
              icon={<Sparkles className="h-5 w-5" />}
            />
            <KpiCard
              label="⚠️ Por quebrarse"
              value={formatNumber(data.en_quiebre + data.para_reponer)}
              hint={`${data.en_quiebre} sin stock · ${data.para_reponer} por reponer`}
              tone="primary"
              icon={<AlertTriangle className="h-5 w-5" />}
            />
          </section>

          <section className="grid md:grid-cols-2 gap-4">
            <KpiCard
              label="Capital total en inventario"
              value={formatCurrency(data.capital_total)}
              tone="default"
            />
            <KpiCard
              label="Días promedio de cobertura"
              value={`${Math.round(data.rotacion_promedio_dias)} días`}
              hint="Cuánto te dura el stock al ritmo actual"
              tone="default"
            />
          </section>

          <section className="grid md:grid-cols-3 gap-4">
            <ActionCard
              title="🔴 Mira qué está muerto"
              text="Lista de productos que no rotan, ordenados por dinero perdido."
              href="/app/dead-products"
            />
            <ActionCard
              title="🟢 Qué deberías comprar"
              text="Sugerencia clara de qué pedir para no quebrarte ni sobrar."
              href="/app/opportunities"
            />
            <ActionCard
              title="📦 Generar orden de compra"
              text="Convierte la sugerencia en una orden lista para enviar al proveedor."
              href="/app/purchase-orders"
            />
          </section>

          <section className="card-glass p-6 flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-xs uppercase tracking-widest text-primary font-bold">Plan actual</div>
              <h2 className="text-2xl font-black mt-1">
                {subscription?.subscription?.plan ? `Estás en ${subscription.subscription.plan}` : "Prueba guiada activa"}
              </h2>
              <p className="text-muted-foreground mt-2 max-w-2xl">
                Mantén visibles los planes dentro de la app para que el cliente entienda qué compra, qué desbloquea y por qué vale la pena seguir.
              </p>
            </div>
            <div className="flex gap-3">
              <Button asChild variant="outline">
                <a href="/app/support">Hablar con soporte</a>
              </Button>
              <Button asChild>
                <a href="/app/plans">Ver planes</a>
              </Button>
            </div>
          </section>

          <UpgradeLadder
            plans={plans?.plans || []}
            currentPlan={subscription?.subscription?.plan || "trial"}
            title="Qué sigue después de ver tu inventario en plata"
            intro="Si el cliente ya entendió el problema, la app debe mostrarle el siguiente paso natural para resolver más y depender menos de la intuición."
          />
        </>
      )}
    </div>
  );
}

function ActionCard({ title, text, href }: { title: string; text: string; href: string }) {
  return (
    <a
      href={href}
      className="card-glass block hover:border-primary/40 transition-all"
    >
      <div className="font-bold text-lg mb-1">{title}</div>
      <div className="text-sm text-muted-foreground">{text}</div>
    </a>
  );
}

function EmptyState() {
  return (
    <div className="card-glass text-center max-w-2xl mx-auto py-16">
      <div className="text-5xl mb-4">📦</div>
      <h2 className="text-2xl font-bold mb-2">Aún no vemos tu inventario</h2>
      <p className="text-muted-foreground mb-6">
        Sube tu Excel de inventario y de ventas y en minutos te mostramos cuánta plata tienes muerta.
      </p>
      <Button asChild size="lg">
        <a href="/app/upload">Subir mi Excel</a>
      </Button>
    </div>
  );
}
