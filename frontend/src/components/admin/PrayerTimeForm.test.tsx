import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { PrayerTimeFormFields } from "@/components/admin/PrayerTimeForm";
import { PRAYER_TIME_INITIAL } from "@/lib/prayerTimeForm";

describe("PrayerTimeFormFields", () => {
  it("shows fixed time input by default", () => {
    render(<PrayerTimeFormFields form={PRAYER_TIME_INITIAL} onChange={vi.fn()} />);
    expect(screen.getByLabelText("שעה (HH:MM)")).toBeInTheDocument();
  });

  it("switches to zmanim fields", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();
    render(<PrayerTimeFormFields form={PRAYER_TIME_INITIAL} onChange={onChange} />);

    await user.click(screen.getByLabelText("זמן הלכתי"));

    expect(onChange).toHaveBeenCalledWith(
      expect.objectContaining({
        time_mode: "zmanim",
        zman_ref: "sunset",
      }),
    );
  });

  it("shows definition preview for zmanim mode", () => {
    render(
      <PrayerTimeFormFields
        form={{
          ...PRAYER_TIME_INITIAL,
          time_mode: "zmanim",
          zman_ref: "sunset",
          offset_minutes: 20,
        }}
        onChange={vi.fn()}
      />,
    );

    expect(screen.getByText("שקיעה + 20 דק'")).toBeInTheDocument();
  });
});
