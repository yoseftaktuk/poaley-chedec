import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { GalleryPage } from "@/pages/GalleryPage";
import { renderWithProviders } from "@/test/utils";

describe("GalleryPage", () => {
  it("renders empty gallery", async () => {
    renderWithProviders(<GalleryPage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "גלריה" })).toBeInTheDocument();
    });
  });
});
