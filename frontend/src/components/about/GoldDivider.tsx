interface GoldDividerProps {
  centered?: boolean;
}

export function GoldDivider({ centered = false }: GoldDividerProps) {
  return <span className={`about-divider${centered ? " about-divider--center" : ""}`} aria-hidden="true" />;
}
