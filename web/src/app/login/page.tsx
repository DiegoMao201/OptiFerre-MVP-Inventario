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

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await api.login(email, password);
      persistSession(res.access_token, res.user);
      router.replace("/app");
    } catch (err: any) {
      setError(err?.message ?? "No pudimos iniciar sesión.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      <section className="hidden lg:flex flex-col justify-between p-10">
        <Link href="/" className="text-sm text-muted-foreground hover:text-foreground">
          ← Volver
        </Link>
        <div className="max-w-md">
          <div className="text-xs uppercase tracking-widest text-primary font-bold mb-3">OptiFerre</div>
          <h1 className="text-4xl font-black mb-4 leading-tight">
            Descubre cuánto dinero tienes quieto en inventario.
          </h1>
          <p className="text-muted-foreground">
            Entra a tu cuenta y mira de una qué productos están muertos, qué se te va a acabar y cuánto deberías comprar.
          </p>
          <div className="space-y-3 mt-8">
            {PLAN_PREVIEW.map((plan) => (
              <div key={plan.key} className="card-glass p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="font-bold">{plan.name}</div>
                  <div className="text-xs text-primary font-semibold">{plan.price}</div>
                </div>
                <p className="text-sm text-muted-foreground mt-2">{plan.hook}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="text-xs text-muted-foreground">© OptiFerre · diegomao.201@gmail.com</div>
      </section>

      <section className="flex items-center justify-center p-6">
        <div className="card-glass w-full max-w-md p-8">
          <h2 className="text-2xl font-bold mb-1">Entrar a tu cuenta</h2>
          <p className="text-sm text-muted-foreground mb-6">Mira tu inventario en plata, no en corazonadas.</p>

          <form onSubmit={onSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Tu correo</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="tu@correo.com"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Contraseña</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="flex justify-end">
              <Link href="/forgot-password" className="text-sm text-primary font-semibold">
                Recuperar contraseña
              </Link>
            </div>
            {error ? <p className="text-sm text-destructive">{error}</p> : null}
            <Button type="submit" className="w-full" size="lg" disabled={loading}>
              {loading ? "Entrando..." : "Entrar a mi cuenta"}
            </Button>
          </form>

          <div className="text-sm text-muted-foreground mt-6 text-center">
            ¿No tienes cuenta?{" "}
            <Link href="/register" className="text-primary font-semibold">
              Empieza gratis 14 días
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
