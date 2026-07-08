import { Clock, Moon, Sun } from "lucide-react";
import { describe, expect, it } from "vitest";

import { getPrayerIcon } from "@/lib/prayerIcons";

describe("getPrayerIcon", () => {
  it("returns Sun for shacharit", () => {
    expect(getPrayerIcon("שחרית")).toBe(Sun);
  });

  it("returns Moon for arvit", () => {
    expect(getPrayerIcon("ערבית")).toBe(Moon);
  });

  it("returns Clock for unknown prayer", () => {
    expect(getPrayerIcon("קידוש לבנה")).toBe(Clock);
  });
});
