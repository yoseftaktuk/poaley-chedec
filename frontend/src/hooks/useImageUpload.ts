import { useState } from "react";

import { ApiError, apiUpload } from "@/lib/api";
import type { UploadImageResponse } from "@/types";

interface UseImageUploadOptions {
  folder?: string;
}

export function useImageUpload({ folder }: UseImageUploadOptions = {}) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = async (file: File): Promise<UploadImageResponse> => {
    setIsUploading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const path = folder ? `/uploads/image?folder=${encodeURIComponent(folder)}` : "/uploads/image";
      return await apiUpload<UploadImageResponse>(path, formData);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "שגיאה בהעלאת התמונה";
      setError(message);
      throw err;
    } finally {
      setIsUploading(false);
    }
  };

  return { upload, isUploading, error, setError };
}
