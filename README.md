# tg-raw

Framework-free experiments with the Telegram Bot API: polling, webhooks, and update handling in plain Python. Built to understand what frameworks like aiogram abstract away.

## How it works

Each numbered folder is one self-contained experiment with its own `main.py` you can read top-to-bottom and run on its own. There are **no shared helpers** — the repeated boilerplate (the `BASE` URL, the token read) is intentional, so every example tells the whole story without chasing imports. Work through them in order.

## Experiments

### Phase 1 — Foundations (the core loop)
- [ ] `01-getme` — call `getMe`; learn the `{"ok": true, "result": {...}}` response shape every method returns
- [ ] `02-polling-echo` — the `getUpdates` long-polling loop + the `offset = last_id + 1` acknowledgment trick
- [ ] `03-update-anatomy` — log and dissect a raw `Update`; see message vs edited_message vs callback_query side by side
- [ ] `04-formatting` — `sendMessage` with HTML and MarkdownV2, entities, and why escaping matters

### Phase 2 — Sending content
- [ ] `05-media` — `sendPhoto` / `sendDocument` / `sendAudio` / `sendVideo`, and reusing a `file_id` instead of re-uploading
- [ ] `06-media-group` — `sendMediaGroup` (albums)
- [ ] `07-special-messages` — location, contact, poll, dice, and `sendChatAction` (the "typing…" indicator)
- [ ] `08-file-download` — `getFile` + fetching the actual bytes a user sent you

### Phase 3 — Interactivity
- [ ] `09-reply-keyboards` — `ReplyKeyboardMarkup`, one-time keyboards, force-reply, removal
- [ ] `10-inline-buttons` — `InlineKeyboardMarkup` + `callback_query` + `answerCallbackQuery`
- [ ] `11-edit-delete` — `editMessageText` / `editMessageReplyMarkup` / `deleteMessage` for live, mutating UIs
- [ ] `12-commands-deeplink` — `setMyCommands` (the command menu) + `/start` deep-link parameters

### Phase 4 — Conversations & state
- [ ] `13-fsm-by-hand` — a multi-step form with per-user state tracked manually (the experiment that makes you *want* a framework)

### Phase 5 — Webhooks & deployment
- [ ] `14-webhook-fastapi` — `setWebhook` + a FastAPI receiver + `secret_token` header verification
- [ ] `15-webhook-ops` — `getWebhookInfo` for debugging, `allowed_updates` filtering, and fast-ack + background processing

### Phase 6 — Robustness (the "production" lessons)
- [ ] `16-rate-limits` — handle `429` with `retry_after`; respect flood limits
- [ ] `17-idempotency` — dedupe duplicate update deliveries so retries are safe
- [ ] `18-logging-errors` — structured logging and capturing API errors cleanly

### Phase 7 — Groups & administration
- [ ] `19-groups` — bot in a group, privacy mode, reacting to mentions
- [ ] `20-chat-info` — `getChat` / `getChatMember` / `getChatAdministrators`
- [ ] `21-moderation` — ban / restrict / promote members, pin messages
- [ ] `22-membership` — `chat_member` updates: joins, leaves, status changes

### Phase 8 — Advanced / specialist (pick by interest)
- [ ] `23-inline-mode` — `answerInlineQuery` (the `@yourbot ...` typeahead anywhere in Telegram)
- [ ] `24-mini-app` — a `web_app` button + validating Web App `initData` (the Mini App path)
- [ ] `25-payments` — `sendInvoice` + `pre_checkout_query` + `successful_payment`
- [ ] `26-reactions` — `setMessageReaction`
- [ ] `27-stickers` — `sendSticker` and working with sticker sets
- [ ] `28-channels` — handling `channel_post` for a bot that admins a channel

---
