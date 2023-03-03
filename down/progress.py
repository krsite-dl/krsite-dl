import time

def progress_handler(current_size, content_length, start):
    elapsed_time = time.time() - start
    bandwidth = current_size / elapsed_time
    percent = (current_size / content_length) * 100
    eta = (content_length - current_size) / bandwidth
    
    if bandwidth >= 1024**2:
        bandwidth_str = f"{bandwidth/1024**2:.2f}MB/s"
    else:
        bandwidth_str = f"{bandwidth/1024:.2f}KB/s"

    if content_length >= 1024**2:
        content_length_str = f"{content_length/1024**2:.2f}MB"
        current_size_str = f"{current_size/1024**2:.2f}"
    else:
        content_length_str = f"{content_length/1024:.2f}KB"
        current_size_str = f"{current_size/1024:.2f}"
    
    if percent == 100:
        percent_str = f"\033[32m{percent:.2f}%\033[37m"
    else:
        percent_str = f"{percent:.2f}%"
    if eta == 0:
        eta_str = f"                 "
    else:
        if eta >= 60:
            eta = eta / 60
            if eta >= 60:
                eta = eta / 60
                if eta >= 24:
                    eta = eta / 24
                    eta_str = f"\033[32m, ETA:{int(eta)} day(s)\033[0m"
                else:
                    eta_str = f"\033[32m, ETA:{int(eta)} h\033[0m"
            else:
                eta_str = f"\033[32m, ETA:{int(eta)} m\033[0m"
        else:
            eta_str = f"\033[32m, ETA:{int(eta)} s\033[0m"

    print(f"\r[Progress] {current_size_str}/{content_length_str} ({percent_str}) \033[36m@\033[37m {bandwidth_str}{eta_str}", end="")