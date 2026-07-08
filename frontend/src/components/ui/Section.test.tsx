import { BookOpen } from "lucide-react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Section, SectionHeader } from "@/components/ui/Section";

describe("Section", () => {
  it("renders children", () => {
    render(
      <Section>
        <p>תוכן סקשן</p>
      </Section>,
    );
    expect(screen.getByText("תוכן סקשן")).toBeInTheDocument();
  });

  it("renders section header with h1", () => {
    render(<SectionHeader icon={BookOpen} title="כותרת" as="h1" />);
    expect(screen.getByRole("heading", { level: 1, name: "כותרת" })).toBeInTheDocument();
  });
});
