"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { persistSession } from "@/lib/auth-storage";
import { PLAN_PREVIEW } from "@/lib/plan-copy";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ company_name: "", full_name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (form.password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres.");
      return;
    }
    setLoading(true);
    try {
      const res = await api.register(form);
      persistSession(res.access_token, res.user);
      router.replace("/app");
    } catch (err: any) {
      setError(err?.message ?? "No pudimos crear tu cuenta.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid lg:grid-cols-[1.05fr_0.95fr] gap-6 p-6 lg:p-10 items-center">
      <section className="space-y-6 max-w-2xl">
        <Link href="/" className="text-xs text-muted-foreground hover:text-foreground">
          ← Volver
        </Link>
        <div>
          <div className="text-xs uppercase tracking-widest text-primary font-bold mb-3">Prueba guiada de 14 días</div>
          <h1 className="text-4xl font-black leading-tight">Empieza con tus archivos y termina con decisiones claras de compra.</h1>
          <p className="text-muted-foreground mt-3 max-w-xl">
            Crea la cuenta, sube tu Excel y mira en pesos qué te está dejando plata quieta, qué se te va a acabar y qué deberías pedir primero.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {PLAN_PREVIEW.map((plan) => (
            <div key={plan.key} className="card-glass p-5">
              <div className="flex items-center justify-between gap-3">
                <div className="font-bold">{plan.name}</div>
                <div className="text-xs text-primary font-semibold">{plan.price}</div>
              </div>
              <p className="text-sm text-muted-foreground mt-3">{plan.hook}</p>
              <ul className="space-y-2 mt-4 text-sm text-muted-foreground list-disc pl-5">
                {plan.bullets.map((bullet) => (
                  <li key={bullet}>{bullet}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <section className="card-glass w-full max-w-md p-8 justify-self-center">
        <h1 className="text-2xl font-bold mb-1">Empieza gratis 14 días</h1>
        <p className="text-sm text-muted-foreground mb-6">
          Sin tarjeta. Sin compromiso. Mira tu plata atrapada.
        </p>

        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label>Nombre de tu negocio</Label>
            <Input value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} required />
          </div>
          <div className="space-y-2">
            <Label>Tu nombre</Label>
            <Input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required />
          </div>
          <div className="space-y-2">
            <Label>Tu correo</Label>
            <Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </div>
          <div className="space-y-2">
            <Label>Contraseña (mínimo 8)</Label>
            <Input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>
          {error ? <p className="text-sm text-destructive">{error}</p> : null}
          <Button type="submit" className="w-full" size="lg" disabled={loading}>
            {loading ? "Creando cuenta..." : "🚀 Activar mi prueba gratis"}
          </Button>
        </form>

        <div className="text-sm text-muted-foreground mt-6 text-center">
          ¿Ya tienes cuenta?{" "}
          <Link href="/login" className="text-primary font-semibold">
            Entrar
          </Link>
        </div>
      </section>
    </div>
  );
}
