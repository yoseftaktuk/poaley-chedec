import { useMikveh } from "@/hooks/usePublicData";
import { formatOpeningSchedules } from "@/lib/formatOpeningSchedules";

export function MikvehPage() {
  const { data: mikveh, isLoading, error } = useMikveh();

  if (isLoading) return <div className="container-page">טוען...</div>;
  if (error || !mikveh) return <div className="container-page">שגיאה בטעינת דף המקווה</div>;

  return (
    <div className="container-page space-y-8">
      <h1 className="section-title">מקווה</h1>

      {mikveh.image_url && (
        <img
          src={mikveh.image_url}
          alt="מקווה"
          className="h-64 w-full rounded-lg object-cover"
          loading="lazy"
        />
      )}

      <section className="card">
        <h2 className="mb-3 text-xl font-bold">מידע כללי</h2>
        <p className="whitespace-pre-line">{mikveh.general_info}</p>
      </section>

      <section className="card">
        <h2 className="mb-3 text-xl font-bold">תעריפים</h2>
        <ul className="space-y-2">
          <li>אברך: {mikveh.avrech_price}₪</li>
          <li>רגיל: {mikveh.regular_price}₪</li>
        </ul>
      </section>

      <section className="card">
        <h2 className="mb-3 text-xl font-bold">שעות פתיחה</h2>
        <ul className="space-y-2">
          {formatOpeningSchedules(mikveh.opening_schedules ?? []).map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2 className="mb-3 text-xl font-bold">תקנון</h2>
        <p className="whitespace-pre-line">{mikveh.regulations}</p>
      </section>
    </div>
  );
}
