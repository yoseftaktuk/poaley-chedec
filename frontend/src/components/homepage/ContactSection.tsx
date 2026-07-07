import { ExternalLink, Mail, MapPin, MessageCircle, Phone } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/Card";
import { Section, SectionHeader } from "@/components/ui/Section";
import { useFadeUpOnScroll } from "@/hooks/useFadeUpOnScroll";
import type { ContactSectionProps } from "@/types/homepage";
import { cn } from "@/lib/utils";

export function ContactSection({ contact, whatsappUrl }: ContactSectionProps) {
  const { ref, visible } = useFadeUpOnScroll();

  return (
    <Section background="surface" id="contact">
      <div ref={ref} className={cn(visible && "animate-fade-up")}>
        <SectionHeader icon={MapPin} title="מיקום" />
        <Card hoverable={false}>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-4">
              {contact.address && (
                <p className="flex items-start gap-3 text-[length:var(--text-body)] leading-relaxed text-[var(--color-text)]">
                  <MapPin size={20} className="mt-0.5 shrink-0 text-[var(--color-gold)]" aria-hidden="true" />
                  {contact.address}
                </p>
              )}
              {contact.phone && (
                <p>
                  <a
                    href={`tel:${contact.phone}`}
                    className="inline-flex items-center gap-3 text-[length:var(--text-body)] no-underline hover:underline"
                  >
                    <Phone size={20} className="shrink-0 text-[var(--color-gold)]" aria-hidden="true" />
                    {contact.phone}
                  </a>
                </p>
              )}
              {contact.email && (
                <p>
                  <a
                    href={`mailto:${contact.email}`}
                    className="inline-flex items-center gap-3 text-[length:var(--text-body)] no-underline hover:underline"
                  >
                    <Mail size={20} className="shrink-0 text-[var(--color-gold)]" aria-hidden="true" />
                    {contact.email}
                  </a>
                </p>
              )}
            </div>
            <div className="flex flex-col items-start gap-4">
              <Button asChild variant="success">
                <a href={whatsappUrl} target="_blank" rel="noopener noreferrer">
                  <MessageCircle size={18} aria-hidden="true" />
                  WhatsApp
                </a>
              </Button>
              {contact.maps_url && (
                <Button asChild variant="outline">
                  <a href={contact.maps_url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink size={18} aria-hidden="true" />
                    פתח במפות Google
                  </a>
                </Button>
              )}
            </div>
          </div>
        </Card>
      </div>
    </Section>
  );
}
