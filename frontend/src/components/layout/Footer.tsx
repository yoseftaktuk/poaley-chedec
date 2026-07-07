import { Link } from "react-router-dom";
import { Clock, Mail, MapPin, MessageCircle, Phone } from "lucide-react";

import { Button } from "@/components/ui/button";
import { NAV_ITEMS, ROUTES } from "@/lib/constants";
import { usePublicSettings } from "@/hooks/usePublicData";
import { useWhatsAppUrl } from "@/hooks/useWhatsAppUrl";

const PRIVACY_STATEMENT =
  "אנו מכבדים את פרטיותכם. המידע שנאסף באתר משמש למטרות תפעול בית הכנסת בלבד ולא יועבר לצדדים שלישיים ללא הסכמתכם.";

export function Footer() {
  const { data: settings } = usePublicSettings();
  const contact = settings?.contact;
  const site = settings?.site;
  const whatsappUrl = useWhatsAppUrl(contact?.whatsapp);

  return (
    <footer className="mt-auto bg-[var(--color-navy)] text-white">
      <div className="mx-auto max-w-6xl px-4 py-16">
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
          <div>
            <h2 className="mb-4 font-display text-xl font-bold">בית כנסת פועלי צדק</h2>
            <p className="text-[length:var(--text-small)] leading-relaxed text-white/75">
              {site?.site_description || "בית כנסת ומקווה באשקלון"}
            </p>
          </div>

          <div>
            <h3 className="mb-4 text-[length:var(--text-body)] font-semibold">ניווט מהיר</h3>
            <ul className="space-y-2.5">
              {NAV_ITEMS.map((item) => (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className="text-[length:var(--text-small)] text-white/75 no-underline transition-colors hover:text-[var(--color-gold)]"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
              <li>
                <a
                  href="/#prayer-times"
                  className="inline-flex items-center gap-1.5 text-[length:var(--text-small)] text-white/75 no-underline transition-colors hover:text-[var(--color-gold)]"
                >
                  <Clock size={14} aria-hidden="true" />
                  זמני תפילות
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-4 text-[length:var(--text-body)] font-semibold">יצירת קשר</h3>
            <div className="space-y-3 text-[length:var(--text-small)] text-white/75">
              {contact?.address && (
                <p className="flex items-start gap-2">
                  <MapPin size={16} className="mt-0.5 shrink-0" aria-hidden="true" />
                  {contact.address}
                </p>
              )}
              {contact?.phone && (
                <p>
                  <a href={`tel:${contact.phone}`} className="inline-flex items-center gap-2 text-white/75 no-underline hover:text-[var(--color-gold)]">
                    <Phone size={16} aria-hidden="true" />
                    {contact.phone}
                  </a>
                </p>
              )}
              {contact?.email && (
                <p>
                  <a href={`mailto:${contact.email}`} className="inline-flex items-center gap-2 text-white/75 no-underline hover:text-[var(--color-gold)]">
                    <Mail size={16} aria-hidden="true" />
                    {contact.email}
                  </a>
                </p>
              )}
            </div>
          </div>

          <div className="flex flex-col items-start gap-4">
            <h3 className="text-[length:var(--text-body)] font-semibold">הישארו בקשר</h3>
            <Button asChild variant="success">
              <a href={whatsappUrl} target="_blank" rel="noopener noreferrer">
                <MessageCircle size={18} aria-hidden="true" />
                WhatsApp
              </a>
            </Button>
          </div>
        </div>
      </div>

      <div className="border-t border-white/15">
        <div className="mx-auto max-w-6xl space-y-3 px-4 py-6 text-center">
          <p className="text-[length:var(--text-small)] leading-relaxed text-white/60">{PRIVACY_STATEMENT}</p>
          <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-[length:var(--text-small)] text-white/60">
            <span>© {new Date().getFullYear()} בית כנסת פועלי צדק</span>
            <span aria-hidden="true">|</span>
            <Link to={ROUTES.accessibility} className="text-white/60 no-underline hover:text-[var(--color-gold)]">
              הצהרת נגישות
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
