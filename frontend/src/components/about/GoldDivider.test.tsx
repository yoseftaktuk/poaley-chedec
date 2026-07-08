import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { GoldDivider } from "@/components/about/GoldDivider";

describe("GoldDivider", () => {
  it("renders decorative divider", () => {
    const { container } = render(<GoldDivider />);
    expect(container.querySelector(".about-divider")).toBeInTheDocument();
  });

  it("applies centered class when centered", () => {
    const { container } = render(<GoldDivider centered />);
    expect(container.querySelector(".about-divider--center")).toBeInTheDocument();
  });
});
