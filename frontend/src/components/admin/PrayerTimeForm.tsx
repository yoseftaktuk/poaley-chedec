import { Input, Label } from "@/components/ui/input";
import { formatTimeDefinition } from "@/lib/zmanimLabels";
import { ZMAN_REF_OPTIONS } from "@/lib/zmanimLabels";
import type { PrayerTimeFormValues, TimeMode } from "@/types/prayerTime";

interface PrayerTimeFormFieldsProps {
  form: PrayerTimeFormValues;
  onChange: (form: PrayerTimeFormValues) => void;
}

export function PrayerTimeFormFields({ form, onChange }: PrayerTimeFormFieldsProps) {
  const setMode = (time_mode: TimeMode) => {
    onChange({
      ...form,
      time_mode,
      prayer_time: time_mode === "fixed" ? form.prayer_time : "",
      zman_ref: time_mode === "zmanim" ? form.zman_ref || "sunset" : "",
    });
  };

  const previewLabel =
    form.time_mode === "zmanim" && form.zman_ref
      ? formatTimeDefinition(form.zman_ref, form.offset_minutes)
      : null;

  return (
    <>
      <div className="grid gap-3 md:grid-cols-2">
        <div>
          <Label htmlFor="prayer_name">תפילה</Label>
          <Input
            id="prayer_name"
            value={form.prayer_name}
            onChange={(e) => onChange({ ...form, prayer_name: e.target.value })}
          />
        </div>
        <div>
          <Label>סוג שעה</Label>
          <div className="mt-2 flex flex-wrap gap-4">
            <label className="flex cursor-pointer items-center gap-2 text-sm">
              <input
                type="radio"
                name="time_mode"
                checked={form.time_mode === "fixed"}
                onChange={() => setMode("fixed")}
              />
              שעה קבועה
            </label>
            <label className="flex cursor-pointer items-center gap-2 text-sm">
              <input
                type="radio"
                name="time_mode"
                checked={form.time_mode === "zmanim"}
                onChange={() => setMode("zmanim")}
              />
              זמן הלכתי
            </label>
          </div>
        </div>
      </div>

      {form.time_mode === "fixed" ? (
        <div>
          <Label htmlFor="prayer_time">שעה (HH:MM)</Label>
          <Input
            id="prayer_time"
            type="time"
            value={form.prayer_time}
            onChange={(e) => onChange({ ...form, prayer_time: e.target.value })}
          />
        </div>
      ) : (
        <div className="grid gap-3 md:grid-cols-2">
          <div>
            <Label htmlFor="zman_ref">זמן הלכתי</Label>
            <select
              id="zman_ref"
              className="mt-1 w-full rounded-[var(--radius-card)] border border-[var(--color-border)] bg-white px-3 py-2"
              value={form.zman_ref}
              onChange={(e) => onChange({ ...form, zman_ref: e.target.value as PrayerTimeFormValues["zman_ref"] })}
            >
              <option value="">בחר זמן</option>
              {ZMAN_REF_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <Label htmlFor="offset_minutes">היסט בדקות (שלילי = לפני)</Label>
            <Input
              id="offset_minutes"
              type="number"
              value={form.offset_minutes}
              onChange={(e) =>
                onChange({ ...form, offset_minutes: Number.parseInt(e.target.value, 10) || 0 })
              }
            />
          </div>
          {previewLabel && (
            <p className="text-sm text-[var(--color-text)] md:col-span-2">
              הגדרה: <span className="font-medium">{previewLabel}</span>
            </p>
          )}
        </div>
      )}
    </>
  );
}
