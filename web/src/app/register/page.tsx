"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { persistSession } from "@/lib/auth-storage";

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
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card-glass w-full max-w-md p-8">
        <Link href="/" className="text-xs text-muted-foreground hover:text-foreground">
          ← Volver
        </Link>
        <h1 className="text-2xl font-bold mt-3 mb-1">Empieza gratis 14 días</h1>
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
      </div>
    </div>
  );
}
