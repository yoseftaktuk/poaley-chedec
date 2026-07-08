import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useHomepage, usePublicSettings } from "@/hooks/usePublicData";
import { createWrapper } from "@/test/utils";

describe("usePublicData", () => {
  it("useHomepage fetches data", async () => {
    const { result } = renderHook(() => useHomepage(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.settings.homepage.welcome_title).toBe("ברוכים הבאים");
  });

  it("usePublicSettings fetches settings", async () => {
    const { result } = renderHook(() => usePublicSettings(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.contact?.phone).toBe("0544329218");
  });
});
