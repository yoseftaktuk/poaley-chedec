import { Button } from "@/components/ui/button";

interface FormActionsProps {
  isEditing: boolean;
  createLabel: string;
  isPending?: boolean;
  onCancel: () => void;
}

export function FormActions({ isEditing, createLabel, isPending, onCancel }: FormActionsProps) {
  return (
    <div className="flex gap-2">
      <Button type="submit" disabled={isPending}>
        {isPending ? "שומר..." : isEditing ? "שמור" : createLabel}
      </Button>
      {isEditing && (
        <Button type="button" variant="outline" onClick={onCancel}>
          ביטול
        </Button>
      )}
    </div>
  );
}
