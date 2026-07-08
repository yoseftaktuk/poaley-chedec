import { Heart } from "lucide-react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { donatePageContent } from "@/content/donatePage";
import { usePublicSettings } from "@/hooks/usePublicData";
import { ROUTES } from "@/lib/constants";

export function DonatePage() {
  const { data: settings, isLoading } = usePublicSettings();
  const { title, whyTitle, body, ctaTitle, buttonFallback, contactLabel } = donatePageContent;

  if (isLoading) return <div className="container-page">טוען...</div>;

  const donationUrl = settings?.donation?.bit_url ?? "";
  const donationText = settings?.donation?.button_text || buttonFallback;

  return (
    <div className="container-page space-y-8">
      <h1 className="section-title">{title}</h1>

      <section className="card space-y-3">
        <h2 className="text-xl font-bold">{whyTitle}</h2>
        <p className="text-[length:var(--text-body)] leading-[var(--leading-body)] text-[var(--color-text)]">
          {body}
        </p>
      </section>

      <section className="card space-y-4">
        <h2 className="text-xl font-bold">{ctaTitle}</h2>
        <div className="flex flex-col gap-[var(--space-3)] sm:flex-row sm:items-center">
          {donationUrl ? (
            <Button asChild size="lg">
              <a href={donationUrl} target="_blank" rel="noopener noreferrer">
                <Heart size={20} aria-hidden="true" />
                {donationText}
              </a>
            </Button>
          ) : null}
          <Button asChild variant="secondary" size="lg">
            <Link to={ROUTES.contact} className="no-underline">
              {contactLabel}
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
