import { act, renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AccessibilityProvider, useAccessibility } from "@/hooks/useAccessibility";

describe("useAccessibility", () => {
  it("throws outside provider", () => {
    expect(() => renderHook(() => useAccessibility())).toThrow(/AccessibilityProvider/);
  });

  it("toggles high contrast", () => {
    const { result } = renderHook(() => useAccessibility(), {
      wrapper: AccessibilityProvider,
    });

    expect(result.current.highContrast).toBe(false);
    act(() => result.current.toggleHighContrast());
    expect(result.current.highContrast).toBe(true);
  });

  it("changes font size", () => {
    const { result } = renderHook(() => useAccessibility(), {
      wrapper: AccessibilityProvider,
    });

    act(() => result.current.setFontSize("large"));
    expect(result.current.fontSize).toBe("large");
    expect(document.documentElement.style.fontSize).toBe("112.5%");
  });
});
