DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS infantry CASCADE;
DROP TABLE IF EXISTS artillery CASCADE;


CREATE TABLE "countries" (
	"country_id" integer NOT NULL,
	"country_name" TEXT NOT NULL,
	"r" integer NOT NULL,
	"g" integer NOT NULL,
	"b" integer NOT NULL,
	CONSTRAINT "countries_pk" PRIMARY KEY ("country_id")
);



CREATE TABLE "infantry" (
	"infantry_id" integer NOT NULL,
	"infantry_name" TEXT NOT NULL,
	"country_id" integer NOT NULL,
	"count" integer NOT NULL,
	"distance" integer NOT NULL,
	"way" integer NOT NULL,
	"error" integer NOT NULL,
	"guard" BOOLEAN NOT NULL,
	CONSTRAINT "infantry_pk" PRIMARY KEY ("infantry_id")
);



CREATE TABLE "artillery" (
	"artillery_id" integer NOT NULL,
	"artillery_name" TEXT NOT NULL,
	"country_id" integer NOT NULL,
	"core_distance" integer NOT NULL,
	"core_error" integer NOT NULL,
	"grapeshot_count" integer NOT NULL,
	"grapeshot_error" integer NOT NULL,
	"grapeshot_distance" integer NOT NULL,
	CONSTRAINT "artillery_pk" PRIMARY KEY ("artillery_id")
);


ALTER TABLE "infantry" ADD CONSTRAINT "infantry_fk0" FOREIGN KEY ("country_id") REFERENCES "countries"("country_id");
ALTER TABLE "artillery" ADD CONSTRAINT "artillery_fk0" FOREIGN KEY ("country_id") REFERENCES "countries"("country_id");




