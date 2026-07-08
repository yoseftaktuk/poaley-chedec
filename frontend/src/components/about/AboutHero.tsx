import type { AboutHeroContent } from "@/types/aboutPage";

interface AboutHeroProps {
  hero: AboutHeroContent;
}

export function AboutHero({ hero }: AboutHeroProps) {
  return (
    <section className="about-hero" aria-label="אודות בית הכנסת">
      <div className="about-hero__image" aria-hidden="true">
        <img src={hero.imageSrc} alt="" fetchPriority="high" decoding="async" />
      </div>
      <div className="about-hero__overlay" aria-hidden="true" />
      <div className="about-hero__content">
        <h1>{hero.title}</h1>
        <p>{hero.subtitle}</p>
      </div>
    </section>
  );
}
