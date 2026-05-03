"use client";

import { useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { formatCurrency, formatNumber } from "@/lib/utils";
import { ShoppingCart } from "lucide-react";

export default function PurchaseOrdersPage() {
  const generate = useMutation({ mutationFn: api.generatePurchaseOrder });

  return (
    <div className="space-y-6 max-w-3xl">
      <header>
        <div className="text-xs uppercase tracking-widest text-accent font-bold">Órdenes de compra</div>
        <h1 className="text-3xl md:text-4xl font-black mt-1">Convierte la sugerencia en una orden lista</h1>
        <p className="text-muted-foreground mt-2 max-w-xl">
          Generamos la orden con todo lo que recomienda el sistema. Después puedes editarla o exportarla a Excel.
        </p>
      </header>

      <div className="card-glass">
        <div className="font-bold mb-2">Crear nueva orden con la sugerencia actual</div>
        <p className="text-sm text-muted-foreground mb-4">
          Toma todos los productos marcados como “comprar” y genera la orden borrador.
        </p>
        <Button onClick={() => generate.mutate()} disabled={generate.isPending} size="lg">
          <ShoppingCart className="h-4 w-4" />
          {generate.isPending ? "Generando..." : "Generar orden de compra"}
        </Button>

        {generate.data ? (
          generate.data.ok ? (
            <div className="mt-6 p-4 rounded-xl border border-accent/40 bg-accent/10">
              <div className="font-semibold text-accent">
                ✅ Orden {generate.data.code} creada
              </div>
              <div className="text-sm text-muted-foreground mt-1">
                {formatNumber(generate.data.items)} productos ·{" "}
                {formatNumber(generate.data.total_units)} unidades ·{" "}
                {formatCurrency(generate.data.total_amount)} total
              </div>
            </div>
          ) : (
            <div className="mt-6 text-sm text-destructive">
              No hay sugerencias activas. Sube ventas y vuelve a analizar.
            </div>
          )
        ) : null}
      </div>
    </div>
  );
}
