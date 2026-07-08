import * as React from "react";

import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, hoverable = true, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "h-full rounded-[var(--radius-card)] border border-[var(--color-border)] bg-white p-[var(--space-6)] shadow-[var(--shadow-card)] md:p-[var(--space-8)]",
        hoverable &&
          "transition-base hover:-translate-y-0.5 hover:shadow-[var(--shadow-card-hover)]",
        className,
      )}
      {...props}
    />
  ),
);
Card.displayName = "Card";
