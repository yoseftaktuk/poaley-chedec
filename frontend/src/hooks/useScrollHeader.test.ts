import { act, renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useScrollHeader } from "@/hooks/useScrollHeader";

describe("useScrollHeader", () => {
  it("returns false when not scrolled", () => {
    Object.defineProperty(window, "scrollY", { value: 0, writable: true });
    const { result } = renderHook(() => useScrollHeader(10));
    expect(result.current).toBe(false);
  });

  it("returns true when scrolled past threshold", () => {
    Object.defineProperty(window, "scrollY", { value: 50, writable: true });
    const { result } = renderHook(() => useScrollHeader(10));
    act(() => {
      window.dispatchEvent(new Event("scroll"));
    });
    expect(result.current).toBe(true);
  });
});
