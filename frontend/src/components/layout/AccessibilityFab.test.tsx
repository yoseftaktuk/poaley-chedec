import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AccessibilityFab } from "@/components/layout/AccessibilityFab";
import { AccessibilityProvider } from "@/hooks/useAccessibility";
import { renderWithProviders } from "@/test/utils";

describe("AccessibilityFab", () => {
  it("renders the accessibility icon inside the FAB button", () => {
    renderWithProviders(
      <AccessibilityProvider>
        <AccessibilityFab />
      </AccessibilityProvider>,
    );

    const button = screen.getByRole("button", { name: "הגדרות נגישות" });
    expect(button).toBeInTheDocument();
    expect(button.querySelector("svg")).toBeInTheDocument();
    expect(button.className).toContain("p-0");
  });
});
