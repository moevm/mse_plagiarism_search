createEntryTable = """
CREATE TABLE IF NOT EXISTS public."Entry"
(
    id integer NOT NULL DEFAULT nextval('"Entry_id_seq"'::regclass),
    name text COLLATE pg_catalog."default",
    "createdAt" date,
    CONSTRAINT "Entry_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public."Entry"
    OWNER to postgres;
"""

createFileTable = """
CREATE TABLE IF NOT EXISTS public."File"
(
    id integer NOT NULL DEFAULT nextval('"File_id_seq"'::regclass),
    "entryId" integer,
    path text COLLATE pg_catalog."default",
    hash character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT "File_pkey" PRIMARY KEY (id),
    CONSTRAINT cascade1 FOREIGN KEY ("entryId")
        REFERENCES public."Entry" (id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE public."File"
    OWNER to postgres;

"""

createCodeFragmentTable = """
CREATE TABLE IF NOT EXISTS public."CodeFragment"
(
    id integer NOT NULL DEFAULT nextval('"CodeFragment_id_seq"'::regclass),
    "fileId" integer,
    "order" integer,
    text character varying(255) COLLATE pg_catalog."default",
    metaphone character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT "CodeFragment_pkey" PRIMARY KEY (id),
    CONSTRAINT cascade2 FOREIGN KEY ("fileId")
        REFERENCES public."File" (id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE public."CodeFragment"
    OWNER to postgres;

"""

createSequences = """
CREATE SEQUENCE IF NOT EXISTS public."Entry_id_seq";
CREATE SEQUENCE IF NOT EXISTS public."File_id_seq";
CREATE SEQUENCE IF NOT EXISTS public."CodeFragment_id_seq";
"""

dropTables = """
DROP TABLE public."CodeFragment";
DROP TABLE public."File";
DROP TABLE public."Entry";
"""