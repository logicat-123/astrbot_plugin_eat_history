DROP TABLE IF EXISTS "message_history";
CREATE TABLE "message_history" (
  "id" integer PRIMARY KEY AUTOINCREMENT,
  "created_at" text,
  "user_id" text,
  "user_nick" text,
  "group_id" text,
  "message_id" text,
  "content" text
);
