import { renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useWhatsAppUrl } from "@/hooks/useWhatsAppUrl";

describe("useWhatsAppUrl", () => {
  it("formats israeli phone number", () => {
    const { result } = renderHook(() => useWhatsAppUrl("0544329218"));
    expect(result.current).toContain("wa.me/972544329218");
  });

  it("returns hash for missing phone", () => {
    const { result } = renderHook(() => useWhatsAppUrl(undefined));
    expect(result.current).toBe("#");
  });
});
