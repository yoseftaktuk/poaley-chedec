import { http, HttpResponse } from "msw";
import { describe, expect, it, vi } from "vitest";

import { formatApiErrorDetail, ApiError, apiFetch, apiUpload, resolveApiBaseUrl } from "@/lib/api";
import { server } from "@/test/mocks/server";

describe("resolveApiBaseUrl", () => {
  it("keeps url that already ends with /api/v1", () => {
    expect(resolveApiBaseUrl("http://localhost:8000/api/v1")).toBe("http://localhost:8000/api/v1");
    expect(resolveApiBaseUrl("https://poaley-chedec-1.onrender.com/api/v1/")).toBe(
      "https://poaley-chedec-1.onrender.com/api/v1",
    );
  });

  it("appends /api/v1 when missing from production host", () => {
    expect(resolveApiBaseUrl("https://poaley-chedec-1.onrender.com")).toBe(
      "https://poaley-chedec-1.onrender.com/api/v1",
    );
  });

  it("uses localhost default when env is empty", () => {
    expect(resolveApiBaseUrl(undefined)).toBe("http://localhost:8000/api/v1");
  });
});

describe("formatApiErrorDetail", () => {
  it("returns string detail as-is", () => {
    expect(formatApiErrorDetail("שגיאה")).toBe("שגיאה");
  });

  it("formats validation error array", () => {
    expect(formatApiErrorDetail([{ msg: "שדה חובה" }])).toBe("שדה חובה");
  });

  it("uses fallback for array items without msg", () => {
    expect(formatApiErrorDetail([{ code: "invalid" }])).toBe("שגיאת אימות");
  });

  it("returns default for unknown detail", () => {
    expect(formatApiErrorDetail(null)).toBe("שגיאה");
  });
});

describe("ApiError", () => {
  it("stores status and message", () => {
    const error = new ApiError(404, "לא נמצא");
    expect(error.status).toBe(404);
    expect(error.message).toBe("לא נמצא");
    expect(error.name).toBe("ApiError");
  });
});

describe("apiFetch", () => {
  it("returns json on success", async () => {
    const result = await apiFetch<{ settings: unknown }>("/homepage");
    expect(result.settings).toBeDefined();
  });

  it("returns undefined on 204", async () => {
    server.use(
      http.delete("http://localhost:8000/api/v1/test-delete", () => new HttpResponse(null, { status: 204 })),
    );
    const result = await apiFetch<void>("/test-delete", { method: "DELETE" });
    expect(result).toBeUndefined();
  });

  it("sends authorization header when token exists", async () => {
    localStorage.setItem("access_token", "my-token");
    let authHeader = "";
    server.use(
      http.get("http://localhost:8000/api/v1/auth/me", ({ request }) => {
        authHeader = request.headers.get("Authorization") ?? "";
        return HttpResponse.json({ id: "1", username: "admin" });
      }),
    );
    await apiFetch("/auth/me");
    expect(authHeader).toBe("Bearer my-token");
  });

  it("clears token on 401 for admin routes", async () => {
    localStorage.setItem("access_token", "bad-token");
    const assign = vi.fn();
    Object.defineProperty(window, "location", {
      value: { pathname: "/admin/prayer-times", assign },
      writable: true,
    });

    server.use(
      http.get("http://localhost:8000/api/v1/prayer-times", () =>
        HttpResponse.json({ detail: "לא מורשה" }, { status: 401 }),
      ),
    );

    await expect(apiFetch("/prayer-times")).rejects.toThrow(ApiError);
    expect(localStorage.getItem("access_token")).toBeNull();
    expect(assign).toHaveBeenCalledWith("/admin/login");
  });

  it("throws ApiError on failed response", async () => {
    server.use(
      http.get("http://localhost:8000/api/v1/fail", () =>
        HttpResponse.json({ detail: "שגיאת שרת" }, { status: 500 }),
      ),
    );
    await expect(apiFetch("/fail")).rejects.toMatchObject({ status: 500, message: "שגיאת שרת" });
  });
});

describe("apiUpload", () => {
  it("uploads form data successfully", async () => {
    server.use(
      http.post("http://localhost:8000/api/v1/uploads/image", () =>
        HttpResponse.json({ url: "https://example.com/img.jpg", public_id: "abc" }),
      ),
    );
    const formData = new FormData();
    formData.append("file", new Blob(["test"]), "test.jpg");
    const result = await apiUpload<{ url: string }>("/uploads/image", formData);
    expect(result.url).toContain("example.com");
  });

  it("throws on upload failure", async () => {
    server.use(
      http.post("http://localhost:8000/api/v1/uploads/image", () =>
        HttpResponse.json({ detail: "שגיאה בהעלאה" }, { status: 400 }),
      ),
    );
    const formData = new FormData();
    await expect(apiUpload("/uploads/image", formData)).rejects.toThrow(ApiError);
  });
});
