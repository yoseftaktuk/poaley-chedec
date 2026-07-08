import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AboutHero } from "@/components/about/AboutHero";

describe("AboutHero", () => {
  it("renders title and subtitle", () => {
    render(
      <AboutHero
        hero={{
          title: "אודות",
          subtitle: "מורשת וקהילה",
          imageSrc: "/test.png",
          imageAlt: "בית כנסת",
        }}
      />,
    );
    expect(screen.getByRole("heading", { name: "אודות" })).toBeInTheDocument();
    expect(screen.getByText("מורשת וקהילה")).toBeInTheDocument();
  });
});
