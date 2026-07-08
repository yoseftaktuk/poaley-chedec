import { http, HttpResponse } from "msw";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { GalleryPage } from "@/pages/GalleryPage";
import { server } from "@/test/mocks/server";
import { renderWithProviders } from "@/test/utils";

describe("GalleryPage error state", () => {
  it("shows error message on fetch failure", async () => {
    server.use(
      http.get("http://localhost:8000/api/v1/gallery/albums", () =>
        HttpResponse.json({ detail: "error" }, { status: 500 }),
      ),
    );
    renderWithProviders(<GalleryPage />);
    await waitFor(() => {
      expect(screen.getByText(/שגיאה בטעינת הגלריה/)).toBeInTheDocument();
    });
  });
});
