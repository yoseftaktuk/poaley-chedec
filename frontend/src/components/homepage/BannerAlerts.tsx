import type { BannerAlertsProps } from "@/types/homepage";

export function BannerAlerts({ banners }: BannerAlertsProps) {
  if (!banners.length) {
    return null;
  }

  return (
    <div className="space-y-4">
      {banners.map((banner) => (
        <div
          key={banner.id}
          className="rounded-2xl border border-[var(--color-gold)] border-s-4 bg-[var(--color-cream)] p-5 text-center text-[length:var(--text-body)] leading-relaxed text-[var(--color-text)] shadow-[var(--shadow-card)]"
          role="alert"
        >
          {banner.message}
        </div>
      ))}
    </div>
  );
}
