#!/usr/bin/env python3
"""
=================================================================
VERIFICATION SCRIPT - E-COMMERCE ANALYTICS PROJECT
=================================================================
Verifies that all components are properly set up and working
"""

import os
import sys
import pandas as pd

def check_structure():
    """Verify project structure"""
    print("\n" + "="*80)
    print("1️⃣ CHECKING PROJECT STRUCTURE")
    print("="*80)
    
    required_dirs = [
        'data/raw',
        'data/processed',
        'notebooks',
        'dashboard',
        'reports',
        '.streamlit'
    ]
    
    required_files = [
        'requirements.txt',
        'pyproject.toml',
        'README.md',
        'dashboard/app.py',
        'notebooks/01_data_cleaning_and_features.ipynb',
        'notebooks/02_eda_and_kpis.ipynb',
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            all_good = False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    return all_good

def check_data():
    """Verify data files"""
    print("\n" + "="*80)
    print("2️⃣ CHECKING DATA FILES")
    print("="*80)
    
    files_to_check = [
        ('data/raw/superstore.csv', 'Raw Data'),
        ('data/processed/superstore_cleaned.csv', 'Cleaned Data'),
        ('data/processed/kpis.csv', 'KPI Metrics'),
    ]
    
    all_good = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, encoding='latin-1', nrows=5)
                print(f"✅ {description} ({file_path})")
                print(f"   Shape: {df.shape}")
            except Exception as e:
                print(f"⚠️ {description} - ERROR: {str(e)[:50]}")
                all_good = False
        else:
            print(f"❌ {description} ({file_path}) - MISSING")
            all_good = False
    
    return all_good

def check_dependencies():
    """Verify key dependencies"""
    print("\n" + "="*80)
    print("3️⃣ CHECKING DEPENDENCIES")
    print("="*80)
    
    packages = [
        ('pandas', 'Data processing'),
        ('numpy', 'Numerical computing'),
        ('matplotlib', 'Visualization'),
        ('seaborn', 'Statistical visualization'),
        ('plotly', 'Interactive visualization'),
        ('streamlit', 'Dashboard framework'),
    ]
    
    all_good = True
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - NOT INSTALLED")
            all_good = False
    
    return all_good

def main():
    print("\n" + "█"*80)
    print("📊 E-COMMERCE ANALYTICS - PROJECT VERIFICATION")
    print("█"*80)
    
    results = []
    results.append(("Structure", check_structure()))
    results.append(("Data", check_data()))
    results.append(("Dependencies", check_dependencies()))
    
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    all_passed = all(result[1] for result in results)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:20} {status}")
    
    print("\n" + "█"*80)
    if all_passed:
        print("✨ ALL CHECKS PASSED! Project is ready to go! 🚀")
    else:
        print("⚠️ SOME CHECKS FAILED. Please review the errors above.")
    print("█"*80 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
