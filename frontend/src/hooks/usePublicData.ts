import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";
import type { GalleryAlbum, GalleryImage, HomepageData, Mikveh, PublicSettings } from "@/types";

export function useHomepage() {
  return useQuery({
    queryKey: ["homepage"],
    queryFn: () => apiFetch<HomepageData>("/homepage"),
    staleTime: 5 * 60 * 1000,
  });
}

export function usePublicSettings() {
  return useQuery({
    queryKey: ["public-settings"],
    queryFn: () => apiFetch<PublicSettings>("/settings/public"),
    staleTime: 10 * 60 * 1000,
  });
}

export function useGalleryAlbums() {
  return useQuery({
    queryKey: ["gallery-albums"],
    queryFn: () => apiFetch<GalleryAlbum[]>("/gallery/albums"),
    staleTime: 5 * 60 * 1000,
  });
}

export function useGalleryImages(albumId: string | undefined) {
  return useQuery({
    queryKey: ["gallery-images", albumId],
    queryFn: () => apiFetch<GalleryImage[]>(`/gallery/albums/${albumId}/images`),
    enabled: Boolean(albumId),
    staleTime: 5 * 60 * 1000,
  });
}

export function useMikveh() {
  return useQuery({
    queryKey: ["mikveh"],
    queryFn: () => apiFetch<Mikveh>("/mikveh"),
    staleTime: 10 * 60 * 1000,
  });
}
