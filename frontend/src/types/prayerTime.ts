export type TimeMode = "fixed" | "zmanim";

export type ZmanRef =
  | "alot_hashachar"
  | "sunrise"
  | "sunset"
  | "tzeit"
  | "chatzot";

export interface PrayerTimeFormValues {
  prayer_name: string;
  days_of_week: number[];
  time_mode: TimeMode;
  prayer_time: string;
  zman_ref: ZmanRef | "";
  offset_minutes: number;
  sort_order: number;
}

export interface PrayerTime {
  id: string;
  prayer_name: string;
  days_of_week: number[];
  time_mode: TimeMode;
  prayer_time: string;
  fixed_time?: string | null;
  zman_ref?: ZmanRef | null;
  offset_minutes?: number;
  time_definition_label?: string | null;
  sort_order: number;
}
