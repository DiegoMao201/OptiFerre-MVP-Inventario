"use client";

import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

const CATEGORY_OPTIONS = [
  { value: "support", label: "Soporte" },
  { value: "billing", label: "Facturación" },
  { value: "access", label: "Acceso" },
  { value: "bug", label: "Error" },
  { value: "integration", label: "Integración" },
];

const PRIORITY_OPTIONS = [
  { value: "low", label: "Baja" },
  { value: "medium", label: "Media" },
  { value: "high", label: "Alta" },
  { value: "critical", label: "Crítica" },
];

export default function SupportPage() {
  const qc = useQueryClient();
  const [selectedTicketId, setSelectedTicketId] = useState<number | null>(null);
  const [form, setForm] = useState({
    subject: "",
    message: "",
    category: "support",
    priority: "medium",
  });
  const [reply, setReply] = useState("");

  const { data: tickets, isLoading } = useQuery({
    queryKey: ["support-tickets"],
    queryFn: api.supportTickets,
  });

  useEffect(() => {
    if (!selectedTicketId && tickets?.items?.length) {
      setSelectedTicketId(tickets.items[0].id);
    }
  }, [tickets, selectedTicketId]);

  const detail = useQuery({
    queryKey: ["support-ticket", selectedTicketId],
    queryFn: () => api.supportTicket(selectedTicketId as number),
    enabled: Boolean(selectedTicketId),
  });

  const createTicket = useMutation({
    mutationFn: api.createSupportTicket,
    onSuccess: async (res) => {
      setForm({ subject: "", message: "", category: "support", priority: "medium" });
      await qc.invalidateQueries({ queryKey: ["support-tickets"] });
      setSelectedTicketId(res.ticket.id);
    },
  });

  const replyTicket = useMutation({
    mutationFn: () => api.replySupportTicket(selectedTicketId as number, reply),
    onSuccess: async () => {
      setReply("");
      await qc.invalidateQueries({ queryKey: ["support-ticket", selectedTicketId] });
      await qc.invalidateQueries({ queryKey: ["support-tickets"] });
    },
  });

  const selectedTicket = useMemo(
    () => tickets?.items.find((item) => item.id === selectedTicketId),
    [tickets, selectedTicketId],
  );

  return (
    <div className="space-y-8 max-w-7xl">
      <header>
        <div className="text-xs uppercase tracking-widest text-primary font-bold">Soporte y tickets</div>
        <h1 className="text-3xl md:text-4xl font-black mt-1">Pide ayuda sin salir de la app.</h1>
        <p className="text-muted-foreground mt-2 max-w-3xl">
          Abre el caso con contexto claro, sigue la conversación y deja trazabilidad de lo que pasó con tu carga, tu acceso o tu facturación.
        </p>
      </header>

      <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <div className="space-y-6">
          <div className="card-glass p-6 space-y-4">
            <div>
              <h2 className="text-xl font-bold">Crear ticket</h2>
              <p className="text-sm text-muted-foreground mt-1">Entre más claro quede el contexto, más rápido te respondemos sin pedirte tres correos extra.</p>
            </div>
            <Input placeholder="Asunto del ticket" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} />
            <div className="grid md:grid-cols-2 gap-3">
              <select className="h-11 rounded-xl border border-white/10 bg-transparent px-4 text-sm" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORY_OPTIONS.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
              </select>
              <select className="h-11 rounded-xl border border-white/10 bg-transparent px-4 text-sm" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
                {PRIORITY_OPTIONS.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
              </select>
            </div>
            <textarea className="min-h-40 rounded-2xl border border-white/10 bg-transparent px-4 py-3 text-sm" placeholder="Explica qué intentaste, qué esperabas ver y qué pasó realmente." value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} />
            {createTicket.isError ? <p className="text-sm text-destructive">{(createTicket.error as Error).message}</p> : null}
            <Button onClick={() => createTicket.mutate(form)} disabled={createTicket.isPending || !form.subject || !form.message}>
              {createTicket.isPending ? "Creando ticket..." : "Crear ticket y enviarlo a soporte"}
            </Button>
          </div>

          <div className="card-glass p-6 space-y-4">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-xl font-bold">Tus tickets</h2>
              {isLoading ? <span className="text-sm text-muted-foreground">Cargando...</span> : null}
            </div>
            <div className="space-y-3">
              {tickets?.items.length ? tickets.items.map((ticket) => (
                <button key={ticket.id} className={`w-full rounded-2xl border px-4 py-4 text-left transition ${selectedTicketId === ticket.id ? "border-primary/40 bg-primary/10" : "border-white/10 hover:border-white/20"}`} onClick={() => setSelectedTicketId(ticket.id)}>
                  <div className="flex items-center justify-between gap-3">
                    <div className="font-semibold">#{ticket.id} · {ticket.subject}</div>
                    <span className="text-xs uppercase tracking-wider text-primary">{ticket.status}</span>
                  </div>
                  <div className="text-sm text-muted-foreground mt-2">{ticket.category} · prioridad {ticket.priority}</div>
                </button>
              )) : <p className="text-sm text-muted-foreground">Todavía no has creado tickets.</p>}
            </div>
          </div>
        </div>

        <div className="card-glass p-6 space-y-4 min-h-[32rem]">
          <div>
            <h2 className="text-xl font-bold">{selectedTicket ? `Ticket #${selectedTicket.id}` : "Selecciona un ticket"}</h2>
            <p className="text-sm text-muted-foreground mt-1">Sigue la conversación y responde sin salir del portal.</p>
          </div>
          <div className="space-y-3 flex-1">
            {detail.data?.messages?.map((message) => (
              <div key={message.id} className="rounded-2xl border border-white/10 p-4">
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span className="font-semibold">{message.author_name}</span>
                  <span className="text-muted-foreground">{new Date(message.created_at).toLocaleString("es-CO")}</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2 whitespace-pre-wrap">{message.body}</p>
              </div>
            ))}
            {!detail.data?.messages?.length ? <p className="text-sm text-muted-foreground">Cuando selecciones un ticket verás aquí el historial.</p> : null}
          </div>
          {selectedTicketId ? (
            <div className="space-y-3 pt-2">
              <textarea className="min-h-32 rounded-2xl border border-white/10 bg-transparent px-4 py-3 text-sm w-full" placeholder="Escribe la actualización o la información adicional para soporte." value={reply} onChange={(e) => setReply(e.target.value)} />
              {replyTicket.isError ? <p className="text-sm text-destructive">{(replyTicket.error as Error).message}</p> : null}
              <Button onClick={() => replyTicket.mutate()} disabled={replyTicket.isPending || !reply.trim()}>
                {replyTicket.isPending ? "Enviando respuesta..." : "Responder ticket"}
              </Button>
            </div>
          ) : null}
        </div>
      </section>
    </div>
  );
}