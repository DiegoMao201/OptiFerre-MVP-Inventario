import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, AlertTriangle, Bot, MapPin, MessageCircle, PackageOpen, ShieldCheck, Wallet, Sparkles } from "lucide-react";
import { PublicAiFaq } from "@/components/public-ai-faq";

const salesPhone = process.env.SALES_CONTACT_PHONE || "+57 300 000 0000";
const whatsappHref = `https://wa.me/${salesPhone.replace(/\D/g, "")}`;

const llmPlanCards = [
  {
    name: "Starter",
    title: "Tu IA concierge",
    text: "Te guía para subir bien los archivos, entender la plataforma y arrancar sin enredos.",
  },
  {
    name: "Pro",
    title: "Tu analista de inventario",
    text: "Lee tus datos y te explica en simple qué está quieto, qué está por quebrarse y qué deberías comprar.",
  },
  {
    name: "Enterprise",
    title: "Tu copiloto operativo",
    text: "Te ayuda a ejecutar órdenes, preparar correos y mover operación con menos fricción.",
  },
];

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
              Tienes <span className="shimmer-text">plata quieta</span> en tu bodega y no lo sabes.
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl">
              Sube tu Excel de inventario y ventas. En minutos ves qué dinero está atrapado, qué productos están muertos y qué compra sí te conviene hacer para vender más sin inflar la bodega.
            </p>
            <div className="flex flex-wrap items-center gap-3">
              <Button asChild size="lg">
                <Link href="/register">
                  Empezar mi prueba gratis <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/demo">Ver ejemplo real</Link>
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">14 días gratis</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">Funciona con tu Excel</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-muted-foreground">Sin tarjeta</span>
            </div>
            <div className="grid gap-3 sm:grid-cols-3 pt-4">
              <TrustBadge icon={<MapPin className="h-4 w-4" />} label="Pereira, Colombia" />
              <TrustBadge icon={<ShieldCheck className="h-4 w-4" />} label="Fundador visible" />
              <TrustBadge icon={<MessageCircle className="h-4 w-4" />} label="WhatsApp real" />
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

        <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr] my-10">
          <div className="card-glass p-8">
            <div className="text-xs uppercase tracking-widest text-primary font-bold">Prueba real</div>
            <h2 className="text-3xl md:text-4xl font-black mt-2">Ferretería en Pereira: números que sí mueven una decisión de compra.</h2>
            <p className="text-muted-foreground mt-3 max-w-2xl">
              Aunque sea un caso piloto, esto baja la incertidumbre y hace tangible el valor del producto en menos de un minuto.
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
              Creador de OptiFerre. Operando desde Pereira y disponible para acompañar personalmente a los primeros clientes que quieran probar la plataforma con su propio Excel.
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
            <div className="text-xs uppercase tracking-widest text-primary font-bold">IA explicada fácil</div>
            <h2 className="text-3xl md:text-4xl font-black">El LLM no es humo: es el nivel de ayuda que recibe el cliente según su plan.</h2>
            <p className="text-muted-foreground max-w-2xl">
              Comercialmente hay que dejarlo simple: en Starter guía, en Pro analiza y en Enterprise ayuda a ejecutar. Eso fortalece confianza y hace lógico el upgrade.
            </p>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {llmPlanCards.map((plan) => (
              <div key={plan.name} className="card-glass p-5">
                <div className="h-10 w-10 rounded-xl bg-primary/15 text-primary grid place-content-center mb-3">
                  <Bot className="h-5 w-5" />
                </div>
                <div className="text-xs uppercase tracking-widest text-primary font-bold">{plan.name}</div>
                <div className="font-bold text-lg mt-2">{plan.title}</div>
                <p className="text-sm text-muted-foreground mt-2">{plan.text}</p>
              </div>
            ))}
          </div>
        </section>

        <PublicAiFaq />

        <section className="rounded-3xl border border-primary/20 bg-primary/5 p-10 text-center my-16">
          <h2 className="text-3xl md:text-4xl font-black mb-3">
            Hoy puedes saber cuánta <span className="shimmer-text">plata tienes muerta</span> en bodega.
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto mb-6">
            14 días gratis, con tu propia data, sin tarjeta y sin compromiso.
          </p>
          <Button asChild size="lg">
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

function TrustBadge({ icon, label }: { icon: React.ReactNode; label: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-muted-foreground flex items-center gap-2">
      <span className="text-primary">{icon}</span>
      <span>{label}</span>
    </div>
  );
}

function ProofCard({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <div className="text-3xl font-black shimmer-text">{value}</div>
      <div className="text-sm text-muted-foreground mt-2">{label}</div>
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
