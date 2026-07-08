import { Mail, MessageCircle, Phone } from "lucide-react";

import { cn } from "@/lib/utils";

export interface SocialLinksProps {
  whatsappUrl?: string;
  phone?: string;
  email?: string;
  className?: string;
  size?: "default" | "lg";
  theme?: "dark" | "light";
}

const sizeClasses = {
  default: "h-11 w-11",
  lg: "h-12 w-12",
} as const;

const iconSizes = {
  default: 20,
  lg: 22,
} as const;

const channelClasses = {
  dark: {
    whatsapp: "bg-[var(--color-whatsapp)] text-white hover:brightness-110",
    phone: "bg-[var(--color-gold)] text-[var(--color-text)] hover:bg-[var(--color-gold-hover)]",
    email: "bg-white text-[var(--color-navy)] hover:bg-[var(--color-cream)]",
  },
  light: {
    whatsapp: "bg-[var(--color-whatsapp)] text-white hover:brightness-110",
    phone: "bg-[var(--color-gold)] text-[var(--color-text)] hover:bg-[var(--color-gold-hover)]",
    email: "bg-[var(--color-cream)] text-[var(--color-navy)] hover:bg-[var(--color-surface)]",
  },
} as const;

export function SocialLinks({
  whatsappUrl,
  phone,
  email,
  className,
  size = "default",
  theme = "dark",
}: SocialLinksProps) {
  const iconSize = iconSizes[size];
  const colors = channelClasses[theme];

  const links = [
    whatsappUrl && whatsappUrl !== "#"
      ? {
          href: whatsappUrl,
          label: "WhatsApp",
          className: colors.whatsapp,
          icon: MessageCircle,
          external: true,
        }
      : null,
    phone
      ? {
          href: `tel:${phone}`,
          label: "טלפון",
          className: colors.phone,
          icon: Phone,
          external: false,
        }
      : null,
    email
      ? {
          href: `mailto:${email}`,
          label: "אימייל",
          className: colors.email,
          icon: Mail,
          external: false,
        }
      : null,
  ].filter(Boolean) as {
    href: string;
    label: string;
    className: string;
    icon: typeof MessageCircle;
    external: boolean;
  }[];

  if (!links.length) {
    return null;
  }

  return (
    <div className={cn("flex flex-wrap items-center gap-[var(--space-2)]", className)}>
      {links.map((link) => {
        const Icon = link.icon;
        return (
          <a
            key={link.label}
            href={link.href}
            target={link.external ? "_blank" : undefined}
            rel={link.external ? "noopener noreferrer" : undefined}
            aria-label={link.label}
            className={cn(
              "social-link inline-flex items-center justify-center rounded-full shadow-[var(--shadow-card)] transition-base motion-safe:hover:scale-[1.05]",
              sizeClasses[size],
              link.className,
            )}
          >
            <Icon size={iconSize} aria-hidden="true" />
          </a>
        );
      })}
    </div>
  );
}
