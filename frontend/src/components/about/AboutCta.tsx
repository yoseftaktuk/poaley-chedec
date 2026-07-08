import { Link } from "react-router-dom";

import { GoldDivider } from "@/components/about/GoldDivider";
import { Button } from "@/components/ui/button";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { cn } from "@/lib/utils";
import type { AboutCtaContent } from "@/types/aboutPage";

interface AboutCtaProps {
  cta: AboutCtaContent;
}

export function AboutCta({ cta }: AboutCtaProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <section className="about-section about-cta" aria-labelledby="about-cta-heading">
      <div className="about-section__inner about-section__inner--narrow">
        <div ref={ref} className={cn(visible && "animate-fade-up")}>
          <h2 id="about-cta-heading" className="about-section-title">
            {cta.title}
          </h2>
          <GoldDivider centered />
          <p className="about-cta__message">{cta.message}</p>
          <Button asChild size="xl" variant="default">
            <Link to={cta.buttonHref} className="no-underline">
              {cta.buttonLabel}
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
