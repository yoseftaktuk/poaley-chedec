import type { PrayerTimeFormValues, TimeMode, ZmanRef } from "@/types/prayerTime";

export function buildPrayerTimePayload(form: PrayerTimeFormValues) {
  const base = {
    prayer_name: form.prayer_name,
    days_of_week: form.days_of_week,
    time_mode: form.time_mode,
    sort_order: form.sort_order,
  };

  if (form.time_mode === "fixed") {
    return {
      ...base,
      prayer_time: form.prayer_time,
    };
  }

  return {
    ...base,
    zman_ref: form.zman_ref as ZmanRef,
    offset_minutes: form.offset_minutes,
  };
}

export function prayerTimeToFormValues(item: {
  prayer_name: string;
  days_of_week: number[];
  time_mode?: TimeMode;
  prayer_time?: string;
  fixed_time?: string | null;
  zman_ref?: ZmanRef | null;
  offset_minutes?: number;
  sort_order: number;
}): PrayerTimeFormValues {
  const timeMode = item.time_mode ?? "fixed";
  return {
    prayer_name: item.prayer_name,
    days_of_week: item.days_of_week,
    time_mode: timeMode,
    prayer_time: timeMode === "fixed" ? item.fixed_time || item.prayer_time || "" : "",
    zman_ref: item.zman_ref ?? "",
    offset_minutes: item.offset_minutes ?? 0,
    sort_order: item.sort_order,
  };
}

export const PRAYER_TIME_INITIAL: PrayerTimeFormValues = {
  prayer_name: "",
  days_of_week: [0],
  time_mode: "fixed",
  prayer_time: "",
  zman_ref: "",
  offset_minutes: 0,
  sort_order: 0,
};
