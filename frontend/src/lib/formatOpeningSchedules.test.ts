import { describe, expect, it } from "vitest";

import { formatOpeningSchedules } from "@/lib/formatOpeningSchedules";

describe("formatOpeningSchedules", () => {
  it("formats schedules with days and hours", () => {
    const result = formatOpeningSchedules([
      { days_of_week: [0, 1], hours: "08:00-12:00" },
    ]);
    expect(result).toEqual(["ימים: ראשון-שני — 08:00-12:00"]);
  });

  it("returns empty array for no schedules", () => {
    expect(formatOpeningSchedules([])).toEqual([]);
  });
});
