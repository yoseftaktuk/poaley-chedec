import { Link } from "react-router-dom";
import { Clock, MapPin } from "lucide-react";

import { SocialLinks } from "@/components/ui/SocialLinks";
import { SiteLogo } from "@/components/ui/SiteLogo";
import { buildWazeUrl } from "@/lib/buildWazeUrl";
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
      <div className="mx-auto max-w-6xl px-4 py-[var(--space-12)]">
        <div className="grid gap-[var(--space-6)] md:grid-cols-2 lg:grid-cols-4">
          <div className="lg:col-span-1">
            <SiteLogo size="lg" className="mb-[var(--space-4)]" />
            <h2 className="mb-[var(--space-4)] font-display text-2xl font-bold">בית כנסת פועלי צדק</h2>
            <p className="text-[length:var(--text-body)] leading-[var(--leading-loose)] text-white/80">
              {site?.site_description || "בית כנסת ומקווה באשקלון"}
            </p>
          </div>

          <div>
            <h3 className="mb-[var(--space-3)] text-[length:var(--text-small)] font-semibold uppercase tracking-wide text-white/60">
              ניווט מהיר
            </h3>
            <ul className="space-y-[var(--space-2)]">
              {NAV_ITEMS.map((item) => (
                <li key={item.path}>
                  <Link to={item.path} className="text-[length:var(--text-small)] transition-base">
                    {item.label}
                  </Link>
                </li>
              ))}
              <li>
                <a
                  href="/#prayer-times"
                  className="inline-flex items-center gap-[var(--space-2)] text-[length:var(--text-small)] transition-base"
                >
                  <Clock size={16} aria-hidden="true" />
                  זמני תפילות
                </a>
              </li>
              {contact?.address && (
                <li>
                  <a
                    href={buildWazeUrl(contact.address)}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label="ניווט לבית הכנסת ב-Waze"
                    className="inline-flex items-center gap-[var(--space-2)] text-[length:var(--text-small)] transition-base"
                  >
                    <MapPin size={16} className="shrink-0" aria-hidden="true" />
                    {contact.address}
                  </a>
                </li>
              )}
            </ul>
          </div>

          <div>
            <h3 className="mb-[var(--space-3)] text-[length:var(--text-small)] font-semibold uppercase tracking-wide text-white/60">
              יצירת קשר
            </h3>
            <SocialLinks
              whatsappUrl={whatsappUrl}
              phone={contact?.phone}
              email={contact?.email}
              className="mt-[var(--space-4)]"
            />
          </div>

          <div>
            <h3 className="mb-[var(--space-3)] text-[length:var(--text-small)] font-semibold uppercase tracking-wide text-white/60">
              מידע נוסף
            </h3>
            <ul className="space-y-[var(--space-2)]">
              <li>
                <Link to={ROUTES.accessibility} className="text-[length:var(--text-small)] transition-base">
                  הצהרת נגישות
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="mx-auto max-w-6xl space-y-[var(--space-3)] px-4 py-[var(--space-4)] text-center">
          <p className="text-[length:var(--text-small)] leading-[var(--leading-loose)] text-white/60">
            {PRIVACY_STATEMENT}
          </p>
          <div className="flex flex-wrap items-center justify-center gap-x-[var(--space-2)] gap-y-[var(--space-2)] text-[length:var(--text-small)] text-white/60">
            <span>© {new Date().getFullYear()} בית כנסת פועלי צדק</span>
            <span aria-hidden="true">|</span>
            <Link to={ROUTES.accessibility} className="transition-base">
              הצהרת נגישות
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
