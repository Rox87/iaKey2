import sys
sys.path.append('c:\\Users\\rodri\\Documents\\mySpace\\iaKey2')
from backend import db
conn = db.get_db()
c = conn.cursor()
c.execute("UPDATE providers SET base_url='https://api.x.ai/v1' WHERE base_url='https://api.x.com/v1'")
conn.commit()
conn.close()
