import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SocialLinks } from "@/components/ui/SocialLinks";

describe("SocialLinks", () => {
  it("renders whatsapp, phone, and email links", () => {
    render(
      <SocialLinks
        whatsappUrl="https://wa.me/123"
        phone="0544329218"
        email="test@example.com"
        theme="light"
      />,
    );
    expect(screen.getByRole("link", { name: "WhatsApp" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "טלפון" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "אימייל" })).toBeInTheDocument();
  });

  it("hides links when values are missing", () => {
    render(<SocialLinks whatsappUrl="#" phone="" email="" theme="dark" />);
    expect(screen.queryByRole("link", { name: "WhatsApp" })).not.toBeInTheDocument();
  });
});
