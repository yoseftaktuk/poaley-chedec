import { Button } from "@/components/ui/button";

export interface CrudColumn<T> {
  key: keyof T;
  label: string;
  render?: (item: T) => React.ReactNode;
}

interface CrudTableProps<T extends { id: string }> {
  items: T[];
  columns: CrudColumn<T>[];
  onEdit: (item: T) => void;
  onDelete: (id: string) => void;
}

export function CrudTable<T extends { id: string }>({
  items,
  columns,
  onEdit,
  onDelete,
}: CrudTableProps<T>) {
  return (
    <table className="w-full border-collapse text-right">
      <thead>
        <tr className="border-b">
          {columns.map((col) => (
            <th key={String(col.key)} className="p-2">
              {col.label}
            </th>
          ))}
          <th className="p-2">פעולות</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id} className="border-b">
            {columns.map((col) => (
              <td key={String(col.key)} className="p-2">
                {col.render ? col.render(item) : String(item[col.key] ?? "")}
              </td>
            ))}
            <td className="p-2">
              <div className="flex gap-2">
                <Button size="sm" variant="outline" onClick={() => onEdit(item)}>
                  ערוך
                </Button>
                <Button size="sm" variant="outline" onClick={() => onDelete(item.id)}>
                  מחק
                </Button>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
