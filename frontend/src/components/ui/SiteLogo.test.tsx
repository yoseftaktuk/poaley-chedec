import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SiteLogo } from "@/components/ui/SiteLogo";
import { SITE_LOGO } from "@/lib/constants";

describe("SiteLogo", () => {
  it("renders img with correct src and alt", () => {
    render(<SiteLogo />);
    const img = screen.getByRole("img", { name: SITE_LOGO.alt });
    expect(img).toHaveAttribute("src", SITE_LOGO.src);
  });

  it("applies size class", () => {
    render(<SiteLogo size="lg" />);
    const img = screen.getByRole("img", { name: SITE_LOGO.alt });
    expect(img).toHaveClass("h-16");
  });
});
