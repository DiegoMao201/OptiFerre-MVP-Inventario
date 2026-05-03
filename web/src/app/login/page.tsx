"use client";

import { useState, type FormEvent, type ReactNode } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { MapPin, MessageCircle, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { persistSession } from "@/lib/auth-storage";
import { PLAN_PREVIEW } from "@/lib/plan-copy";

const salesPhone = process.env.NEXT_PUBLIC_SALES_CONTACT_PHONE || "+57 300 000 0000";
const whatsappHref = `https://wa.me/${salesPhone.replace(/\D/g, "")}`;

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: FormEvent) => {
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
          <div className="text-xs uppercase tracking-widest text-primary font-bold mb-3">OptiFerre · Para ferreterías y depósitos</div>
          <h1 className="text-4xl font-black mb-4 leading-tight">
            Entra y mira dónde tienes la plata quieta y qué sí deberías volver a vender.
          </h1>
          <p className="text-muted-foreground">
            Aquí no vienes a ver gráficos bonitos. Vienes a ver qué tienes muerto, qué se te puede acabar y cómo dejar de comprar a ojo.
          </p>
          <div className="grid gap-3 sm:grid-cols-3 mt-6">
            <TrustPill icon={<MapPin className="h-4 w-4" />} label="Pereira" />
            <TrustPill icon={<ShieldCheck className="h-4 w-4" />} label="Caso piloto real" />
            <TrustPill icon={<MessageCircle className="h-4 w-4" />} label="WhatsApp directo" />
          </div>
          <div className="card-glass p-4 mt-6">
            <div className="text-xs uppercase tracking-widest text-primary font-bold">Ejemplo real</div>
            <div className="text-2xl font-black mt-2">$12.000.000 quietos</div>
            <p className="text-sm text-muted-foreground mt-2">
              Ferretería en Pereira: 22 productos muertos detectados y compras más claras en 2 semanas.
            </p>
          </div>
          <div className="card-glass p-4 mt-4">
            <div className="text-xs uppercase tracking-widest text-primary font-bold">Ayuda según tu plan</div>
            <div className="space-y-3 mt-3 text-sm text-muted-foreground">
              <p><strong className="text-foreground">Starter:</strong> te ayuda a subir bien los archivos y arrancar rápido.</p>
              <p><strong className="text-foreground">Pro:</strong> te muestra qué está quieto y qué sí conviene volver a pedir.</p>
              <p><strong className="text-foreground">Enterprise:</strong> te ayuda a dejar listas compras y mensajes para proveedores.</p>
            </div>
          </div>
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
        <div className="flex items-center justify-between gap-4 text-xs text-muted-foreground">
          <span>© OptiFerre · diegomao.201@gmail.com</span>
          <a href={whatsappHref} target="_blank" rel="noreferrer" className="text-primary font-semibold">WhatsApp</a>
        </div>
      </section>

      <section className="flex items-center justify-center p-6">
        <div className="card-glass w-full max-w-md p-8">
          <h2 className="text-2xl font-bold mb-1">Entrar a tu cuenta</h2>
          <p className="text-sm text-muted-foreground mb-6">Entra y mira qué te está enterrando plata y qué sí deberías mover primero.</p>

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
          <div className="mt-5 rounded-2xl border border-primary/20 bg-primary/10 p-4 text-sm text-muted-foreground">
            Si todavía no conoces la app, entra a la prueba y mira un ejemplo real de plata quieta, productos muertos y compras más claras.
          </div>
        </div>
      </section>
    </div>
  );
}

function TrustPill({ icon, label }: { icon: ReactNode; label: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-3 py-3 text-sm text-muted-foreground flex items-center gap-2">
      <span className="text-primary">{icon}</span>
      <span>{label}</span>
    </div>
  );
}
