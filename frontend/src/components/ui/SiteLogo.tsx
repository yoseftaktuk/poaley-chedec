import { SITE_LOGO } from "@/lib/constants";
import { cn } from "@/lib/utils";

const SIZE_CLASSES = {
  sm: "h-10",
  md: "h-12",
  lg: "h-16",
} as const;

interface SiteLogoProps {
  size?: keyof typeof SIZE_CLASSES;
  className?: string;
}

export function SiteLogo({ size = "md", className }: SiteLogoProps) {
  return (
    <img
      src={SITE_LOGO.src}
      alt={SITE_LOGO.alt}
      className={cn("w-auto object-contain", SIZE_CLASSES[size], className)}
      decoding="async"
    />
  );
}
