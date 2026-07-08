import { describe, expect, it } from "vitest";

import { buildWazeUrl } from "@/lib/buildWazeUrl";

describe("buildWazeUrl", () => {
  it("encodes address in query", () => {
    const url = buildWazeUrl("אפרים 52, אשקלון");
    expect(url).toContain("waze.com/ul");
    expect(url).toContain(encodeURIComponent("אפרים 52, אשקלון"));
    expect(url).toContain("navigate=yes");
  });
});
