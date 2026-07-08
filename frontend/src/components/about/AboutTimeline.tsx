import { Calendar, Flame, Landmark, Users, type LucideIcon } from "lucide-react";

import { GoldDivider } from "@/components/about/GoldDivider";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { cn } from "@/lib/utils";
import type { AboutTimelineIcon, AboutTimelineItem } from "@/types/aboutPage";

const iconMap: Record<AboutTimelineIcon, LucideIcon> = {
  calendar: Calendar,
  flame: Flame,
  users: Users,
  landmark: Landmark,
};

interface TimelineItemProps {
  item: AboutTimelineItem;
}

function TimelineItem({ item }: TimelineItemProps) {
  const { ref, visible } = useFadeUpOnScroll();
  const Icon = iconMap[item.icon];

  return (
    <article ref={ref} className={cn("about-timeline-item", visible && "animate-fade-up")}>
      <div className="about-timeline-item__header">
        <span className="about-timeline-item__icon" aria-hidden="true">
          <Icon size={22} />
        </span>
        <div>
          {item.year && <p className="about-timeline-item__year">{item.year}</p>}
          <h2 className="about-timeline-item__title">{item.title}</h2>
        </div>
      </div>
      <p className="about-timeline-item__body">{item.body}</p>
    </article>
  );
}

interface AboutTimelineProps {
  title: string;
  items: AboutTimelineItem[];
}

export function AboutTimeline({ title, items }: AboutTimelineProps) {
  return (
    <section className="about-section" aria-labelledby="about-timeline-heading">
      <div className="about-section__inner">
        <h2 id="about-timeline-heading" className="about-section-title">
          {title}
        </h2>
        <GoldDivider />
        <div className="about-timeline">
          {items.map((item) => (
            <TimelineItem key={item.id} item={item} />
          ))}
        </div>
      </div>
    </section>
  );
}
