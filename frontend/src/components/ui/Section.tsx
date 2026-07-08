import type { LucideIcon } from "lucide-react";
import * as React from "react";

import { cn } from "@/lib/utils";

const backgroundVariants = {
  white: "bg-white",
  cream: "bg-[var(--color-cream)]",
  surface: "bg-[var(--color-surface)]",
  navy: "bg-[var(--color-navy)] text-white",
  transparent: "bg-transparent",
} as const;

export interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  background?: keyof typeof backgroundVariants;
  containerClassName?: string;
}

export const Section = React.forwardRef<HTMLElement, SectionProps>(
  ({ className, background = "white", containerClassName, children, ...props }, ref) => (
    <section
      ref={ref}
      className={cn("w-full py-[var(--section-py)]", backgroundVariants[background], className)}
      {...props}
    >
      <div className={cn("mx-auto max-w-6xl px-4", containerClassName)}>{children}</div>
    </section>
  ),
);
Section.displayName = "Section";

export interface SectionHeaderProps {
  icon: LucideIcon;
  title: string;
  className?: string;
  iconClassName?: string;
  light?: boolean;
  as?: "h1" | "h2";
}

export function SectionHeader({
  icon: Icon,
  title,
  className,
  iconClassName,
  light = false,
  as: Heading = "h2",
}: SectionHeaderProps) {
  return (
    <div className={cn("mb-[var(--space-6)] flex items-center gap-[var(--space-3)]", className)}>
      <span
        className={cn(
          "flex h-12 w-12 shrink-0 items-center justify-center rounded-full",
          light ? "bg-white/15 text-white" : "bg-[var(--color-cream)] text-[var(--color-navy)]",
          iconClassName,
        )}
        aria-hidden="true"
      >
        <Icon size={20} />
      </span>
      <Heading
        className={cn(
          "font-display text-[length:var(--text-section-title)] font-bold leading-[var(--leading-tight)]",
          light ? "text-white" : "text-[var(--color-navy)]",
        )}
      >
        {title}
      </Heading>
    </div>
  );
}
