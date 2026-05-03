import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, AlertTriangle, PackageOpen, Wallet, Sparkles } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      <header className="container flex items-center justify-between py-6">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-primary/20 border border-primary/40 grid place-content-center text-primary font-black">O</div>
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
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-bold text-primary uppercase tracking-widest">
              💰 Para ferreterías y depósitos
            </div>
            <h1 className="text-4xl md:text-6xl font-black leading-[1.05]">
              Tienes <span className="text-primary">plata muerta</span> en tu bodega y todavía no lo sabes.
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl">
              Sube tu Excel de inventario y de ventas. En minutos te decimos qué productos están quietos, cuáles se te van a acabar y cuánto deberías comprar la próxima vez. Sin instalar nada.
            </p>
            <div className="flex flex-wrap items-center gap-3">
              <Button asChild size="lg">
                <Link href="/register">
                  Empezar mi prueba gratis <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/login">Ya tengo cuenta</Link>
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">14 días gratis</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">Funciona con tu Excel</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">Sin tarjeta</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <FeatureBox icon={<Wallet className="h-5 w-5" />} title="💰 Plata muerta" text="Cuánto dinero está congelado en bodega ahora mismo." />
            <FeatureBox icon={<AlertTriangle className="h-5 w-5" />} title="⚠️ Quiebre" text="Qué productos se te van a acabar antes de tiempo." />
            <FeatureBox icon={<PackageOpen className="h-5 w-5" />} title="📦 Compra justa" text="Cuánto pedir para no quebrarte y no sobrar." />
            <FeatureBox icon={<Sparkles className="h-5 w-5" />} title="✨ Estrellas" text="Los productos que sí rotan y debes proteger." />
          </div>
        </section>

        <section className="py-20 grid md:grid-cols-3 gap-6">
          <Step number="1" title="Subes tu Excel" text="El mismo archivo que ya manejas. No tienes que cambiar de sistema." />
          <Step number="2" title="Analizamos en minutos" text="Cruzamos tu inventario con tus ventas y calculamos lo que importa." />
          <Step number="3" title="Te damos decisiones claras" text="Qué vender, qué no comprar, qué pedir y cuánta plata recuperas." />
        </section>

        <section className="rounded-3xl border border-primary/20 bg-primary/5 p-10 text-center my-16">
          <h2 className="text-3xl md:text-4xl font-black mb-3">
            Hoy puedes saber cuánta plata tienes muerta en bodega.
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto mb-6">
            14 días gratis, con tu propia data, sin tarjeta y sin compromiso.
          </p>
          <Button asChild size="lg">
            <Link href="/register">
              Quiero ver mi plata atrapada <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
        </section>
      </main>

      <footer className="container py-8 text-xs text-muted-foreground border-t border-white/5">
        © {new Date().getFullYear()} OptiFerre · Diego Mauricio Garcia · diegomao.201@gmail.com
      </footer>
    </div>
  );
}

function FeatureBox({ icon, title, text }: { icon: React.ReactNode; title: string; text: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <div className="h-10 w-10 rounded-xl bg-primary/15 text-primary grid place-content-center mb-3">{icon}</div>
      <div className="font-semibold mb-1">{title}</div>
      <div className="text-sm text-muted-foreground">{text}</div>
    </div>
  );
}

function Step({ number, title, text }: { number: string; title: string; text: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-card/40 p-6">
      <div className="text-primary text-xs font-bold tracking-widest mb-2">PASO {number}</div>
      <div className="font-bold text-xl mb-2">{title}</div>
      <div className="text-sm text-muted-foreground">{text}</div>
    </div>
  );
}
