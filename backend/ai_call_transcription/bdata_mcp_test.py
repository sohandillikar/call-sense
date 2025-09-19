import requests
import json
import time
from datetime import datetime

class BrightDataSnapshotHandler:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.brightdata.com/datasets/v3"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def check_snapshot_progress(self, snapshot_id):
        """Check the progress/status of a snapshot"""
        url = f"{self.base_url}/progress"
        params = {"snapshot_id": snapshot_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error checking progress: {e}")
            return None
    
    def download_snapshot(self, snapshot_id, format="json", compress=False, part=1, batch_size=None):
        """Download snapshot results"""
        url = f"{self.base_url}/snapshot/{snapshot_id}"
        params = {"format": format}
        
        if compress:
            params["compress"] = "true"
        if batch_size:
            params["batch_size"] = batch_size
            params["part"] = part
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            if format.lower() == "json":
                return response.json()
            else:
                return response.text
                
        except requests.exceptions.RequestException as e:
            print(f"Error downloading snapshot: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            return None
    
    def get_snapshot_parts(self, snapshot_id, format="json", compress=False, batch_size=None):
        """Get information about snapshot parts"""
        url = f"{self.base_url}/snapshot/{snapshot_id}/parts"
        params = {"format": format}
        
        if compress:
            params["compress"] = "true"
        if batch_size:
            params["batch_size"] = batch_size
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting snapshot parts: {e}")
            return None
    
    def list_snapshots(self, dataset_id):
        """List all snapshots for a dataset"""
        url = f"{self.base_url}/snapshot"
        params = {"dataset_id": dataset_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing snapshots: {e}")
            return None
    
    def wait_for_completion(self, snapshot_id, max_wait_time=600, check_interval=30):
        """Wait for a snapshot to complete, with timeout"""
        print(f"Waiting for snapshot {snapshot_id} to complete...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            progress = self.check_snapshot_progress(snapshot_id)
            
            if not progress:
                print("Failed to check progress")
                return False
            
            status = progress.get("status", "unknown")
            print(f"Current status: {status}")
            
            if status == "ready":
                print("✅ Snapshot is ready for download!")
                return True
            elif status in ["failed", "error"]:
                print("❌ Snapshot failed!")
                return False
            elif status in ["running", "collecting", "processing"]:
                print(f"⏳ Still {status}... waiting {check_interval} seconds")
                time.sleep(check_interval)
            else:
                print(f"Unknown status: {status}")
                time.sleep(check_interval)
        
        print("⏰ Timeout reached!")
        return False

def main():
    # Your API token and snapshot ID
    API_TOKEN = "70ae0eed540bad116ddb12796cb86d23e5facc2ebda12e8a397763ebddffc767"
    SNAPSHOT_ID = "s_mfr3f0jo2jvnopa2wt"
    DATASET_ID = "gd_m8d03he47z8nwb5xc"
    
    handler = BrightDataSnapshotHandler(API_TOKEN)
    
    print("=== BrightData Snapshot Handler ===")
    print(f"Snapshot ID: {SNAPSHOT_ID}")
    print(f"Time: {datetime.now()}")
    
    # Step 1: Check current progress
    print("\n1. Checking snapshot progress...")
    progress = handler.check_snapshot_progress(SNAPSHOT_ID)
    if progress:
        print(f"Progress: {json.dumps(progress, indent=2)}")
        status = progress.get("status", "unknown")
        
        if status == "ready":
            print("✅ Snapshot is ready!")
        elif status in ["running", "collecting", "processing"]:
            print(f"⏳ Snapshot is still {status}")
            # Wait for completion
            if handler.wait_for_completion(SNAPSHOT_ID):
                status = "ready"
        else:
            print(f"Status: {status}")
    
    # Step 2: Try to download if ready
    if progress and progress.get("status") == "ready":
        print("\n2. Downloading snapshot results...")
        results = handler.download_snapshot(SNAPSHOT_ID, format="json")
        
        if results:
            print("✅ Successfully downloaded results!")
            print(f"Results: {json.dumps(results, indent=2)[:500]}...")  # Show first 500 chars
            
            # Save to file
            with open(f"snapshot_{SNAPSHOT_ID}.json", "w") as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved to snapshot_{SNAPSHOT_ID}.json")
        else:
            print("❌ Failed to download results")
    
    # Step 3: List all snapshots for this dataset
    print(f"\n3. Listing all snapshots for dataset {DATASET_ID}...")
    snapshots = handler.list_snapshots(DATASET_ID)
    if snapshots:
        print(f"Found {len(snapshots)} snapshots:")
        for snapshot in snapshots:
            print(f"  - {snapshot.get('id', 'N/A')} | Status: {snapshot.get('status', 'N/A')} | Created: {snapshot.get('created_at', 'N/A')}")

if __name__ == "__main__":
    main()