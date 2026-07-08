import { useQuery } from "@tanstack/react-query";
import { Link, NavLink, Navigate, Outlet, useNavigate } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { useLogout } from "@/hooks/useAuth";
import { apiFetch } from "@/lib/api";
import type { PrayerTime, TorahLesson, Event, BannerMessage, ContactMessage, AuditLog } from "@/types";

const ADMIN_SECTIONS = [
  { path: "/admin", label: "לוח בקרה", end: true },
  { path: "/admin/prayer-times", label: "זמני תפילות" },
  { path: "/admin/torah-lessons", label: "שיעורי תורה" },
  { path: "/admin/events", label: "אירועים" },
  { path: "/admin/gallery", label: "גלריה" },
  { path: "/admin/mikveh", label: "מקווה" },
  { path: "/admin/banners", label: "באנרים" },
  { path: "/admin/settings", label: "הגדרות" },
  { path: "/admin/messages", label: "הודעות" },
  { path: "/admin/audit", label: "יומן פעולות" },
] as const;

export function AdminLayout() {
  const token = localStorage.getItem("access_token");
  const logout = useLogout();
  const navigate = useNavigate();

  const session = useQuery({
    queryKey: ["auth-me"],
    queryFn: () => apiFetch<{ id: string; username: string }>("/auth/me"),
    enabled: Boolean(token),
    retry: false,
  });

  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }

  if (session.isLoading) {
    return <div className="flex min-h-screen items-center justify-center">טוען...</div>;
  }

  if (session.isError) {
    localStorage.removeItem("access_token");
    return <Navigate to="/admin/login" replace />;
  }

  const handleLogout = () => {
    logout.mutate(undefined, {
      onSettled: () => {
        localStorage.removeItem("access_token");
        navigate("/admin/login");
      },
    });
  };

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 border-l border-[var(--color-border)] bg-[var(--color-muted)] p-4">
        <h1 className="mb-6 text-lg font-bold">ניהול אתר</h1>
        <nav className="space-y-2">
          {ADMIN_SECTIONS.map((section) => (
            <NavLink
              key={section.path}
              to={section.path}
              end={"end" in section ? section.end : false}
              className={({ isActive }) =>
                `block rounded px-3 py-2 no-underline hover:bg-white ${isActive ? "bg-white font-bold" : ""}`
              }
            >
              {section.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-6 space-y-2">
          <Button variant="outline" className="w-full" asChild>
            <Link to="/">לחזרה לאתר</Link>
          </Button>
          <Button variant="outline" className="w-full" onClick={handleLogout}>
            התנתק
          </Button>
        </div>
      </aside>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}

export function AdminDashboardPage() {
  const prayerTimes = useQuery({ queryKey: ["admin-prayer"], queryFn: () => apiFetch<PrayerTime[]>("/prayer-times") });
  const lessons = useQuery({ queryKey: ["admin-lessons"], queryFn: () => apiFetch<TorahLesson[]>("/torah-lessons") });
  const events = useQuery({ queryKey: ["admin-events"], queryFn: () => apiFetch<Event[]>("/events") });
  const banners = useQuery({ queryKey: ["admin-banners"], queryFn: () => apiFetch<BannerMessage[]>("/banners") });
  const messages = useQuery({
    queryKey: ["admin-messages"],
    queryFn: () => apiFetch<ContactMessage[]>("/admin/contact-messages"),
  });

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">לוח בקרה</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card"><p className="text-2xl font-bold">{prayerTimes.data?.length ?? 0}</p><p>זמני תפילות</p></div>
        <div className="card"><p className="text-2xl font-bold">{lessons.data?.length ?? 0}</p><p>שיעורי תורה</p></div>
        <div className="card"><p className="text-2xl font-bold">{events.data?.length ?? 0}</p><p>אירועים</p></div>
        <div className="card"><p className="text-2xl font-bold">{banners.data?.length ?? 0}</p><p>באנרים</p></div>
        <div className="card"><p className="text-2xl font-bold">{messages.data?.length ?? 0}</p><p>הודעות יצירת קשר</p></div>
      </div>
    </div>
  );
}

export function AdminAuditPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["admin-audit"],
    queryFn: () => apiFetch<AuditLog[]>("/admin/audit-logs"),
  });

  if (isLoading) return <p>טוען...</p>;

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">יומן פעולות</h1>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-right">
          <thead>
            <tr className="border-b">
              <th className="p-2">תאריך</th>
              <th className="p-2">פעולה</th>
              <th className="p-2">ישות</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((log) => (
              <tr key={log.id} className="border-b">
                <td className="p-2">{new Date(log.created_at).toLocaleString("he-IL")}</td>
                <td className="p-2">{log.action}</td>
                <td className="p-2">{log.entity_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
