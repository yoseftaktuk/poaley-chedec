import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useLoginMutation, useLogout } from "@/hooks/useAuth";
import { createWrapper } from "@/test/utils";

describe("useAuth", () => {
  it("login mutation stores token on success", async () => {
    const { result } = renderHook(() => useLoginMutation(), { wrapper: createWrapper() });

    result.current.mutate({ username: "admin", password: "changeme123" });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(localStorage.getItem("access_token")).toBe("test-token");
  });

  it("login mutation fails with invalid credentials", async () => {
    const { result } = renderHook(() => useLoginMutation(), { wrapper: createWrapper() });

    result.current.mutate({ username: "admin", password: "wrong" });

    await waitFor(() => expect(result.current.isError).toBe(true));
  });

  it("logout clears token", async () => {
    localStorage.setItem("access_token", "test-token");
    const { result } = renderHook(() => useLogout(), { wrapper: createWrapper() });

    result.current.mutate();

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(localStorage.getItem("access_token")).toBeNull();
  });
});
