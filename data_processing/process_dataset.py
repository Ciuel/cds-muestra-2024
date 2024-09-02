import pandas as pd
from multiprocessing import Pool, freeze_support

CHUNK_SIZE = 100000

def process_csv_chunked(in_path, out_path, func, chunk_size=CHUNK_SIZE, read_kwargs={}, write_kwargs={}, num_processes=1):
        i = 0
        header_written = False
        pool = Pool(processes=num_processes)

        for chunk in pd.read_csv(in_path, chunksize=chunk_size, encoding="utf-8", engine='c', low_memory=False, **read_kwargs):
            results = pool.map(func, [chunk])
            processed_chunk = results[0]

            if header_written:
                processed_chunk.to_csv(out_path, mode="a", index=False, encoding="utf-8", header=False, **write_kwargs)
            else:
                processed_chunk.to_csv(out_path, mode="w", index=False, encoding="utf-8", **write_kwargs)
                header_written = True

            i += 1
            print(f"Chunk {i} done")

        pool.close()
        pool.join()
