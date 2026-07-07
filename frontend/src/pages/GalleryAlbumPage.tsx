import { useParams } from "react-router-dom";

import { useGalleryImages } from "@/hooks/usePublicData";

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
          <figure key={image.id} className="card p-2">
            <img
              src={image.image_url}
              alt={image.title || "תמונה"}
              className="h-56 w-full rounded object-cover"
              loading="lazy"
            />
            {image.title && <figcaption className="mt-2 text-center text-sm">{image.title}</figcaption>}
          </figure>
        ))}
      </div>
    </div>
  );
}
