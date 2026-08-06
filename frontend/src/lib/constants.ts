import type { NavItem } from "@/types/nav";

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

export const DONATE_EXTERNAL_URL = "https://www.matara.pro/nedarimplus/online/?mosad=7018669" as const;

export const HEADER_NAV_ITEMS: readonly NavItem[] = [
  { path: ROUTES.home, label: "דף הבית" },
  { path: ROUTES.about, label: "אודות" },
  { path: ROUTES.gallery, label: "גלריה" },
  { path: ROUTES.mikveh, label: "מקווה" },
  { path: ROUTES.donate, label: "תרומה" },
  { path: ROUTES.contact, label: "צור קשר" },
];

export const FOOTER_NAV_ITEMS: readonly NavItem[] = [
  { path: ROUTES.home, label: "דף הבית" },
  { path: ROUTES.about, label: "אודות" },
  { path: ROUTES.gallery, label: "גלריה" },
  { path: ROUTES.mikveh, label: "מקווה" },
  { path: DONATE_EXTERNAL_URL, label: "תרומה", external: true },
  { path: ROUTES.contact, label: "צור קשר" },
];

export const DAY_NAMES = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"] as const;
