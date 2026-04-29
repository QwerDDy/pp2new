DROP PROCEDURE IF EXISTS UPSET_USER(TEXT, TEXT, TEXT, INT,DATE);

CREATE PROCEDURE UPSET_USER(u TEXT, p TEXT,t TEXT,g INT,b DATE)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phonebook(name, number,emil,group_id,birthday)
    VALUES (u, p, t,g,b)
    ON CONFLICT (number)
    DO UPDATE SET name = EXCLUDED.name,
    emil = EXCLUDED.emil,
    group_id = EXCLUDED.group_id
    birthday = EXCLUDED.birthday;
END;
$$;

CREATE OR REPLACE PROCEDURE UPDATE_NAME(oldnumber TEXT,oldname TEXT, new_name TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF oldnumber IS NOT NULL THEN
    UPDATE phonebook SET name = new_name WHERE number = oldnumber;
    ELSIF oldname IS NOT NULL AND oldnumber IS NULL THEN
    UPDATE phonebook SET name = new_name WHERE name = oldname;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE DELETE_COL(delname TEXT, delnumber TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF delnumber IS NOT NULL THEN
    DELETE FROM phonebook WHERE number = delnumber;
    ELSIF delname IS NOT NULL AND delnumber IS NULL THEN
    DELETE FROM phonebook WHERE name = delname;
    END IF;
END;
$$;



CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE phonebook
    SET group_id = p_group_id
    WHERE name = p_contact_name;
END;
$$;



/*psql -U postgres -d newDB -p 5433 -f Endterm/TSIS1/procedures.sql*/