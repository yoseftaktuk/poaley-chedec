import { describe, expect, it } from "vitest";

import { formatTimeDefinition, getZmanLabel } from "@/lib/zmanimLabels";

describe("zmanimLabels", () => {
  it("returns Hebrew label for zman ref", () => {
    expect(getZmanLabel("sunset")).toBe("שקיעה");
  });

  it("formats definition with positive offset", () => {
    expect(formatTimeDefinition("sunset", 20)).toBe("שקיעה + 20 דק'");
  });

  it("formats definition with negative offset", () => {
    expect(formatTimeDefinition("sunrise", -10)).toBe("זריחה - 10 דק'");
  });

  it("formats definition without offset", () => {
    expect(formatTimeDefinition("tzeit", 0)).toBe("צאת הכוכבים");
  });
});
