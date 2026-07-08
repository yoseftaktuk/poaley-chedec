import { renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";

describe("useFadeUpOnScroll", () => {
  it("starts not visible", () => {
    const { result } = renderHook(() => useFadeUpOnScroll());
    expect(result.current.visible).toBe(false);
    expect(result.current.ref).toBeDefined();
  });
});
