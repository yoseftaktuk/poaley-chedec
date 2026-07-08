import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { MikvehPage } from "@/pages/MikvehPage";
import { renderWithProviders } from "@/test/utils";

describe("MikvehPage", () => {
  it("renders mikveh info", async () => {
    renderWithProviders(<MikvehPage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "מקווה" })).toBeInTheDocument();
    });
    expect(screen.getByRole("heading", { name: "מידע כללי" })).toBeInTheDocument();
    expect(screen.getByText(/אברך/)).toBeInTheDocument();
  });
});
