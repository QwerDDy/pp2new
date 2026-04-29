from connect import connecting
import json
conn = connecting()
cur = conn.cursor()

ist = True
while(ist):
    inp = input()
    if inp == "1":
        pinp = input()
        cur.execute("SELECT * FROM SEARCH_NAME(%s)", (pinp,))
        print(cur.fetchall())
    if inp == "2":
        pinp = input()
        cur.execute("SELECT * FROM SEARCH_NUMBER(%s)", (pinp,))
        print(cur.fetchall())
    if inp == "3":
        inp_name = input("name:")
        inp_number = input("number:")
        inp_email = input("email:")
        group_id = input("group (1-4)")
        birthday = input("birthday")
        cur.execute("CALL UPSET_USER(%s,%s,%s,%s,%s)",(inp_name,inp_number,inp_email,group_id,birthday))
        print('good!')
        conn.commit()
    if inp == "4":
        inp_oname = input()
        inp_onumber = input()
        inp_name = input()
        cur.execute("CALL UPDATE_NAME(%s,%s,%s)",(inp_onumber,inp_oname,inp_name))
        print('good!')
        conn.commit()
    if inp == "5":
        inp_dname = input()
        inp_dnumber = input()
        cur.execute("CALL DELETE_COL(%s,%s)",(inp_dname,inp_dnumber))
        print('good!')
        conn.commit()
    if inp == "6":
        email = input("email search: ")
        cur.execute("SELECT * FROM SEARCH_EMAIL(%s)", (email,))
        print(cur.fetchall())
    
    if inp == "7":
        print("'name'-sort by name")
        print("'number'- sort by number")
        print("'other' - without sorting")
        vsort = input("sort by:")
        cur.execute("SELECT * FROM SORT_CONTACTS(%s)",(vsort,))
        print(cur.fetchall())

    if inp == "8":
        limit = 2
        offset = 0

        while True:
            cur.execute("SELECT * FROM GET_CONTACTS_PAGE(%s,%s)", (limit, offset))
            rows = cur.fetchall()

            print("\nPAGE:")
            for r in rows:
                print(r)

            cmd = input("next / prev / quit: ")

            if cmd == "next":
                offset += limit
            elif cmd == "prev" and offset > 0:
                offset -= limit
            elif cmd == "quit":
                break
    
    


    if inp == "9":
        cur.execute("""
            SELECT 
                p.name,
                p.number,
                p.emil,
                p.group_id,
                p.birthday,
                g.name AS group_name
            FROM phonebook p
            LEFT JOIN groups g ON p.group_id = g.id
        """)
        
        rows = cur.fetchall()

        data = []

        for r in rows:
            data.append({
                "name": r[0],
                "number": r[1],
                "email": r[2],
                "group_id": r[3],
                "birthday": r[4].isoformat() if r[4] else None,
                "group": r[5]
            })

        with open("Endterm/TSIS1/contacts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("export done")

    if inp == "10":

        with open("Endterm/TSIS1/contacts.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            cur.execute("""
                INSERT INTO phonebook(name, number, emil, group_id, birthday)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (number)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    emil = EXCLUDED.emil,
                    group_id = EXCLUDED.group_id,
                    birthday = EXCLUDED.birthday
            """, (
                item["name"],
                item["number"],
                item.get("email"),
                item.get("group_id"),
                item.get("birthday")
            ))

        conn.commit()
        print("IMPORT DONE")

    if inp == "11":
        name = input("contact name: ")
        group_id = int(input("group id: "))
        cur.execute("CALL move_to_group(%s, %s)",(name, group_id))
        conn.commit()
        print("moved")


    if inp =="12":
        print('poka!\n')
        print('final result: ')
        ist = False

cur.execute("SELECT * FROM phonebook;")
print(cur.fetchall())

conn.close()

