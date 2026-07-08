import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AboutPage } from "@/pages/AboutPage";
import { renderWithProviders } from "@/test/utils";

describe("AboutPage", () => {
  it("renders hero title", () => {
    renderWithProviders(<AboutPage />);
    expect(screen.getByRole("heading", { level: 1, name: /אודות בית הכנסת/ })).toBeInTheDocument();
  });

  it("renders timeline sections", () => {
    renderWithProviders(<AboutPage />);
    expect(screen.getByText("הקמה בשנת 1950")).toBeInTheDocument();
    expect(screen.getByText("רוח החסידות")).toBeInTheDocument();
  });

  it("renders stats section", () => {
    renderWithProviders(<AboutPage />);
    expect(screen.getByText("במספרים")).toBeInTheDocument();
    expect(screen.getByText("שנות קיום")).toBeInTheDocument();
    expect(screen.getByText("עשרות")).toBeInTheDocument();
  });

  it("renders CTA with contact link", () => {
    renderWithProviders(<AboutPage />);
    expect(screen.getByRole("link", { name: "צור קשר" })).toHaveAttribute("href", "/contact");
  });
});
