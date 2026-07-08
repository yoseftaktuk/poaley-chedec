import { Clock } from "lucide-react";

import { Section, SectionHeader } from "@/components/ui/Section";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { formatDaysOfWeek } from "@/lib/formatDays";
import { isPrayerToday } from "@/lib/isPrayerToday";
import { getPrayerIcon } from "@/lib/prayerIcons";
import type { PrayerTimesSectionProps } from "@/types/homepage";
import { cn } from "@/lib/utils";

export function PrayerTimesSection({ prayerTimes }: PrayerTimesSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="white" id="prayer-times">
      <div ref={ref} className={cn(visible && "animate-fade-up")}>
        <SectionHeader icon={Clock} title="זמני תפילות" />
        <div className="overflow-x-auto rounded-[var(--radius-card)] border border-[var(--color-border)] shadow-[var(--shadow-card)]">
          <table className="w-full min-w-[480px] border-collapse text-right">
            <thead>
              <tr className="bg-[var(--color-navy)] text-white">
                <th className="px-[var(--space-8)] py-5 text-[length:var(--text-body)] font-semibold">תפילה</th>
                <th className="px-[var(--space-8)] py-5 text-[length:var(--text-body)] font-semibold">ימים</th>
                <th className="px-[var(--space-8)] py-5 text-[length:var(--text-body)] font-semibold">שעה</th>
              </tr>
            </thead>
            <tbody>
              {prayerTimes.map((pt) => {
                const isToday = isPrayerToday(pt.days_of_week);
                const PrayerIcon = getPrayerIcon(pt.prayer_name);
                return (
                  <tr
                    key={pt.id}
                    className={cn(
                      "border-b border-[var(--color-border)] transition-base last:border-b-0",
                      isToday && "border-s-4 border-s-[var(--color-gold)] bg-[var(--color-cream)]",
                    )}
                    aria-current={isToday ? "true" : undefined}
                  >
                    <td className="px-[var(--space-8)] py-6">
                      <span className="flex items-center justify-end gap-[var(--space-2)] text-[length:var(--text-body)] font-medium text-[var(--color-text)]">
                        <PrayerIcon size={20} className="shrink-0 text-[var(--color-gold)]" aria-hidden="true" />
                        {pt.prayer_name}
                      </span>
                    </td>
                    <td className="px-[var(--space-8)] py-6 text-[length:var(--text-body)] text-[var(--color-text)]">
                      {formatDaysOfWeek(pt.days_of_week)}
                    </td>
                    <td className="px-[var(--space-8)] py-6 text-[length:var(--text-body)] font-bold text-[var(--color-navy)]">
                      {pt.prayer_time}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </Section>
  );
}
