import { BookOpen } from "lucide-react";

import { BannerAlerts } from "@/components/homepage/BannerAlerts";
import { Card } from "@/components/ui/Card";
import { Section, SectionHeader } from "@/components/ui/Section";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import type { BannerMessage } from "@/types";
import type { RabbiMessageSectionProps } from "@/types/homepage";
import { cn } from "@/lib/utils";

interface HomeIntroSectionProps extends RabbiMessageSectionProps {
  banners: BannerMessage[];
}

export function HomeIntroSection({ banners, rabbiName, message }: HomeIntroSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="white" className="border-b border-[var(--color-border)]">
      <div ref={ref} className={cn(visible && "animate-fade-up")}>
        {banners.length > 0 && (
          <div className="mb-[var(--space-6)]">
            <BannerAlerts banners={banners} />
          </div>
        )}
        <SectionHeader icon={BookOpen} title={`דברי הרב ${rabbiName}`} />
        <Card hoverable={false} className="border-s-4 border-s-[var(--color-gold)]">
          <blockquote className="font-display text-[length:var(--text-body)] leading-[var(--leading-loose)] text-[var(--color-text)]">
            {message}
          </blockquote>
        </Card>
      </div>
    </Section>
  );
}
