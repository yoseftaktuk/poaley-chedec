export function AboutDecorations() {
  return (
    <div className="about-decorations" aria-hidden="true">
      <svg className="about-decoration about-decoration--scroll" viewBox="0 0 120 80" fill="none">
        <path
          d="M20 10 C20 5 30 5 30 10 L30 70 C30 75 20 75 20 70 Z M90 10 C90 5 100 5 100 10 L100 70 C100 75 90 75 90 70 Z"
          stroke="currentColor"
          strokeWidth="1.5"
        />
        <path d="M30 20 L90 20 M30 35 L90 35 M30 50 L90 50" stroke="currentColor" strokeWidth="0.75" />
        <path d="M10 40 Q60 30 110 40" stroke="currentColor" strokeWidth="1" />
      </svg>

      <svg className="about-decoration about-decoration--menorah" viewBox="0 0 80 60" fill="none">
        <path d="M40 55 L40 25" stroke="currentColor" strokeWidth="1.5" />
        <path d="M40 25 L25 10 M40 25 L40 8 M40 25 L55 10" stroke="currentColor" strokeWidth="1.5" />
        <path d="M30 55 L50 55" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="25" cy="8" r="3" stroke="currentColor" strokeWidth="1" />
        <circle cx="40" cy="5" r="3" stroke="currentColor" strokeWidth="1" />
        <circle cx="55" cy="8" r="3" stroke="currentColor" strokeWidth="1" />
      </svg>

      <svg className="about-decoration about-decoration--arch" viewBox="0 0 100 80" fill="none">
        <path
          d="M10 75 L10 35 Q50 5 90 35 L90 75"
          stroke="currentColor"
          strokeWidth="1.5"
        />
        <path d="M25 75 L25 42 Q50 22 75 42 L75 75" stroke="currentColor" strokeWidth="0.75" />
      </svg>
    </div>
  );
}
