import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/input";
import { ApiError, apiFetch, apiUpload } from "@/lib/api";
import type { GalleryAlbum, GalleryImage } from "@/types";

interface GalleryAlbumImagesProps {
  albums: GalleryAlbum[];
}

export function GalleryAlbumImages({ albums }: GalleryAlbumImagesProps) {
  const qc = useQueryClient();
  const [selectedAlbumId, setSelectedAlbumId] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { data: images = [], isLoading } = useQuery({
    queryKey: ["gallery-album-images", selectedAlbumId],
    queryFn: () => apiFetch<GalleryImage[]>(`/gallery/albums/${selectedAlbumId}/images`),
    enabled: Boolean(selectedAlbumId),
  });

  const remove = useMutation({
    mutationFn: (imageId: string) => apiFetch(`/gallery/images/${imageId}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["gallery-album-images", selectedAlbumId] }),
  });

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !selectedAlbumId) {
      return;
    }

    setIsUploading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      await apiUpload<GalleryImage>(
        `/gallery/images/upload?album_id=${selectedAlbumId}`,
        formData,
      );
      qc.invalidateQueries({ queryKey: ["gallery-album-images", selectedAlbumId] });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "שגיאה בהעלאת התמונה");
    } finally {
      setIsUploading(false);
      event.target.value = "";
    }
  };

  return (
    <div className="card space-y-4">
      <h2 className="text-lg font-bold">תמונות באלבום</h2>
      <div>
        <Label>בחר אלבום</Label>
        <select
          className="mt-1 w-full rounded border border-[var(--color-border)] p-2"
          value={selectedAlbumId}
          onChange={(e) => setSelectedAlbumId(e.target.value)}
        >
          <option value="">— בחר אלבום —</option>
          {albums.map((album) => (
            <option key={album.id} value={album.id}>
              {album.title}
            </option>
          ))}
        </select>
      </div>

      {selectedAlbumId && (
        <>
          <div>
            <Label>הוסף תמונה לאלבום</Label>
            <input
              type="file"
              accept="image/*"
              className="mt-1 block w-full"
              disabled={isUploading}
              onChange={handleFileChange}
            />
            {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
          </div>

          {isLoading ? (
            <p>טוען תמונות...</p>
          ) : images.length === 0 ? (
            <p className="text-sm text-gray-500">אין תמונות באלבום זה</p>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3">
              {images.map((image) => (
                <div key={image.id} className="space-y-2 rounded border border-[var(--color-border)] p-2">
                  <img
                    src={image.image_url}
                    alt={image.title || "תמונה"}
                    className="h-32 w-full rounded object-cover"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="w-full"
                    onClick={() => remove.mutate(image.id)}
                  >
                    מחק
                  </Button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
