CREATE TABLE "languages_list"(
    "id" BIGINT NOT NULL,
    "python" BIGINT NOT NULL,
    "javascript" BIGINT NOT NULL,
    "sql" BIGINT NOT NULL,
    "java" BIGINT NOT NULL,
    "c" BIGINT NOT NULL,
    "php" BIGINT NOT NULL,
    "swift" BIGINT NOT NULL,
    "css" BIGINT NOT NULL,
    "html" BIGINT NOT NULL,
    "go" BIGINT NOT NULL,
    "kotlin" BIGINT NOT NULL,
    "typescript" BIGINT NOT NULL,
    "ruby" BIGINT NOT NULL,
    "rust" BIGINT NOT NULL,
    "c#" BIGINT NOT NULL
);
ALTER TABLE
    "languages_list" ADD PRIMARY KEY("id");
CREATE TABLE "filetype"("id" BIGINT NOT NULL);
ALTER TABLE
    "filetype" ADD PRIMARY KEY("id");
CREATE TABLE "user_upload"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "filetype" BIGINT NOT NULL,
    "name" VARCHAR(80) NOT NULL
);
ALTER TABLE
    "user_upload" ADD PRIMARY KEY("id");
CREATE TABLE "users_languages"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "language_id" BIGINT NOT NULL,
    "skill" BIGINT NOT NULL DEFAULT '5'
);
ALTER TABLE
    "users_languages" ADD PRIMARY KEY("id");
CREATE TABLE "frameworks"(
    "id" BIGINT NOT NULL,
    "name" BIGINT NOT NULL,
    "languages" BIGINT NOT NULL
);
ALTER TABLE
    "frameworks" ADD PRIMARY KEY("id");
CREATE TABLE "user"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(80) NOT NULL,
    "password" VARCHAR(1000) NOT NULL,
    "firstname" VARCHAR(80) NOT NULL,
    "lastname" VARCHAR(80) NOT NULL
);
ALTER TABLE
    "user" ADD PRIMARY KEY("id");
ALTER TABLE
    "user" ADD CONSTRAINT "user_username_unique" UNIQUE("username");
CREATE TABLE "languages"(
    "id" BIGINT NOT NULL,
    "name" BIGINT NOT NULL
);
ALTER TABLE
    "languages" ADD PRIMARY KEY("id");
CREATE TABLE "users_frameworks"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "framework_id" BIGINT NOT NULL,
    "skill" BIGINT NOT NULL DEFAULT '5'
);
ALTER TABLE
    "users_frameworks" ADD PRIMARY KEY("id");
CREATE TABLE "frameworks_list"(
    "id" BIGINT NOT NULL,
    "react_native" BIGINT NOT NULL,
    "nodejs" BIGINT NOT NULL,
    "expressjs" BIGINT NOT NULL,
    "jquery" BIGINT NOT NULL,
    "django" BIGINT NOT NULL,
    "flask" BIGINT NOT NULL,
    "pytorch" BIGINT NOT NULL,
    "git" BIGINT NOT NULL,
    "ruby_on_rails" BIGINT NOT NULL,
    "spring" BIGINT NOT NULL,
    "spark" BIGINT NOT NULL,
    "angularjs" BIGINT NOT NULL,
    "reactjs" BIGINT NOT NULL,
    "vuejs" BIGINT NOT NULL,
    "pidgin" BIGINT NOT NULL,
    "apache" BIGINT NOT NULL,
    "tensorflow" BIGINT NOT NULL
);
ALTER TABLE
    "frameworks_list" ADD PRIMARY KEY("id");
ALTER TABLE
    "frameworks" ADD CONSTRAINT "frameworks_languages_foreign" FOREIGN KEY("languages") REFERENCES "languages"("id");
ALTER TABLE
    "users_frameworks" ADD CONSTRAINT "users_frameworks_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "users_frameworks" ADD CONSTRAINT "users_frameworks_framework_id_foreign" FOREIGN KEY("framework_id") REFERENCES "frameworks"("id");
ALTER TABLE
    "users_languages" ADD CONSTRAINT "users_languages_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "user_upload" ADD CONSTRAINT "user_upload_filetype_foreign" FOREIGN KEY("filetype") REFERENCES "filetype"("id");
ALTER TABLE
    "users_languages" ADD CONSTRAINT "users_languages_language_id_foreign" FOREIGN KEY("language_id") REFERENCES "languages"("id");
ALTER TABLE
    "user_upload" ADD CONSTRAINT "user_upload_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");