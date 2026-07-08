import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { ContactPage } from "@/pages/ContactPage";
import { renderWithProviders } from "@/test/utils";

describe("ContactPage", () => {
  it("renders contact form", async () => {
    renderWithProviders(<ContactPage />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "צור קשר" })).toBeInTheDocument();
    });
    expect(screen.getByLabelText("שם")).toBeInTheDocument();
    expect(screen.getByLabelText("אימייל")).toBeInTheDocument();
  });

  it("shows validation errors for empty submit", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ContactPage />);
    await waitFor(() => screen.getByRole("button", { name: "שלח הודעה" }));
    await user.click(screen.getByRole("button", { name: "שלח הודעה" }));
    await waitFor(() => {
      expect(screen.getByText(/שם חייב/)).toBeInTheDocument();
    });
  });

  it("submits valid form", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ContactPage />);
    await waitFor(() => screen.getByLabelText("שם"));

    await user.type(screen.getByLabelText("שם"), "ישראל ישראלי");
    await user.type(screen.getByLabelText("טלפון"), "0501234567");
    await user.type(screen.getByLabelText("אימייל"), "test@example.com");
    await user.type(screen.getByLabelText("הודעה"), "הודעת בדיקה ארוכה");
    await user.click(screen.getByRole("button", { name: "שלח הודעה" }));

    await waitFor(() => {
      expect(screen.getByText(/נשלחה בהצלחה/)).toBeInTheDocument();
    });
  });
});
