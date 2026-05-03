"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatCurrency, formatNumber } from "@/lib/utils";

export default function DeadProductsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["dead-products"],
    queryFn: () => api.deadProducts(200)
  });

  return (
    <div className="space-y-6 max-w-6xl">
      <header>
        <div className="text-xs uppercase tracking-widest text-destructive font-bold">Plata muerta</div>
        <h1 className="text-3xl md:text-4xl font-black mt-1">Productos que te están comiendo el flujo de caja</h1>
        <p className="text-muted-foreground mt-2 max-w-xl">
          Estos llevan meses sin moverse. Decide cuáles rematar, devolver o dejar de pedir.
        </p>
      </header>

      {data ? (
        <div className="card-glass !p-4">
          <div className="text-sm text-muted-foreground mb-3 px-2">
            {formatNumber(data.total)} productos · {formatCurrency(data.total_value)} congelados
          </div>
          <div className="overflow-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-muted-foreground border-b border-white/5">
                  <th className="px-3 py-2">SKU</th>
                  <th className="px-3 py-2">Producto</th>
                  <th className="px-3 py-2 text-right">Stock</th>
                  <th className="px-3 py-2 text-right">Valor en bodega</th>
                  <th className="px-3 py-2 text-right">Te cuesta/mes</th>
                  <th className="px-3 py-2">Categoría</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((row) => (
                  <tr key={row.sku} className="border-b border-white/5 hover:bg-white/5">
                    <td className="px-3 py-2 font-mono text-xs">{row.sku}</td>
                    <td className="px-3 py-2">{row.nombre}</td>
                    <td className="px-3 py-2 text-right">{formatNumber(row.stock_actual)}</td>
                    <td className="px-3 py-2 text-right text-destructive font-semibold">
                      {formatCurrency(row.valor_inventario)}
                    </td>
                    <td className="px-3 py-2 text-right">{formatCurrency(row.costo_oportunidad_mensual)}</td>
                    <td className="px-3 py-2 text-muted-foreground">{row.categoria || "—"}</td>
                  </tr>
                ))}
                {data.items.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-3 py-8 text-center text-muted-foreground">
                      🎉 No detectamos productos muertos. Tu rotación está sana.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="text-muted-foreground">{isLoading ? "Cargando..." : "Sin datos."}</div>
      )}
    </div>
  );
}
