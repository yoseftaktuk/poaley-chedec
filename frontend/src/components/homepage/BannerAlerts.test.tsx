import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { BannerAlerts } from "@/components/homepage/BannerAlerts";

describe("BannerAlerts", () => {
  it("renders nothing when empty", () => {
    const { container } = render(<BannerAlerts banners={[]} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("renders banner messages", () => {
    render(
      <BannerAlerts
        banners={[
          {
            id: "1",
            message: "הודעה חשובה",
            is_active: true,
            priority: 1,
            days_of_week: [],
            starts_at: null,
            ends_at: null,
          },
        ]}
      />,
    );
    expect(screen.getByText("הודעה חשובה")).toBeInTheDocument();
  });
});
