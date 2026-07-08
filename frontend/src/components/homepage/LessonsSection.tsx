import { ArrowLeft, BookOpen, Calendar, Clock } from "lucide-react";
import { memo } from "react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/Card";
import { Section, SectionHeader } from "@/components/ui/Section";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import { formatDaysOfWeek } from "@/lib/formatDays";
import type { TorahLesson } from "@/types";
import type { LessonsSectionProps } from "@/types/homepage";
import { cn } from "@/lib/utils";

interface LessonCardProps {
  lesson: TorahLesson;
  contactPath: string;
}

const LessonCard = memo(function LessonCard({ lesson, contactPath }: LessonCardProps) {
  return (
    <Card className="flex flex-col">
      <div className="mb-[var(--space-4)] flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-cream)] text-[var(--color-navy)]">
        <BookOpen size={24} aria-hidden="true" />
      </div>
      <h3 className="mb-[var(--space-2)] font-display text-[length:var(--text-card-title)] font-bold leading-[var(--leading-tight)] text-[var(--color-navy)]">
        {lesson.lesson_name}
      </h3>
      <p className="mb-[var(--space-4)] text-[length:var(--text-small)] text-[var(--color-text)]/70">
        רב: {lesson.rabbi_name}
      </p>
      <div className="mb-[var(--space-4)] flex flex-wrap items-center gap-[var(--space-4)] text-[length:var(--text-small)] text-[var(--color-text)]">
        <span className="inline-flex items-center gap-[var(--space-2)]">
          <Calendar size={16} className="text-[var(--color-gold)]" aria-hidden="true" />
          {formatDaysOfWeek(lesson.days_of_week)}
        </span>
        <span className="inline-flex items-center gap-[var(--space-2)]">
          <Clock size={16} className="text-[var(--color-gold)]" aria-hidden="true" />
          {lesson.lesson_time}
        </span>
      </div>
      {lesson.description && (
        <p className="mb-[var(--space-6)] line-clamp-3 flex-1 text-[length:var(--text-body)] leading-[var(--leading-body)] text-[var(--color-text)]">
          {lesson.description}
        </p>
      )}
      <div className="mt-auto">
        <Button asChild variant="outline">
          <Link to={contactPath} className="no-underline">
            פרטים נוספים
            <ArrowLeft size={16} aria-hidden="true" />
          </Link>
        </Button>
      </div>
    </Card>
  );
});

export function LessonsSection({ lessons, contactPath }: LessonsSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="cream" id="lessons">
      <div ref={ref} className={cn(visible && "animate-fade-up")}>
        <SectionHeader icon={BookOpen} title="שיעורי תורה" />
        <div className="grid gap-[var(--space-4)] md:grid-cols-2">
          {lessons.map((lesson) => (
            <LessonCard key={lesson.id} lesson={lesson} contactPath={contactPath} />
          ))}
        </div>
      </div>
    </Section>
  );
}
