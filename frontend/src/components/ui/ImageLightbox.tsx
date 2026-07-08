import * as Dialog from "@radix-ui/react-dialog";
import { X } from "lucide-react";

export interface ImageLightboxProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  src: string;
  alt: string;
}

export function ImageLightbox({ open, onOpenChange, src, alt }: ImageLightboxProps) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/80" />
        <Dialog.Content
          className="fixed inset-0 z-50 flex items-center justify-center p-[var(--space-4)] outline-none"
          aria-label="תמונה מוגדלת"
        >
          <Dialog.Close
            className="absolute end-4 top-4 inline-flex h-11 w-11 items-center justify-center rounded-full bg-white/15 text-white transition-base hover:bg-white/25 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"
            aria-label="סגור"
          >
            <X size={22} aria-hidden="true" />
          </Dialog.Close>
          <img
            src={src}
            alt={alt}
            className="max-h-[90vh] max-w-[90vw] object-contain"
          />
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
