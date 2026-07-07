export const ROUTES = {
  home: "/",
  gallery: "/gallery",
  mikveh: "/mikveh",
  contact: "/contact",
  accessibility: "/accessibility",
  admin: "/admin",
  adminLogin: "/admin/login",
} as const;

export const NAV_ITEMS = [
  { path: ROUTES.home, label: "דף הבית" },
  { path: ROUTES.gallery, label: "גלריה" },
  { path: ROUTES.mikveh, label: "מקווה" },
  { path: ROUTES.contact, label: "צור קשר" },
] as const;

export const DAY_NAMES = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"] as const;
