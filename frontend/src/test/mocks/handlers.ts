import { http, HttpResponse } from "msw";

const API_BASE = "http://localhost:8000/api/v1";

export const mockHomepage = {
  settings: {
    homepage: {
      welcome_title: "ברוכים הבאים",
      welcome_text: "בית כנסת ומקווה",
      rabbi_message: "שלום וברכה",
      rabbi_name: "אליהו תקתוק",
    },
    contact: {
      rabbi_name: "אליהו תקתוק",
      address: "אפרים 52, אשקלון",
      phone: "0544329218",
      whatsapp: "0544329218",
      email: "test@example.com",
      maps_url: "https://maps.google.com",
    },
    donation: { bit_url: "https://example.com/donate", button_text: "תרומה" },
    site: { site_name: "בית כנסת פועלי צדק", site_description: "אשקלון" },
  },
  prayer_times: [],
  torah_lessons: [],
  events: [],
  banners: [],
};

export const mockPublicSettings = {
  homepage: mockHomepage,
  contact: {
    rabbi_name: "אליהו תקתוק",
    address: "אפרים 52, אשקלון",
    phone: "0544329218",
    whatsapp: "0544329218",
    email: "test@example.com",
    maps_url: "https://maps.google.com",
  },
  donation: { bit_url: "https://example.com/donate", button_text: "תרומה" },
  site: { site_name: "בית כנסת פועלי צדק", site_description: "אשקלון" },
  seo_global: { title: "בית כנסת", description: "תיאור", og_image: "" },
  seo_pages: { home: { title: "דף הבית", description: "" } },
  accessibility_statement: { title: "הצהרת נגישות", content: "תוכן נגישות" },
};

export const handlers = [
  http.get(`${API_BASE}/homepage`, () => HttpResponse.json(mockHomepage)),
  http.get(`${API_BASE}/settings/public`, () => HttpResponse.json(mockPublicSettings)),
  http.get(`${API_BASE}/gallery/albums`, () => HttpResponse.json([])),
  http.get(`${API_BASE}/gallery/albums/:albumId/images`, () => HttpResponse.json([])),
  http.get(`${API_BASE}/mikveh`, () =>
    HttpResponse.json({
      general_info: "מידע כללי",
      regulations: "תקנון",
      avrech_price: 10,
      regular_price: 15,
      opening_schedules: [],
    }),
  ),
  http.post(`${API_BASE}/contact`, async () =>
    HttpResponse.json({ message: "ההודעה נשלחה בהצלחה" }, { status: 201 }),
  ),
  http.post(`${API_BASE}/auth/login`, async ({ request }) => {
    const body = (await request.json()) as { username: string; password: string };
    if (body.username === "admin" && body.password === "changeme123") {
      return HttpResponse.json({ access_token: "test-token", token_type: "bearer" });
    }
    return HttpResponse.json({ detail: "שם משתמש או סיסמה שגויים" }, { status: 401 });
  }),
  http.post(`${API_BASE}/auth/logout`, () => HttpResponse.json({ message: "התנתקת בהצלחה" })),
];
