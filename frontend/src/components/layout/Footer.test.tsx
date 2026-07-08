import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Footer } from "@/components/layout/Footer";
import { renderWithProviders } from "@/test/utils";

describe("Footer", () => {
  it("renders navigation links", async () => {
    renderWithProviders(<Footer />);
    await waitFor(() => {
      expect(screen.getByText("ניווט מהיר")).toBeInTheDocument();
    });
    expect(screen.getByRole("link", { name: "אודות" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "דף הבית" })).toBeInTheDocument();
  });
});
