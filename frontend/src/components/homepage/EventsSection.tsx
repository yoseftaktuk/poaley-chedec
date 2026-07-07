import { ArrowLeft, Calendar, Clock } from "lucide-react";
import { memo } from "react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { Section, SectionHeader } from "@/components/ui/Section";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import type { Event } from "@/types";
import type { EventsSectionProps } from "@/types/homepage";
import { cn } from "@/lib/utils";

interface EventCardProps {
  event: Event;
  contactPath: string;
}

const EventCard = memo(function EventCard({ event, contactPath }: EventCardProps) {
  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-[var(--radius-card)] border border-[var(--color-border)] bg-white shadow-[var(--shadow-card)] transition-all duration-300 hover:-translate-y-1 hover:shadow-[var(--shadow-card-hover)]">
      {event.image_url && (
        <div className="relative aspect-[16/9] w-full overflow-hidden bg-[var(--color-muted)]">
          <img
            src={event.image_url}
            alt={event.title}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
          <span className="absolute start-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-[var(--color-navy)] px-3 py-1.5 text-[length:var(--text-small)] font-medium text-white shadow-md">
            <Calendar size={14} aria-hidden="true" />
            {event.event_date}
          </span>
        </div>
      )}
      <div className="flex flex-1 flex-col p-6 md:p-8">
        {!event.image_url && (
          <span className="mb-3 inline-flex w-fit items-center gap-1.5 rounded-full bg-[var(--color-cream)] px-3 py-1.5 text-[length:var(--text-small)] font-medium text-[var(--color-navy)]">
            <Calendar size={14} aria-hidden="true" />
            {event.event_date}
          </span>
        )}
        <div className="mb-2 flex items-center gap-1.5 text-[length:var(--text-small)] text-[var(--color-text)]/70">
          <Clock size={16} className="text-[var(--color-gold)]" aria-hidden="true" />
          {event.event_time}
        </div>
        <h3 className="mb-3 font-display text-[length:var(--text-card-title)] font-bold text-[var(--color-navy)]">
          {event.title}
        </h3>
        <p className="mb-6 line-clamp-2 flex-1 text-[length:var(--text-body)] leading-relaxed text-[var(--color-text)]">
          {event.description}
        </p>
        <div className="mt-auto">
          <Button asChild variant="outline" size="sm">
            <Link to={contactPath} className="no-underline">
              פרטים נוספים
              <ArrowLeft size={16} aria-hidden="true" />
            </Link>
          </Button>
        </div>
      </div>
    </article>
  );
});

export function EventsSection({ events, contactPath }: EventsSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="white" id="events">
      <div ref={ref} className={cn(visible && "animate-fade-up")}>
        <SectionHeader icon={Calendar} title="אירועים קרובים" />
        <div className="grid gap-6 md:grid-cols-2">
          {events.map((event) => (
            <EventCard key={event.id} event={event} contactPath={contactPath} />
          ))}
        </div>
      </div>
    </Section>
  );
}
