import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ContactSection } from "@/components/homepage/ContactSection";

describe("ContactSection", () => {
  const contact = {
    rabbi_name: "הרב",
    address: "אפרים 52, אשקלון",
    phone: "0544329218",
    whatsapp: "0544329218",
    email: "test@example.com",
    maps_url: "https://maps.google.com",
  };

  it("renders contact details", () => {
    render(<ContactSection contact={contact} whatsappUrl="https://wa.me/123" />);
    expect(screen.getByText("אפרים 52, אשקלון")).toBeInTheDocument();
    expect(screen.getByText("0544329218")).toBeInTheDocument();
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /פתח במפות Google/ })).toBeInTheDocument();
  });

  it("omits optional fields when missing", () => {
    render(
      <ContactSection
        contact={{ ...contact, address: "", maps_url: "" }}
        whatsappUrl="#"
      />,
    );
    expect(screen.queryByText("אפרים 52, אשקלון")).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /פתח במפות Google/ })).not.toBeInTheDocument();
  });
});
