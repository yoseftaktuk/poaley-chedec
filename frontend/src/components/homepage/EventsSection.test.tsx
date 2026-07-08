import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { EventsSection } from "@/components/homepage/EventsSection";
import { renderWithProviders } from "@/test/utils";

describe("EventsSection", () => {
  it("renders events", () => {
    renderWithProviders(
      <EventsSection
        events={[
          {
            id: "1",
            title: "אירוע קהילתי",
            description: "תיאור",
            event_date: "2099-06-15",
            event_time: "18:00",
            image_url: null,
            show_on_homepage: true,
            created_at: "2026-01-01T00:00:00Z",
          },
        ]}
        contactPath="/contact"
      />,
    );
    expect(screen.getByText("אירוע קהילתי")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /פרטים נוספים/ })).toBeInTheDocument();
  });

  it("renders event with image", () => {
    renderWithProviders(
      <EventsSection
        events={[
          {
            id: "2",
            title: "אירוע עם תמונה",
            description: "תיאור",
            event_date: "2099-07-01",
            event_time: "19:00",
            image_url: "/event.jpg",
            show_on_homepage: true,
            created_at: "2026-01-01T00:00:00Z",
          },
        ]}
        contactPath="/contact"
      />,
    );
    expect(screen.getByRole("img", { name: "אירוע עם תמונה" })).toBeInTheDocument();
  });
});
