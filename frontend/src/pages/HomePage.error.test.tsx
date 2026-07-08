import { http, HttpResponse } from "msw";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { HomePage } from "@/pages/HomePage";
import { server } from "@/test/mocks/server";
import { renderWithProviders } from "@/test/utils";

describe("HomePage error state", () => {
  it("shows error when homepage fetch fails", async () => {
    server.use(
      http.get("http://localhost:8000/api/v1/homepage", () =>
        HttpResponse.json({ detail: "error" }, { status: 500 }),
      ),
    );
    renderWithProviders(<HomePage />);
    await waitFor(() => {
      expect(screen.getByText(/שגיאה בטעינת הדף/)).toBeInTheDocument();
    });
  });
});
