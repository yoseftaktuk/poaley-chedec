export function resolveApiBaseUrl(raw: string | undefined): string {
  const base = (raw?.trim() || "http://localhost:8000/api/v1").replace(/\/+$/, "");
  if (base.endsWith("/api/v1")) {
    return base;
  }
  return `${base}/api/v1`;
}

const API_BASE_URL = resolveApiBaseUrl(import.meta.env.VITE_API_BASE_URL);

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function formatApiErrorDetail(detail: unknown): string {
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail
      .map((item) => (typeof item === "object" && item && "msg" in item ? String(item.msg) : "שגיאת אימות"))
      .join(", ");
  }
  return "שגיאה";
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem("access_token");
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const requestUrl = `${API_BASE_URL}${path}`;
  // #region agent log
  if (!(globalThis as { __apiDebugLogged?: boolean }).__apiDebugLogged) {
    (globalThis as { __apiDebugLogged?: boolean }).__apiDebugLogged = true;
    fetch("http://127.0.0.1:7692/ingest/4d309d4e-7975-426c-8ff0-d9cc7d6ed167", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "1545be" },
      body: JSON.stringify({
        sessionId: "1545be",
        location: "api.ts:apiFetch",
        message: "api request url",
        data: { apiBaseUrl: API_BASE_URL, path, requestUrl },
        timestamp: Date.now(),
        runId: "pre-fix",
        hypothesisId: "A",
      }),
    }).catch(() => {});
  }
  // #endregion

  const response = await fetch(requestUrl, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "שגיאה" }));
    if (response.status === 401 && !path.startsWith("/auth/login")) {
      localStorage.removeItem("access_token");
      if (window.location.pathname.startsWith("/admin") && window.location.pathname !== "/admin/login") {
        window.location.assign("/admin/login");
      }
    }
    throw new ApiError(response.status, formatApiErrorDetail(error.detail));
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export async function apiUpload<T>(path: string, formData: FormData): Promise<T> {
  const token = localStorage.getItem("access_token");
  const headers: HeadersInit = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers,
    body: formData,
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "שגיאה בהעלאה" }));
    throw new ApiError(response.status, formatApiErrorDetail(error.detail));
  }

  return response.json() as Promise<T>;
}
