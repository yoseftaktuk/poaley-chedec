import { Link } from "react-router-dom";

import { useGalleryAlbums } from "@/hooks/usePublicData";

export function GalleryPage() {
  const { data: albums, isLoading, error } = useGalleryAlbums();

  if (isLoading) return <div className="container-page">טוען...</div>;
  if (error) return <div className="container-page">שגיאה בטעינת הגלריה</div>;

  return (
    <div className="container-page">
      <h1 className="section-title">גלריה</h1>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {albums?.map((album) => (
          <Link
            key={album.id}
            to={`/gallery/${album.id}`}
            className="card card-flush block overflow-hidden no-underline"
          >
            {album.cover_image_url && (
              <img
                src={album.cover_image_url}
                alt={album.title}
                className="h-48 w-full object-cover"
                loading="lazy"
              />
            )}
            <div className="space-y-1 p-[var(--space-6)] md:p-[var(--space-8)]">
              <h2 className="font-bold">{album.title}</h2>
              <p className="text-sm">{album.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
