from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20  # 最大线程数

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # 线程数
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))  # map()返回生成器
    return len(list(res))

if __name__ == '__main__':
    main(download_many)