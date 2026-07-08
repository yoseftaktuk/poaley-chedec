import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { AdminLoginPage } from "@/pages/admin/AdminLoginPage";
import { renderWithProviders } from "@/test/utils";

describe("AdminLoginPage", () => {
  it("renders login form", () => {
    renderWithProviders(<AdminLoginPage />);
    expect(screen.getByLabelText(/שם משתמש/)).toBeInTheDocument();
    expect(screen.getByLabelText(/סיסמה/)).toBeInTheDocument();
  });

  it("shows error on invalid credentials", async () => {
    const user = userEvent.setup();
    renderWithProviders(<AdminLoginPage />);

    await user.type(screen.getByLabelText(/שם משתמש/), "admin");
    await user.type(screen.getByLabelText(/סיסמה/), "wrong");
    await user.click(screen.getByRole("button", { name: /התחבר/ }));

    await waitFor(() => {
      expect(screen.getByText(/שגוי/)).toBeInTheDocument();
    });
  });

  it("logs in with valid credentials", async () => {
    const user = userEvent.setup();
    renderWithProviders(<AdminLoginPage />);

    await user.type(screen.getByLabelText(/שם משתמש/), "admin");
    await user.type(screen.getByLabelText(/סיסמה/), "changeme123");
    await user.click(screen.getByRole("button", { name: /התחבר/ }));

    await waitFor(() => {
      expect(localStorage.getItem("access_token")).toBe("test-token");
    });
  });
});
