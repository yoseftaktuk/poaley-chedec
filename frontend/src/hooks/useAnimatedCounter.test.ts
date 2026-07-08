import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useAnimatedCounter } from "@/hooks/useAnimatedCounter";

describe("useAnimatedCounter", () => {
  it("starts at zero", () => {
    const { result } = renderHook(() => useAnimatedCounter({ target: 75 }));
    expect(result.current.displayValue).toBe(0);
  });
});
