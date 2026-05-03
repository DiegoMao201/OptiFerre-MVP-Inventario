"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

const SUGGESTED_QUESTIONS = [
  "¿Qué hace la app exactamente?",
  "¿Qué hace la IA en Starter, Pro y Enterprise?",
  "¿Necesito cambiar mi sistema o solo subir Excel?",
  "¿Cómo sé si esto sí me sirve para mi ferretería?",
];

export function PublicAiFaq() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const askQuestion = async (value: string) => {
    if (!value.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.publicAssistant(value.trim());
      setAnswer(res.answer);
      setQuestion(value);
    } catch (err: any) {
      setError(err?.message ?? "No pudimos responder en este momento.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card-glass p-6 md:p-8 space-y-5">
      <div>
        <div className="text-xs uppercase tracking-widest text-primary font-bold">Asistente IA en vivo</div>
        <h3 className="text-2xl md:text-3xl font-black mt-1">Haz una pregunta y mira cómo responde el LLM de la app.</h3>
        <p className="text-muted-foreground mt-2 max-w-3xl">
          Desde Starter te guía, en Pro te explica el inventario y en Enterprise te ayuda a ejecutar. Aquí puedes probar cómo se comunica.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {SUGGESTED_QUESTIONS.map((item) => (
          <button
            key={item}
            className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-sm text-muted-foreground hover:border-primary/40 hover:text-foreground"
            onClick={() => askQuestion(item)}
            disabled={loading}
          >
            {item}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-3 md:flex-row">
        <textarea
          className="min-h-28 w-full rounded-2xl border border-white/10 bg-transparent px-4 py-3 text-sm"
          placeholder="Escribe la pregunta que te haría un cliente antes de pagar..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <Button className="md:self-end" size="lg" onClick={() => askQuestion(question)} disabled={loading || !question.trim()}>
          {loading ? "Respondiendo..." : "Preguntar al asistente"}
        </Button>
      </div>

      {error ? <p className="text-sm text-destructive">{error}</p> : null}

      <div className="rounded-2xl border border-primary/20 bg-primary/10 p-5 min-h-28">
        <div className="text-xs uppercase tracking-widest text-primary font-bold mb-2">Respuesta</div>
        <p className="text-sm leading-7 text-foreground whitespace-pre-wrap">
          {answer || "Haz una pregunta frecuente y te mostramos cómo la IA aterriza el valor comercial de OptiFerre."}
        </p>
      </div>
    </section>
  );
}