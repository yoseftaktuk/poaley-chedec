import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { Button } from "@/components/ui/button";

describe("Button", () => {
  it("renders children", () => {
    render(<Button>לחץ כאן</Button>);
    expect(screen.getByRole("button", { name: "לחץ כאן" })).toBeInTheDocument();
  });

  it("calls onClick when clicked", async () => {
    const user = userEvent.setup();
    const onClick = vi.fn();
    render(<Button onClick={onClick}>לחץ</Button>);
    await user.click(screen.getByRole("button"));
    expect(onClick).toHaveBeenCalledOnce();
  });

  it("is disabled when disabled prop is set", () => {
    render(<Button disabled>מושבת</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("renders outline variant", () => {
    render(<Button variant="outline">מתאר</Button>);
    expect(screen.getByRole("button")).toBeInTheDocument();
  });
});
