import { describe, expect, it } from "vitest";

import { DONATE_EXTERNAL_URL, FOOTER_NAV_ITEMS, HEADER_NAV_ITEMS, ROUTES } from "@/lib/constants";

describe("constants", () => {
  it("defines expected routes", () => {
    expect(ROUTES.home).toBe("/");
    expect(ROUTES.about).toBe("/about");
    expect(ROUTES.donate).toBe("/donate");
    expect(ROUTES.contact).toBe("/contact");
  });

  it("includes about and donate in header nav items", () => {
    const labels = HEADER_NAV_ITEMS.map((item) => item.label);
    expect(labels).toContain("אודות");
    expect(labels).toContain("דף הבית");
    expect(labels).toContain("תרומה");
  });

  it("keeps the donate page route in the header while externalizing the footer donate item", () => {
    const headerDonateItem = HEADER_NAV_ITEMS.find((item) => item.label === "תרומה");
    const footerDonateItem = FOOTER_NAV_ITEMS.find((item) => item.label === "תרומה");
    expect(ROUTES.donate).toBe("/donate");
    expect(headerDonateItem).toMatchObject({
      path: ROUTES.donate,
    });
    expect(footerDonateItem).toMatchObject({
      path: DONATE_EXTERNAL_URL,
      external: true,
    });
  });
});
