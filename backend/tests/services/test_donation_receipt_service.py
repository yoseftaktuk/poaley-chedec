from unittest.mock import AsyncMock, patch

import pytest

from app.services.donation_receipt_service import DonationReceiptService, STATUS_SENT


@pytest.mark.asyncio
async def test_process_delivery_sms_success(db_session):
    from app.models import DonationReceipt

    record = DonationReceipt(
        transaction_id="555",
        donor_name="ישראל",
        donor_phone="0522514139",
        amount="50",
        receipt_url="https://files.ezcount.co.il/front/documents/get/abc",
        status="send_pending",
    )
    db_session.add(record)
    await db_session.commit()
    await db_session.refresh(record)

    service = DonationReceiptService(db_session)
    with patch(
        "app.services.donation_receipt_service.send_sms",
        new_callable=AsyncMock,
        return_value={"responseStatus": "OK", "oks": ["0522514139"]},
    ):
        await service.process_delivery(record.id)

    await db_session.refresh(record)
    assert record.status == STATUS_SENT
    assert record.channel == "sms"


@pytest.mark.asyncio
async def test_process_delivery_falls_back_to_whatsapp(db_session):
    from app.models import DonationReceipt
    from app.services.messaging.sms_client import SmsSendError

    record = DonationReceipt(
        transaction_id="556",
        donor_phone="0522514139",
        receipt_url="https://files.ezcount.co.il/front/documents/get/abc",
        status="send_pending",
    )
    db_session.add(record)
    await db_session.commit()
    await db_session.refresh(record)

    service = DonationReceiptService(db_session)
    with (
        patch(
            "app.services.donation_receipt_service.send_sms",
            new_callable=AsyncMock,
            side_effect=SmsSendError("fail"),
        ),
        patch(
            "app.services.donation_receipt_service.send_whatsapp",
            new_callable=AsyncMock,
            return_value={"idMessage": "wa-1"},
        ),
    ):
        await service.process_delivery(record.id)

    await db_session.refresh(record)
    assert record.status == STATUS_SENT
    assert record.channel == "whatsapp"
