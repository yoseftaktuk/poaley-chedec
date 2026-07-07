import { useCallback, useState } from "react";

export function useCrudForm<TForm>(initialValues: TForm) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [form, setForm] = useState<TForm>(initialValues);

  const isEditing = editingId !== null;

  const startEdit = useCallback((id: string, values: TForm) => {
    setEditingId(id);
    setForm(values);
  }, []);

  const cancelEdit = useCallback(() => {
    setEditingId(null);
    setForm(initialValues);
  }, [initialValues]);

  const resetForm = useCallback(() => {
    setEditingId(null);
    setForm(initialValues);
  }, [initialValues]);

  return {
    editingId,
    form,
    setForm,
    isEditing,
    startEdit,
    cancelEdit,
    resetForm,
  };
}
