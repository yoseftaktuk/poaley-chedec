import { Heart } from "lucide-react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Badge } from "@/components/ui/Badge";

describe("Badge", () => {
  it("renders label", () => {
    render(<Badge>תגית</Badge>);
    expect(screen.getByText("תגית")).toBeInTheDocument();
  });

  it("renders with icon", () => {
    render(<Badge icon={Heart}>אהבה</Badge>);
    expect(screen.getByText("אהבה")).toBeInTheDocument();
  });

  it("renders cream variant", () => {
    render(<Badge variant="cream">קרם</Badge>);
    expect(screen.getByText("קרם")).toBeInTheDocument();
  });
});
