"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, AlertTriangle, Bot, MapPin, MessageCircle, PackageOpen, ShieldCheck, Wallet, Sparkles } from "lucide-react";
import { PublicAiFaq } from "@/components/public-ai-faq";

const salesPhone = "+57 320 504 6277";
const whatsappHref = `https://wa.me/${salesPhone.replace(/\D/g, "")}`;

const helpPlanCards = [
  {
    name: "Starter",
    title: "Te acompaña a arrancar",
    text: "Te ayuda a subir bien los archivos y empezar sin perder tiempo en errores y enredos.",
  },
  {
    name: "Pro",
    title: "Te muestra dónde está la plata quieta",
    text: "Te dice en palabras simples qué está quieto, qué se te puede acabar y qué sí vale la pena volver a pedir.",
  },
  {
    name: "Enterprise",
    title: "Te ayuda a mover compras más rápido",
    text: "Te deja pasar de mirar el problema a dejar listas compras y mensajes para el proveedor.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(250,204,21,0.18),_transparent_22%),radial-gradient(circle_at_20%_20%,_rgba(14,165,233,0.18),_transparent_28%),radial-gradient(circle_at_80%_10%,_rgba(34,197,94,0.14),_transparent_24%),linear-gradient(180deg,_rgba(8,15,31,1)_0%,_rgba(8,12,24,1)_100%)]">
      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute left-[-8rem] top-16 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="absolute right-[-5rem] top-24 h-80 w-80 rounded-full bg-yellow-300/20 blur-3xl" />
        <div className="absolute bottom-10 left-1/3 h-64 w-64 rounded-full bg-primary/20 blur-3xl" />
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-300/70 to-transparent shadow-[0_0_25px_rgba(103,232,249,0.8)]" />
      </div>
      <header className="container flex items-center justify-between py-6">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl border border-cyan-300/40 bg-cyan-300/15 grid place-content-center text-cyan-200 font-black shadow-[0_0_24px_rgba(103,232,249,0.35)]">O</div>
          <div className="font-bold tracking-tight text-lg">OptiFerre</div>
        </div>
        <nav className="flex items-center gap-3">
          <Link href="/login" className="text-sm text-muted-foreground hover:text-foreground">
            Entrar
          </Link>
          <Button asChild size="sm">
            <Link href="/register">Empezar gratis</Link>
          </Button>
        </nav>
      </header>

      <main className="container">
        <section className="grid lg:grid-cols-2 gap-10 py-16 items-center">
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-300/35 bg-cyan-300/10 px-4 py-1.5 text-xs font-bold text-cyan-200 uppercase tracking-widest shadow-[0_0_30px_rgba(34,211,238,0.18)]">
              💰 Para ferreterías y depósitos
            </div>
            <h1 className="text-4xl md:text-6xl font-black leading-[1.05]">
              Tienes <span className="shimmer-text">plata quieta</span> en tu bodega y no lo sabes.
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl">
              Sube tu Excel de inventario y ventas. En minutos ves qué dinero está atrapado, qué productos están muertos y qué compra sí te conviene hacer para vender más sin inflar la bodega.
            </p>
            <div className="rounded-3xl border border-yellow-300/30 bg-yellow-300/10 px-5 py-4 shadow-[0_0_35px_rgba(253,224,71,0.14)]">
              <div className="text-xs font-black uppercase tracking-[0.25em] text-yellow-200">Prueba gratis destacada</div>
              <div className="mt-2 text-base font-semibold text-yellow-50">14 días para ver con tus propios números qué plata tienes quieta, sin tarjeta y sin enredos.</div>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <Button asChild size="lg" className="shadow-[0_0_30px_rgba(250,204,21,0.35)]">
                <Link href="/register">
                  Empezar mi prueba gratis <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/demo">Ver ejemplo real</Link>
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="rounded-full border border-yellow-300/20 bg-yellow-300/10 px-3 py-1 text-xs text-yellow-100">14 días gratis</span>
              <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs text-cyan-100">Funciona con tu Excel</span>
              <span className="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1 text-xs text-emerald-100">Sin tarjeta</span>
            </div>
            <div className="grid gap-3 sm:grid-cols-3 pt-4">
              <TrustBadge icon={<MapPin className="h-4 w-4" />} label="Pereira, Colombia" />
              <TrustBadge icon={<ShieldCheck className="h-4 w-4" />} label="Fundador visible" />
              <TrustBadge icon={<MessageCircle className="h-4 w-4" />} label="WhatsApp real" />
            </div>
          </div>

          <div className="relative grid grid-cols-2 gap-4">
            <div className="absolute -inset-4 -z-10 rounded-[2rem] bg-gradient-to-br from-cyan-400/10 via-transparent to-yellow-300/10 blur-2xl" />
            <FeatureBox icon={<Wallet className="h-5 w-5" />} title="💰 Plata muerta" text="Cuánto dinero está congelado en bodega ahora mismo." />
            <FeatureBox icon={<AlertTriangle className="h-5 w-5" />} title="⚠️ Quiebre" text="Qué productos se te van a acabar antes de tiempo." />
            <FeatureBox icon={<PackageOpen className="h-5 w-5" />} title="📦 Compra justa" text="Cuánto pedir para no quebrarte y no sobrar." />
            <FeatureBox icon={<Sparkles className="h-5 w-5" />} title="✨ Estrellas" text="Los productos que sí rotan y debes proteger." />
          </div>
        </section>

        <section className="py-20 grid md:grid-cols-3 gap-6">
          <Step number="1" title="Subes tu Excel" text="El mismo archivo que ya manejas. No tienes que cambiar de sistema." />
          <Step number="2" title="Te mostramos el problema" text="Ves rápido qué está quieto, qué se te va a acabar y por dónde se te está yendo la plata." />
          <Step number="3" title="Te damos decisiones claras" text="Qué vender, qué no comprar, qué pedir y cuánta plata recuperas." />
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr] my-10">
          <div className="card-glass p-8">
            <div className="text-xs uppercase tracking-widest text-primary font-bold">Prueba real</div>
            <h2 className="text-3xl md:text-4xl font-black mt-2">Ferretería en Pereira: números que sí mueven una decisión de compra.</h2>
            <p className="text-muted-foreground mt-3 max-w-2xl">
              Aunque sea un caso piloto, esto ayuda a que el cliente vea rápido si la app le puede ahorrar plata y mejorar sus compras.
            </p>
            <div className="grid md:grid-cols-3 gap-4 mt-6">
              <ProofCard value="$12.000.000" label="quietos en inventario" />
              <ProofCard value="22" label="productos muertos detectados" />
              <ProofCard value="2 semanas" label="para mejorar la compra" />
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 mt-6 text-sm text-muted-foreground">
              Resultado esperado del piloto: dejar de recomprar lento, priorizar lo que sí vende y hablar de compras con números, no con corazonadas.
            </div>
          </div>

          <div className="card-glass p-8">
            <div className="text-xs uppercase tracking-widest text-primary font-bold">Quién está detrás</div>
            <h2 className="text-3xl font-black mt-2">Diego Mauricio Garcia</h2>
            <p className="text-muted-foreground mt-3">
              Creador de OptiFerre. Trabajando desde Pereira y disponible para mostrar personalmente cómo sacar plata atrapada de la bodega usando el mismo Excel de siempre.
            </p>
            <div className="space-y-3 mt-6 text-sm">
              <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">Pereira, Colombia</div>
              <a className="block rounded-2xl border border-white/10 bg-white/5 px-4 py-3 hover:border-primary/40" href="mailto:diegomao.201@gmail.com">diegomao.201@gmail.com</a>
              <a className="block rounded-2xl border border-primary/30 bg-primary/10 px-4 py-3 hover:border-primary/50" href={whatsappHref} target="_blank" rel="noreferrer">
                WhatsApp: {salesPhone}
              </a>
            </div>
          </div>
        </section>

        <section className="grid gap-6 my-16 lg:grid-cols-[0.9fr_1.1fr] items-start">
          <div className="space-y-4">
            <div className="inline-flex items-center rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs uppercase tracking-widest text-primary font-bold shadow-[0_0_24px_rgba(245,158,11,0.16)]">Ayuda según tu plan</div>
            <h2 className="text-3xl md:text-4xl font-black">No compras palabras raras. Compras ayuda para vender mejor y dejar plata menos tiempo quieta.</h2>
            <p className="text-muted-foreground max-w-2xl">
              El mensaje tiene que ser simple: primero te ayudan a arrancar, luego te muestran dónde estás perdiendo plata y después te ayudan a mover compras más rápido.
            </p>
            <div className="rounded-3xl border border-cyan-300/25 bg-cyan-300/10 p-5 shadow-[0_0_35px_rgba(34,211,238,0.12)]">
              <div className="text-xs uppercase tracking-[0.25em] text-cyan-200 font-black">IA que responde enfocada</div>
              <p className="mt-3 text-sm text-cyan-50/90">
                Aquí no ves una IA genérica. Ves una ayuda que responde sobre inventario, compras y plata quieta. Y en Enterprise pasa de responder a ayudarte a dejar tareas listas para mover el negocio más rápido.
              </p>
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {helpPlanCards.map((plan) => (
              <div key={plan.name} className={`card-glass p-5 ${plan.name === "Enterprise" ? "border-primary/40 shadow-[0_0_40px_rgba(245,158,11,0.18)]" : ""}`}>
                <div className="h-10 w-10 rounded-xl bg-primary/15 text-primary grid place-content-center mb-3 shadow-[0_0_22px_rgba(245,158,11,0.18)]">
                  <Bot className="h-5 w-5" />
                </div>
                <div className="text-xs uppercase tracking-widest text-primary font-bold">{plan.name}</div>
                <div className="font-bold text-lg mt-2">{plan.title}</div>
                <p className="text-sm text-muted-foreground mt-2">{plan.text}</p>
                {plan.name === "Enterprise" ? (
                  <div className="mt-4 rounded-2xl border border-yellow-300/25 bg-yellow-300/10 px-3 py-2 text-xs font-semibold text-yellow-100">
                    La IA toma más trabajo operativo y te ayuda a automatizar mucho más del día a día.
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </section>

        <section className="relative my-16">
          <div className="pointer-events-none absolute inset-x-10 top-0 -z-10 h-full rounded-[2rem] bg-gradient-to-r from-cyan-400/10 via-primary/10 to-yellow-300/10 blur-3xl" />
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div>
              <div className="inline-flex items-center rounded-full border border-cyan-300/30 bg-cyan-300/10 px-4 py-1.5 text-xs uppercase tracking-widest text-cyan-200 font-bold shadow-[0_0_24px_rgba(34,211,238,0.18)]">
                LLM super importante
              </div>
              <h2 className="mt-3 text-3xl md:text-4xl font-black">Mira cómo responde la IA metida en el negocio, no por fuera.</h2>
            </div>
            <div className="max-w-md rounded-3xl border border-primary/25 bg-primary/10 px-5 py-4 text-sm text-primary-foreground/90 shadow-[0_0_35px_rgba(245,158,11,0.15)]">
              Mientras más sube el plan, más ayuda te da: desde orientarte hasta dejarte trabajo listo para automatizar compras, prioridades y seguimiento.
            </div>
          </div>
          <PublicAiFaq />
        </section>

        <section className="rounded-3xl border border-primary/30 bg-[linear-gradient(135deg,rgba(245,158,11,0.16),rgba(34,211,238,0.1),rgba(250,204,21,0.12))] p-10 text-center my-16 shadow-[0_0_60px_rgba(245,158,11,0.14)]">
          <h2 className="text-3xl md:text-4xl font-black mb-3">
            Hoy puedes saber cuánta <span className="shimmer-text">plata tienes muerta</span> en bodega.
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto mb-6">
            14 días gratis, con tu propia data, sin tarjeta y sin compromiso.
          </p>
          <Button asChild size="lg" className="shadow-[0_0_36px_rgba(250,204,21,0.35)]">
            <Link href="/register">
              Quiero ver mi plata atrapada <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <div className="flex flex-wrap justify-center gap-3 mt-4">
            <Button asChild size="lg" variant="outline">
              <Link href="/demo">Ver ejemplo real</Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <a href={whatsappHref} target="_blank" rel="noreferrer">Hablar por WhatsApp</a>
            </Button>
          </div>
        </section>
      </main>

      <footer className="container py-8 text-xs text-muted-foreground border-t border-white/5">
        © 2026 OptiFerre · Diego Mauricio Garcia · diegomao.201@gmail.com
      </footer>
    </div>
  );
}

function TrustBadge({ icon, label }: { icon: ReactNode; label: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-muted-foreground flex items-center gap-2 shadow-[0_0_24px_rgba(255,255,255,0.04)]">
      <span className="text-primary">{icon}</span>
      <span>{label}</span>
    </div>
  );
}

function ProofCard({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5 shadow-[0_0_30px_rgba(250,204,21,0.08)]">
      <div className="text-3xl font-black shimmer-text">{value}</div>
      <div className="text-sm text-muted-foreground mt-2">{label}</div>
    </div>
  );
}

function FeatureBox({ icon, title, text }: { icon: ReactNode; title: string; text: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5 shadow-[0_0_30px_rgba(34,211,238,0.06)]">
      <div className="h-10 w-10 rounded-xl bg-primary/15 text-primary grid place-content-center mb-3 shadow-[0_0_20px_rgba(245,158,11,0.18)]">{icon}</div>
      <div className="font-semibold mb-1">{title}</div>
      <div className="text-sm text-muted-foreground">{text}</div>
    </div>
  );
}

function Step({ number, title, text }: { number: string; title: string; text: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-card/40 p-6 shadow-[0_0_30px_rgba(255,255,255,0.03)]">
      <div className="text-primary text-xs font-bold tracking-widest mb-2">PASO {number}</div>
      <div className="font-bold text-xl mb-2">{title}</div>
      <div className="text-sm text-muted-foreground">{text}</div>
    </div>
  );
}
