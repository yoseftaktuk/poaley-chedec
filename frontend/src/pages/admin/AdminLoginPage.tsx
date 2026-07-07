import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Navigate, useNavigate } from "react-router-dom";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Input, Label } from "@/components/ui/input";
import { useLoginMutation } from "@/hooks/useAuth";

const loginSchema = z.object({
  username: z.string().min(1, "שם משתמש חובה"),
  password: z.string().min(1, "סיסמה חובה"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function AdminLoginPage() {
  const mutation = useLoginMutation();
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  if (token) {
    return <Navigate to="/admin" replace />;
  }

  const onSubmit = (data: LoginFormValues) => {
    mutation.mutate(data, {
      onSuccess: () => navigate("/admin", { replace: true }),
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--color-muted)] p-4">
      <form onSubmit={handleSubmit(onSubmit)} className="card w-full max-w-md space-y-4">
        <h1 className="text-center text-2xl font-bold">כניסת מנהלים</h1>
        <div>
          <Label htmlFor="username">שם משתמש</Label>
          <Input id="username" {...register("username")} autoComplete="username" />
          {errors.username && <p className="text-sm text-red-600">{errors.username.message}</p>}
        </div>
        <div>
          <Label htmlFor="password">סיסמה</Label>
          <Input id="password" type="password" {...register("password")} autoComplete="current-password" />
          {errors.password && <p className="text-sm text-red-600">{errors.password.message}</p>}
        </div>
        <Button type="submit" className="w-full" disabled={mutation.isPending}>
          {mutation.isPending ? "מתחבר..." : "התחבר"}
        </Button>
        {mutation.isError && <p className="text-center text-red-600">שם משתמש או סיסמה שגויים</p>}
      </form>
    </div>
  );
}
