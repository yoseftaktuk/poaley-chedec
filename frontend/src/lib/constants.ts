export const SITE_LOGO = {
  src: "/images/logo.png",
  alt: 'לוגו קהילת פועלי צדק (ע"ר) — רחוב אפרים 52, אשקלון',
} as const;

export const ROUTES = {
  home: "/",
  about: "/about",
  gallery: "/gallery",
  mikveh: "/mikveh",
  donate: "/donate",
  contact: "/contact",
  accessibility: "/accessibility",
  admin: "/admin",
  adminLogin: "/admin/login",
} as const;

export const NAV_ITEMS = [
  { path: ROUTES.home, label: "דף הבית" },
  { path: ROUTES.about, label: "אודות" },
  { path: ROUTES.gallery, label: "גלריה" },
  { path: ROUTES.mikveh, label: "מקווה" },
  { path: ROUTES.donate, label: "תרומה" },
  { path: ROUTES.contact, label: "צור קשר" },
] as const;

export const DAY_NAMES = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"] as const;
