import { Outlet } from "react-router-dom";

import { AccessibilityFab } from "@/components/layout/AccessibilityFab";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";

export function PublicLayout() {
  return (
    <div className="site-background flex min-h-screen flex-col">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:p-4">
        דלג לתוכן הראשי
      </a>
      <Header />
      <main id="main-content" className="flex-1">
        <Outlet />
      </main>
      <Footer />
      <AccessibilityFab />
    </div>
  );
}
