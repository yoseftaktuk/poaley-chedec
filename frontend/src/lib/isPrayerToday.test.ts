import { describe, expect, it, vi } from "vitest";

import { isPrayerToday } from "@/lib/isPrayerToday";

describe("isPrayerToday", () => {
  it("returns true for empty days array", () => {
    expect(isPrayerToday([])).toBe(true);
  });

  it("returns true when today is included", () => {
    const today = new Date().getDay();
    expect(isPrayerToday([today])).toBe(true);
  });

  it("returns false when today is not included", () => {
    const today = new Date().getDay();
    const other = (today + 1) % 7;
    vi.spyOn(Date.prototype, "getDay").mockReturnValue(other);
    expect(isPrayerToday([today])).toBe(false);
  });
});
