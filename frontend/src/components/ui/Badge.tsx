import type { LucideIcon } from "lucide-react";
import * as React from "react";

import { cn } from "@/lib/utils";

const badgeVariants = {
  navy: "bg-[var(--color-navy)] text-white shadow-[var(--shadow-card)]",
  cream: "bg-[var(--color-cream)] text-[var(--color-navy)]",
} as const;

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  icon?: LucideIcon;
  variant?: keyof typeof badgeVariants;
}

export function Badge({ className, icon: Icon, variant = "navy", children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-[length:var(--text-small)] font-medium",
        badgeVariants[variant],
        className,
      )}
      {...props}
    >
      {Icon && <Icon size={16} aria-hidden="true" />}
      {children}
    </span>
  );
}
