"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { UploadCloud, FileSpreadsheet, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { UpgradeLadder } from "@/components/upgrade-ladder";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function UploadPage() {
  const qc = useQueryClient();
  const [inventoryFile, setInventoryFile] = useState<File | null>(null);
  const [salesFile, setSalesFile] = useState<File | null>(null);
  const { data: templates } = useQuery({
    queryKey: ["templates"],
    queryFn: api.templates,
  });
  const { data: plans } = useQuery({
    queryKey: ["plans"],
    queryFn: api.plans,
  });
  const { data: subscription } = useQuery({
    queryKey: ["subscription"],
    queryFn: api.subscription,
  });

  const upload = useMutation({
    mutationFn: () => {
      if (!inventoryFile) throw new Error("Selecciona el archivo de inventario.");
      return api.uploadInventory(inventoryFile, salesFile);
    },
    onSuccess: () => {
      qc.invalidateQueries();
    }
  });

  return (
    <div className="space-y-6 max-w-3xl">
      <header>
        <div className="text-xs uppercase tracking-widest text-primary font-bold">Subir información</div>
        <h1 className="text-3xl md:text-4xl font-black mt-1">Sube tu Excel y deja que veamos tu plata</h1>
        <p className="text-muted-foreground mt-2 max-w-xl">
          Necesitamos tu inventario actual y, si lo tienes, tus ventas de los últimos meses. Cuanto más completo, mejor.
        </p>
      </header>

      <div className="grid md:grid-cols-2 gap-4">
        <DropZone
          label="📦 Inventario actual"
          description="CSV o Excel con SKU, stock y costo unitario."
          file={inventoryFile}
          onChange={setInventoryFile}
        />
        <DropZone
          label="🧾 Ventas (opcional pero recomendado)"
          description="CSV o Excel con SKU, fecha y cantidad vendida."
          file={salesFile}
          onChange={setSalesFile}
        />
      </div>

      <section className="space-y-4">
        <div>
          <div className="text-xs uppercase tracking-widest text-primary font-bold">Formatos oficiales</div>
          <h2 className="text-2xl font-black mt-1">Descarga la plantilla correcta antes de subir.</h2>
          <p className="text-muted-foreground mt-2 max-w-2xl">
            Así evitas errores de columnas, reduces idas y vueltas y el cliente entiende exactamente qué debe entregar.
          </p>
        </div>
        <div className="grid gap-4 lg:grid-cols-3">
          {templates?.items.map((template) => (
            <div key={template.key} className="card-glass p-5 space-y-4">
              <div>
                <div className="font-bold text-lg">{template.title}</div>
                <p className="text-sm text-muted-foreground mt-2">{template.description}</p>
              </div>
              <div className="flex flex-wrap gap-2">
                {template.required_columns.map((column) => (
                  <span key={column} className="rounded-full border border-white/10 px-3 py-1 text-xs text-muted-foreground">
                    {column}
                  </span>
                ))}
              </div>
              <div className="flex gap-3">
                <Button asChild variant="outline" size="sm">
                  <a href={`${BASE_URL}${template.csv_url}`} target="_blank" rel="noreferrer">
                    <Download className="h-4 w-4" />
                    CSV
                  </a>
                </Button>
                <Button asChild variant="outline" size="sm">
                  <a href={`${BASE_URL}${template.xlsx_url}`} target="_blank" rel="noreferrer">
                    <Download className="h-4 w-4" />
                    XLSX
                  </a>
                </Button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <div className="flex items-center gap-3">
        <Button size="lg" onClick={() => upload.mutate()} disabled={!inventoryFile || upload.isPending}>
          <UploadCloud className="h-4 w-4" />
          {upload.isPending ? "Subiendo..." : "Subir y analizar"}
        </Button>
        {upload.isError ? (
          <span className="text-destructive text-sm">{(upload.error as Error)?.message}</span>
        ) : null}
        {upload.isSuccess ? (
          <span className="text-accent text-sm">
            ✅ {upload.data.inventory_upserted} productos cargados ·{" "}
            {upload.data.sales_upserted} ventas procesadas. Revisa tu dashboard.
          </span>
        ) : null}
      </div>

      <UpgradeLadder
        plans={plans?.plans || []}
        currentPlan={subscription?.subscription?.plan || "trial"}
        compact
        title="Después de cargar bien, el siguiente paso es sacarle decisiones al dato"
        intro="Aquí es donde la app debe llevar al cliente de ordenar archivos a recuperar caja y luego a ejecutar compras con menos fricción."
      />
    </div>
  );
}

function DropZone({
  label,
  description,
  file,
  onChange
}: {
  label: string;
  description: string;
  file: File | null;
  onChange: (f: File | null) => void;
}) {
  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const f = e.dataTransfer.files?.[0];
    if (f) onChange(f);
  };

  return (
    <label
      className="card-glass cursor-pointer block border-dashed border-2 border-white/10 hover:border-primary/40 transition"
      onDragOver={(e) => e.preventDefault()}
      onDrop={onDrop}
    >
      <div className="flex items-center gap-3 mb-3">
        <FileSpreadsheet className="h-5 w-5 text-primary" />
        <div className="font-semibold">{label}</div>
      </div>
      <div className="text-xs text-muted-foreground mb-4">{description}</div>
      <input
        type="file"
        accept=".csv,.xls,.xlsx"
        className="hidden"
        onChange={(e) => onChange(e.target.files?.[0] ?? null)}
      />
      <div className="text-sm">
        {file ? (
          <span className="text-accent">{file.name}</span>
        ) : (
          <span className="text-muted-foreground">Arrastra el archivo aquí o haz clic.</span>
        )}
      </div>
    </label>
  );
}
