import { ArrowLeft, Calendar, Clock } from "lucide-react";
import { memo } from "react";
import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/button";
import { MediaCard, MediaCardImage } from "@/components/ui/MediaCard";
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
    <MediaCard
      media={
        event.image_url ? (
          <MediaCardImage
            src={event.image_url}
            alt={event.title}
            fit="contain"
            enlargeable
            overlay={
              <span className="absolute start-4 top-4">
                <Badge icon={Calendar} variant="navy">
                  {event.event_date}
                </Badge>
              </span>
            }
          />
        ) : undefined
      }
      footer={
        <Button asChild variant="outline">
          <Link to={contactPath} className="no-underline">
            פרטים נוספים
            <ArrowLeft size={16} aria-hidden="true" />
          </Link>
        </Button>
      }
    >
      {!event.image_url && (
        <Badge icon={Calendar} variant="cream">
          {event.event_date}
        </Badge>
      )}
      <div className="flex items-center gap-[var(--space-2)] text-[length:var(--text-small)] text-[var(--color-text)]/70">
        <Clock size={16} className="text-[var(--color-gold)]" aria-hidden="true" />
        {event.event_time}
      </div>
      <h3 className="font-display text-[length:var(--text-card-title)] font-bold leading-[var(--leading-tight)] text-[var(--color-navy)]">
        {event.title}
      </h3>
      <p className="line-clamp-3 text-[length:var(--text-body)] leading-[var(--leading-body)] text-[var(--color-text)]">
        {event.description}
      </p>
    </MediaCard>
  );
});

export function EventsSection({ events, contactPath }: EventsSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="white" id="events">
      <div ref={ref} className={cn(visible && "animate-fade-up")}>
        <SectionHeader icon={Calendar} title="אירועים קרובים" />
        <div className="grid gap-[var(--space-4)] md:grid-cols-2">
          {events.map((event) => (
            <EventCard key={event.id} event={event} contactPath={contactPath} />
          ))}
        </div>
      </div>
    </Section>
  );
}
