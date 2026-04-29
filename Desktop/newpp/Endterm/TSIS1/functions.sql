DROP FUNCTION IF EXISTS SEARCH_NAME(TEXT);
DROP FUNCTION IF EXISTS SEARCH_NUMBER(TEXT);
DROP FUNCTION IF EXISTS SEARCH_EMAIL(TEXT);
DROP FUNCTION IF EXISTS SORT_CONTACTS(TEXT);
DROP FUNCTION IF EXISTS GET_CONTACTS_PAGE(INT,INT);

CREATE OR REPLACE FUNCTION SEARCH_NAME(pattern TEXT)
RETURNS TABLE(name VARCHAR, number VARCHAR,emil VARCHAR, group_id INT,birthday DATE) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.name,phonebook.number,phonebook.emil,phonebook.group_id,phonebook.birthday
    FROM phonebook
    WHERE phonebook.name ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION SEARCH_NUMBER(pattern TEXT)
RETURNS TABLE(name VARCHAR, number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.name AS name,
           phonebook.number AS number
    FROM phonebook
    WHERE phonebook.number = pattern;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION SEARCH_EMAIL(pattern TEXT)
RETURNS TABLE(name VARCHAR, number VARCHAR, emil VARCHAR,group_id INT,birthday DATE) as $$
BEGIN
    RETURN QUERY
    SELECT phonebook.name,phonebook.number,phonebook.emil,phonebook.group_id,phonebook.birthday
    FROM phonebook
    where phonebook.emil ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION SORT_CONTACTS(p_sort TEXT)
RETURNS TABLE(name VARCHAR, number VARCHAR, emil VARCHAR, group_id INT,birthday DATE) AS $$
BEGIN
    IF p_sort = 'name' THEN
        RETURN QUERY
        SELECT * FROM phonebook
        ORDER BY name;

    ELSIF p_sort = 'number' THEN
        RETURN QUERY
        SELECT * FROM phonebook
        ORDER BY number;

    ELSE
        RETURN QUERY
        SELECT * FROM phonebook;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION GET_CONTACTS_PAGE(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, number VARCHAR, emil VARCHAR,group_id INT,birthday DATE) AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    ORDER BY name
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

/*psql -U postgres -d newDB -p 5433 -f Endterm/TSIS1/functions.sql*/