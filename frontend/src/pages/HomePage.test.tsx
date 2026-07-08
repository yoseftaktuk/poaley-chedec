import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { HomePage } from "@/pages/HomePage";
import { renderWithProviders } from "@/test/utils";

describe("HomePage", () => {
  it("renders homepage sections after loading", async () => {
    renderWithProviders(<HomePage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { level: 1, name: "ברוכים הבאים" })).toBeInTheDocument();
    });
    expect(screen.getByText(/דברי הרב/)).toBeInTheDocument();
  });
});
