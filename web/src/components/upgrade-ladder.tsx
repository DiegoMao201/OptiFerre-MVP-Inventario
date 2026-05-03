"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

type PlanCard = {
  key: string;
  name: string;
  tagline: string;
  summary: string;
  sales_pitch: string;
  upgrade_trigger: string;
  cta_label: string;
  price_monthly_usd: number;
};

type UpgradeLadderProps = {
  plans: PlanCard[];
  currentPlan?: string | null;
  title: string;
  intro: string;
  compact?: boolean;
};

const PLAN_ORDER = ["starter", "trial", "pro", "enterprise"];

export function UpgradeLadder({ plans, currentPlan, title, intro, compact = false }: UpgradeLadderProps) {
  const normalizedCurrent = (currentPlan || "trial").toLowerCase();
  const currentRank = PLAN_ORDER.indexOf(normalizedCurrent);
  const nextPlans = plans.filter((plan) => PLAN_ORDER.indexOf(plan.key) > currentRank).slice(0, compact ? 1 : 2);

  if (!nextPlans.length) {
    return null;
  }

  return (
    <section className="card-glass p-6 space-y-5">
      <div>
        <div className="text-xs uppercase tracking-widest text-primary font-bold">Escalera de valor</div>
        <h2 className="text-2xl font-black mt-1">{title}</h2>
        <p className="text-muted-foreground mt-2 max-w-3xl">{intro}</p>
      </div>

      <div className={`grid gap-4 ${compact ? "md:grid-cols-1" : "md:grid-cols-2"}`}>
        {nextPlans.map((plan) => (
          <article key={plan.key} className="rounded-2xl border border-white/10 bg-white/5 p-5 space-y-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-widest text-primary font-bold">{plan.tagline}</div>
                <h3 className="text-xl font-black mt-1">{plan.name}</h3>
              </div>
              <div className="text-right">
                <div className="text-2xl font-black">USD {plan.price_monthly_usd}</div>
                <div className="text-xs text-muted-foreground">por mes</div>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">{plan.sales_pitch}</p>
            <div className="rounded-2xl border border-primary/20 bg-primary/10 px-4 py-3 text-sm text-foreground">
              <strong className="block mb-1">Qué te desbloquea</strong>
              {plan.summary}
            </div>
            <div className="text-sm text-muted-foreground">
              <strong className="text-foreground block mb-1">Cuándo tiene sentido subir</strong>
              {plan.upgrade_trigger}
            </div>
            <Button asChild className="w-full" variant={plan.key === "pro" ? "default" : "outline"}>
              <Link href="/app/plans">{plan.cta_label}</Link>
            </Button>
          </article>
        ))}
      </div>
    </section>
  );
}