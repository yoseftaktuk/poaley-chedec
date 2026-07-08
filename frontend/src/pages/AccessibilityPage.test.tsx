import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AccessibilityPage } from "@/pages/AccessibilityPage";
import { renderWithProviders } from "@/test/utils";

describe("AccessibilityPage", () => {
  it("renders accessibility statement", async () => {
    renderWithProviders(<AccessibilityPage />);
    await waitFor(() => {
      expect(screen.getByText("תוכן נגישות")).toBeInTheDocument();
    });
    expect(screen.getByRole("heading", { name: "הצהרת נגישות" })).toBeInTheDocument();
  });
});
