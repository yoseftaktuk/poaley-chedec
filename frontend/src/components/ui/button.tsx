import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-xl text-[length:var(--text-body)] font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-navy)] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 motion-safe:hover:scale-[1.02] motion-safe:active:scale-[0.98]",
  {
    variants: {
      variant: {
        default:
          "bg-[var(--color-gold)] text-[var(--color-text)] shadow-md hover:bg-[var(--color-gold-hover)]",
        outline:
          "border border-[var(--color-border)] bg-transparent text-[var(--color-navy)] hover:bg-[var(--color-cream)]",
        secondary: "bg-white text-[var(--color-navy)] shadow-sm hover:bg-[var(--color-cream)]",
        success: "bg-[var(--color-whatsapp)] text-white shadow-md hover:brightness-110",
        danger: "bg-[var(--color-danger)] text-white shadow-md hover:brightness-110",
        ghost: "text-[var(--color-navy)] hover:bg-[var(--color-cream)]",
      },
      size: {
        default: "h-11 px-5 py-2",
        sm: "h-9 px-4 text-[length:var(--text-small)]",
        lg: "h-12 min-h-12 px-8 py-3 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />;
  },
);
Button.displayName = "Button";
