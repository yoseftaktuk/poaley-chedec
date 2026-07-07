export function isPrayerToday(daysOfWeek: number[]): boolean {
  if (!daysOfWeek.length) {
    return true;
  }
  return daysOfWeek.includes(new Date().getDay());
}
