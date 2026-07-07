import { Helmet } from "react-helmet-async";

import { usePublicSettings } from "@/hooks/usePublicData";
import type { SeoMeta } from "@/types";

interface SeoHeadProps {
  pageKey?: keyof SeoMeta | string;
  meta?: Partial<SeoMeta>;
}

export function SeoHead({ pageKey = "home", meta }: SeoHeadProps) {
  const { data: settings } = usePublicSettings();
  const global = settings?.seo_global;
  const pageMeta = settings?.seo_pages?.[pageKey as string];

  const title = meta?.title || pageMeta?.title || global?.title || "בית כנסת פועלי צדק";
  const description =
    meta?.description || pageMeta?.description || global?.description || "בית כנסת פועלי צדק באשקלון";
  const path = meta?.path || "/";
  const siteName = settings?.site?.site_name || "בית כנסת פועלי צדק";
  const baseUrl = settings?.site?.base_url || "https://poaleitzedek.org";
  const canonical = `${baseUrl}${path}`;
  const ogImage = global?.og_image || "";

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Synagogue",
    name: siteName,
    address: {
      "@type": "PostalAddress",
      streetAddress: settings?.contact?.address,
      addressLocality: "אשקלון",
      addressCountry: "IL",
    },
    telephone: settings?.contact?.phone,
    url: baseUrl,
  };

  return (
    <Helmet>
      <html lang="he" dir="rtl" />
      <title>{title}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={canonical} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content="website" />
      <meta property="og:url" content={canonical} />
      <meta property="og:locale" content="he_IL" />
      {ogImage && <meta property="og:image" content={ogImage} />}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
    </Helmet>
  );
}
