import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { cn } from "@/lib/utils";

interface AboutIntroProps {
  intro: string;
}

export function AboutIntro({ intro }: AboutIntroProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <section className="about-section">
      <div className="about-section__inner about-section__inner--narrow">
        <div ref={ref} className={cn(visible && "animate-fade-up")}>
          <p>{intro}</p>
        </div>
      </div>
    </section>
  );
}
