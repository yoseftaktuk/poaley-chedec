import { HomeIntroSection } from "@/components/homepage/HomeIntroSection";
import { ContactSection } from "@/components/homepage/ContactSection";
import { DonationsSection } from "@/components/homepage/DonationsSection";
import { EventsSection } from "@/components/homepage/EventsSection";
import { LessonsSection } from "@/components/homepage/LessonsSection";
import { PrayerTimesSection } from "@/components/homepage/PrayerTimesSection";
import { HeroSection } from "@/components/layout/HeroSection";
import { useWhatsAppUrl } from "@/hooks/useWhatsAppUrl";
import { useHomepage } from "@/hooks/usePublicData";
import { ROUTES } from "@/lib/constants";

export function HomePage() {
  const { data, isLoading, error } = useHomepage();
  const whatsappUrl = useWhatsAppUrl(data?.settings.contact?.whatsapp);

  if (isLoading) {
    return <div className="container-page py-24 text-center text-[length:var(--text-body)]">טוען...</div>;
  }

  if (error || !data) {
    return (
      <div className="container-page py-24 text-center text-[length:var(--text-body)] text-[var(--color-danger)]">
        שגיאה בטעינת הדף
      </div>
    );
  }

  const { settings, prayer_times, torah_lessons, events, banners } = data;
  const contact = settings.contact;
  const donation = settings.donation;
  const homepage = settings.homepage;

  return (
    <>
      <HeroSection
        title={homepage.welcome_title}
        text={homepage.welcome_text}
        donationUrl={donation.bit_url}
        donationText={donation.button_text || "תרומה"}
        whatsappUrl={whatsappUrl}
      />

      <HomeIntroSection
        banners={banners}
        rabbiName={homepage.rabbi_name}
        message={homepage.rabbi_message}
      />
      <PrayerTimesSection prayerTimes={prayer_times} />
      <LessonsSection lessons={torah_lessons} contactPath={ROUTES.contact} />
      <EventsSection events={events} contactPath={ROUTES.contact} />
      <DonationsSection
        donationUrl={donation.bit_url}
        donationText={donation.button_text || "תרומה"}
        contactPath={ROUTES.contact}
      />
      <ContactSection contact={contact} whatsappUrl={whatsappUrl} />
    </>
  );
}
