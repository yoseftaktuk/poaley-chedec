import type { BannerMessage, Event, PrayerTime, TorahLesson } from "@/types";

export interface BannerAlertsProps {
  banners: BannerMessage[];
}

export interface RabbiMessageSectionProps {
  rabbiName: string;
  message: string;
}

export interface PrayerTimesSectionProps {
  prayerTimes: PrayerTime[];
}

export interface LessonsSectionProps {
  lessons: TorahLesson[];
  contactPath: string;
}

export interface EventsSectionProps {
  events: Event[];
  contactPath: string;
}

export interface DonationsSectionProps {
  donationUrl: string;
  donationText: string;
  contactPath: string;
}

export interface ContactSectionProps {
  contact: Record<string, string>;
  whatsappUrl: string;
}
