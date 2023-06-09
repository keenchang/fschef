import os
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv('DATABASE_URL').replace("postgres:", "postgresql:"))


def create_table(schema_name, table_name, cmd):
    create_refresh_updated_at_func = """
        DROP FUNCTION IF EXISTS {schema}.refresh_updated_at() CASCADE;
        CREATE FUNCTION {schema}.refresh_updated_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql AS
        $func$
        BEGIN
        NEW.updated_at := now();
        RETURN NEW;
        END
        $func$;
        """

    create_trigger = """
        CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
        FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
        """

    with engine.connect() as conn:
        conn.execute(text(cmd))
        conn.execute(text(create_refresh_updated_at_func.format(schema=schema_name)))
        conn.execute(text(create_trigger.format(schema=schema_name, table=table_name)))
        conn.commit()

