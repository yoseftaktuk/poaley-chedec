import { Heart } from "lucide-react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { Section, SectionHeader } from "@/components/ui/Section";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import type { DonationsSectionProps } from "@/types/homepage";
import { cn } from "@/lib/utils";

export function DonationsSection({ donationUrl, donationText, contactPath }: DonationsSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="navy" id="donations">
      <div ref={ref} className={cn("text-center", visible && "animate-fade-up")}>
        <SectionHeader icon={Heart} title="תרומה לבית הכנסת" light className="justify-center" />
        <p className="mx-auto mb-8 max-w-2xl text-[length:var(--text-body)] leading-relaxed text-white/85">
          תרומתכם מאפשרת לנו להמשיך ולקיים את פעילות בית הכנסת, שיעורי התורה והקהילה. כל תרומה,
          קטנה כגדולה, תורמת לשגשוג הקהילה.
        </p>
        <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button asChild size="lg">
            <a href={donationUrl} target="_blank" rel="noopener noreferrer">
              <Heart size={20} aria-hidden="true" />
              {donationText}
            </a>
          </Button>
          <Button asChild variant="secondary" size="lg">
            <Link to={contactPath} className="no-underline">
              צור קשר
            </Link>
          </Button>
        </div>
      </div>
    </Section>
  );
}
