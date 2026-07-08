import { http, HttpResponse } from "msw";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { GalleryPage } from "@/pages/GalleryPage";
import { server } from "@/test/mocks/server";
import { renderWithProviders } from "@/test/utils";

describe("GalleryPage with albums", () => {
  it("renders album list", async () => {
    server.use(
      http.get("http://localhost:8000/api/v1/gallery/albums", () =>
        HttpResponse.json([
          {
            id: "album-1",
            title: "אלבום שבת",
            description: "תמונות",
            cover_image_url: null,
            sort_order: 0,
            is_published: true,
          },
        ]),
      ),
    );
    renderWithProviders(<GalleryPage />);
    await waitFor(() => {
      expect(screen.getByText("אלבום שבת")).toBeInTheDocument();
    });
  });
});
