export function useWhatsAppUrl(whatsapp?: string): string {
  if (!whatsapp) {
    return "#";
  }
  return `https://wa.me/972${whatsapp.replace(/^0/, "")}`;
}
