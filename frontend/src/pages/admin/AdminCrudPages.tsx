import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { CrudTable } from "@/components/admin/CrudTable";
import { DaySelector } from "@/components/admin/DaySelector";
import { FormActions } from "@/components/admin/FormActions";
import { GalleryAlbumImages } from "@/components/admin/GalleryAlbumImages";
import { ImageUpload } from "@/components/admin/ImageUpload";
import { Button } from "@/components/ui/button";
import { Input, Label, Textarea } from "@/components/ui/input";
import { useCrudForm } from "@/hooks/useCrudForm";
import { apiFetch } from "@/lib/api";
import { formatDaysOfWeek } from "@/lib/formatDays";
import type { BannerMessage, Event, GalleryAlbum, Mikveh, OpeningSchedule, PrayerTime, TorahLesson } from "@/types";

const PRAYER_INITIAL = { prayer_name: "", days_of_week: [0], prayer_time: "", sort_order: 0 };
const LESSON_INITIAL = { lesson_name: "", rabbi_name: "", days_of_week: [0], lesson_time: "", description: "" };
const EVENT_INITIAL = {
  title: "",
  description: "",
  event_date: "",
  event_time: "",
  image_url: null as string | null,
  image_public_id: null as string | null | undefined,
  show_on_homepage: true,
};
const BANNER_INITIAL = { message: "", is_active: true, priority: 0, days_of_week: [] as number[] };
const SCHEDULE_INITIAL: OpeningSchedule = { days_of_week: [0], hours: "" };
const ALBUM_INITIAL = {
  title: "",
  description: "",
  cover_image_url: null as string | null,
  cover_public_id: null as string | null | undefined,
  is_published: true,
};

