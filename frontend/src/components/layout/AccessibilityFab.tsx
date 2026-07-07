import { Accessibility } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { useAccessibility } from "@/hooks/useAccessibility";
import { ROUTES } from "@/lib/constants";

export function AccessibilityFab() {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const { fontSize, highContrast, setFontSize, toggleHighContrast } = useAccessibility();

  useEffect(() => {
    if (!open) {
      return;
    }

    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  return (
    <div ref={containerRef} className="fixed bottom-4 end-4 z-50">
      {open && (
        <div
          className="absolute bottom-full end-0 mb-2 min-w-[220px] rounded-xl border border-[var(--color-border)] bg-white p-4 shadow-lg"
          role="region"
          aria-label="הגדרות נגישות"
        >
          <p className="mb-3 text-sm font-medium">נגישות</p>
          <div className="flex flex-col gap-2">
            <Button
              size="sm"
              variant={fontSize === "normal" ? "default" : "outline"}
              onClick={() => setFontSize("normal")}
              aria-pressed={fontSize === "normal"}
            >
              גופן רגיל
            </Button>
            <Button
              size="sm"
              variant={fontSize === "large" ? "default" : "outline"}
              onClick={() => setFontSize("large")}
              aria-pressed={fontSize === "large"}
            >
              גופן גדול
            </Button>
            <Button
              size="sm"
              variant={fontSize === "xlarge" ? "default" : "outline"}
              onClick={() => setFontSize("xlarge")}
              aria-pressed={fontSize === "xlarge"}
            >
              גופן גדול מאוד
            </Button>
            <Button
              size="sm"
              variant={highContrast ? "default" : "outline"}
              onClick={toggleHighContrast}
              aria-pressed={highContrast}
            >
              ניגודיות גבוהה
            </Button>
          </div>
          <hr className="my-3 border-[var(--color-border)]" />
          <Link
            to={ROUTES.accessibility}
            className="block text-sm no-underline hover:underline"
            onClick={() => setOpen(false)}
          >
            הצהרת נגישות
          </Link>
        </div>
      )}

      <Button
        type="button"
        size="lg"
        className="h-14 w-14 rounded-full shadow-lg"
        aria-label="הגדרות נגישות"
        aria-expanded={open}
        onClick={() => setOpen((prev) => !prev)}
      >
        <Accessibility size={24} />
      </Button>
    </div>
  );
}
