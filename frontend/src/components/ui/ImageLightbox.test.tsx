import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ImageLightbox } from "@/components/ui/ImageLightbox";

describe("ImageLightbox", () => {
  it("renders image when open", () => {
    render(
      <ImageLightbox open src="/test.jpg" alt="תמונת בדיקה" onOpenChange={vi.fn()} />,
    );
    expect(screen.getByRole("img", { name: "תמונת בדיקה" })).toBeInTheDocument();
  });

  it("calls onOpenChange when close clicked", async () => {
    const user = userEvent.setup();
    const onOpenChange = vi.fn();
    render(
      <ImageLightbox open src="/test.jpg" alt="תמונה" onOpenChange={onOpenChange} />,
    );
    await user.click(screen.getByRole("button", { name: "סגור" }));
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });
});
