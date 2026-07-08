import { describe, expect, it } from "vitest";

import { NAV_ITEMS, ROUTES } from "@/lib/constants";

describe("constants", () => {
  it("defines expected routes", () => {
    expect(ROUTES.home).toBe("/");
    expect(ROUTES.about).toBe("/about");
    expect(ROUTES.contact).toBe("/contact");
  });

  it("includes about in nav items", () => {
    const labels = NAV_ITEMS.map((item) => item.label);
    expect(labels).toContain("אודות");
    expect(labels).toContain("דף הבית");
  });
});
