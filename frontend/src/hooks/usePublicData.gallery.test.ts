import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useGalleryImages } from "@/hooks/usePublicData";
import { createWrapper } from "@/test/utils";

describe("useGalleryImages", () => {
  it("does not fetch when albumId is undefined", () => {
    const { result } = renderHook(() => useGalleryImages(undefined), { wrapper: createWrapper() });
    expect(result.current.fetchStatus).toBe("idle");
  });

  it("fetches images when albumId is provided", async () => {
    const { result } = renderHook(() => useGalleryImages("album-1"), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual([]);
  });
});
