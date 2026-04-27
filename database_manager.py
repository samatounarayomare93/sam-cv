#!/usr/bin/env python
"""
database_manager.py - Database backup, restore, and management utilities
Usage: python database_manager.py --backup | --restore | --status
"""

import sqlite3
import json
import gzip
from pathlib import Path
from datetime import datetime
import sys
import argparse

class DatabaseManager:
    def __init__(self, db_path: str = "chronos.db"):
        self.db_path = Path(db_path)
        self.backups_dir = Path("backups")
        self.backups_dir.mkdir(exist_ok=True)
    
    def get_connection(self):
        """Get database connection"""
        if not self.db_path.exists():
            return None
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return None
    
    def backup_database(self, compress: bool = True) -> bool:
        """Backup database to file"""
        try:
            conn = self.get_connection()
            if not conn:
                print("❌ Cannot connect to database")
                return False
            
            # Dump database to SQL
            sql_dump = "\n".join(conn.iterdump())
            conn.close()
            
            # Create backup file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"chronos_backup_{timestamp}"
            
            if compress:
                backup_file = self.backups_dir / f"{backup_name}.sql.gz"
                with gzip.open(backup_file, 'wt') as f:
                    f.write(sql_dump)
            else:
                backup_file = self.backups_dir / f"{backup_name}.sql"
                backup_file.write_text(sql_dump)
            
            size_mb = backup_file.stat().st_size / 1024 / 1024
            print(f"✅ Backup created: {backup_file} ({size_mb:.2f}MB)")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def restore_database(self, backup_file: str) -> bool:
        """Restore database from backup"""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                print(f"❌ Backup file not found: {backup_file}")
                return False
            
            # Read backup
            if backup_file.endswith('.gz'):
                import gzip
                with gzip.open(backup_path, 'rt') as f:
                    sql_dump = f.read()
            else:
                sql_dump = backup_path.read_text()
            
            # Backup current database
            if self.db_path.exists():
                self.backup_database()
            
            # Restore
            conn = sqlite3.connect(str(self.db_path))
            conn.executescript(sql_dump)
            conn.commit()
            conn.close()
            
            print(f"✅ Database restored from: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def get_database_status(self) -> dict:
        """Get database status and statistics"""
        status = {
            "exists": self.db_path.exists(),
            "size_mb": 0,
            "tables": [],
            "total_records": 0,
            "last_modified": None
        }
        
        try:
            if self.db_path.exists():
                # File info
                stat = self.db_path.stat()
                status["size_mb"] = stat.st_size / 1024 / 1024
                status["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                
                # Database info
                conn = self.get_connection()
                if conn:
                    cursor = conn.cursor()
                    
                    # Get tables
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    
                    for table_row in tables:
                        table_name = table_row[0]
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        
                        status["tables"].append({
                            "name": table_name,
                            "records": count
                        })
                        status["total_records"] += count
                    
                    conn.close()
        except Exception as e:
            status["error"] = str(e)
        
        return status
    
    def optimize_database(self) -> bool:
        """Optimize database"""
        try:
            conn = self.get_connection()
            if not conn:
                print("❌ Cannot connect to database")
                return False
            
            cursor = conn.cursor()
            cursor.execute("VACUUM")
            cursor.execute("ANALYZE")
            conn.commit()
            conn.close()
            
            print("✅ Database optimized")
            return True
        except Exception as e:
            print(f"❌ Optimization failed: {e}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        backups = list(self.backups_dir.glob("chronos_backup_*.sql*"))
        
        print("\n📊 Available Backups:")
        print("-" * 60)
        
        if not backups:
            print("No backups found")
            return
        
        for backup in sorted(backups, reverse=True):
            size_mb = backup.stat().st_size / 1024 / 1024
            mtime = datetime.fromtimestamp(backup.stat().st_mtime)
            print(f"  • {backup.name} ({size_mb:.2f}MB) - {mtime}")
    
    def print_status(self):
        """Print database status"""
        print("\n" + "="*60)
        print("DATABASE STATUS")
        print("="*60)
        
        status = self.get_database_status()
        
        if not status["exists"]:
            print("❌ Database does not exist")
            print("   Will be created on first run")
            return
        
        print(f"✅ Database exists")
        print(f"   Size: {status['size_mb']:.2f}MB")
        print(f"   Last modified: {status['last_modified']}")
        print(f"   Tables: {len(status['tables'])}")
        print(f"   Total records: {status['total_records']}")
        
        if status["tables"]:
            print("\n   Table details:")
            for table in status["tables"]:
                print(f"   • {table['name']}: {table['records']} records")

def main():
    parser = argparse.ArgumentParser(description="Database Management Utility")
    parser.add_argument("--backup", action="store_true", help="Backup database")
    parser.add_argument("--restore", type=str, help="Restore from backup file")
    parser.add_argument("--status", action="store_true", help="Show database status")
    parser.add_argument("--optimize", action="store_true", help="Optimize database")
    parser.add_argument("--list", action="store_true", help="List backups")
    
    args = parser.parse_args()
    
    manager = DatabaseManager()
    
    if args.backup:
        manager.backup_database()
    elif args.restore:
        manager.restore_database(args.restore)
    elif args.status:
        manager.print_status()
    elif args.optimize:
        manager.optimize_database()
    elif args.list:
        manager.list_backups()
    else:
        manager.print_status()

if __name__ == "__main__":
    main()
