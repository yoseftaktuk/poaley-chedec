import { GoldDivider } from "@/components/about/GoldDivider";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { cn } from "@/lib/utils";
import type { AboutVerseContent } from "@/types/aboutPage";

interface AboutVerseProps {
  verse: AboutVerseContent;
}

export function AboutVerse({ verse }: AboutVerseProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <section className="about-section" aria-labelledby="about-verse-heading">
      <div className="about-section__inner about-section__inner--narrow">
        <h2 id="about-verse-heading" className="sr-only">
          פסוק מקרא
        </h2>
        <div ref={ref} className={cn("about-verse", visible && "animate-fade-up")}>
          <blockquote cite={verse.reference}>
            <p>{verse.text}</p>
          </blockquote>
          <GoldDivider centered />
          <cite>{verse.reference}</cite>
        </div>
      </div>
    </section>
  );
}
