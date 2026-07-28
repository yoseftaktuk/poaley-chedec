import { http, HttpResponse } from "msw";
import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Footer } from "@/components/layout/Footer";
import { DONATE_EXTERNAL_URL } from "@/lib/constants";
import { mockPublicSettings } from "@/test/mocks/handlers";
import { server } from "@/test/mocks/server";
import { renderWithProviders } from "@/test/utils";

const API_BASE = "http://localhost:8000/api/v1";

describe("Footer", () => {
  it("renders navigation links", async () => {
    renderWithProviders(<Footer />);
    await waitFor(() => {
      expect(screen.getByText("ניווט מהיר")).toBeInTheDocument();
    });
    expect(screen.getByRole("link", { name: "אודות" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "דף הבית" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "תרומה" })).toHaveAttribute("href", DONATE_EXTERNAL_URL);
    expect(screen.getByRole("link", { name: "תרומה" })).toHaveAttribute("target", "_blank");
  });

  it("omits Waze link when address is missing", async () => {
    server.use(
      http.get(`${API_BASE}/settings/public`, () =>
        HttpResponse.json({
          ...mockPublicSettings,
          contact: { ...mockPublicSettings.contact, address: "" },
        }),
      ),
    );

    renderWithProviders(<Footer />);
    await waitFor(() => {
      expect(screen.getByText("ניווט מהיר")).toBeInTheDocument();
    });

    expect(screen.queryByLabelText("ניווט לבית הכנסת ב-Waze")).not.toBeInTheDocument();
  });
});
