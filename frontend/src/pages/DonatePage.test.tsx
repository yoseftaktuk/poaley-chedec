import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DonatePage } from "@/pages/DonatePage";
import { renderWithProviders } from "@/test/utils";

describe("DonatePage", () => {
  it("renders title and body", async () => {
    renderWithProviders(<DonatePage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "תרומה" })).toBeInTheDocument();
    });
    expect(screen.getByRole("heading", { name: "למה לתרום?" })).toBeInTheDocument();
    expect(screen.getByText(/תרומתכם מאפשרת לנו/)).toBeInTheDocument();
  });

  it("links to the donation URL and contact page", async () => {
    renderWithProviders(<DonatePage />);
    await waitFor(() => {
      expect(screen.getByRole("link", { name: /תרומה/ })).toBeInTheDocument();
    });

    const donateLink = screen.getByRole("link", { name: /תרומה/ });
    expect(donateLink).toHaveAttribute("href", "https://example.com/donate");
    expect(donateLink).toHaveAttribute("target", "_blank");
    expect(donateLink).toHaveAttribute("rel", "noopener noreferrer");

    expect(screen.getByRole("link", { name: "צור קשר" })).toHaveAttribute("href", "/contact");
  });
});
