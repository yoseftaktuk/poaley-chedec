import { Link, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { useScrollHeader } from "@/hooks/useScrollHeader";
import { NAV_ITEMS } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function Header() {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const scrolled = useScrollHeader();

  return (
    <header
      className={cn(
        "sticky top-0 z-50 h-[75px] border-b border-[var(--color-border)] bg-white transition-shadow duration-300",
        scrolled && "shadow-md",
      )}
    >
      <div className="mx-auto flex h-full max-w-6xl items-center justify-between px-4">
        <Link
          to="/"
          className="font-display text-xl font-bold text-[var(--color-navy)] no-underline md:text-2xl"
        >
          בית כנסת פועלי צדק
        </Link>

        <nav className="hidden items-center gap-8 md:flex" aria-label="ניווט ראשי">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "relative text-[17px] no-underline transition-colors duration-200 hover:text-[var(--color-gold)]",
                  isActive
                    ? "font-semibold text-[var(--color-navy)] after:absolute after:-bottom-1 after:start-0 after:h-0.5 after:w-full after:rounded-full after:bg-[var(--color-gold)]"
                    : "text-[var(--color-text)]",
                )}
                aria-current={isActive ? "page" : undefined}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <Button
          variant="ghost"
          size="sm"
          className="md:hidden"
          aria-label={open ? "סגור תפריט" : "פתח תפריט"}
          aria-expanded={open}
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </Button>
      </div>

      <nav
        className={cn(
          "overflow-hidden border-t border-[var(--color-border)] bg-white transition-all duration-300 md:hidden",
          open ? "max-h-96 opacity-100" : "max-h-0 opacity-0",
        )}
        aria-label="ניווט נייד"
        aria-hidden={!open}
      >
        <ul className="space-y-1 px-4 py-4">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={cn(
                    "block rounded-lg px-3 py-3 text-[17px] no-underline transition-colors",
                    isActive
                      ? "bg-[var(--color-cream)] font-semibold text-[var(--color-navy)]"
                      : "text-[var(--color-text)] hover:bg-[var(--color-cream)]",
                  )}
                  onClick={() => setOpen(false)}
                  aria-current={isActive ? "page" : undefined}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
}
