import { Clock, Moon, Sun, type LucideIcon } from "lucide-react";

const PRAYER_ICON_MAP: { keywords: string[]; icon: LucideIcon }[] = [
  { keywords: ["שחרית", "שחר"], icon: Sun },
  { keywords: ["מנחה"], icon: Sun },
  { keywords: ["ערבית", "ערב"], icon: Moon },
  { keywords: ["קבלת", "שבת"], icon: Moon },
];

export function getPrayerIcon(prayerName: string): LucideIcon {
  const normalized = prayerName.trim();
  for (const entry of PRAYER_ICON_MAP) {
    if (entry.keywords.some((keyword) => normalized.includes(keyword))) {
      return entry.icon;
    }
  }
  return Clock;
}
