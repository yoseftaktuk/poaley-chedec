import { act, renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useImageLightbox } from "@/hooks/useImageLightbox";

describe("useImageLightbox", () => {
  it("starts closed", () => {
    const { result } = renderHook(() => useImageLightbox());
    expect(result.current.open).toBe(false);
  });

  it("opens and closes lightbox", () => {
    const { result } = renderHook(() => useImageLightbox());

    act(() => result.current.openLightbox());
    expect(result.current.open).toBe(true);

    act(() => result.current.closeLightbox());
    expect(result.current.open).toBe(false);
  });

  it("setOpen controls state directly", () => {
    const { result } = renderHook(() => useImageLightbox());
    act(() => result.current.setOpen(true));
    expect(result.current.open).toBe(true);
  });
});
