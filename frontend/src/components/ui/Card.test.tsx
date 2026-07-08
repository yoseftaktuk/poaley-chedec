import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Card } from "@/components/ui/Card";

describe("Card", () => {
  it("renders children", () => {
    render(<Card>תוכן הכרטיס</Card>);
    expect(screen.getByText("תוכן הכרטיס")).toBeInTheDocument();
  });

  it("renders without hoverable class when hoverable is false", () => {
    const { container } = render(<Card hoverable={false}>תוכן</Card>);
    expect(container.firstChild).not.toHaveClass("hover:-translate-y-0.5");
  });
});
