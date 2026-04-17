#!/usr/bin/env python3
# ============================================================
# run.py
# Main Entry Point for Charity Blockchain Platform
# ============================================================

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.app import app

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔗 CHARITY BLOCKCHAIN PLATFORM")
    print("="*70)
    print("\n✅ System Status:")
    print("   • Blockchain Engine: Ready")
    print("   • Consensus Algorithm: Ready (Byzantine Fault Tolerance)")
    print("   • Authentication System: Ready")
    print("   • Database: Local (data.json)")
    
    print("\n📍 Server Configuration:")
    print("   • Host: 127.0.0.1")
    print("   • Port: 8080")
    print("   • URL: http://127.0.0.1:8080")
    
    print("\n👤 Default Credentials:")
    print("   Admin Account:")
    print("   • Username: Admin")
    print("   • Password: Admin@123")
    print("\n   Manager Account:")
    print("   • Username: Charity_Manager")
    print("   • Password: Manager@123")
    
    print("\n📚 Documentation:")
    print("   • Demo Guide: README_DEMO.md")
    print("   • Smart Contract: contracts/CONTRACT_NOTES.md")
    
    print("\n" + "="*70)
    print("Starting Flask server...")
    print("="*70 + "\n")
    
    app.run(debug=True, port=8080, host="127.0.0.1")
