import type { ZmanRef } from "@/types/prayerTime";

export const ZMAN_REF_OPTIONS: { value: ZmanRef; label: string }[] = [
  { value: "alot_hashachar", label: "עלות השחר" },
  { value: "sunrise", label: "זריחה" },
  { value: "sunset", label: "שקיעה" },
  { value: "tzeit", label: "צאת הכוכבים" },
  { value: "chatzot", label: "חצות היום" },
];

const ZMAN_LABELS: Record<ZmanRef, string> = Object.fromEntries(
  ZMAN_REF_OPTIONS.map((option) => [option.value, option.label]),
) as Record<ZmanRef, string>;

export function getZmanLabel(ref: ZmanRef | string | null | undefined): string {
  if (!ref) return "";
  return ZMAN_LABELS[ref as ZmanRef] ?? ref;
}

export function formatTimeDefinition(
  ref: ZmanRef | string | null | undefined,
  offsetMinutes: number,
): string {
  const label = getZmanLabel(ref);
  if (!label) return "";
  if (offsetMinutes === 0) return label;
  if (offsetMinutes > 0) return `${label} + ${offsetMinutes} דק'`;
  return `${label} - ${Math.abs(offsetMinutes)} דק'`;
}
