from training.pipeline import Pipeline
import time


def main():
    pipeline = Pipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Total Training time:", execution_time, "seconds")