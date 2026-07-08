import type { BannerAlertsProps } from "@/types/homepage";

export function BannerAlerts({ banners }: BannerAlertsProps) {
  if (!banners.length) {
    return null;
  }

  return (
    <div className="space-y-[var(--space-2)]">
      {banners.map((banner) => (
        <div
          key={banner.id}
          className="rounded-[var(--radius-card)] border border-[var(--color-gold)] border-s-4 bg-[var(--color-cream)] p-[var(--space-3)] text-center text-[length:var(--text-body)] leading-[var(--leading-body)] text-[var(--color-text)] shadow-[var(--shadow-card)]"
          role="alert"
        >
          {banner.message}
        </div>
      ))}
    </div>
  );
}
