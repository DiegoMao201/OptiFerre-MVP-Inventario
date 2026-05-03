"use client";

import { ReactNode } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LayoutDashboard, PackageX, Sparkles, UploadCloud, ShoppingCart, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { clearSession, getUser } from "@/lib/auth-storage";

const NAV = [
  { href: "/app", label: "Dashboard", icon: LayoutDashboard },
  { href: "/app/dead-products", label: "Productos muertos", icon: PackageX },
  { href: "/app/opportunities", label: "Qué comprar", icon: Sparkles },
  { href: "/app/upload", label: "Subir Excel", icon: UploadCloud },
  { href: "/app/purchase-orders", label: "Órdenes de compra", icon: ShoppingCart }
];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const user = typeof window !== "undefined" ? getUser() : null;

  const logout = () => {
    clearSession();
    router.replace("/login");
  };

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 hidden md:flex flex-col gap-2 border-r border-white/5 bg-card/40 backdrop-blur p-5">
        <div className="mb-6">
          <div className="text-xs uppercase tracking-widest text-primary font-bold">OptiFerre</div>
          <div className="text-base font-semibold mt-1 truncate">{user?.company_name || "Tu negocio"}</div>
          <div className="text-xs text-muted-foreground truncate">{user?.email}</div>
        </div>
        <nav className="flex-1 space-y-1">
          {NAV.map((item) => {
            const active = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all",
                  active
                    ? "bg-primary/15 text-primary border border-primary/30"
                    : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        <Button variant="ghost" className="justify-start text-muted-foreground" onClick={logout}>
          <LogOut className="h-4 w-4" />
          Cerrar sesión
        </Button>
      </aside>
      <main className="flex-1 p-6 md:p-10 overflow-x-hidden">{children}</main>
    </div>
  );
}
