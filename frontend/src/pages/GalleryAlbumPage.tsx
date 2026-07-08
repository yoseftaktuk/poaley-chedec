import { ZoomIn } from "lucide-react";
import { useParams } from "react-router-dom";

import { ImageLightbox } from "@/components/ui/ImageLightbox";
import { useGalleryImages } from "@/hooks/usePublicData";
import { useImageLightbox } from "@/hooks/useImageLightbox";
import type { GalleryImage } from "@/types";

function AlbumImageCard({ image }: { image: GalleryImage }) {
  const { open, setOpen, openLightbox } = useImageLightbox();
  const alt = image.title || "תמונה";

  return (
    <figure className="card card-flush overflow-hidden">
      <button
        type="button"
        onClick={openLightbox}
        className="group/image relative block h-56 w-full cursor-zoom-in border-0 bg-transparent p-0"
        aria-label="הגדל תמונה"
      >
        <img
          src={image.image_url}
          alt={alt}
          className="h-full w-full object-cover"
          loading="lazy"
        />
        <span className="absolute bottom-4 start-4 inline-flex items-center gap-[var(--space-1)] rounded-full bg-[var(--color-navy)]/80 px-3 py-1.5 text-[length:var(--text-small)] text-white opacity-0 transition-base group-hover/image:opacity-100 group-focus-visible/image:opacity-100">
          <ZoomIn size={16} aria-hidden="true" />
          הגדל
        </span>
      </button>
      {image.title && (
        <figcaption className="px-[var(--space-4)] py-2 text-center text-sm">{image.title}</figcaption>
      )}
      <ImageLightbox open={open} onOpenChange={setOpen} src={image.image_url} alt={alt} />
    </figure>
  );
}

export function GalleryAlbumPage() {
  const { albumId } = useParams<{ albumId: string }>();
  const { data: images, isLoading, error } = useGalleryImages(albumId);

  if (isLoading) return <div className="container-page">טוען...</div>;
  if (error) return <div className="container-page">שגיאה בטעינת התמונות</div>;

  return (
    <div className="container-page">
      <h1 className="section-title">תמונות באלבום</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {images?.map((image) => (
          <AlbumImageCard key={image.id} image={image} />
        ))}
      </div>
    </div>
  );
}
