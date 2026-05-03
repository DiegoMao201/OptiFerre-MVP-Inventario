"use client";

import { Suspense, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<ResetPasswordFallback />}>
      <ResetPasswordContent />
    </Suspense>
  );
}

function ResetPasswordContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = useMemo(() => searchParams.get("token") || "", [searchParams]);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    if (!token) {
      setError("Falta el token de recuperación.");
      return;
    }
    if (password.length < 8) {
      setError("La nueva contraseña debe tener al menos 8 caracteres.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden.");
      return;
    }
    setLoading(true);
    try {
      const res = await api.resetPassword(token, password);
      setMessage(res.message);
      setTimeout(() => router.replace("/login"), 1200);
    } catch (err: any) {
      setError(err?.message ?? "No pudimos actualizar tu contraseña.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card-glass w-full max-w-md p-8">
        <Link href="/login" className="text-xs text-muted-foreground hover:text-foreground">
          ← Volver al login
        </Link>
        <h1 className="text-2xl font-bold mt-3 mb-2">Define tu nueva contraseña</h1>
        <p className="text-sm text-muted-foreground mb-6">
          Usa una clave que puedas recordar y vuelve a entrar a tu cuenta sin perder continuidad.
        </p>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="password">Nueva contraseña</Label>
            <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Repite la contraseña</Label>
            <Input id="confirmPassword" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          </div>
          {message ? <p className="text-sm text-accent">{message}</p> : null}
          {error ? <p className="text-sm text-destructive">{error}</p> : null}
          <Button type="submit" className="w-full" size="lg" disabled={loading}>
            {loading ? "Actualizando..." : "Guardar nueva contraseña"}
          </Button>
        </form>
      </div>
    </div>
  );
}

function ResetPasswordFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card-glass w-full max-w-md p-8">
        <h1 className="text-2xl font-bold mb-2">Cargando recuperación</h1>
        <p className="text-sm text-muted-foreground">
          Estamos preparando el enlace para que cambies tu contraseña.
        </p>
      </div>
    </div>
  );
}