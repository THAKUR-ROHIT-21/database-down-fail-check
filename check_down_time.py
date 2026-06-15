import pymysql, time
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────
HOST ='Enter database_Endpoints' 
USER ='Enter user name here'
PASS = 'Enter Password here'

down_start   = 0
prev_host    = ""
failover_log = []

print("\n🔍 Failover Monitor ")
print("=" * 55)

while True:
    try:
        cur = pymysql.connect(host=HOST, 
                              user=USER, 
                              password=PASS, 
                              connect_timeout=10).cursor()
        cur.execute("SELECT @@hostname, NOW()")
        host, now = cur.fetchone()

        if down_start:
            dt      = round(time.time() - down_start, 1)
            switched = host != prev_host
            failover_log.append({'dt': dt, 'from': prev_host, 'to': host, 'switched': switched})
            print(f"\n{'='*55}")
            print(f"✅ RECOVERED!")
            print(f"   Downtime : {int(dt//60)}m {int(dt%60)}s ({dt}s)")
            print(f"   From     : {prev_host}")
            print(f"   To       : {host}")
            print(f"   Result   : {'⚡️ HOST SWITCHED!' if switched else '⚠️ Same server'}")
            print(f"{'='*55}")
            print(f"\n📊 FAILOVER LOG ({len(failover_log)} events):")
            print(f"{'#':<4} {'Downtime':<10} {'From':<35} {'To':<35} {'Switch'}")
            print("-" * 90)
            for i in range(len(failover_log)):
                
                log = failover_log[i]
                print(f"{i+1:<4} {log['dt']:<10} {log['from']:<35} {log['to']:<35} {'⚡️YES' if log['switched'] else '⚠️NO'}")
            print()
            down_start = 0

        prev_host = host
        print(f"✅ {now} | {host}")

    except:
        if not down_start:
            down_start = time.time()
            print(f"\n❌ DOWN! {datetime.now().strftime('%H:%M:%S')} | {prev_host}")
        else:
            elapsed = round(time.time() - down_start, 1)
            print(f"⏳ {int(elapsed//60)}m {int(elapsed%60)}s")

    time.sleep(2)