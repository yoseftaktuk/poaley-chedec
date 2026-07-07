import { usePublicSettings } from "@/hooks/usePublicData";

export function AccessibilityPage() {
  const { data: settings } = usePublicSettings();
  const statement = settings?.accessibility_statement;

  return (
    <div className="container-page">
      <h1 className="section-title">{statement?.title || "הצהרת נגישות"}</h1>
      <div className="card prose max-w-none">
        <p className="whitespace-pre-line">{statement?.content}</p>
        <p className="mt-6">
          האתר תומך בהגדלת גופן, מצב ניגודיות גבוהה, ניווט מקלדת ותמיכה בקוראי מסך.
          ניתן לשנות הגדרות נגישות באמצעות כפתור הנגישות בפינה השמאלית התחתונה של המסך.
        </p>
      </div>
    </div>
  );
}
