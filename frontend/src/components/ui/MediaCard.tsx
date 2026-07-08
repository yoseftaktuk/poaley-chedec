import { ZoomIn } from "lucide-react";
import * as React from "react";

import { ImageLightbox } from "@/components/ui/ImageLightbox";
import { useImageLightbox } from "@/hooks/useImageLightbox";
import { cn } from "@/lib/utils";

export interface MediaCardProps extends React.HTMLAttributes<HTMLElement> {
  media?: React.ReactNode;
  footer?: React.ReactNode;
}

export const MediaCard = React.forwardRef<HTMLElement, MediaCardProps>(
  ({ className, media, footer, children, ...props }, ref) => (
    <article
      ref={ref}
      className={cn(
        "group flex h-full flex-col overflow-hidden rounded-[var(--radius-card)] border border-[var(--color-border)] bg-white shadow-[var(--shadow-card)] transition-base hover:-translate-y-0.5 hover:shadow-[var(--shadow-card-hover)]",
        className,
      )}
      {...props}
    >
      {media}
      <div className="flex flex-1 flex-col p-[var(--space-6)] md:p-[var(--space-8)]">
        <div className="flex flex-1 flex-col space-y-4">{children}</div>
        {footer && <div className="mt-[var(--space-4)]">{footer}</div>}
      </div>
    </article>
  ),
);
MediaCard.displayName = "MediaCard";

export interface MediaCardImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  overlay?: React.ReactNode;
  fit?: "cover" | "contain";
  enlargeable?: boolean;
}

export function MediaCardImage({
  className,
  overlay,
  alt = "",
  fit = "cover",
  enlargeable = false,
  src,
  ...props
}: MediaCardImageProps) {
  const { open, setOpen, openLightbox } = useImageLightbox();
  const imageSrc = typeof src === "string" ? src : "";

  const imageElement = (
    <img
      alt={alt}
      src={src}
      className={cn(
        "h-full w-full transition-base",
        !enlargeable && "motion-safe:group-hover:scale-[1.03]",
        fit === "contain"
          ? "object-contain p-[var(--space-2)]"
          : "object-cover",
        className,
      )}
      loading="lazy"
      {...props}
    />
  );

  const containerClassName = cn(
    "relative aspect-[16/10] w-full overflow-hidden",
    fit === "contain" ? "bg-[var(--color-cream)]" : "bg-[var(--color-muted)]",
  );

  if (enlargeable && imageSrc) {
    return (
      <>
        <div className={containerClassName}>
          <button
            type="button"
            onClick={openLightbox}
            className="group/image relative h-full w-full cursor-zoom-in border-0 bg-transparent p-0"
            aria-label="הגדל תמונה"
          >
            {imageElement}
            <span className="absolute bottom-4 start-4 inline-flex items-center gap-[var(--space-1)] rounded-full bg-[var(--color-navy)]/80 px-3 py-1.5 text-[length:var(--text-small)] text-white opacity-0 transition-base group-hover/image:opacity-100 group-focus-visible/image:opacity-100">
              <ZoomIn size={16} aria-hidden="true" />
              הגדל
            </span>
          </button>
          {overlay && <div className="pointer-events-none absolute inset-0">{overlay}</div>}
        </div>
        <ImageLightbox open={open} onOpenChange={setOpen} src={imageSrc} alt={alt} />
      </>
    );
  }

  return (
    <div className={containerClassName}>
      {imageElement}
      {overlay}
    </div>
  );
}
