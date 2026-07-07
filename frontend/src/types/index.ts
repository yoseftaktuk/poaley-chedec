export interface PrayerTime {
  id: string;
  prayer_name: string;
  days_of_week: number[];
  prayer_time: string;
  sort_order: number;
}

export interface TorahLesson {
  id: string;
  lesson_name: string;
  rabbi_name: string;
  days_of_week: number[];
  lesson_time: string;
  description: string;
  is_active: boolean;
}

export interface Event {
  id: string;
  title: string;
  description: string;
  event_date: string;
  event_time: string;
  image_url: string | null;
  show_on_homepage: boolean;
  created_at: string;
}

export interface GalleryAlbum {
  id: string;
  title: string;
  description: string;
  cover_image_url: string | null;
  sort_order: number;
  is_published: boolean;
}

export interface GalleryImage {
  id: string;
  album_id: string;
  title: string;
  cloudinary_public_id: string;
  image_url: string;
  sort_order: number;
}

export interface Mikveh {
  id: string;
  general_info: string;
  regulations: string;
  image_url: string | null;
  avrech_price: number;
  regular_price: number;
  opening_schedules: OpeningSchedule[];
}

export interface OpeningSchedule {
  days_of_week: number[];
  hours: string;
}

export interface BannerMessage {
  id: string;
  message: string;
  is_active: boolean;
  starts_at: string | null;
  ends_at: string | null;
  priority: number;
  days_of_week: number[];
}

export interface HomepageData {
  settings: {
    homepage: Record<string, string>;
    contact: Record<string, string>;
    donation: Record<string, string>;
    site: Record<string, string>;
  };
  prayer_times: PrayerTime[];
  torah_lessons: TorahLesson[];
  events: Event[];
  banners: BannerMessage[];
}

export interface PublicSettings {
  contact: Record<string, string>;
  donation: Record<string, string>;
  site: Record<string, string>;
  seo_global: Record<string, string>;
  seo_pages: Record<string, Record<string, string>>;
  accessibility_statement: Record<string, string>;
  homepage: Record<string, string>;
}

export interface ContactFormData {
  name: string;
  phone: string;
  email: string;
  message: string;
}

export interface LoginFormData {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UploadImageResponse {
  url: string;
  public_id: string;
}

export interface AuditLog {
  id: string;
  user_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  changes: Record<string, unknown>;
  created_at: string;
}

export interface ContactMessage {
  id: string;
  name: string;
  phone: string;
  email: string;
  message: string;
  email_sent: boolean;
  created_at: string;
}

export interface AccessibilitySettings {
  fontSize: "normal" | "large" | "xlarge";
  highContrast: boolean;
}

export interface SeoMeta {
  title: string;
  description: string;
  path: string;
}
