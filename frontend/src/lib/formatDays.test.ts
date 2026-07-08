import { describe, expect, it } from "vitest";

import { formatDaysOfWeek } from "@/lib/formatDays";

describe("formatDaysOfWeek", () => {
  it("returns all week label for empty array", () => {
    expect(formatDaysOfWeek([])).toBe("כל השבוע");
  });

  it("formats single day", () => {
    expect(formatDaysOfWeek([0])).toBe("ראשון");
  });

  it("formats consecutive range", () => {
    expect(formatDaysOfWeek([0, 1, 2])).toBe("ראשון-שלישי");
  });

  it("formats non-consecutive days", () => {
    expect(formatDaysOfWeek([0, 2, 4])).toBe("ראשון, שלישי, חמישי");
  });

  it("deduplicates days", () => {
    expect(formatDaysOfWeek([1, 1, 3])).toBe("שני, רביעי");
  });
});
