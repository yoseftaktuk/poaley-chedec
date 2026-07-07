import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import type { AccessibilitySettings } from "@/types";

interface AccessibilityContextValue extends AccessibilitySettings {
  setFontSize: (size: AccessibilitySettings["fontSize"]) => void;
  toggleHighContrast: () => void;
}

const STORAGE_KEY = "a11y-settings";

const defaultSettings: AccessibilitySettings = {
  fontSize: "normal",
  highContrast: false,
};

const AccessibilityContext = createContext<AccessibilityContextValue | null>(null);

function loadSettings(): AccessibilitySettings {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? (JSON.parse(stored) as AccessibilitySettings) : defaultSettings;
  } catch {
    return defaultSettings;
  }
}

export function AccessibilityProvider({ children }: { children: React.ReactNode }) {
  const [settings, setSettings] = useState<AccessibilitySettings>(loadSettings);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    document.documentElement.setAttribute("data-contrast", settings.highContrast ? "high" : "normal");
    document.documentElement.style.fontSize =
      settings.fontSize === "large" ? "112.5%" : settings.fontSize === "xlarge" ? "125%" : "100%";
  }, [settings]);

  const setFontSize = useCallback((fontSize: AccessibilitySettings["fontSize"]) => {
    setSettings((prev) => ({ ...prev, fontSize }));
  }, []);

  const toggleHighContrast = useCallback(() => {
    setSettings((prev) => ({ ...prev, highContrast: !prev.highContrast }));
  }, []);

  const value = useMemo(
    () => ({ ...settings, setFontSize, toggleHighContrast }),
    [settings, setFontSize, toggleHighContrast],
  );

  return <AccessibilityContext.Provider value={value}>{children}</AccessibilityContext.Provider>;
}

export function useAccessibility() {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error("useAccessibility must be used within AccessibilityProvider");
  }
  return context;
}
