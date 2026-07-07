import { useRef } from "react";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/input";
import { useImageUpload } from "@/hooks/useImageUpload";

interface ImageUploadProps {
  imageUrl: string | null;
  publicId?: string | null;
  onChange: (imageUrl: string | null, publicId?: string | null) => void;
  folder?: string;
  label?: string;
}

export function ImageUpload({
  imageUrl,
  onChange,
  folder,
  label = "העלאת תמונה",
}: ImageUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const { upload, isUploading, error } = useImageUpload({ folder });

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    try {
      const result = await upload(file);
      onChange(result.url, result.public_id);
    } finally {
      event.target.value = "";
    }
  };

  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      {imageUrl && (
        <div className="flex aspect-[4/3] w-full max-w-xs items-center justify-center overflow-hidden rounded border border-[var(--color-border)] bg-[var(--color-muted)]">
          <img
            src={imageUrl}
            alt="תצוגה מקדימה"
            className="max-h-full max-w-full object-contain"
          />
        </div>
      )}
      <div className="flex flex-wrap gap-2">
        <Button
          type="button"
          variant="outline"
          disabled={isUploading}
          onClick={() => inputRef.current?.click()}
        >
          {isUploading ? "מעלה..." : imageUrl ? "החלף תמונה" : "בחר תמונה"}
        </Button>
        {imageUrl && (
          <Button type="button" variant="outline" onClick={() => onChange(null, null)}>
            הסר תמונה
          </Button>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleFileChange}
      />
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
