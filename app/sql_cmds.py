from flask import current_app
from app.extensions import db
import sqlalchemy as sa


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

    with current_app.app_context():
        db.engine.execute(cmd)
        db.engine.execute(sa.text(create_refresh_updated_at_func.format(schema=schema_name)))
        db.engine.execute(sa.text(create_trigger.format(schema=schema_name, table=table_name)))

