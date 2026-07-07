import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Input, Label, Textarea } from "@/components/ui/input";
import { useContactMutation } from "@/hooks/useAuth";
import { usePublicSettings } from "@/hooks/usePublicData";

const contactSchema = z.object({
  name: z.string().min(2, "שם חייב להכיל לפחות 2 תווים"),
  phone: z.string().min(5, "מספר טלפון לא תקין"),
  email: z.string().email("אימייל לא תקין"),
  message: z.string().min(5, "הודעה חייבת להכיל לפחות 5 תווים"),
});

type ContactFormValues = z.infer<typeof contactSchema>;

export function ContactPage() {
  const { data: settings } = usePublicSettings();
  const contact = settings?.contact;
  const mutation = useContactMutation();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ContactFormValues>({
    resolver: zodResolver(contactSchema),
  });

  const onSubmit = (data: ContactFormValues) => {
    mutation.mutate(data, {
      onSuccess: () => reset(),
    });
  };

  return (
    <div className="container-page">
      <h1 className="section-title">צור קשר</h1>

      <div className="grid gap-8 md:grid-cols-2">
        <div className="card space-y-3">
          <h2 className="text-xl font-bold">פרטי התקשרות</h2>
          <p>רב: {contact?.rabbi_name}</p>
          <p>כתובת: {contact?.address}</p>
          <p>טלפון: <a href={`tel:${contact?.phone}`}>{contact?.phone}</a></p>
          <p>אימייל: <a href={`mailto:${contact?.email}`}>{contact?.email}</a></p>
          {contact?.maps_url && (
            <a href={contact.maps_url} target="_blank" rel="noopener noreferrer">
              פתח במפות Google
            </a>
          )}
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-4" noValidate>
          <div>
            <Label htmlFor="name">שם</Label>
            <Input id="name" {...register("name")} aria-invalid={!!errors.name} />
            {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>}
          </div>
          <div>
            <Label htmlFor="phone">טלפון</Label>
            <Input id="phone" type="tel" {...register("phone")} aria-invalid={!!errors.phone} />
            {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>}
          </div>
          <div>
            <Label htmlFor="email">אימייל</Label>
            <Input id="email" type="email" {...register("email")} aria-invalid={!!errors.email} />
            {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
          </div>
          <div>
            <Label htmlFor="message">הודעה</Label>
            <Textarea id="message" {...register("message")} aria-invalid={!!errors.message} />
            {errors.message && <p className="mt-1 text-sm text-red-600">{errors.message.message}</p>}
          </div>
          <Button type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "שולח..." : "שלח הודעה"}
          </Button>
          {mutation.isSuccess && <p className="text-green-700">ההודעה נשלחה בהצלחה!</p>}
          {mutation.isError && <p className="text-red-600">שגיאה בשליחת ההודעה</p>}
        </form>
      </div>
    </div>
  );
}
