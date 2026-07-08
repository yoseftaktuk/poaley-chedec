import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { HeroSection } from "@/components/layout/HeroSection";
import { renderWithProviders } from "@/test/utils";

describe("HeroSection", () => {
  it("renders title and action buttons", () => {
    renderWithProviders(
      <HeroSection
        title="ברוכים הבאים"
        text="בית כנסת באשקלון"
        donationUrl="https://donate.example.com"
        donationText="תרומה"
        whatsappUrl="https://wa.me/123"
      />,
    );
    expect(screen.getByRole("heading", { name: "ברוכים הבאים" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /תרומה/ })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /WhatsApp/i })).toBeInTheDocument();
  });
});
