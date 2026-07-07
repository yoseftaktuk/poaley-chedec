import { DAY_NAMES } from "@/lib/constants";

interface DaySelectorProps {
  value: number[];
  onChange: (days: number[]) => void;
  allowEmpty?: boolean;
  label?: string;
}

export function DaySelector({ value, onChange, allowEmpty = false, label = "ימים" }: DaySelectorProps) {
  const toggleDay = (day: number) => {
    if (value.includes(day)) {
      const next = value.filter((d) => d !== day);
      if (!allowEmpty && next.length === 0) {
        return;
      }
      onChange(next);
      return;
    }
    onChange([...value, day].sort((a, b) => a - b));
  };

  return (
    <div>
      <p className="mb-2 text-sm font-medium">{label}</p>
      <div className="flex flex-wrap gap-3">
        {DAY_NAMES.map((name, index) => (
          <label key={name} className="flex items-center gap-1 text-sm">
            <input
              type="checkbox"
              checked={value.includes(index)}
              onChange={() => toggleDay(index)}
            />
            {name}
          </label>
        ))}
      </div>
      {allowEmpty && value.length === 0 && (
        <p className="mt-1 text-xs text-gray-500">לא נבחרו ימים — פעיל בכל ימות השבוע</p>
      )}
    </div>
  );
}
