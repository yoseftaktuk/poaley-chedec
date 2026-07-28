import { http, HttpResponse } from "msw";
import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DONATE_EXTERNAL_URL } from "@/lib/constants";
import { DonatePage } from "@/pages/DonatePage";
import { mockPublicSettings } from "@/test/mocks/handlers";
import { server } from "@/test/mocks/server";
import { renderWithProviders } from "@/test/utils";

const API_BASE = "http://localhost:8000/api/v1";

describe("DonatePage", () => {
  it("shows loading state", () => {
    server.use(
      http.get(`${API_BASE}/settings/public`, async () => {
        await new Promise((resolve) => setTimeout(resolve, 200));
        return HttpResponse.json(mockPublicSettings);
      }),
    );

    renderWithProviders(<DonatePage />);
    expect(screen.getByText("טוען...")).toBeInTheDocument();
  });

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
    expect(donateLink).toHaveAttribute("href", DONATE_EXTERNAL_URL);
    expect(donateLink).toHaveAttribute("target", "_blank");
    expect(donateLink).toHaveAttribute("rel", "noopener noreferrer");

    expect(screen.getByRole("link", { name: "צור קשר" })).toHaveAttribute("href", "/contact");
  });

  it("uses fallback button label when button_text is empty", async () => {
    server.use(
      http.get(`${API_BASE}/settings/public`, () =>
        HttpResponse.json({
          ...mockPublicSettings,
          donation: { bit_url: "https://example.com/donate", button_text: "" },
        }),
      ),
    );

    renderWithProviders(<DonatePage />);
    await waitFor(() => {
      expect(screen.getByRole("link", { name: "תרומה לבית הכנסת" })).toBeInTheDocument();
    });
  });

  it("still shows donate button when URL is missing from settings", async () => {
    server.use(
      http.get(`${API_BASE}/settings/public`, () =>
        HttpResponse.json({
          ...mockPublicSettings,
          donation: { bit_url: "", button_text: "" },
        }),
      ),
    );

    renderWithProviders(<DonatePage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "תרומה" })).toBeInTheDocument();
    });

    expect(screen.getByRole("link", { name: /תרומה לבית הכנסת/ })).toHaveAttribute("href", DONATE_EXTERNAL_URL);
    expect(screen.getByRole("link", { name: "צור קשר" })).toBeInTheDocument();
  });

  it("handles missing donation settings", async () => {
    const { donation: _donation, ...settingsWithoutDonation } = mockPublicSettings;

    server.use(
      http.get(`${API_BASE}/settings/public`, () => HttpResponse.json(settingsWithoutDonation)),
    );

    renderWithProviders(<DonatePage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "תרומה" })).toBeInTheDocument();
    });

    expect(screen.getByRole("link", { name: /תרומה/ })).toHaveAttribute("href", DONATE_EXTERNAL_URL);
    expect(screen.getByRole("link", { name: "צור קשר" })).toBeInTheDocument();
  });
});
