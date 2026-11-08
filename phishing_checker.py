import re
from urllib.parse import urlparse

def inspect_url(raw_url):
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []
    if not url:
        return ["No URL entered."]
    
    candidate = url if "://" in url else "http://" + url
    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ["This text is not a valid URL format."]
        
    host = (parsed.hostname or "").lower()
    
    if not host:
        return ["Could not identify a hostname."]
    
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")
    
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")
        
    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")
        
    return findings

def main():
    # Option E: Improved output formatting (headers and nice borders)
    print("=" * 45)
    print("   EWB Phishing URL Awareness Checker")
    print("   Text checks only — this program does not open URLs.")
    print("=" * 45)
    
    # Option A: Loop with quit command
    while True:
        raw_url = input("\nEnter a sample URL (or type 'q' to quit): ")
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("\nGoodbye! Stay alert online.")
            break
            
        print("\n" + "-" * 30)
        print(" INSPECTION RESULTS:")
        print("-" * 30)
        
        # Option E: Numbered list formatting for findings
        for i, item in enumerate(inspect_url(raw_url), 1):
            print(f" {i}. {item}")
            
        print("-" * 30)
        print("Reminder: Never enter passwords from unexpected links.")

if __name__ == "__main__":
    main()