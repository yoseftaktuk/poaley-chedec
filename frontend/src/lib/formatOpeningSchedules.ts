import { formatDaysOfWeek } from "@/lib/formatDays";

interface OpeningSchedule {
  days_of_week: number[];
  hours: string;
}

export function formatOpeningSchedules(schedules: OpeningSchedule[]): string[] {
  return schedules.map((schedule) => `ימים: ${formatDaysOfWeek(schedule.days_of_week)} — ${schedule.hours}`);
}
