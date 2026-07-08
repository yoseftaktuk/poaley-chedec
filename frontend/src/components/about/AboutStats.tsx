import { GoldDivider } from "@/components/about/GoldDivider";
import { useAnimatedCounter } from "@/hooks/useAnimatedCounter";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { cn } from "@/lib/utils";
import type { AboutStat, AboutStatCounter } from "@/types/aboutPage";

function StatCounter({ stat }: { stat: AboutStatCounter }) {
  const { ref, displayValue } = useAnimatedCounter({ target: stat.value });

  return (
    <div ref={ref} className="about-stat" aria-live="polite">
      <p className="about-stat__value">
        {displayValue}
        {stat.suffix}
      </p>
      <p className="about-stat__label">{stat.label}</p>
    </div>
  );
}

function StatText({ stat }: { stat: Extract<AboutStat, { type: "text" }> }) {
  return (
    <div className="about-stat">
      <p className="about-stat__value">{stat.displayText}</p>
      <p className="about-stat__label">{stat.label}</p>
    </div>
  );
}

interface AboutStatsProps {
  title: string;
  stats: AboutStat[];
}

export function AboutStats({ title, stats }: AboutStatsProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <section className="about-section" aria-labelledby="about-stats-heading">
      <div className="about-section__inner">
        <h2 id="about-stats-heading" className="about-section-title">
          {title}
        </h2>
        <GoldDivider />
        <div ref={ref} className={cn("about-stats-grid", visible && "animate-fade-up")}>
          {stats.map((stat) =>
            stat.type === "counter" ? (
              <StatCounter key={stat.id} stat={stat} />
            ) : (
              <StatText key={stat.id} stat={stat} />
            ),
          )}
        </div>
      </div>
    </section>
  );
}
