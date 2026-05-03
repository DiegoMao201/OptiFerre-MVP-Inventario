"use client";

import { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function KpiCard({
  label,
  value,
  hint,
  icon,
  tone = "default"
}: {
  label: string;
  value: string;
  hint?: string;
  icon?: ReactNode;
  tone?: "default" | "danger" | "success" | "primary";
}) {
  const toneClasses = {
    default: "from-white/5 to-white/0 border-white/10",
    primary: "from-primary/15 to-primary/0 border-primary/30",
    danger: "from-destructive/20 to-destructive/0 border-destructive/30",
    success: "from-accent/20 to-accent/0 border-accent/30"
  }[tone];

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl border bg-gradient-to-br p-5 shadow-xl",
        toneClasses
      )}
    >
      <div className="flex items-start justify-between">
        <span className="text-xs uppercase tracking-wider text-muted-foreground">{label}</span>
        {icon ? <span className="text-foreground/70">{icon}</span> : null}
      </div>
      <div className="mt-3 text-3xl font-bold leading-tight">{value}</div>
      {hint ? <div className="mt-2 text-xs text-muted-foreground">{hint}</div> : null}
    </div>
  );
}