export function AdminPrayerTimesPage() {
  const qc = useQueryClient();
  const { data = [] } = useQuery({
    queryKey: ["admin-prayer"],
    queryFn: () => apiFetch<PrayerTime[]>("/prayer-times"),
  });
  const { editingId, form, setForm, isEditing, startEdit, cancelEdit, resetForm } =
    useCrudForm(PRAYER_INITIAL);

  const save = useMutation({
    mutationFn: () => {
      if (isEditing && editingId) {
        return apiFetch(`/prayer-times/${editingId}`, { method: "PUT", body: JSON.stringify(form) });
      }
      return apiFetch("/prayer-times", { method: "POST", body: JSON.stringify(form) });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-prayer"] });
      resetForm();
    },
  });
  const remove = useMutation({
    mutationFn: (id: string) => apiFetch(`/prayer-times/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-prayer"] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">זמני תפילות</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <div className="grid gap-3 md:grid-cols-2">
          <div>
            <Label>תפילה</Label>
            <Input
              value={form.prayer_name}
              onChange={(e) => setForm({ ...form, prayer_name: e.target.value })}
            />
          </div>
          <div>
            <Label>שעה</Label>
            <Input
              value={form.prayer_time}
              onChange={(e) => setForm({ ...form, prayer_time: e.target.value })}
            />
          </div>
        </div>
        <DaySelector
          value={form.days_of_week}
          onChange={(days_of_week) => setForm({ ...form, days_of_week })}
        />
        <FormActions
          isEditing={isEditing}
          createLabel="הוסף"
          isPending={save.isPending}
          onCancel={cancelEdit}
        />
        {save.isError && (
          <p className="text-sm text-red-600">
            {save.error instanceof Error ? save.error.message : "שגיאה בשמירה"}
          </p>
        )}
      </form>
      <CrudTable
        items={data}
        columns={[
          { key: "prayer_name", label: "תפילה" },
          {
            key: "days_of_week",
            label: "ימים",
            render: (item) => formatDaysOfWeek(item.days_of_week),
          },
          { key: "prayer_time", label: "שעה" },
        ]}
        onEdit={(item) =>
          startEdit(item.id, {
            prayer_name: item.prayer_name,
            days_of_week: item.days_of_week,
            prayer_time: item.prayer_time,
            sort_order: item.sort_order,
          })
        }
        onDelete={(id) => remove.mutate(id)}
      />
    </div>
  );
}

export function AdminTorahLessonsPage() {
  const qc = useQueryClient();
  const { data = [] } = useQuery({
    queryKey: ["admin-lessons"],
    queryFn: () => apiFetch<TorahLesson[]>("/torah-lessons"),
  });
  const { editingId, form, setForm, isEditing, startEdit, cancelEdit, resetForm } =
    useCrudForm(LESSON_INITIAL);

  const save = useMutation({
    mutationFn: () => {
      if (isEditing && editingId) {
        return apiFetch(`/torah-lessons/${editingId}`, {
          method: "PUT",
          body: JSON.stringify({ ...form, is_active: true }),
        });
      }
      return apiFetch("/torah-lessons", {
        method: "POST",
        body: JSON.stringify({ ...form, is_active: true }),
      });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-lessons"] });
      resetForm();
    },
  });
  const remove = useMutation({
    mutationFn: (id: string) => apiFetch(`/torah-lessons/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-lessons"] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">שיעורי תורה</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <Input
          placeholder="שם השיעור"
          value={form.lesson_name}
          onChange={(e) => setForm({ ...form, lesson_name: e.target.value })}
        />
        <Input
          placeholder="שם הרב"
          value={form.rabbi_name}
          onChange={(e) => setForm({ ...form, rabbi_name: e.target.value })}
        />
        <DaySelector
          value={form.days_of_week}
          onChange={(days_of_week) => setForm({ ...form, days_of_week })}
        />
        <Input
          placeholder="שעה"
          value={form.lesson_time}
          onChange={(e) => setForm({ ...form, lesson_time: e.target.value })}
        />
        <Textarea
          placeholder="תיאור"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <FormActions
          isEditing={isEditing}
          createLabel="הוסף"
          isPending={save.isPending}
          onCancel={cancelEdit}
        />
      </form>
      <CrudTable
        items={data}
        columns={[
          { key: "lesson_name", label: "שיעור" },
          { key: "rabbi_name", label: "רב" },
          {
            key: "days_of_week",
            label: "ימים",
            render: (item) => formatDaysOfWeek(item.days_of_week),
          },
          { key: "lesson_time", label: "שעה" },
        ]}
        onEdit={(item) =>
          startEdit(item.id, {
            lesson_name: item.lesson_name,
            rabbi_name: item.rabbi_name,
            days_of_week: item.days_of_week,
            lesson_time: item.lesson_time,
            description: item.description,
          })
        }
        onDelete={(id) => remove.mutate(id)}
      />
    </div>
  );
}

export function AdminEventsPage() {
  const qc = useQueryClient();
  const { data = [] } = useQuery({
    queryKey: ["admin-events"],
    queryFn: () => apiFetch<Event[]>("/events"),
  });
  const { editingId, form, setForm, isEditing, startEdit, cancelEdit, resetForm } =
    useCrudForm(EVENT_INITIAL);

  const save = useMutation({
    mutationFn: () => {
      const payload = {
        title: form.title,
        description: form.description,
        event_date: form.event_date,
        event_time: form.event_time,
        image_url: form.image_url,
        show_on_homepage: form.show_on_homepage,
        ...(form.image_public_id ? { image_public_id: form.image_public_id } : {}),
      };
      if (isEditing && editingId) {
        return apiFetch(`/events/${editingId}`, { method: "PUT", body: JSON.stringify(payload) });
      }
      return apiFetch("/events", { method: "POST", body: JSON.stringify(payload) });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-events"] });
      resetForm();
    },
  });
  const remove = useMutation({
    mutationFn: (id: string) => apiFetch(`/events/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-events"] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">אירועים</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          if (!form.title.trim() || !form.event_date) {
            return;
          }
          save.mutate();
        }}
      >
        <Input
          placeholder="כותרת"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        />
        <Textarea
          placeholder="תיאור"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <Input
          type="date"
          value={form.event_date}
          onChange={(e) => setForm({ ...form, event_date: e.target.value })}
          required
        />
        <Input
          placeholder="שעה"
          value={form.event_time}
          onChange={(e) => setForm({ ...form, event_time: e.target.value })}
        />
        <ImageUpload
          imageUrl={form.image_url}
          publicId={form.image_public_id}
          folder="poaley-chedec/events"
          onChange={(imageUrl, publicId) =>
            setForm({ ...form, image_url: imageUrl, image_public_id: publicId ?? null })
          }
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={form.show_on_homepage}
            onChange={(e) => setForm({ ...form, show_on_homepage: e.target.checked })}
          />
          הצג בדף הבית
        </label>
        <FormActions
          isEditing={isEditing}
          createLabel="הוסף"
          isPending={save.isPending}
          onCancel={cancelEdit}
        />
        {save.isError && (
          <p className="text-sm text-red-600">
            {save.error instanceof Error ? save.error.message : "שגיאה בשמירה"}
          </p>
        )}
      </form>
      <CrudTable
        items={data}
        columns={[
          { key: "title", label: "כותרת" },
          { key: "event_date", label: "תאריך" },
          { key: "event_time", label: "שעה" },
          {
            key: "image_url",
            label: "תמונה",
            render: (item) =>
              item.image_url ? (
                <img src={item.image_url} alt="" className="h-10 w-10 rounded object-cover" />
              ) : (
                "—"
              ),
          },
          {
            key: "show_on_homepage",
            label: "דף הבית",
            render: (item) => (item.show_on_homepage ? "כן" : "לא"),
          },
        ]}
        onEdit={(item) =>
          startEdit(item.id, {
            title: item.title,
            description: item.description,
            event_date: item.event_date,
            event_time: item.event_time,
            image_url: item.image_url,
            image_public_id: undefined,
            show_on_homepage: item.show_on_homepage,
          })
        }
        onDelete={(id) => remove.mutate(id)}
      />
    </div>
  );
}

export function AdminBannersPage() {
  const qc = useQueryClient();
  const { data = [] } = useQuery({
    queryKey: ["admin-banners"],
    queryFn: () => apiFetch<BannerMessage[]>("/banners"),
  });
  const { editingId, form, setForm, isEditing, startEdit, cancelEdit, resetForm } =
    useCrudForm(BANNER_INITIAL);

  const save = useMutation({
    mutationFn: () => {
      if (isEditing && editingId) {
        return apiFetch(`/banners/${editingId}`, { method: "PUT", body: JSON.stringify(form) });
      }
      return apiFetch("/banners", { method: "POST", body: JSON.stringify(form) });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-banners"] });
      resetForm();
    },
  });
  const remove = useMutation({
    mutationFn: (id: string) => apiFetch(`/banners/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-banners"] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">באנרים</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <Input
          value={form.message}
          onChange={(e) => setForm({ ...form, message: e.target.value })}
          placeholder="הודעת באנר"
        />
        <Input
          type="number"
          value={form.priority}
          onChange={(e) => setForm({ ...form, priority: Number(e.target.value) })}
          placeholder="עדיפות"
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={form.is_active}
            onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
          />
          פעיל
        </label>
        <DaySelector
          value={form.days_of_week}
          onChange={(days_of_week) => setForm({ ...form, days_of_week })}
          allowEmpty
        />
        <p className="text-xs text-gray-500">השאר ריק להצגה בכל ימות השבוע</p>
        <FormActions
          isEditing={isEditing}
          createLabel="הוסף"
          isPending={save.isPending}
          onCancel={cancelEdit}
        />
      </form>
      <CrudTable
        items={data}
        columns={[
          { key: "message", label: "הודעה" },
          { key: "priority", label: "עדיפות" },
          {
            key: "is_active",
            label: "פעיל",
            render: (item) => (item.is_active ? "כן" : "לא"),
          },
          {
            key: "days_of_week",
            label: "ימים",
            render: (item) => formatDaysOfWeek(item.days_of_week),
          },
        ]}
        onEdit={(item) =>
          startEdit(item.id, {
            message: item.message,
            is_active: item.is_active,
            priority: item.priority,
            days_of_week: item.days_of_week ?? [],
          })
        }
        onDelete={(id) => remove.mutate(id)}
      />
    </div>
  );
}

export function AdminMikvehPage() {
  const qc = useQueryClient();
  const { data } = useQuery({ queryKey: ["mikveh"], queryFn: () => apiFetch<Mikveh>("/mikveh") });
  const [form, setForm] = useState<Partial<Mikveh> & { image_public_id?: string | null }>({});

  const save = useMutation({
    mutationFn: () => apiFetch("/mikveh", { method: "PUT", body: JSON.stringify({ ...data, ...form }) }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mikveh"] }),
  });

  const current = { ...data, ...form };
  const schedules = current.opening_schedules ?? [];

  const updateSchedules = (opening_schedules: OpeningSchedule[]) => {
    setForm({ ...form, opening_schedules });
  };

  const addSchedule = () => {
    updateSchedules([...schedules, { ...SCHEDULE_INITIAL }]);
  };

  const updateSchedule = (index: number, patch: Partial<OpeningSchedule>) => {
    updateSchedules(schedules.map((schedule, i) => (i === index ? { ...schedule, ...patch } : schedule)));
  };

  const removeSchedule = (index: number) => {
    updateSchedules(schedules.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">מקווה</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <Textarea
          placeholder="מידע כללי"
          value={current.general_info || ""}
          onChange={(e) => setForm({ ...form, general_info: e.target.value })}
        />
        <Textarea
          placeholder="תקנון"
          value={current.regulations || ""}
          onChange={(e) => setForm({ ...form, regulations: e.target.value })}
        />
        <ImageUpload
          imageUrl={current.image_url ?? null}
          publicId={form.image_public_id}
          folder="poaley-chedec/mikveh"
          onChange={(imageUrl, publicId) =>
            setForm({ ...form, image_url: imageUrl ?? undefined, image_public_id: publicId ?? null })
          }
        />
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <Label>שעות פתיחה</Label>
            <Button type="button" variant="outline" size="sm" onClick={addSchedule}>
              הוסף לוח זמנים
            </Button>
          </div>
          {schedules.map((schedule, index) => (
            <div key={index} className="space-y-2 rounded border border-[var(--color-border)] p-3">
              <DaySelector
                value={schedule.days_of_week}
                onChange={(days_of_week) => updateSchedule(index, { days_of_week })}
              />
              <Textarea
                placeholder="שעות פתיחה"
                value={schedule.hours}
                onChange={(e) => updateSchedule(index, { hours: e.target.value })}
              />
              <Button type="button" variant="outline" size="sm" onClick={() => removeSchedule(index)}>
                מחק לוח זמנים
              </Button>
            </div>
          ))}
        </div>
        <Input
          type="number"
          placeholder="מחיר אברך"
          value={current.avrech_price ?? 10}
          onChange={(e) => setForm({ ...form, avrech_price: Number(e.target.value) })}
        />
        <Input
          type="number"
          placeholder="מחיר רגיל"
          value={current.regular_price ?? 15}
          onChange={(e) => setForm({ ...form, regular_price: Number(e.target.value) })}
        />
        <Button type="submit">שמור</Button>
      </form>
    </div>
  );
}

export function AdminMessagesPage() {
  const { data = [] } = useQuery({
    queryKey: ["admin-messages"],
    queryFn: () => apiFetch<import("@/types").ContactMessage[]>("/admin/contact-messages"),
  });

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">הודעות יצירת קשר</h1>
      <div className="space-y-4">
        {data.map((msg) => (
          <div key={msg.id} className="card">
            <p className="font-bold">
              {msg.name} - {msg.phone}
            </p>
            <p className="text-sm">{msg.email}</p>
            <p className="mt-2">{msg.message}</p>
            <p className="mt-2 text-xs text-gray-500">
              {new Date(msg.created_at).toLocaleString("he-IL")}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export function AdminSettingsPage() {
  const qc = useQueryClient();
  const { data } = useQuery({
    queryKey: ["admin-settings-homepage"],
    queryFn: () => apiFetch<{ key: string; value: Record<string, string> }>("/settings/homepage"),
  });
  const [value, setValue] = useState<Record<string, string>>({});

  const save = useMutation({
    mutationFn: () =>
      apiFetch("/settings/homepage", {
        method: "PUT",
        body: JSON.stringify({ value: { ...data?.value, ...value } }),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-settings-homepage"] }),
  });

  const current = { ...data?.value, ...value };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">הגדרות דף הבית</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <Input
          placeholder="כותרת ברוכים הבאים"
          value={current.welcome_title || ""}
          onChange={(e) => setValue({ ...value, welcome_title: e.target.value })}
        />
        <Textarea
          placeholder="טקסט ברוכים הבאים"
          value={current.welcome_text || ""}
          onChange={(e) => setValue({ ...value, welcome_text: e.target.value })}
        />
        <Textarea
          placeholder="דברי הרב"
          value={current.rabbi_message || ""}
          onChange={(e) => setValue({ ...value, rabbi_message: e.target.value })}
        />
        <Button type="submit">שמור</Button>
      </form>
    </div>
  );
}

export function AdminGalleryPage() {
  const qc = useQueryClient();
  const { data: albums = [] } = useQuery({
    queryKey: ["gallery-albums-admin"],
    queryFn: () => apiFetch<GalleryAlbum[]>("/gallery/albums?all=true"),
  });
  const { editingId, form, setForm, isEditing, startEdit, cancelEdit, resetForm } =
    useCrudForm(ALBUM_INITIAL);

  const save = useMutation({
    mutationFn: () => {
      if (isEditing && editingId) {
        return apiFetch(`/gallery/albums/${editingId}`, { method: "PUT", body: JSON.stringify(form) });
      }
      return apiFetch("/gallery/albums", { method: "POST", body: JSON.stringify(form) });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["gallery-albums-admin"] });
      qc.invalidateQueries({ queryKey: ["gallery-albums"] });
      resetForm();
    },
  });
  const remove = useMutation({
    mutationFn: (id: string) => apiFetch(`/gallery/albums/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["gallery-albums-admin"] });
      qc.invalidateQueries({ queryKey: ["gallery-albums"] });
    },
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">גלריה</h1>
      <form
        className="card space-y-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <Input
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          placeholder="שם אלבום"
        />
        <Textarea
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          placeholder="תיאור"
        />
        <ImageUpload
          imageUrl={form.cover_image_url}
          publicId={form.cover_public_id}
          folder="poaley-chedec/gallery/covers"
          label="תמונת כריכה"
          onChange={(cover_image_url, cover_public_id) =>
            setForm({ ...form, cover_image_url, cover_public_id: cover_public_id ?? null })
          }
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={form.is_published}
            onChange={(e) => setForm({ ...form, is_published: e.target.checked })}
          />
          מפורסם
        </label>
        <FormActions
          isEditing={isEditing}
          createLabel="צור אלבום"
          isPending={save.isPending}
          onCancel={cancelEdit}
        />
      </form>
      <CrudTable
        items={albums}
        columns={[
          { key: "title", label: "אלבום" },
          { key: "description", label: "תיאור" },
          {
            key: "is_published",
            label: "מפורסם",
            render: (item) => (item.is_published ? "כן" : "לא"),
          },
          {
            key: "cover_image_url",
            label: "כריכה",
            render: (item) =>
              item.cover_image_url ? (
                <img src={item.cover_image_url} alt="" className="h-10 w-10 rounded object-cover" />
              ) : (
                "—"
              ),
          },
        ]}
        onEdit={(item) =>
          startEdit(item.id, {
            title: item.title,
            description: item.description,
            cover_image_url: item.cover_image_url,
            cover_public_id: undefined,
            is_published: item.is_published,
          })
        }
        onDelete={(id) => remove.mutate(id)}
      />
      <GalleryAlbumImages albums={albums} />
    </div>
  );
}
