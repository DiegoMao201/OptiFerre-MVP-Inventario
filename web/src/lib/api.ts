"use client";

import { clearSession, getToken } from "./auth-storage";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  payload: unknown;
  constructor(message: string, status: number, payload: unknown) {
    super(message);
    this.status = status;
    this.payload = payload;
  }
}

type RequestOptions = RequestInit & { auth?: boolean; isForm?: boolean };

export async function apiFetch<T>(path: string, opts: RequestOptions = {}): Promise<T> {
  const headers = new Headers(opts.headers);
  if (!opts.isForm && opts.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (opts.auth !== false) {
    const token = getToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...opts, headers });
  const text = await res.text();
  let payload: unknown = null;
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = text;
    }
  }

  if (!res.ok) {
    if (res.status === 401) clearSession();
    const message =
      (payload && typeof payload === "object" && "detail" in payload && typeof (payload as Record<string, unknown>).detail === "string"
        ? (payload as Record<string, string>).detail
        : null) || `Error ${res.status}`;
    throw new ApiError(message, res.status, payload);
  }

  return payload as T;
}

export const api = {
  login: (email: string, password: string) =>
    apiFetch<{
      access_token: string;
      token_type: string;
      user: import("./auth-storage").AuthUser;
    }>(`/auth/login`, {
      method: "POST",
      auth: false,
      body: JSON.stringify({ email, password })
    }),
  register: (data: { company_name: string; full_name: string; email: string; password: string }) =>
    apiFetch<{
      access_token: string;
      token_type: string;
      user: import("./auth-storage").AuthUser;
    }>(`/auth/register`, {
      method: "POST",
      auth: false,
      body: JSON.stringify(data)
    }),
  me: () => apiFetch<import("./auth-storage").AuthUser>(`/auth/me`),
  dashboardSummary: () =>
    apiFetch<{
      has_data: boolean;
      dinero_atrapado: number;
      dinero_atrapado_mensual: number;
      productos_muertos: number;
      productos_muertos_valor: number;
      productos_estrella: number;
      en_quiebre: number;
      para_reponer: number;
      capital_total: number;
      rotacion_promedio_dias: number;
    }>(`/dashboard/summary`),
  runAnalysis: () =>
    apiFetch(`/analysis/run`, { method: "POST" }),
  deadProducts: (limit = 100) =>
    apiFetch<{
      items: Array<{
        sku: string;
        nombre: string;
        categoria?: string | null;
        estado: string;
        stock_actual: number;
        valor_inventario: number;
        dias_cobertura?: number | null;
        sugerencia_compra: number;
        costo_oportunidad_mensual: number;
        abc?: string | null;
        xyz?: string | null;
      }>;
      total: number;
      total_value: number;
    }>(`/products/dead?limit=${limit}`),
  opportunities: (limit = 100) =>
    apiFetch<{
      items: Array<{
        sku: string;
        nombre: string;
        categoria?: string | null;
        estado: string;
        stock_actual: number;
        valor_inventario: number;
        dias_cobertura?: number | null;
        sugerencia_compra: number;
        costo_oportunidad_mensual: number;
      }>;
      total: number;
      total_value: number;
    }>(`/products/opportunities?limit=${limit}`),
  generatePurchaseOrder: () =>
    apiFetch<{
      ok: boolean;
      id?: number;
      code?: string;
      items: number;
      total_units: number;
      total_amount: number;
    }>(`/purchase-orders/generate`, {
      method: "POST",
      body: JSON.stringify({})
    }),
  uploadInventory: async (inventory: File, sales?: File | null) => {
    const form = new FormData();
    form.append("inventory", inventory);
    if (sales) form.append("sales", sales);
    return apiFetch<{
      ok: boolean;
      inventory_rows: number;
      inventory_upserted: number;
      sales_rows: number;
      sales_upserted: number;
    }>(`/inventory/upload`, { method: "POST", body: form, isForm: true });
  }
};
