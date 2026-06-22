import time
import pymysql
from pymysql import OperationalError, Error

# Database Credentials
HOST_MUMBAI = 'Endpoint-1'
HOST_VERGINA = 'Endpoint-2'

USER = 'User Name'
PASS = 'Password'
PORT = 3306


def measure_db_latency(host, attempts=5):   # Increased attempts for better accuracy
    """Measure connection latency to MySQL RDS using PyMySQL"""
    latencies = []
    print(f"\n🔌 Testing connection to: {host}")
   
    for i in range(attempts):
        start_time = time.time()
        conn = None
        try:
            conn = pymysql.connect(
                host=host,
                user=USER,
                password=PASS,
                port=PORT,
                connect_timeout=10,
                read_timeout=10,
                write_timeout=10
            )
           
            # Quick test query
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
           
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            latencies.append(latency)
           
            print(f"   Attempt {i+1}: ✅ {latency:.2f} ms")
           
        except (OperationalError, Error) as e:
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            print(f"   Attempt {i+1}: ❌ Failed ({latency:.2f} ms) - {str(e)[:100]}")
            latencies.append(None)
       
        finally:
            if conn:
                conn.close()
   
    # Calculate statistics
    successful = [lat for lat in latencies if lat is not None]
    if successful:
        avg_latency = sum(successful) / len(successful)
        min_latency = min(successful)
        max_latency = max(successful)
        
        print(f"   📊 Summary → Avg: {avg_latency:.2f} ms | Min: {min_latency:.2f} ms | Max: {max_latency:.2f} ms")
        return avg_latency
    else:
        print("   ❌ All attempts failed")
        return None


def calculate_speed_factor(lat1, lat2, name1="Mumbai", name2="Virginia"):
    """Calculate how many times faster one is compared to another"""
    if lat1 is None or lat2 is None:
        return None
    
    if lat1 < lat2:
        factor = lat2 / lat1
        print(f"\n🚀 {name1} is *{factor:.2f}x FASTER* than {name2}")
    elif lat2 < lat1:
        factor = lat1 / lat2
        print(f"\n🚀 {name2} is *{factor:.2f}x FASTER* than {name1}")
    else:
        print("\n⚖️ Both have almost same latency")
    return factor


if __name__ == "__main__":
    print("🌍 RDS Cross-Region Latency Test (PyMySQL)")
    print("=" * 70)

    print("\n📍 Testing Mumbai (ap-south-1)...")
    mumbai_latency = measure_db_latency(HOST_MUMBAI)

    print("\n📍 Testing Virginia (us-east-1)...")
    virginia_latency = measure_db_latency(HOST_VERGINA)

    print("\n" + "=" * 70)
    print("🏁 FINAL RESULTS:")

    if mumbai_latency is not None:
        print(f"   🇮🇳 Mumbai    : {mumbai_latency:.2f} ms")

    if virginia_latency is not None:
        print(f"   🇺🇸 Virginia  : {virginia_latency:.2f} ms")

    calculate_speed_factor(mumbai_latency, virginia_latency, "Mumbai", "Virginia")
