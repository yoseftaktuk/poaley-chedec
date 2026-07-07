import { DAY_NAMES } from "@/lib/constants";

export function formatDaysOfWeek(days: number[]): string {
  if (!days.length) {
    return "כל השבוע";
  }

  const sorted = [...new Set(days)].sort((a, b) => a - b);
  const groups: number[][] = [];
  let current: number[] = [];

  for (const day of sorted) {
    if (!current.length || day === current[current.length - 1] + 1) {
      current.push(day);
    } else {
      groups.push(current);
      current = [day];
    }
  }
  if (current.length) {
    groups.push(current);
  }

  return groups
    .map((group) => {
      if (group.length === 1) {
        return DAY_NAMES[group[0]];
      }
      return `${DAY_NAMES[group[0]]}-${DAY_NAMES[group[group.length - 1]]}`;
    })
    .join(", ");
}
