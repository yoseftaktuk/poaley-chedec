import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Header } from "@/components/layout/Header";
import { ROUTES } from "@/lib/constants";
import { renderWithProviders } from "@/test/utils";

describe("Header", () => {
  it("renders donate as an internal donate-page link", () => {
    renderWithProviders(<Header />);

    const donateLink = screen.getByRole("link", { name: "תרומה" });
    expect(donateLink).toHaveAttribute("href", ROUTES.donate);
    expect(donateLink).not.toHaveAttribute("target");
  });
});
