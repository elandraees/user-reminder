create database user-reminder-service-db
drop table if exists users;
CREATE TABLE "users" (
  "user_id" serial PRIMARY KEY,
  "username" varchar unique,
  "password" varchar,
  "email_address" varchar,
  "status_id" int,
  "billing_customer_id" bigint,
  "create_date" timestamp,
  "last_update" timestamp
);
CREATE UNIQUE INDEX user_id_idx on users (user_id);
CREATE UNIQUE INDEX username_users_idx on users (username);
CREATE UNIQUE INDEX email_address_users_idx on users (email_address);

drop table if exists reminders;
CREATE TABLE "reminders" (
  "reminder_id" serial PRIMARY KEY,
  "user_id" bigint,
  "reminder_date" timestamp,
  "note" varchar(255)
);
CREATE INDEX user_id_reminders_idx on reminders (user_id)