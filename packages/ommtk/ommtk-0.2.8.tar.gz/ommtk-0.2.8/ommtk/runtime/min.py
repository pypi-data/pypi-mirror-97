if __name__ == '__main__':
    import _pickle as pickle

    import sys
    import os

    if len(sys.argv[1:]) != 3:
        print("Usage: python min.py step_count pickled_sim end_parmed")
        exit(1)
    else:
        step_count, pickled_sim, new_parmed_file = sys.argv[1:]

        try:
            with open(pickled_sim, 'rb') as handle:
                mdsim = pickle.load(handle)
        except:
            raise
        mdsim.cwd = os.getcwd()
        mdsim._build_sim()

        new_parmed = mdsim.minimize(max_steps=int(step_count), save_h5=True)

        with open(new_parmed_file,'wb') as handle:
            pickle.dump(new_parmed.__getstate__(), handle)
