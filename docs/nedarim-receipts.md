# קבלות נדרים פלוס

אחרי תרומה מוצלחת בנדרים פלוס, נדרים שולחים עדכון לשרת. השרת מאמת שהעדכון באמת מנדרים, שומר את העסקה בטבלה `donation_receipts`, ומחזיר מזהה מספרי קבוע.

שליחת ה-SMS וה-WhatsApp, וסנכרון העסקאות שלא הגיעו ב-webhook, מחוברים בקוד אבל עדיין לא השלב שצריך להפעיל ב-production.

## מה קורה כשמגיע webhook

השרת ב-production: [https://poaley-chedec-1.onrender.com](https://poaley-chedec-1.onrender.com)

נדרים שולחים `POST` עם `application/json` לכתובת:

`https://poaley-chedec-1.onrender.com/api/v1/webhooks/nedarim/transactions`

הסדר בשרת:

1. בלי `NEDARIM_WEBHOOK_SECRET` הבקשה נדחית (`503`).
2. החתימה נבדקת על **הבתים הגולמיים** של הגוף, לפני פענוח JSON.
3. חתימה חסרה, שגויה, או עם חותמת זמן רחוקה מדי מהשעון של השרת נדחית (`401`).
4. JSON לא תקין, בלי `TransactionId`, עם `Status=Error` (סירוב), או עם `MosadNumber` של מוסד אחר נדחה (`400`).
5. העסקה נשמרת או מתעדכנת לפי `TransactionId`.
6. השרת עונה `200` עם המזהה המספרי של הרשומה.

דוגמת תשובה:

```json
{ "WEBDocID": 17 }
```

נדרים שומרים את המספר הזה על העסקה בשדה `CallBackId`. לכן `WEBDocID` הוא עמודה רצה בטבלה (`web_doc_id`), לא חישוב חד-פעמי. אותה עסקה תמיד מחזירה את אותו מספר.

נדרים לא מנסים שוב אם השרת נכשל. תשובה שאינה `200` מגיעה אליהם כהתראת מייל.

## אימות החתימה

שתי כותרות:

| כותרת | משמעות |
| --- | --- |
| `X-Nedarim-Timestamp` | שניות UTC מאז 1970 |
| `X-Nedarim-Signature` | `v1=` ואחריו HMAC-SHA256 בהקסה |

החתימה מחושבת על המחרוזת `timestamp + "." + גוף הבקשה כמו שהתקבל`, עם הסוד כטקסט UTF-8.

חלון ברירת המחדל הוא 5 דקות (`NEDARIM_HMAC_MAX_SKEW_SECONDS=300`). השוואה של החתימה היא בזמן קבוע. הלוג רושם רק שמזהה העסקה נשמר, בלי טלפון ובלי מייל.

## מה נשמר

שורה אחת לכל `TransactionId`. כפילות מעדכנת את אותה שורה. אם הסטטוס כבר `sent`, השדות לא נדרסים ולא נשלחת הודעה שוב.

| שדה אצלנו | מגיע מנדרים |
| --- | --- |
| `transaction_id` | `TransactionId` |
| `amount`, `currency` | `Amount`, `Currency` (`1` שקל, `2` דולר) |
| `groupe` | `Groupe` |
| `confirmation` | `Confirmation` |
| `transaction_time` | `TransactionTime` |
| `donor_name` | `ClientName` |
| `donor_phone` | `Phone`, אחרי נרמול לנייד ישראלי `05XXXXXXXX` |
| `donor_email` | `Mail` |
| `receipt_created` | `ReceiptCreated` |
| `receipt_doc_num` | `ReceiptDocNum` |
| `receipt_data` | `ReceiptData` כמו שהגיע |
| `receipt_url` | קישור לצפייה, אם אפשר להרכיב אותו בלי קריאה נוספת |

מספר זהות, 4 ספרות אחרונות של הכרטיס ותוקף לא נשמרים.

קישור הקבלה, כשאפשר בלי קריאה לנדרים:

1. אם `ReceiptData` מתחיל ב-`http` — משתמשים בו כמו שהוא.
2. אם הוא UUID — הקישור הוא `https://files.ezcount.co.il/front/documents/get/<ReceiptData>`.
3. אחרת הקישור נשאר ריק והסטטוס הוא `receipt_pending`.

## סטטוס אחרי השמירה

| סטטוס | מתי |
| --- | --- |
| `skipped_no_phone` | אין טלפון נייד ישראלי תקין. לא ממשיכים לשליחה. |
| `receipt_pending` | יש טלפון, ואין עדיין קישור קבלה. |
| `send_pending` | יש טלפון ויש קישור. |
| `sent` | כבר נשלח. webhook חוזר לא משנה את הרשומה. |

כשיש מה להמשיך (`receipt_pending` או `send_pending`), הבקשה נרשמת לעיבוד ברקע אחרי ה-`200`. העיבוד הזה שייך לשליחה ולסנכרון, לא להגדרת ה-webhook עצמה.

## משתני סביבה לשלב הזה

ב-`.env` מקומי או ב-Render. לא לשים ערכים אמיתיים ב-git.

| משתנה | תפקיד |
| --- | --- |
| `NEDARIM_MOSAD_ID` | מספר המוסד. ברירת מחדל `7018669`. |
| `NEDARIM_WEBHOOK_SECRET` | סוד ה-HMAC ממסך ההגדרות של נדרים. חובה. |
| `NEDARIM_HMAC_MAX_SKEW_SECONDS` | חלון חותמת הזמן. ברירת מחדל `300`. |

הטבלה נוצרת בהפעלת השרת. אם הטבלה כבר קיימת בלי `web_doc_id` או `receipt_data`, העמודות האלה מתווספות בהפעלה.

## הגדרה ב-Render

בשירות ה-API ב-Render, `CORS_ORIGINS` מאפשר קריאות מהדפדפן של ה-frontend בלבד. עדכון העסקה מנדרים הוא `POST` נפרד, משרת אל שרת, לא מהאתר.

אין להוסיף את נדרים ל-`CORS_ORIGINS`. בקשה בלי כותרת `Origin` של דפדפן לא נחסמת שם, והכתובת הציבורית כבר מקבלת `POST`.

מה כן להגדיר ב-Render → Environment, בנוסף למשתני ה-frontend:

| משתנה | ערך |
| --- | --- |
| `NEDARIM_WEBHOOK_SECRET` | סוד ה-HMAC מנדרים. בלי זה ה-`POST` נענה ב-`503`. |
| `NEDARIM_MOSAD_ID` | `7018669` |

אחרי שמירה צריך deploy מחדש של השירות, כדי שהמשתנה ייטען.

## הגדרה בנדרים

1. הגדרות → API → Webhook.
2. בשדה עדכוני עסקאות: `https://poaley-chedec-1.onrender.com/api/v1/webhooks/nedarim/transactions`
3. להפעיל חתימת HMAC, ולהעתיק את הסוד ל-`NEDARIM_WEBHOOK_SECRET` לפני הלחיצה על הפעלה.
4. אחרי פריסה, "שליחת בדיקה" אמורה לקבל `200` וליצור שורה ב-`donation_receipts`.

עדכוני סירובים והקמת הוראת קבע לא נשמרים בכתובת הזו.

## מה השלבים הבאים

- **שליחה:** SMS דרך ימות המשיח (`YEMOT_API_KEY`), ואם נכשל — WhatsApp דרך GreenAPI.
- **סנכרון:** `POST https://poaley-chedec-1.onrender.com/api/v1/internal/nedarim/reconcile` עם הכותרת `X-Reconcile-Secret`, כדי להשלים עסקאות שה-webhook שלהן לא הגיע. נדרים לא משדרים שוב כישלון.
