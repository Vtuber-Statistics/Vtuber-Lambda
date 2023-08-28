--
-- CreateTable
--
DROP TABLE IF EXISTS channel;
CREATE TABLE channel (
    "id" SERIAL PRIMARY KEY,
	"vtuber_name"	VARCHAR(20)	NOT NULL,
	"group"	VARCHAR(20)	NOT NULL,
	"country"	VARCHAR(10)	NOT NULL,
	"channel_name"	VARCHAR(50)	NOT NULL,
	"custom_url"	VARCHAR(50)	NOT NULL,
	"thumbnail_url"	VARCHAR(255)	NOT NULL,
	"created_at"	TIMESTAMP   NOT NULL,
	"subscriber_count"	INTEGER	NOT NULL,
	"total_view_count"	INTEGER	NOT NULL,
	"video_count"	INTEGER	NOT NULL,
	"youtube_api_channel_id"    VARCHAR(50)	NOT NULL,

	UNIQUE ("vtuber_name", "channel_name", "custom_url", "youtube_api_channel_id")
);

DROP TABLE IF EXISTS video;
CREATE TABLE video (
    "id" SERIAL PRIMARY KEY,
	"title"	VARCHAR(255)	NOT NULL,
	"video_url"	VARCHAR(255)	NOT NULL,
	"thumbnail_url"	VARCHAR(255)	NOT NULL,
	"is_live"	BOOLEAN	NOT NULL,
	"view_count"	INTEGER	NOT NULL,
	"like_count"	INTEGER	NOT NULL,
	"comment_count"	INTEGER	NOT NULL,
	"created_at"	TIMESTAMP   NOT NULL,
	"youtube_api_video_id"	VARCHAR(50)	NOT NULL,
	"channel_id"	INTEGER	NOT NULL
);

--
-- AddForeignKey
--
ALTER TABLE video ADD CONSTRAINT "fk_channel_id" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE ON UPDATE CASCADE;