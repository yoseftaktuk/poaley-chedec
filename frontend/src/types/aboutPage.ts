export type AboutTimelineIcon = "calendar" | "flame" | "users" | "landmark";

export interface AboutHeroContent {
  title: string;
  subtitle: string;
  imageSrc: string;
  imageAlt: string;
}

export interface AboutTimelineItem {
  id: string;
  year?: string;
  title: string;
  body: string;
  icon: AboutTimelineIcon;
}

export interface AboutStatCounter {
  id: string;
  label: string;
  type: "counter";
  value: number;
  suffix?: string;
}

export interface AboutStatText {
  id: string;
  label: string;
  type: "text";
  displayText: string;
}

export type AboutStat = AboutStatCounter | AboutStatText;

export interface AboutVerseContent {
  text: string;
  reference: string;
}

export interface AboutCtaContent {
  title: string;
  message: string;
  buttonLabel: string;
  buttonHref: string;
}

export interface AboutPageContent {
  hero: AboutHeroContent;
  intro: string;
  timelineTitle: string;
  timeline: AboutTimelineItem[];
  statsTitle: string;
  stats: AboutStat[];
  verse: AboutVerseContent;
  cta: AboutCtaContent;
}
