#! /usr/bin/env python3
import os
import shutil
import re
import tarfile
from datetime import datetime, timedelta


# Define the log file directory and destination directory
cur_dir = os.getcwd()
log_dir = f"{cur_dir}/application_log"


def get_x_days_ago_date(days_ago):
    '''
    Return the date of x days ago in format YYYY-MM-DD
    '''
    today = datetime.now().date()
    return today - timedelta(days_ago)


def list_log_files(date):
    '''
    List all log files for a given date
    '''
    pattern = r"application\.log\.{}_\d+".format(date)
    return [f for f in os.listdir(cur_dir) if re.match(pattern, f)]


def create_log_dir():
    '''
    Create log directory to store logs
    '''
    os.makedirs(log_dir, exist_ok=True)


def tar_files(date, log_files):
    '''
    Compress log files
    '''
    filename = f'application.log.{date}.tar.gz'
    with tarfile.open(filename, "w:gz") as tar:
        for log_file in log_files:
            file_path = os.path.join(cur_dir, log_file)
            tar.add(file_path, arcname=os.path.basename(log_file))
            os.remove(file_path)
    return filename



def move_logs(date):
    '''
    Move logs to log directory
    '''
    log_files = list_log_files(date)
    tar_filename = tar_files(date, log_files)
    src_path = os.path.join(cur_dir, tar_filename)
    dest_path = os.path.join(log_dir, tar_filename)
    shutil.move(src_path, dest_path)


def move_yesterdays_logs():
    '''
    Move logs from yesterday to the log directory
    '''
    yesterday = get_x_days_ago_date(1)
    move_logs(yesterday)


def enforce_retention(retention_in_days):
    '''
    Delete any logs one day older than retention
    '''
    delete_date = get_x_days_ago_date(retention_in_days + 1)
    log_file_name = f'application.log.{delete_date}.tar.gz'
    log_file = os.path.join(log_dir, log_file_name)
    try:
        os.remove(log_file)
    except FileNotFoundError:
        pass


create_log_dir()
move_yesterdays_logs()
enforce_retention(14)

print("Log files moved successfully.")
