import { useState } from "react";

export function useImageLightbox() {
  const [open, setOpen] = useState(false);

  return {
    open,
    setOpen,
    openLightbox: () => setOpen(true),
    closeLightbox: () => setOpen(false),
  };
}
