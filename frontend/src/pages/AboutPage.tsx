import { AboutCta } from "@/components/about/AboutCta";
import { AboutDecorations } from "@/components/about/AboutDecorations";
import { AboutHero } from "@/components/about/AboutHero";
import { AboutIntro } from "@/components/about/AboutIntro";
import { AboutStats } from "@/components/about/AboutStats";
import { AboutTimeline } from "@/components/about/AboutTimeline";
import { AboutVerse } from "@/components/about/AboutVerse";
import { aboutPageContent } from "@/content/aboutPage";
import "@/styles/about.css";

export function AboutPage() {
  const { hero, intro, timelineTitle, timeline, statsTitle, stats, verse, cta } = aboutPageContent;

  return (
    <div className="about-page">
      <AboutDecorations />
      <AboutHero hero={hero} />
      <AboutIntro intro={intro} />
      <AboutTimeline title={timelineTitle} items={timeline} />
      <AboutStats title={statsTitle} stats={stats} />
      <AboutVerse verse={verse} />
      <AboutCta cta={cta} />
    </div>
  );
}
