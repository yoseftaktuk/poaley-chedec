import { Heart, MessageCircle } from "lucide-react";

import { Button } from "@/components/ui/button";

interface HeroSectionProps {
  title: string;
  text: string;
  donationUrl: string;
  donationText: string;
  whatsappUrl: string;
}

export function HeroSection({
  title,
  text,
  donationUrl,
  donationText,
  whatsappUrl,
}: HeroSectionProps) {
  return (
    <section className="hero" aria-label="ברוכים הבאים">
      <div className="hero__image" aria-hidden="true">
        <img
          src="/images/hero-synagogue.png"
          alt=""
          fetchPriority="high"
          decoding="async"
        />
      </div>
      <div className="hero__overlay" aria-hidden="true" />
      <div className="hero__content">
        <h1>{title}</h1>
        <p>{text}</p>
        <div className="hero__actions">
          <Button asChild size="xl">
            <a href={donationUrl} target="_blank" rel="noopener noreferrer">
              <Heart size={22} aria-hidden="true" />
              {donationText}
            </a>
          </Button>
          <Button asChild variant="success" size="xl">
            <a href={whatsappUrl} target="_blank" rel="noopener noreferrer">
              <MessageCircle size={22} aria-hidden="true" />
              WhatsApp
            </a>
          </Button>
        </div>
      </div>
    </section>
  );
}
