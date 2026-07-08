import { lazy, Suspense } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { SeoHead } from "@/components/SeoHead";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { ROUTES } from "@/lib/constants";

const HomePage = lazy(() => import("@/pages/HomePage").then((m) => ({ default: m.HomePage })));
const GalleryPage = lazy(() => import("@/pages/GalleryPage").then((m) => ({ default: m.GalleryPage })));
const GalleryAlbumPage = lazy(() => import("@/pages/GalleryAlbumPage").then((m) => ({ default: m.GalleryAlbumPage })));
const MikvehPage = lazy(() => import("@/pages/MikvehPage").then((m) => ({ default: m.MikvehPage })));
const ContactPage = lazy(() => import("@/pages/ContactPage").then((m) => ({ default: m.ContactPage })));
const AccessibilityPage = lazy(() => import("@/pages/AccessibilityPage").then((m) => ({ default: m.AccessibilityPage })));
const AboutPage = lazy(() => import("@/pages/AboutPage").then((m) => ({ default: m.AboutPage })));
const AdminLoginPage = lazy(() => import("@/pages/admin/AdminLoginPage").then((m) => ({ default: m.AdminLoginPage })));
const AdminLayout = lazy(() => import("@/pages/admin/AdminLayout").then((m) => ({ default: m.AdminLayout })));
const AdminDashboardPage = lazy(() => import("@/pages/admin/AdminLayout").then((m) => ({ default: m.AdminDashboardPage })));
const AdminAuditPage = lazy(() => import("@/pages/admin/AdminLayout").then((m) => ({ default: m.AdminAuditPage })));
const AdminPrayerTimesPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminPrayerTimesPage })));
const AdminTorahLessonsPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminTorahLessonsPage })));
const AdminEventsPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminEventsPage })));
const AdminGalleryPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminGalleryPage })));
const AdminMikvehPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminMikvehPage })));
const AdminBannersPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminBannersPage })));
const AdminSettingsPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminSettingsPage })));
const AdminMessagesPage = lazy(() => import("@/pages/admin/AdminCrudPages").then((m) => ({ default: m.AdminMessagesPage })));

function PageLoader() {
  return <div className="container-page">טוען...</div>;
}

function PublicPage({
  pageKey,
  path,
  children,
}: {
  pageKey: string;
  path?: string;
  children: React.ReactNode;
}) {
  return (
    <>
      <SeoHead pageKey={pageKey} meta={path ? { path } : undefined} />
      {children}
    </>
  );
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route element={<PublicLayout />}>
            <Route index element={<PublicPage pageKey="home"><HomePage /></PublicPage>} />
            <Route path={ROUTES.about} element={<PublicPage pageKey="about" path="/about"><AboutPage /></PublicPage>} />
            <Route path={ROUTES.gallery} element={<PublicPage pageKey="gallery"><GalleryPage /></PublicPage>} />
            <Route path={`${ROUTES.gallery}/:albumId`} element={<PublicPage pageKey="gallery"><GalleryAlbumPage /></PublicPage>} />
            <Route path={ROUTES.mikveh} element={<PublicPage pageKey="mikveh"><MikvehPage /></PublicPage>} />
            <Route path={ROUTES.contact} element={<PublicPage pageKey="contact"><ContactPage /></PublicPage>} />
            <Route path={ROUTES.accessibility} element={<PublicPage pageKey="accessibility"><AccessibilityPage /></PublicPage>} />
          </Route>

          <Route path={ROUTES.adminLogin} element={<AdminLoginPage />} />
          <Route path={ROUTES.admin} element={<AdminLayout />}>
            <Route index element={<AdminDashboardPage />} />
            <Route path="prayer-times" element={<AdminPrayerTimesPage />} />
            <Route path="torah-lessons" element={<AdminTorahLessonsPage />} />
            <Route path="events" element={<AdminEventsPage />} />
            <Route path="gallery" element={<AdminGalleryPage />} />
            <Route path="mikveh" element={<AdminMikvehPage />} />
            <Route path="banners" element={<AdminBannersPage />} />
            <Route path="settings" element={<AdminSettingsPage />} />
            <Route path="messages" element={<AdminMessagesPage />} />
            <Route path="audit" element={<AdminAuditPage />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
