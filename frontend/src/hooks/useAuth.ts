import { useMutation } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";
import type { ContactFormData, LoginFormData, TokenResponse } from "@/types";

export function useContactMutation() {
  return useMutation({
    mutationFn: (data: ContactFormData) =>
      apiFetch<{ message: string }>("/contact", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  });
}

export function useLoginMutation() {
  return useMutation({
    mutationFn: (data: LoginFormData) =>
      apiFetch<TokenResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: (data) => {
      localStorage.setItem("access_token", data.access_token);
    },
  });
}

export function useLogout() {
  return useMutation({
    mutationFn: () => apiFetch<{ message: string }>("/auth/logout", { method: "POST" }),
    onSuccess: () => {
      localStorage.removeItem("access_token");
    },
  });
}
