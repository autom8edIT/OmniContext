import base64
import urllib.parse
import google_auth_pb2
import base64

def decode_google_auth_url(url: str):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "otpauth-migration":
        raise ValueError("Invalid scheme")
    
    query = urllib.parse.parse_qs(parsed.query)
    if "data" not in query:
        raise ValueError("No data parameter found")
    
    data = query["data"][0]
    # Google Auth uses a slightly non-standard base64 (maybe?) or just padded
    # Actually it's standard base64 but often needs padding
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    
    decoded = base64.b64decode(data)
    
    payload = google_auth_pb2.MigrationPayload()
    payload.ParseFromString(decoded)
    
    results = []
    for otp in payload.otp_parameters:
        # Secret is bytes, needs to be base32 encoded for standard TOTP apps
        import base64
        import base32_lib # Wait, let's use standard base64.b32encode
        secret_b32 = base64.b32encode(otp.secret).decode('utf-8').replace('=', '')
        
        results.append({
            "name": otp.name,
            "issuer": otp.issuer,
            "secret": secret_b32,
            "type": "TOTP" if otp.type == google_auth_pb2.MigrationPayload.OTP_TOTP else "HOTP",
            "algorithm": "SHA1" if otp.algorithm == google_auth_pb2.MigrationPayload.ALGO_SHA1 else "Unknown"
        })
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            res = decode_google_auth_url(sys.argv[1])
            import json
            print(json.dumps(res, indent=2))
        except Exception as e:
            print(f"Error: {e}")
