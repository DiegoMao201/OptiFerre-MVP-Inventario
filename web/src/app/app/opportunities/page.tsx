"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatCurrency, formatNumber } from "@/lib/utils";

export default function OpportunitiesPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["opportunities"],
    queryFn: () => api.opportunities(200)
  });

  return (
    <div className="space-y-6 max-w-6xl">
      <header>
        <div className="text-xs uppercase tracking-widest text-accent font-bold">Qué comprar</div>
        <h1 className="text-3xl md:text-4xl font-black mt-1">Productos que sí debes pedir ya</h1>
        <p className="text-muted-foreground mt-2 max-w-xl">
          Aquí va lo que se te va a acabar o ya está en quiebre. Si lo pides hoy, no pierdes ventas.
        </p>
      </header>

      {data ? (
        <div className="card-glass !p-4">
          <div className="text-sm text-muted-foreground mb-3 px-2">
            {formatNumber(data.total)} oportunidades · {formatCurrency(data.total_value)} en compra recomendada
          </div>
          <div className="overflow-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-muted-foreground border-b border-white/5">
                  <th className="px-3 py-2">SKU</th>
                  <th className="px-3 py-2">Producto</th>
                  <th className="px-3 py-2">Estado</th>
                  <th className="px-3 py-2 text-right">Stock hoy</th>
                  <th className="px-3 py-2 text-right">Días que aguanta</th>
                  <th className="px-3 py-2 text-right">Sugerimos comprar</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((row) => (
                  <tr key={row.sku} className="border-b border-white/5 hover:bg-white/5">
                    <td className="px-3 py-2 font-mono text-xs">{row.sku}</td>
                    <td className="px-3 py-2">{row.nombre}</td>
                    <td className="px-3 py-2">
                      <Badge state={row.estado} />
                    </td>
                    <td className="px-3 py-2 text-right">{formatNumber(row.stock_actual)}</td>
                    <td className="px-3 py-2 text-right">
                      {row.dias_cobertura == null ? "—" : `${Math.round(row.dias_cobertura)} d`}
                    </td>
                    <td className="px-3 py-2 text-right text-accent font-semibold">
                      {formatNumber(row.sugerencia_compra)} u
                    </td>
                  </tr>
                ))}
                {data.items.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-3 py-8 text-center text-muted-foreground">
                      Por ahora no hay urgencias de compra.
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

function Badge({ state }: { state: string }) {
  const map: Record<string, string> = {
    QUIEBRE: "bg-destructive/20 text-destructive border-destructive/40",
    REPONER: "bg-primary/20 text-primary border-primary/40",
    OK: "bg-accent/20 text-accent border-accent/40",
    SOBRESTOCK: "bg-muted text-muted-foreground border-white/10"
  };
  const cls = map[state] || "bg-muted text-muted-foreground";
  return <span className={`text-xs font-bold px-2 py-1 rounded-md border ${cls}`}>{state}</span>;
}
