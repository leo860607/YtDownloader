import tqdm, sys, time
def updateprogress(i):
  progress.update(i)
progress = tqdm.tqdm(file=sys.stderr, unit="B", unit_scale=True, total=100)
with progress:
    for i in range(100):
        updateprogress(i)
        time.sleep(0.01)
print ("exiting")